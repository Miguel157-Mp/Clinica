import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class Doctor:
    def __init__(self, nombre, nacimiento, sexo, cedula, carnet, especialidades, clave):
        self.nombre = nombre
        self.nacimiento = nacimiento
        self.sexo = sexo
        self.cedula = cedula
        self.carnet = carnet
        self.especialidades = especialidades
        self.clave = generate_password_hash(clave)

    def save(self):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO doctores (nombre, fecha_nacimiento, sexo, cedula, nro_carnet, clave, especialidad)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (self.nombre, self.nacimiento, self.sexo, self.cedula, self.carnet, self.clave, self.especialidades[0]))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error de SQLite: {e}")
                raise e
            
            
class Cita:
    def __init__(self, doctor_id, patient_id, fecha, motivo):
                self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.fecha = fecha
        self.motivo = motivo

    def save(self):
                with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
                        cursor.execute('''
            INSERT INTO citas (doctor_id, patient_id, fecha, motivo)
            VALUES (?, ?, ?, ?)
            ''', (self.doctor_id, self.patient_id, self.fecha, self.motivo))
            conn.commit()

    @staticmethod
    def find_by_id(appointment_id):
                with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
                        cursor.execute('SELECT * FROM appointments WHERE id = ?', (appointment_id,))
            return cursor.fetchone()

    @staticmethod
    def list():
                with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM citas')
            rows = cursor.fetchall()
            return [{"id": row[0], "doctor_id": row[1], "patient_id": row[2], "fecha": row[3], "motivo": row[4]} for row in rows]
            
