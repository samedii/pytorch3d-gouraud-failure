import torch
import pytorch3d
import torch
import numpy as np
import numpy as np
import pytorch3d.renderer
import pytorch3d.io


def cameras(azims, device):
    R, T = pytorch3d.renderer.look_at_view_transform(
        25.6, 15.0, azims, at=((0.0, 10.0, 0.0),)
    )
    return pytorch3d.renderer.FoVPerspectiveCameras(
        device=device, R=R, T=T, znear=1, zfar=1000
    )


def renderer(azims, image_size, device):
    cameras_ = cameras(azims, device)
    return pytorch3d.renderer.MeshRenderer(
        rasterizer=pytorch3d.renderer.MeshRasterizer(
            cameras=cameras_,
            raster_settings=pytorch3d.renderer.RasterizationSettings(
                image_size=image_size,
                blur_radius=np.log(1.0 / 1e-4 - 1.0) * 1e-5,
                faces_per_pixel=50,
            ),
        ),
        shader=pytorch3d.renderer.SoftGouraudShader(
            device=device,
            cameras=cameras_,
            lights=pytorch3d.renderer.lighting.AmbientLights(device=device),
            blend_params=pytorch3d.renderer.BlendParams(
                background_color=(1.0, 1.0, 1.0),
            ),
        ),
    )


def render(mesh, azims, image_size, device):
    return renderer(azims, image_size, device)(mesh)


DEVICE = torch.device("cuda")
BATCH_SIZE = 4
IMAGE_SIZE = (256, 256)

mesh = pytorch3d.io.load_objs_as_meshes(
    ["person.obj"],
    device=DEVICE,
)
texture = torch.zeros((1, mesh.verts_packed().shape[0], 3), device=DEVICE)
mesh.textures = pytorch3d.renderer.TexturesVertex(verts_features=texture)


azims = torch.rand(BATCH_SIZE, device=DEVICE)
with torch.no_grad():
    images = render(mesh.extend(BATCH_SIZE), azims, IMAGE_SIZE, DEVICE)
