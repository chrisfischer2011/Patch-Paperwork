from typing import Optional, Dict
from models.project import AmpProject, AmpRack

class AmpRackHandler:
    """Modular handler for creating and managing amp racks and projects."""
    def __init__(self):
        self.current_project: Optional[AmpProject] = None

    def create_new_project(self, name: str, customer: str = "Adamson", venue: str = None) -> AmpProject:
        self.current_project = AmpProject(
            project_name=name,
            customer=customer,
            venue=venue
        )
        return self.current_project

    def add_rack(self, rack_data: Dict) -> AmpRack:
        rack = AmpRack(**rack_data)
        if self.current_project:
            self.current_project.add_rack(rack)
        return rack

    def get_patch_summary(self) -> str:
        if self.current_project:
            return self.current_project.generate_patch_summary()
        return "No project loaded."