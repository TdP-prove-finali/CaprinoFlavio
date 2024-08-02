from dataclasses import dataclass
@dataclass
class Earthquake:
    time: str
    latitude: float
    longitude: float
    depth: float
    mag: float
    magType: str
    nst: float
    gap: float
    dmin: float
    rms: float
    net: str
    id: str
    updated: str
    place: str
    type: str
    horizontalError: float
    depthError: float
    magError: float
    magNst: float
    status: str
    locationSource: str
    magSource: str

    def __str__(self):
        return f"{self.id}, {self.place}, {self.time}"

    def __hash__(self):
        return hash(self.id)