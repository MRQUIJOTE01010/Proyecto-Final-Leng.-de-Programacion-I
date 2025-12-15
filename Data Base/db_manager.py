import sqlite3
import os

class DBManager:
    def __init__(self, db_name="clinica.db"):
        # Aseguramos que la base de datos se cree en la carpeta correcta
        self.db_name = db_name

    def conectar(self):
        """Establece la conexión con la base de datos"""
        conn = sqlite3.connect(self.db_name)
        # Esto permite acceder a las columnas por nombre en lugar de por índice numérico
        conn.row_factory = sqlite3.Row 
        return conn

    def inicializar_db(self):
        """Crea las tablas si no existen"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        # Activar claves foráneas (Foreign Keys)
        cursor.execute("PRAGMA foreign_keys = ON;")

        # 1. Tabla DOCTORES
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                especialidad TEXT NOT NULL,
                telefono TEXT NOT NULL,
                horario TEXT NOT NULL
            )
        """)

        # 2. Tabla PACIENTES
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                dni TEXT UNIQUE NOT NULL,
                telefono TEXT,
                email TEXT
            )
        """)

        # 3. Tabla CITAS (Relaciona las dos anteriores)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,  -- Formato esperado: YYYY-MM-DD
                hora TEXT NOT NULL,   -- Formato esperado: HH:MM
                motivo TEXT,
                FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE,
                FOREIGN KEY (doctor_id) REFERENCES doctores (id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        conn.close()
        print("Base de datos inicializada correctamente.")

    def ejecutar_consulta(self, query, parametros=()):
        """
        Función genérica para INSERT, UPDATE, DELETE.
        Tus compañeros usarán esto para no repetir código.
        """
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(query, parametros)
            conn.commit()
            return cursor.lastrowid 
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    def obtener_datos(self, query, parametros=()):
        """
        Función genérica para SELECT (Leer datos).
        Devuelve una lista de resultados.
        """
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(query, parametros)

            resultados = [dict(row) for row in cursor.fetchall()]
            return resultados
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return []
        finally:
            conn.close()

# Bloque de prueba (solo se ejecuta si corres este archivo directamente)
if __name__ == "__main__":
    db = DBManager()
    db.inicializar_db()
