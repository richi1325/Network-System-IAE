import re
import os
import subprocess
from sqlalchemy import create_engine

def create_connection():
    return create_engine(f'postgresql+psycopg2://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["HOST"]}/{os.environ["POSTGRES_DB"]}').connect()

def nmap(ip):
    response =  subprocess.Popen(f'nmap {ip} --host-timeout 10s', shell=True, stdout=subprocess.PIPE)
    res = response.communicate()
    if response.returncode == 0:
        output = res[0].decode()
        data = output.split("\n")
        flag = False
        table = []
        for line in data:
            if 'PORT' in line:
                flag = True
            elif flag:
                row = {}
                if info:= re.findall(r"([0-9]+)/([a-zA-Z0-9-]+)\s+([a-zA-Z-]+)\s+([a-z-A-Z0-9-]+)\s*",line):
                    info = info[0]
                    row["Puerto"] = info[0]
                    row["Protocolo"] = info[1]
                    row["Estado"] = info[2]
                    row["Servicio"] = info[3]
                    table.append(row)
                else:
                    break
        return table
    else:
        return None