"""FreeCAD macro: import a DXF parcel boundary (from QGIS export) and report
its bounding box / scale, so the sketch can be checked against known
real-world dimensions before building on top of it.

Run inside FreeCAD (Macro > Execute, or via MCP execute_code):

    exec(open("/home/nrg/Documents/FreeCAD/scripts/import_boundary.py").read())
    import_boundary("/home/nrg/Documents/FreeCAD/source-data/kadastrs/robeza.dxf")
"""
import FreeCAD
import importDXF


def import_boundary(dxf_path, doc=None):
    doc = doc or FreeCAD.ActiveDocument or FreeCAD.newDocument("maja")
    importDXF.insert(dxf_path, doc.Name)
    doc.recompute()

    imported = [o for o in doc.Objects if o.TypeId.startswith("Part::") or o.TypeId.startswith("Draft::")]
    if not imported:
        FreeCAD.Console.PrintWarning("No objects found after DXF import.\n")
        return None

    bbox = imported[0].Shape.BoundBox
    for obj in imported[1:]:
        if hasattr(obj, "Shape"):
            bbox.add(obj.Shape.BoundBox)

    FreeCAD.Console.PrintMessage(
        f"Imported {len(imported)} object(s). "
        f"BoundBox: {bbox.XLength:.0f} x {bbox.YLength:.0f} mm "
        f"(= {bbox.XLength/1000:.1f} x {bbox.YLength/1000:.1f} m)\n"
    )
    return imported
