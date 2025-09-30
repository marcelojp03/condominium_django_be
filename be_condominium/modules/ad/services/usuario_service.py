from modules.ad.repositories import usuario_repository

def obtener_todos():
    return usuario_repository.listar_todos()

def obtener(usuario_id):
    return usuario_repository.obtener_por_id(usuario_id)

def crear(datos, rol_id=None):
    return usuario_repository.crear(datos, rol_id)

def actualizar(usuario_id, datos):
    usuario = usuario_repository.obtener_por_id(usuario_id)
    if usuario:
        return usuario_repository.actualizar(usuario, datos)
    return None

def eliminar(usuario_id):
    usuario = usuario_repository.obtener_por_id(usuario_id)
    if usuario:
        usuario_repository.eliminar(usuario)
        return True
    return False
