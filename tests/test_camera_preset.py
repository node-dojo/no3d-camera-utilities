"""Blender 5.2+ acceptance probe for the 100 mm icon camera preset."""

from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import no3d_camera_utilities as addon  # noqa: E402


scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 0.001
scene.unit_settings.length_unit = "MILLIMETERS"

addon.register()
try:
    result = bpy.ops.object.add_100mm_ortho_icon_camera(placement="WORLD")
    assert result == {"FINISHED"}
    camera = scene.camera
    assert camera is not None
    assert camera.name == "100mm Ortho - Icon cam"
    assert camera.data.type == "ORTHO"
    assert abs(camera.data.ortho_scale - 100.0) < 1e-3
    assert abs(camera.location.z - 100.0) < 1e-3
    assert abs(camera.location.x) < 1e-6 and abs(camera.location.y) < 1e-6
    assert len(camera.children) == 1
    guide = camera.children[0]
    assert guide.name == "threes guide"
    assert guide.get("no3d_camera_guide") == "thirds"
    assert guide.hide_render
    assert len(guide.data.edges) == 8
    assert tuple(round(v, 6) for v in guide.matrix_world.translation) == (0.0, 0.0, 0.0)
    assert scene.render.resolution_x == scene.render.resolution_y == 2048
    print("ICON_CAMERA_PRESET_OK")
finally:
    addon.unregister()
