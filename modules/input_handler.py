from models.project import AmpProject
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

def save_project(project: AmpProject, filename: Optional[str] = None) -> str:
    """Save project to JSON for persistence."""
    if filename is None:
        safe_name = ''.join(c if c.isalnum() else '_' for c in project.project_name)
        filename = f"{safe_name}_{datetime.now().strftime('%Y%m%d')}.json"
    
    filepath = Path('projects') / filename
    filepath.parent.mkdir(exist_ok=True)
    
    with open(filepath, 'w') as f:
        f.write(project.model_dump_json(indent=2))
    
    return str(filepath)

def load_project(filename: str) -> AmpProject:
    """Load project from JSON."""
    with open(filename, 'r') as f:
        data = json.load(f)
    return AmpProject.model_validate(data)
