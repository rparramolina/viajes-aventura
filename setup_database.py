from config.database import ConexionBD
import os

def inicializar_bd():
    print("Inicializando base de datos...")
    bd = ConexionBD()
    conn = bd.conectar()
    if not conn:
        print("No se pudo conectar a la BD. Verifique config/settings.py y que Postgres esté corriendo.")
        return

    cursor = conn.cursor()
    
    # Seleccionar el esquema según el motor
    from config.settings import DB_ENGINE
    nombre_esquema = 'esquema_sqlserver.sql' if DB_ENGINE == 'sqlserver' else 'esquema.sql'
    
    ruta_esquema = os.path.join(os.path.dirname(__file__), nombre_esquema)
    with open(ruta_esquema, 'r') as f:
        sql = f.read()

    try:
        cursor.execute(sql)
        conn.commit()
        print("Tablas creadas exitosamente.")
    except Exception as e:
        conn.rollback()
        print(f"Error al crear tablas: {e}")
    finally:
        bd.cerrar()

if __name__ == "__main__":
    inicializar_bd()
