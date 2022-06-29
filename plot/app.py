import os
import json
import pandas as pd
import plotly.express as px

from datetime import date
from bs4 import BeautifulSoup
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
      conn.close()
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
      
      buttons = []
      for index, _ in enumerate(df.index):
         buttons.append(f'<button class="button_edit" onclick="edit_row({str(index)});">Editar</button>')
      df["Editar"] = buttons


      df.index.name = None
      table = df.to_html(render_links=True, escape=False, justify='center')
      table = table.replace("None","")
      table = table.replace("<th></th>", "<th>ip</th>")
      soup = BeautifulSoup(table, "html.parser")
      html_tags = soup.find("tbody").find_all("tr")
      for each_tag in html_tags:
         each_tag.attrs['id'] = html_tags.index(each_tag)

      propietarios = conn.execute("SELECT id, propietario FROM propietarios")
      modelos = conn.execute("SELECT id, modelo FROM modelos")
      conn.close()

      opciones_propietarios = []
      propietarios_json = {}
      opciones_modelos = []
      modelos_json = {}


      for propietario in propietarios:
         propietarios_json[propietario[1]] = propietario[0]
         opciones_propietarios.append(f"<option value=\"{propietario[0]}\">{propietario[1]}</option>")
      for modelo in modelos:
         modelos_json[modelo[1]] = modelo[0]
         opciones_modelos.append(f"<option value=\"{modelo[0]}\">{modelo[1]}</option>")

      return render_template(
         'home.html',
         table=soup,
         propietarios_json = json.dumps(propietarios_json),
         modelos_json = json.dumps(modelos_json)
      )

@app.route('/processing/<ip>')
def processip(ip):
   return render_template('processing.html', ip=ip)

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

@app.route('/search/<ip>')
def plot(ip):
   conn = create_connection()
   try:
      id = pd.read_sql(con=conn, sql=f"SELECT id FROM ips WHERE ip='{ip}'")
      df = pd.read_sql(con=conn, sql=f"SELECT * FROM pings WHERE ip_id={id.loc[0].loc['id']}")
      conn.close()
      fig = px.line(df, x='date_time', y="time_ms")
      fig.update_layout({
         'plot_bgcolor': 'rgba(211,211,211, 0.8)',
         'paper_bgcolor': 'rgba(255, 255, 255, 0.8)',
      })
      fig.update_traces(line_color='#CA8A04', line_width=4)
      graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
      df = pd.DataFrame(nmap(ip))
      table = df.to_html(index=False, justify='center')
      conn.close()
      return render_template('graph.html',ip=ip, graphJSON=graphJSON,table=table)
   except:
      conn.close()
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
   propietarios = conn.execute("SELECT id, propietario FROM propietarios")
   modelos = conn.execute("SELECT id, modelo FROM modelos")
   conn.close()

   opciones_propietarios = ""
   opciones_modelos = ""

   for propietario in propietarios:
      opciones_propietarios += f"<option value=\"{propietario[0]}\">{propietario[1]}</option>\n"
   for modelo in modelos:
      opciones_modelos += f"<option value=\"{modelo[0]}\">{modelo[1]}</option>\n"

   return render_template(
      'home.html',
      table=table,
      propietarios = opciones_propietarios,
      modelos = opciones_modelos
   )

@app.route('/update', methods=['POST'])
def edit():
   if request.method == 'POST':
      conn = create_connection()
      data_new = dict(request.form)
      data_last = json.loads(data_new.pop("last"))
      if data_new.get("modelo-input", None):
         conn.execute(f'INSERT INTO modelos(modelo) VALUES (\'{data_new["modelo-input"]}\')')
         data_new["modelo_id"] = str(next(conn.execute(f"SELECT lastval()"))[0])
         data_new.pop("modelo-input")
      if data_new.get("propietario-input", None):
         conn.execute(f'INSERT INTO propietarios(propietario) VALUES (\'{data_new["propietario-input"]}\')')
         data_new["propietario_id"] = str(next(conn.execute(f"SELECT lastval()"))[0])
         data_new.pop("propietario-input")
      query = ""
      if data_new.get("mac") != "":
         query += f'mac = \'{data_new.get("mac")}\',\n'
      if data_new.get("descripcion") != "":
         query += f'descripcion = \'{data_new.get("descripcion")}\',\n'
      if data_new.get("extension") != "":
         query += f'extension = \'{data_new.get("extension")}\',\n'
      query += f'estatus_id = \'1\',\n'         
      query += f'fecha_registro = \'{date.today()}\',\n'
      query += f'propietario_id = \'{data_new.get("propietario_id")}\',\n'
      query += f'modelo_id = \'{data_new.get("modelo_id")}\''
      conn.execute(f"""
         UPDATE ips 
         SET {query}
         WHERE ip = '{data_new["ip"]}'
      """)
      conn.close()
      return redirect("/")

if __name__ == "__main__":
   app.run()