from flask import Flask, request
from flask_cors import CORS
from controller.database import initialize_database
from controller.models import Doctor, Cita  # Added Cita import
import sqlite3
import random

app = Flask(__name__)
CORS(app)

initialize_database()

def generar_nro_carnet():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        while True:
            nro_carnet = str(random.randint(100000, 999999))
            cursor.execute('SELECT nro_carnet FROM doctores WHERE nro_carnet = ?', (nro_carnet,))
            if not cursor.fetchone():
                return nro_carnet

@app.route('/registro_doctor', methods=['POST'])
def doctor():
    try:
        data = request.get_json()
        nombre = data['nombre']
        nacimiento = data['nacimiento']
        sexo = data['sexo']
        cedula = data['cedula']
        carnet = generar_nro_carnet()
        especialidades = [data['especialidad']]
        clave = data['clave']
        confirmar_clave = data['confirmar_clave']

        if clave != confirmar_clave:
            return {"error": "Las claves no coinciden"}, 400

        doctor = Doctor(nombre, nacimiento, sexo, cedula, carnet, especialidades, clave)
        doctor.save()
        return {"message": "Doctor creado exitosamente"}, 201
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
    
    
@app.route('/crear_cita', methods=['POST'])
def crear_cita_route():
    try:
        data = request.get_json()
        doctor_id = data['doctor_id']
        patient_id = data['patient_id']
        fecha = data['fecha']
        motivo = data['motivo']

        cita = Cita(doctor_id, patient_id, fecha, motivo)
        cita.save()

        return {"message": "Cita creada exitosamente"}, 201
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/citas', methods=['GET'])
def citas():
    try:
        citas = Cita.list()  # Ensure Cita is imported and used here
        return {"citas": citas}, 200
    except Exception as e:
        return {"error": str(e)}, 500