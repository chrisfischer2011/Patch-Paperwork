from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class AmpRack(BaseModel):
    rack_id: str
    rack_type: str = "112 Amp Rack"
    serial_number: Optional[str] = None
    position: int = 1
    channels: List[str] = Field(default_factory=list)
    notes: Optional[str] = None

class AmpProject(BaseModel):
    project_name: str
    date_created: datetime = Field(default_factory=datetime.now)
    racks: List[AmpRack] = Field(default_factory=list)
    customer: str = "Adamson"
    venue: Optional[str] = None

    def add_rack(self, rack: AmpRack):
        self.racks.append(rack)

    def generate_patch_summary(self):
        """Generate summary for shop build and crew cabling paperwork."""
        return f"Project: {self.project_name}\nTotal Racks: {len(self.racks)}"