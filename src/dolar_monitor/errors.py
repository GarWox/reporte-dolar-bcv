class MonitorError(Exception):
    """Error base del monitor."""


class SourceError(MonitorError):
    """Una fuente de datos no respondió o devolvió datos inesperados."""


class NotificationError(MonitorError):
    """No se pudo entregar el reporte a un canal de notificación."""
