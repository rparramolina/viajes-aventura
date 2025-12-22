from config.database import ConexionBD
from modelos.usuario import Usuario
import oracledb

class RepositorioUsuario:
    def __init__(self):
        self.bd = ConexionBD()

    def guardar(self, usuario):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return None
        
        # Insertar (Oracle specific)
        sql = """
            INSERT INTO usuarios (nombre, email, password_hash, es_admin)
            VALUES (:1, :2, :3, :4)
            RETURNING id INTO :5
        """
        try:
            id_variable = cursor.var(oracledb.NUMBER)
            cursor.execute(sql, (usuario.nombre, usuario.email, usuario.password_hash, usuario.es_admin, id_variable))
            id_generado = id_variable.getvalue()[0]
            self.bd.conexion.commit()
            usuario.id_usuario = id_generado
            return usuario
        except Exception as e:
            self.bd.conexion.rollback()
            print(f"Error al guardar usuario: {e}")
            import traceback
            traceback.print_exc()
            return None

    def obtener_por_email(self, email):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return None
        sql = "SELECT id, nombre, email, password_hash, es_admin FROM usuarios WHERE email = :1"
        cursor.execute(sql, (email,))
        resultado = cursor.fetchone()
        if resultado:
            return Usuario(*resultado)
        return None

    def obtener_por_id(self, id_usuario):
        cursor = self.bd.obtener_cursor()
        if not cursor:
            return None
        sql = "SELECT id, nombre, email, password_hash, es_admin FROM usuarios WHERE id = :1"
        cursor.execute(sql, (id_usuario,))
        resultado = cursor.fetchone()
        if resultado:
            return Usuario(*resultado)
        return None
