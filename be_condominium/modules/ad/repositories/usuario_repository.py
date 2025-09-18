from modules.ad.models.usuario import Usuario

def listar_todos():
    return Usuario.objects.all()

def obtener_por_id(usuario_id):
    return Usuario.objects.filter(id=usuario_id).first()

def crear(datos):
    return Usuario.objects.create(**datos)

def actualizar(usuario, datos):
    for key, value in datos.items():
        setattr(usuario, key, value)
    usuario.save()
    return usuario

def eliminar(usuario):
    usuario.delete()
