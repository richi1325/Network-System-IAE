#!/usr/bin/python3
import os
import re
import subprocess
from sqlalchemy import create_engine

conn = create_engine(f'postgresql+psycopg2://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["HOST"]}/{os.environ["POSTGRES_DB"]}').connect()
TIME_SERVER_DOWN = -1

ips = conn.execute(f"SELECT id, ip FROM ips WHERE es_monitoreado = TRUE")
for ip in ips:
    response =  subprocess.Popen(f'ping -c 1 {ip[1]}', shell=True, stdout=subprocess.PIPE)
    res = response.communicate()
    if response.returncode == 0:
        output = res[0].decode()
        time_ms = re.findall(r'time=([0-9]+.*[0-9]*) ms$',output.split("\n")[1])[0]
        conn.execute(f'INSERT INTO pings(ip_id, time_ms) VALUES ({ip[0]}, {time_ms})')
        conn.execute(f"UPDATE ips SET estatus_id = 2 WHERE ip = '{ip[1]}'")
    else:
        conn.execute(f'INSERT INTO pings(ip_id, time_ms) VALUES ({ip[0]}, {TIME_SERVER_DOWN})')
        conn.execute(f"UPDATE ips SET estatus_id = 3 WHERE ip = '{ip[1]}'")

conn.close()