# No3d Camera Utilities

## Draw Camera Frame

Position the 3D viewport exactly as desired, run **Draw Camera Frame**, then
drag the complete output boundary. The resulting camera preserves the current
viewport projection and maps the marquee to the entire render frame:

- orthographic viewport → orthographic camera;
- perspective viewport → perspective camera with solved lens and shift;
- output aspect comes from the marquee's pixel dimensions;
- selection is optional metadata and never changes framing;
- no implicit padding or camera parenting;
- cancelling creates no camera.

**Fit Selected Mesh — Orthographic** remains available as the secondary,
geometry-driven workflow.

A Blender add-on providing 2D/3D mesh camera tools, framing helpers, and render utilities.

## Features

- Make 2D and 3D mesh cameras from selected geometry
- Framing plane and marquee-based camera fitting
- Mesh camera render utilities

## Requirements

- Blender 4.2 or newer

## Installation

1. Download or clone this repository.
2. In Blender, go to **Edit > Preferences > Add-ons > Install…**
3. Select the `no3d_camera_utilities/__init__.py` file (or a zip of the `no3d_camera_utilities` folder).
4. Enable **No3d Camera Utilities** in the add-ons list.

## Usage

Open the sidebar in the 3D Viewport (press `N`) and select the **No3d Cam** tab.

Panel location: `View3D > Sidebar > No3d Cam`
