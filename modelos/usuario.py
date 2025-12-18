class Usuario:
    def __init__(self, id_usuario, nombre, email, password_hash, es_admin=False):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.password_hash = password_hash
        self.es_admin = es_admin

    def __str__(self):
        return f"Usuario(id={self.id_usuario}, nombre={self.nombre}, email={self.email}, admin={self.es_admin})"
