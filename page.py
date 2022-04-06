from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1' 
app.config['MYSQL_USER'] = 'userDAW'
app.config['MYSQL_PASSWORD'] = '12345678Daw'
app.config['MYSQL_DB'] = 'abasi'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #configuracio que ens converteix els resultats de les query en diccionaris

conn = MySQL(app)
app.secret_key = 'my_s3cr3t_k3y'

#mètode cridat per a eliminar registres de la bbdd passant la del registre id com a parametre
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_website(id):
    cur = conn.connection.cursor() #obrim conexio amb la bbdd
    cur.execute('DELETE FROM websites WHERE website_id = {0}'.format(id))  #donem el valor amb la query que volguem
    conn.connection.commit() #executem la query
    cur.close() #tanquem el cursor d'acces a la bbdd
    flash('Contacte eliminat correctament')
    return redirect(url_for('show_websites'))
    
#mètode que retorna els valors d'un registre de websites i retorna també els valors de la taula webtypes en un dropdown
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_website(id):
    cur = conn.connection.cursor() 
    cur.execute('SELECT * FROM websites WHERE website_id = %s', (id,))
    data = cur.fetchall() #emmagatzemem el valor que retorna la query en un dictionary
    cur.close()
    cur = conn.connection.cursor()
    cur.execute('SELECT * FROM webtypes')
    dataTypes = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-website.html', website = data, types = dataTypes, productes_active="class=active")

#mètode que agafa els valors dels inputs i actualitza el registre indicat de la bbdd
@app.route('/update/<id>', methods=['POST'])
def update_website(id):
    if request.method == 'POST':
        dominio = request.form['dominio'] #agafem el valor de cada input i els emmagatzemem en variables
        tipus = request.form['web-types']
        paginas = request.form['pagina']
        usuario = request.form['usuari']
        cur = conn.connection.cursor() #obrim la conexio i despres li passem la query que volem executar amb les variables creades
        cur.execute('UPDATE websites SET domini = %s, tipus = %s, pagines = %s, usuari = %s WHERE website_id = %s ', (dominio, tipus, paginas, usuario, id))
        conn.connection.commit() #e
        cur.close()
        flash('Contacte actualitzat correctament')
        return redirect(url_for('show_websites'))    
        
#mètode que ens retorna tots els registres de la taula websites i retorna el nom de la webtype del registre i no el id
@app.route('/websites', methods = ['POST', 'GET'])
def show_websites():
    cur = conn.connection.cursor()
    cur.execute('SELECT w.website_id, w.domini, wt.nom , w.pagines, w.usuari, wt.image FROM websites w, webtypes wt where w.tipus=wt.type_id')
    data = cur.fetchall()
    cur.close()
    return render_template('websites.html', websites = data, productes_active="class=active")
    

#mètode que realitza inserts amb les dades del form
@app.route('/add_website', methods=['POST'])
def add_website():
    if request.method == 'POST':
        dominio = request.form['dominio']
        tipus = request.form['web-types']
        paginas = request.form['paginas']
        usuario = request.form['usuario']
        cur = conn.connection.cursor()
        cur.execute('INSERT INTO websites (domini, tipus, pagines, usuari) VALUES (%s, %s, %s, %s)',(dominio, tipus, paginas, usuario))
        conn.connection.commit() 
        flash('Registre afegit correctament')
        cur.close()
        return redirect(url_for('show_websites'))

#home
@app.route('/')
def index():
    return render_template('index.html', home_active="class=active")
    
#web-service    
@app.route('/query-dict')
def querydict():
    return render_template('query-dict.html', gestio_active="class=active")
    
    

#metode que ens retorna en format json tots els registres de la taula websites
@app.route('/productes', methods = ['POST', 'GET'])
def productes():
    cur = conn.connection.cursor()
    cur.execute('SELECT w.website_id, w.domini, wt.nom , w.pagines, w.usuari FROM websites w, webtypes wt where w.tipus=wt.type_id')
    data = cur.fetchall()
    cur.close()    
    return jsonify({'websites':data, 'message':'Resultat de websites'})   


#metode que ens retorna el registre amb id passada per url
@app.route('/query-dict/<website_id>')
def get_product(website_id):
    cur = conn.connection.cursor()
    cur.execute('SELECT * FROM websites') 
    websites = cur.fetchall()
    cur.close()    
    website_found = [
        website for website in websites if website['website_id']==int(website_id)]
    if len(website_found) > 0:
        return jsonify({'website': website_found[0],'message': 'Detall del lloc web'})
    else:
        return jsonify({'message': 'Lloc web no trobat'})
    
    
#mètode per al formulari de la url gestio que ens mostra els webtypes a un dropdown
@app.route('/gestio', methods = ['POST', 'GET'])
def gestio():    
    cur = conn.connection.cursor()
    cur.execute('SELECT * FROM webtypes')
    data = cur.fetchall()
    cur.close()
    print(data)
    return render_template("gestio.html",  types=data, productes_active="class=active")

#mètode que crida a al html descargas
@app.route('/descargas', methods = ['POST', 'GET'])
def descargas():
	return render_template("descargas.html", contacta_active="class=active")

   



if __name__ == "__main__":
    app.run(debug=True)