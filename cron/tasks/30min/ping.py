#!/usr/bin/python3
import os
import re
import subprocess
from sqlalchemy import create_engine

conn = create_engine(f'postgresql+psycopg2://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["HOST"]}/{os.environ["POSTGRES_DB"]}').connect()
TIME_SERVER_DOWN = 99999.999

hostnames = [
    '132.248.3.70',
    '132.248.3.71',
    '132.248.3.72',
]

for hostname in hostnames:
    try:
        ip_id = next(conn.execute(f"SELECT id FROM ips WHERE ip='{hostname}'"))[0]
    except:
        conn.execute(f"INSERT INTO ips(ip) VALUES ('{hostname}')")
        ip_id = next(conn.execute(f"SELECT lastval()"))[0]
    response =  subprocess.Popen(f'ping -c 1 {hostname}', shell=True, stdout=subprocess.PIPE)
    res = response.communicate()
    if response.returncode == 0:
        output = res[0].decode()
        time_ms = re.findall(r'time=([0-9]+.*[0-9]*) ms$',output.split("\n")[1])[0]
        conn.execute(f'INSERT INTO pings(ip_id, time_ms) VALUES ({ip_id}, {time_ms})')
    else:
        conn.execute(f'INSERT INTO pings(ip_id, time_ms) VALUES ({ip_id}, {TIME_SERVER_DOWN})')

conn.close()
