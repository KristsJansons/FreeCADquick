"""FreeCAD macro: build BIM walls from a simple JSON dimension description,
instead of hand-writing Sketcher/Arch calls for every wall.

JSON shape (see scripts/example_dims.json):

    {
      "wall_height_mm": 2700,
      "wall_thickness_mm": 250,
      "walls": [
        {"start": [0, 0], "end": [8000, 0]},
        {"start": [8000, 0], "end": [8000, 6000]}
      ]
    }

Points are [x, y] in millimetres, in the document's working plane (z=0).

Run inside FreeCAD (Macro > Execute, or via MCP execute_code):

    exec(open("/home/nrg/Documents/FreeCAD/scripts/build_from_dims.py").read())
    build_from_dims("/home/nrg/Documents/FreeCAD/scripts/example_dims.json")
"""
import json

import FreeCAD
import Draft
import Arch


def build_from_dims(json_path, doc=None):
    doc = doc or FreeCAD.ActiveDocument or FreeCAD.newDocument("maja")

    with open(json_path) as f:
        spec = json.load(f)

    height = spec.get("wall_height_mm", 2700)
    thickness = spec.get("wall_thickness_mm", 250)

    walls = []
    for i, seg in enumerate(spec["walls"]):
        start = FreeCAD.Vector(*seg["start"], 0)
        end = FreeCAD.Vector(*seg["end"], 0)
        line = Draft.make_line(start, end)
        wall = Arch.makeWall(line, width=thickness, height=height)
        wall.Label = seg.get("label", f"Wall{i+1}")
        walls.append(wall)

    doc.recompute()
    FreeCAD.Console.PrintMessage(f"Built {len(walls)} wall(s).\n")
    return walls
