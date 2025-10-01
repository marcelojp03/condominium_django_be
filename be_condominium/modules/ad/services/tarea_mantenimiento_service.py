from modules.ad.repositories.tarea_mantenimiento_repository import TareaMantenimientoRepository

class TareaMantenimientoService:

    @staticmethod
    def listar_tareas():
        return TareaMantenimientoRepository.listar()

    @staticmethod
    def obtener_tarea(idtarea):
        return TareaMantenimientoRepository.obtener_por_id(idtarea)

    @staticmethod
    def crear_tarea(data):
        return TareaMantenimientoRepository.crear(data)

    @staticmethod
    def actualizar_tarea(idtarea, data):
        return TareaMantenimientoRepository.actualizar(idtarea, data)

    @staticmethod
    def eliminar_tarea(idtarea):
        return TareaMantenimientoRepository.eliminar(idtarea)
