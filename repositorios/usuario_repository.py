from config.database import ConexionBD
from modelos.usuario import Usuario
from utils.sql_compat import query_compat

class RepositorioUsuario:
    def __init__(self):
        self.bd = ConexionBD()

    def guardar(self, usuario):
        cursor = self.bd.obtener_cursor()
        sql = query_compat("""
            INSERT INTO usuarios (nombre, email, password_hash, es_admin)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """)
        try:
            cursor.execute(sql, (usuario.nombre, usuario.email, usuario.password_hash, usuario.es_admin))
            id_generado = cursor.fetchone()[0]
            self.bd.conexion.commit()
            usuario.id_usuario = id_generado
            return usuario
        except Exception as e:
            self.bd.conexion.rollback()
            print(f"Error al guardar usuario: {e}")
            return None

    def obtener_por_email(self, email):
        cursor = self.bd.obtener_cursor()
        sql = "SELECT id, nombre, email, password_hash, es_admin FROM usuarios WHERE email = %s"
        cursor.execute(query_compat(sql), (email,))
        resultado = cursor.fetchone()
        if resultado:
            return Usuario(*resultado)
        return None

    def obtener_por_id(self, id_usuario):
        cursor = self.bd.obtener_cursor()
        sql = "SELECT id, nombre, email, password_hash, es_admin FROM usuarios WHERE id = %s"
        cursor.execute(query_compat(sql), (id_usuario,))
        resultado = cursor.fetchone()
        if resultado:
            return Usuario(*resultado)
        return None
