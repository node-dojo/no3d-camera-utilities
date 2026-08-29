"""Blender 5.2+ acceptance probe for Draw Camera Frame.

Run with:
  blender --factory-startup --background --python tests/test_draw_camera_frame.py
"""

from pathlib import Path
import sys

import bpy
from mathutils import Matrix


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import no3d_camera_utilities as addon  # noqa: E402


def check_projection(projection):
    scene = bpy.context.scene
    depsgraph = bpy.context.evaluated_depsgraph_get()
    viewport_size = (1200, 800)
    marquee = (180, 120, 930, 650)

    source_data = bpy.data.cameras.new(f"SourceData_{projection}")
    source = bpy.data.objects.new(f"Source_{projection}", source_data)
    scene.collection.objects.link(source)
    source.matrix_world = Matrix.Identity(4)
    source_data.type = projection
    source_data.lens = 47.0
    source_data.ortho_scale = 12.0
    projection_matrix = source.calc_matrix_camera(
        depsgraph,
        x=viewport_size[0],
        y=viewport_size[1],
        scale_x=1.0,
        scale_y=1.0,
    )

    camera_data = bpy.data.cameras.new(f"ResultData_{projection}")
    camera = bpy.data.objects.new(f"Result_{projection}", camera_data)
    scene.collection.objects.link(camera)
    res_x, res_y, corners = addon.configure_camera_from_view_marquee(
        scene,
        camera,
        source.matrix_world.inverted(),
        projection_matrix @ source.matrix_world.inverted(),
        viewport_size,
        marquee,
        projection,
        source_data.lens,
        0.01,
        1000.0,
        2048,
    )
    error_px = addon.camera_marquee_projection_error_px(scene, camera, corners)

    expected_aspect = (marquee[2] - marquee[0]) / (marquee[3] - marquee[1])
    actual_aspect = res_x / res_y
    assert abs(actual_aspect - expected_aspect) <= 1.0 / min(res_x, res_y)
    assert camera.data.type == projection
    assert camera.parent is None
    assert error_px <= 0.5, (projection, error_px)
    print(f"DRAW_CAMERA_FRAME_{projection}_OK error_px={error_px:.6f}")


check_projection("PERSP")
check_projection("ORTHO")
print("DRAW_CAMERA_FRAME_TEST_OK")
