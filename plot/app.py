import os
import json
import pandas as pd
import plotly.express as px
from src.utils import create_connection, nmap
from plotly.utils import PlotlyJSONEncoder
from flask import Flask, render_template, send_from_directory, request, redirect

app = Flask(__name__)
# app.debug = False

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')

@app.route('/', methods=['GET', 'POST'])
def home():
   conn = create_connection()
   if request.method == 'POST':
      data = dict(request.form)
      data["estatus_id"] = "1"
      if data.get("modelo-input", None):
         conn.execute(f'INSERT INTO modelos(modelo) VALUES (\'{data["modelo-input"]}\')')
         data["modelo_id"] = str(next(conn.execute(f"SELECT lastval()"))[0])
         data.pop("modelo-input")
      if data.get("propietario-input", None):
         conn.execute(f'INSERT INTO propietarios(propietario) VALUES (\'{data["propietario-input"]}\')')
         data["propietario_id"] = str(next(conn.execute(f"SELECT lastval()"))[0])
         data.pop("propietario-input")
      print("INSERT INTO ips({key}) VALUES({value})".format(key=",".join(data.keys()),value=",".join(data.values())))
      for delete in [key for key in data.keys() if not data[key]]:
         data.pop(delete)
      conn.execute("INSERT INTO ips({}) VALUES('{}')".format(",".join(data.keys()),"','".join(data.values())))
      return redirect("/")

   elif request.method == 'GET':
      df = pd.read_sql(sql = """
      SELECT ip.ip, ip.mac, ip.descripcion, e.estatus, p.propietario, m.modelo, ip.extension, ip.fecha_registro
      FROM ips AS ip
      LEFT JOIN estatus e on e.id = ip.estatus_id
      LEFT JOIN modelos m on m.id = ip.modelo_id
      LEFT JOIN propietarios p on p.id = ip.propietario_id
      WHERE  es_monitoreado = TRUE;
      """,con = conn,index_col="ip")
      
      buttons = map(lambda x: f'<button class="button_mon" onclick="location.href=\'/processing/{x}\';">Historial</button>', df.index)
      df["Monitorear"] = list(buttons)
      buttons = map(lambda x: f'<button class="button_del" onclick="location.href=\'/delete/{x}\';">Eliminar</button>', df.index)
      df["Eliminar"] = list(buttons)

      df.index.name = None
      table = df.to_html(render_links=True, escape=False, justify='center')
      table = table.replace("None","")
      table = table.replace("<th></th>", "<th>ip</th>")
      return render_template('simple.html',  table=table)

@app.route('/processing/<subject>')
def processip(subject):
   return render_template('processing.html', ip=subject)

@app.route('/delete/<ip>')
def delete(ip):
   conn = create_connection()
   conn.execute(f"UPDATE ips SET es_monitoreado = FALSE WHERE ip = '{ip}'")
   conn.close()
   return redirect("/")

@app.route('/activate/<ip>')
def acticate(ip):
   conn = create_connection()
   conn.execute(f"UPDATE ips SET es_monitoreado = TRUE WHERE ip = '{ip}'")
   conn.close()
   return redirect("/delete")

@app.route('/search/<subject>')
def plot(subject):
   conn = create_connection()
   try:
      id = pd.read_sql(con=conn, sql=f"SELECT id FROM ips WHERE ip='{subject}'")
      df = pd.read_sql(con=conn, sql=f"SELECT * FROM pings WHERE ip_id={id.loc[0].loc['id']}")
      conn.close()
      fig = px.line(df, x='date_time', y="time_ms")
      fig.update_layout({
         'plot_bgcolor': 'rgba(211,211,211, 0.8)',
         'paper_bgcolor': 'rgba(255, 255, 255, 0.8)',
      })
      fig.update_traces(line_color='#CA8A04', line_width=4)
      graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
      df = pd.DataFrame(nmap(subject))
      table = df.to_html(index=False, justify='center')
      return render_template('graph.html',ip=subject, graphJSON=graphJSON,table=table)
   except:
      return render_template('nomedia.html')

@app.route('/add')
def html_table():
   conn = create_connection()
   propietarios = conn.execute("SELECT id, propietario FROM propietarios")
   modelos = conn.execute("SELECT id, modelo FROM modelos")
   conn.close()

   opciones_propietarios = ""
   opciones_modelos = ""

   for propietario in propietarios:
      opciones_propietarios += f"<option value=\"{propietario[0]}\">{propietario[1]}</option>\n"
   for modelo in modelos:
      opciones_modelos += f"<option value=\"{modelo[0]}\">{modelo[1]}</option>\n"
   return render_template('add_ip.html', 
            options_propietarios=opciones_propietarios, 
            options_modelos = opciones_modelos,
   )

@app.route('/delete')
def delete_ips():
   conn = create_connection()
   df = pd.read_sql(sql = """
   SELECT ip.ip, ip.mac, ip.descripcion, e.estatus, p.propietario, m.modelo, ip.extension, ip.fecha_registro
   FROM ips AS ip
   LEFT JOIN estatus e on e.id = ip.estatus_id
   LEFT JOIN modelos m on m.id = ip.modelo_id
   LEFT JOIN propietarios p on p.id = ip.propietario_id
   WHERE es_monitoreado = FALSE;
   """,con = conn,index_col="ip")
   
   buttons = map(lambda x: f'<button class="button_mon" onclick="location.href=\'/processing/{x}\';">Historial</button>', df.index)
   df["Monitorear"] = list(buttons)
   buttons = map(lambda x: f'<button class="button_act" onclick="location.href=\'/activate/{x}\';">Activar</button>', df.index)
   df["Activar"] = list(buttons)

   df.index.name = None
   table = df.to_html(render_links=True, escape=False, justify='center')
   table = table.replace("None","")
   table = table.replace("<th></th>", "<th>ip</th>")
   return render_template('simple.html',  table=table)

if __name__ == "__main__":
   app.run()