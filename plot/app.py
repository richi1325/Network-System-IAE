import os
import json
import pandas as pd
import plotly.express as px
from src.utils import create_connection
from plotly.utils import PlotlyJSONEncoder
from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)
# app.debug = False


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')

@app.route('/', methods=['GET', 'POST'])
def home():
   if request.method == 'POST':
      return request.form
   elif request.method == 'GET':
      df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
                     'B': [5, 6, 7, 8, 9],
                     'C': ['a', 'b', 'c--', 'd', 'e']})
      table = df.to_html()
      table = table.replace("<th></th>", "<th>index</th>")
      return render_template('simple.html',  table=table)

@app.route('/search/<subject>')
def chart1(subject):
   conn = create_connection()
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

@app.route('/add')
def html_table():
   conn = create_connection()
   propietarios = conn.execute("SELECT propietario FROM propietarios")
   modelos = conn.execute("SELECT modelo FROM modelos")
   conn.close()

   opciones_propietarios = ""
   opciones_modelos = ""

   for propietario in propietarios:
      opciones_propietarios += f"<option>{propietario[0]}</option>\n"
   for modelo in modelos:
      opciones_modelos += f"<option>{modelo[0]}</option>\n"

   return render_template('add_ip.html', options_propietarios=opciones_propietarios, options_modelos = opciones_modelos)

if __name__ == "__main__":
   app.run()