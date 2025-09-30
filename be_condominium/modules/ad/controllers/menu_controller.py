from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models.usuario_rol import UsuarioRol
from ..models.rol_recurso import RolRecurso
from ..models.recurso import Recurso
from ..models.subrecurso import Subrecurso


@api_view(['GET'])
def obtener_menu_por_usuario(request, usuario_id):
    try:
        # Obtener todos los roles del usuario
        roles_usuario = UsuarioRol.objects.filter(usuario_id=usuario_id).values_list('rol_id', flat=True)

        # Obtener todos los permisos (rol-recurso-subrecurso) asociados a esos roles
        permisos = RolRecurso.objects.filter(rol_id__in=roles_usuario)

        # Construir el menú agrupado por recurso
        menu = {}
        for permiso in permisos:
            recurso = permiso.recurso
            subrecurso = permiso.subrecurso

            if recurso.id not in menu:
                menu[recurso.id] = {
                    "nombre": recurso.nombre,
                    "descripcion": recurso.descripcion,
                    "subrecursos": []
                }

            menu[recurso.id]["subrecursos"].append({
                "nombre": subrecurso.nombre,
                "descripcion": subrecurso.descripcion,
                "url": subrecurso.url
            })

        # Convertir el diccionario en lista
        menu_final = list(menu.values())
        return Response(menu_final, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
