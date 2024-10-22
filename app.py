from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'

def generar_id():
    if 'registros' in session and len(session['registros']) > 0:
        return max(item['id'] for item in session['registros']) + 1
    else:
        return 1

@app.route("/")
def index():
    if 'registros' not in session:
        session['registros'] = [] 
    return render_template('index.html')

@app.route("/registra", methods=['POST'])
def registra():
    fecha = request.form['fecha']
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    turno = request.form['turno']
    seminarios = request.form.getlist('seminarios')

    nuevo_registro = {
        'id': generar_id(),
        'fecha': fecha,
        'nombre': nombre,
        'apellidos': apellidos,
        'turno': turno,
        'seminarios': seminarios
    }

    session['registros'].append(nuevo_registro)
    session.modified = True
    return redirect(url_for('registro'))

@app.route("/registro")
def registro():
    registros = session.get('registros', [])
    return render_template('registro.html', registros=registros)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    registros = session.get('registros', [])
    registro = next((r for r in registros if r['id'] == id), None)

    if not registro:
        return redirect(url_for('registro'))

    if request.method == 'POST':
        registro['fecha'] = request.form['fecha']
        registro['nombre'] = request.form['nombre']
        registro['apellidos'] = request.form['apellidos']
        registro['turno'] = request.form['turno']
        registro['seminarios'] = request.form.getlist('seminarios')
        session.modified = True
        return redirect(url_for('registro'))

    return render_template('editar.html', registro=registro)

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    registros = session.get('registros', [])
    registro = next((r for r in registros if r['id'] == id), None)
    
    if registro:
        session['registros'].remove(registro)
        session.modified = True
    
    return redirect(url_for('registro'))

if __name__ == "__main__":
    app.run(debug=True)
