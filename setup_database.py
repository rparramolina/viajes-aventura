from config.database import ConexionBD
import os

def inicializar_bd():
    print("Inicializando base de datos Oracle...")
    bd = ConexionBD()
    conn = bd.conectar()
    if not conn:
        print("No se pudo conectar a la BD Oracle. Verifique config/settings.py.")
        return

    cursor = conn.cursor()
    
    nombre_esquema = 'esquema_oracle.sql'
    ruta_esquema = os.path.join(os.path.dirname(__file__), nombre_esquema)
    
    if not os.path.exists(ruta_esquema):
        print(f"Error: No se encontró el archivo de esquema {nombre_esquema}")
        bd.cerrar()
        return

    with open(ruta_esquema, 'r') as f:
        sql_content = f.read()

    try:
        # Oracle: Separar por '/' para ejecutar bloques PL/SQL
        comandos = sql_content.split('/')
        for comando in comandos:
            clean_comando = comando.strip()
            if clean_comando:
                cursor.execute(clean_comando)
            
        conn.commit()
        print("Tablas creadas exitosamente en Oracle.")
    except Exception as e:
        conn.rollback()
        print(f"Error al crear tablas en Oracle: {e}")
    finally:
        bd.cerrar()

if __name__ == "__main__":
    inicializar_bd()
