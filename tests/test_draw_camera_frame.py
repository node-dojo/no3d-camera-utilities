"""Blender 5.2+ acceptance probe for Draw Camera Frame.

Run with:
  blender --factory-startup --background --python tests/test_draw_camera_frame.py
"""

from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace

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
        viewport_distance=10.0,
        long_edge_px=2048,
    )
    error_px = addon.camera_marquee_projection_error_px(scene, camera, corners)

    expected_aspect = (marquee[2] - marquee[0]) / (marquee[3] - marquee[1])
    actual_aspect = res_x / res_y
    assert abs(actual_aspect - expected_aspect) <= 1.0 / min(res_x, res_y)
    assert camera.data.type == projection
    assert camera.parent is None
    if projection == "ORTHO":
        assert all((camera.matrix_world.inverted() @ point).z < 0.0 for point in corners)
    assert error_px <= 0.5, (projection, error_px)
    print(f"DRAW_CAMERA_FRAME_{projection}_OK error_px={error_px:.6f}")


check_projection("PERSP")
check_projection("ORTHO")

original_filepath = bpy.data.filepath
assert addon.framed_view_output_path.__name__ == "framed_view_output_path"
with tempfile.TemporaryDirectory() as temp_dir:
    blend_path = str(Path(temp_dir) / "framed-test.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    output_path = Path(addon.framed_view_output_path())
    assert output_path.parent == Path(temp_dir)
    assert output_path.name.startswith("framed_view_")
    assert output_path.suffix == ".png"
    render_scene = addon.create_framed_render_scene(bpy.context.scene, str(output_path))
    assert render_scene.render.image_settings.file_format == "PNG"
    bpy.data.scenes.remove(render_scene)

visible = bpy.data.objects.new("Visible", None)
hidden = bpy.data.objects.new("Viewport Hidden", None)
bpy.context.scene.collection.objects.link(visible)
bpy.context.scene.collection.objects.link(hidden)
hidden.hide_set(True)
snapshot = addon.snapshot_hide_render(bpy.context.scene)
addon.hide_viewport_hidden_for_render(bpy.context)
assert visible.hide_render is False
assert hidden.hide_render is True
addon.restore_hide_render(bpy.context.scene, snapshot)
assert hidden.hide_render is False

visible.hide_render = True
enabled, disabled, changed = addon.match_render_visibility_to_viewport(bpy.context)
assert (enabled, disabled, changed) == (len(bpy.context.scene.objects) - 1, 1, 2)
assert visible.hide_render is False
assert hidden.hide_render is True

addon.register()
assert hasattr(bpy.ops.render, "no3d_framed_view_clipboard")
assert hasattr(bpy.ops.render, "no3d_match_visibility_to_viewport")
plain_camera_data = bpy.data.cameras.new("Plain Active Camera Data")
plain_camera = bpy.data.objects.new("Plain Active Camera", plain_camera_data)
bpy.context.scene.collection.objects.link(plain_camera)
plain_camera_context = SimpleNamespace(
    scene=SimpleNamespace(camera=plain_camera),
    area=SimpleNamespace(type="VIEW_3D"),
)
assert addon.RENDER_OT_no3d_framed_view_clipboard.poll(plain_camera_context)
addon.unregister()
print("DRAW_CAMERA_FRAME_TEST_OK")
