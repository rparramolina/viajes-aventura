from config.database import ConexionBD
import os

def inicializar_bd():
    print("Inicializando base de datos...")
    bd = ConexionBD()
    conn = bd.conectar()
    if not conn:
        from config.settings import DB_ENGINE
        print(f"No se pudo conectar a la BD ({DB_ENGINE}). Verifique config/settings.py y el archivo .env.")
        return

    cursor = conn.cursor()
    
    # Seleccionar el esquema según el motor
    from config.settings import DB_ENGINE
    
    if DB_ENGINE == 'sqlserver':
        nombre_esquema = 'esquema_sqlserver.sql'
    elif DB_ENGINE == 'oracle':
        nombre_esquema = 'esquema_oracle.sql'
    else:
        nombre_esquema = 'esquema.sql'
    
    ruta_esquema = os.path.join(os.path.dirname(__file__), nombre_esquema)
    with open(ruta_esquema, 'r') as f:
        sql_content = f.read()

    try:
        if DB_ENGINE == 'oracle':
            # Oracle: Separar por '/' para ejecutar bloques PL/SQL
            comandos = sql_content.split('/')
            for comando in comandos:
                if comando.strip():
                    cursor.execute(comando)
        else:
            # Postgres/SQLServer: Ejecutar todo el script (dependiendo del driver puede requerir split)
            cursor.execute(sql_content)
            
        conn.commit()
        print(f"Tablas creadas exitosamente para {DB_ENGINE}.")
    except Exception as e:
        conn.rollback()
        print(f"Error al crear tablas: {e}")
    finally:
        bd.cerrar()

if __name__ == "__main__":
    inicializar_bd()
