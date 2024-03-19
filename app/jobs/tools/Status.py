from enum import Enum


class Status(Enum):
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    FLYING = "flying"
    SCANNING = "scanning"
