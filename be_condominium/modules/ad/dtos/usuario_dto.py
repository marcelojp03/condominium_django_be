from rest_framework import serializers
from modules.ad.models.usuario import Usuario
from modules.ad.models.rol import Rol
from modules.ad.dtos.rol_dto import RolSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    rol_id = serializers.IntegerField(write_only=True, required=False)
    rol_nombre = serializers.SerializerMethodField()    
    password = serializers.CharField(write_only=True, required=False)    
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'correo', 'foto', 'estado', 'roles', 'rol_id', 'rol_nombre', 'password']

    def get_roles(self, obj):
        roles = obj.roles  # usa el @property
        return RolSerializer(roles, many=True).data

    def get_rol_nombre(self, obj):
        rol = obj.roles.first()
        return rol.nombre if rol else None

    def validate_correo(self, value):
        usuario_id = self.instance.id if self.instance else None
        if Usuario.objects.exclude(id=usuario_id).filter(correo=value).exists():
            raise serializers.ValidationError("Este correo ya está en uso por otro usuario.")
        return value        