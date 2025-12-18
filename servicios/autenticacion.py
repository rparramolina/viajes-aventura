from repositorios.usuario_repository import RepositorioUsuario
from modelos.usuario import Usuario
from utils.seguridad import crear_password_hash, verificar_password, hash_to_string, string_to_hash

class ServicioAutenticacion:
    def __init__(self):
        self.repo_usuario = RepositorioUsuario()
        self.usuario_actual = None

    def registrar_usuario(self, nombre, email, password, es_admin=False):
        if self.repo_usuario.obtener_por_email(email):
            raise Exception("El email ya está registrado.")
        
        # Crear hash
        password_bytes = crear_password_hash(password)
        password_hex = hash_to_string(password_bytes)
        
        nuevo_usuario = Usuario(None, nombre, email, password_hex, es_admin)
        return self.repo_usuario.guardar(nuevo_usuario)

    def login(self, email, password):
        usuario = self.repo_usuario.obtener_por_email(email)
        if usuario:
            stored_hash = string_to_hash(usuario.password_hash)
            if verificar_password(password, stored_hash):
                self.usuario_actual = usuario
                return usuario
        return None

    def logout(self):
        self.usuario_actual = None

    def esta_autenticado(self):
        return self.usuario_actual is not None

    def es_admin(self):
        return self.usuario_actual and self.usuario_actual.es_admin
