# No3d Camera Utilities

No3d Camera Utilities 1.1.1 provides viewport-first camera framing and a
separate geometry-driven orthographic fit workflow. It is developed and
verified in Blender 5.2+.

## Draw Camera Frame

Use this when the creative intention is already visible in the viewport and
you want to draw the exact output boundary without first naming, selecting, or
fitting an object.

1. Position the 3D viewport at the desired angle and scale.
2. Open `N-panel → No3d Cam → Camera Framing`.
3. Run **Draw Camera Frame**.
4. Drag the complete output boundary and release to create the camera.

While drawing, Blender's native crosshair cursor indicates that the framing
tool is loaded. Hold `Space` and move the pointer to reposition the entire
in-progress rectangle without changing its dimensions. Release `Space` to
continue resizing. Press `Esc` or right-click to cancel without creating scene
data.

The resulting camera preserves the viewport projection and maps the marquee to
the complete render frame:

- orthographic viewport → orthographic camera;
- perspective viewport → perspective camera with solved lens and shift;
- output aspect comes from the marquee's pixel dimensions;
- selection is optional metadata and never changes framing;
- no implicit padding or camera parenting;
- the cursor becomes Blender's crosshair while the tool is active;
- hold `Space` while dragging to reposition the complete frame;
- cancelling creates no camera.

The camera is positioned from the viewport, not from the selected object or a
world plane. In orthographic views, Blender's view matrix may be centered on
the navigation pivot rather than a usable camera eye point. Version 1.1.1
accounts for this by backing the camera away by the captured viewport distance,
keeping the viewed subject in front of the camera without changing the drawn
boundary.

After completion, the new camera becomes the scene camera and Blender enters
camera view. The saved render should contain the region that was inside the
marquee.

## Selected Mesh Fit

**Fit Selected Mesh — Orthographic** remains available as the secondary,
geometry-driven workflow. It deliberately has different semantics: selection
defines the subject bounds. Use Draw Camera Frame when the viewport and your
gesture should be authoritative.

Legacy 3D mesh-camera and editable framing-plane operators remain registered
for file/API compatibility, but their controls are no longer exposed as the
recommended framing workflow.

## Features

- Projection-aware viewport marquee framing
- Perspective lens and shift reconstruction
- Orthographic scale, position, and safe-depth reconstruction
- Selected-mesh orthographic fitting
- Mesh camera render utilities

## Troubleshooting

### Camera settings are missing from Properties

This is normally Blender editor state, not a Camera Utilities registration
failure. The Properties editor can be pinned to another datablock, such as a
Geometry Nodes group. While pinned, it ignores the selected camera and the
native green Camera Data Properties tab is unavailable.

Clear the pin in the Properties editor header, then select the camera again.
The Camera Data tab should return. No add-on reload is required.

### A camera created before 1.1.1 looks past the subject

Delete or replace that camera and draw the frame again. Cameras created by the
earlier orthographic placement code are not migrated automatically because
changing existing scene cameras could invalidate intentional edits.

### The result has the right aspect but the wrong content

Confirm that the viewport was positioned before starting the command and that
the boundary was drawn in the same 3D Viewport where the command was invoked.
Selection does not recenter Draw Camera Frame; this is intentional.

## Compatibility

- Extension manifest minimum: Blender 4.2
- Current development and acceptance target: Blender 5.2+

## Installation

1. Download or clone this repository.
2. In Blender, go to **Edit > Preferences > Add-ons > Install…**
3. Select the `no3d_camera_utilities/__init__.py` file (or a zip of the `no3d_camera_utilities` folder).
4. Enable **No3d Camera Utilities** in the add-ons list.

## Usage

Open the sidebar in the 3D Viewport (press `N`) and select the **No3d Cam** tab.

Panel location: `View3D > Sidebar > No3d Cam`
