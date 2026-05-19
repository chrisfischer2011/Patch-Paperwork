from models.project import AmpRack, AmpProject
from typing import Optional

def create_amp_rack(rack_id: str, rack_type: str = "112 Amp Rack", serial_number: Optional[str] = None, position: int = 1, channels: list = None, notes: Optional[str] = None) -> AmpRack:
    if channels is None:
        channels = []
    return AmpRack(
        rack_id=rack_id,
        rack_type=rack_type,
        serial_number=serial_number,
        position=position,
        channels=channels,
        notes=notes
    )

class AmpRackHandler:
    def __init__(self):
        self.project = AmpProject(project_name="New Project")

    def add_rack(self, rack):
        self.project.add_rack(rack)
        return self.project