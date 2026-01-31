import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
app.secret_key = 'ste_dev'

# Configurar Firebase - COM O NOME CORRETO DO ARQUIVO
cred = credentials.Certificate("sistema-para-clinicas-firebase-adminsdk-fbsvc-be7122231b.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Função para gerar ID único
def gerar_id():
    return str(int(os.urandom(4).hex(), 16))
# -----------------
#   ROTA PRINCIPAL
# -----------------
@app.route('/')
def index():
    try:
        # Buscar dados do Firestore
        pacientes_ref = db.collection('pacientes').stream()
        pacientes = [doc.to_dict() for doc in pacientes_ref]
        
        medicos_ref = db.collection('medicos').stream()
        medicos = [doc.to_dict() for doc in medicos_ref]
        
        consultas_ref = db.collection('consultas').stream()
        consultas = [doc.to_dict() for doc in consultas_ref]
        
        return render_template('index.html', pacientes=pacientes, medicos=medicos, consultas=consultas)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('index.html', pacientes=[], medicos=[], consultas=[])
# ----------------
# ROTA PACIENTES
# -------------------
@app.route('/pacientes')
def listar_pacientes():
    try:
        pacientes_ref = db.collection('pacientes').stream()
        pacientes = [doc.to_dict() for doc in pacientes_ref]
        return render_template('pacientes.html', pacientes=pacientes)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('pacientes.html', pacientes=[])
@app.route('/pacientes/novo', methods=['GET', 'POST'])
def novo_paciente():
    if request.method == 'POST':
        try:
            paciente = {
                'id': gerar_id(),
                'nome': request.form['nome'],
                'cpf': request.form['cpf'],
                'telefone': request.form['telefone']
            }
            db.collection('pacientes').add(paciente)
            flash('Paciente cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_pacientes'))
        except Exception as e:
            flash(f'Erro ao cadastrar paciente: {e}', 'error')
    return render_template('novo_paciente.html')

@app.route('/medicos')
def listar_medicos():
    try:
        medicos_ref = db.collection('medicos').stream()
        medicos = [doc.to_dict() for doc in medicos_ref]
        return render_template('medicos.html', medicos=medicos)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('medicos.html', medicos=[])

@app.route('/medicos/novo', methods=['GET', 'POST'])
def novo_medico():
    if request.method == 'POST':
        try:
            medico = {
                'id': gerar_id(),
                'nome': request.form['nome'],
                'especialidade': request.form['especialidade'],
                'crm': request.form['crm']
            }
            db.collection('medicos').add(medico)
            flash('Médico cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_medicos'))
        except Exception as e:
            flash(f'Erro ao cadastrar médico: {e}', 'error')
    return render_template('novo_medico.html')

@app.route('/consultas')
def listar_consultas():
    try:
        consultas_ref = db.collection('consultas').stream()
        consultas = [doc.to_dict() for doc in consultas_ref]
        return render_template('consultas.html', consultas=consultas)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('consultas.html', consultas=[])

@app.route('/consultas/nova', methods=['GET', 'POST'])
def nova_consulta():
    if request.method == 'POST':
        try:
            consulta = {
                'id': gerar_id(),
                'paciente': request.form['paciente'],
                'medico': request.form['medico'],
                'data': request.form['data_consulta'],
                'hora': request.form['hora_consulta']
            }
            db.collection('consultas').add(consulta)
            flash('Consulta agendada com sucesso!', 'success')
            return redirect(url_for('listar_consultas'))
        except Exception as e:
            flash(f'Erro ao agendar consulta: {e}', 'error')
    
    try:
        pacientes_ref = db.collection('pacientes').stream()
        pacientes = [doc.to_dict() for doc in pacientes_ref]
        
        medicos_ref = db.collection('medicos').stream()
        medicos = [doc.to_dict() for doc in medicos_ref]
        
        return render_template('nova_consulta.html', pacientes=pacientes, medicos=medicos)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('nova_consulta.html', pacientes=[], medicos=[])

@app.route('/agendamentos')
def agendamentos():
    try:
        consultas_ref = db.collection('consultas').stream()
        consultas = [doc.to_dict() for doc in consultas_ref]
        return render_template('agendamentos.html', consultas=consultas)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('agendamentos.html', consultas=[])

@app.route('/prontuarios')
def prontuarios():
    return render_template('prontuarios.html')

@app.route('/financeiro')
def financeiro():
    return render_template('financeiro.html')

@app.route('/estoque')
def estoque():
    return render_template('estoque.html')

@app.route('/relatorios')
def relatorios():
    return render_template('relatorios.html')

@app.route('/configuracao')
def configuracao():
    return render_template('configuracao.html')

if __name__ == '__main__':
    app.run(debug=True)
