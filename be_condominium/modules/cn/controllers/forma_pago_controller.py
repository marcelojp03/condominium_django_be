from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from modules.cn.services.forma_pago_service import FormaPagoService
from modules.cn.dtos.forma_pago_dto import FormaPagoSerializer

@api_view(['GET'])
def forma_pago_listar(request):
    formas = FormaPagoService.listar_formas()
    serializer = FormaPagoSerializer(formas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def forma_pago_detalle(request, idformapago):
    forma = FormaPagoService.obtener_forma(idformapago)
    if forma:
        serializer = FormaPagoSerializer(forma)
        return Response(serializer.data)
    return Response({'error': 'Forma de pago no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def forma_pago_crear(request):
    serializer = FormaPagoSerializer(data=request.data)
    if serializer.is_valid():
        FormaPagoService.crear_forma(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def forma_pago_actualizar(request, idformapago):
    serializer = FormaPagoSerializer(data=request.data)
    if serializer.is_valid():
        FormaPagoService.actualizar_forma(idformapago, serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def forma_pago_eliminar(request, idformapago):
    FormaPagoService.eliminar_forma(idformapago)
    return Response({'mensaje': 'Forma de pago desactivada'}, status=status.HTTP_204_NO_CONTENT)
