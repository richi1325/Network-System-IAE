import os
import json
import pandas as pd
from plotly.utils import PlotlyJSONEncoder
import plotly.express as px
from flask import Flask, render_template
from sqlalchemy import create_engine

app = Flask(__name__)

@app.route('/<subject>')
def chart1(subject):
   conn = create_engine(f'postgresql+psycopg2://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["HOST"]}/{os.environ["POSTGRES_DB"]}').connect()
   try:
      id = pd.read_sql(con=conn, sql=f"SELECT id FROM ips WHERE ip='{subject}'")
      df = pd.read_sql(con=conn, sql=f"SELECT * FROM pings WHERE ip_id={id.loc[0].loc['id']}")
      conn.close()
      fig = px.line(df, x='date_time', y="time_ms")
      graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
      header = f"Time serie - {subject}"
      return render_template('graph.html', graphJSON=graphJSON, header=header)
   except:
      return render_template('nomedia.html')