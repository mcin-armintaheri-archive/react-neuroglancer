from __future__ import print_function

import argparse
import numpy as np

import neuroglancer

ap = argparse.ArgumentParser()
ap.add_argument(
    '-a',
    '--bind-address',
    help='Bind address for Python web server.  Use 127.0.0.1 (the default) to restrict access '
    'to browers running on the local machine, use 0.0.0.0 to permit access from remote browsers.')
ap.add_argument(
    '--static-content-url', help='Obtain the Neuroglancer client code from the specified URL.')
args = ap.parse_args()

def set_server_bind_adress(neuroglancer, address="localhost", port=9000):
    neuroglancer.set_server_bind_address(address, port)

if args.bind_address:
    set_server_bind_adress(neuroglancer, args.bind_address)
else:
    set_server_bind_adress(neuroglancer)

a = np.zeros((3, 100, 100, 100), dtype=np.uint8)
ix, iy, iz = np.meshgrid(* [np.linspace(0, 1, n) for n in a.shape[1:]], indexing='ij')
a[0, :, :, :] = np.abs(np.sin(4 * (ix + iy))) * 255
a[1, :, :, :] = np.abs(np.sin(4 * (iy + iz))) * 255
a[2, :, :, :] = np.abs(np.sin(4 * (ix + iz))) * 255

b = np.cast[np.uint32](np.floor(np.sqrt((ix - 0.5)**2 + (iy - 0.5)**2 + (iz - 0.5)**2) * 10))
b = np.pad(b, 1, 'constant')

viewer = neuroglancer.Viewer()
with viewer.txn() as s:
    s.voxel_size = [500000, 500000, 500000]
    s.layers.append(
        name='a',
        layer=neuroglancer.LocalVolume(
            data=a,
            # offset is in nm, not voxels
            offset=(20000, 30000, 15000),
            voxel_size=s.voxel_size,
        ),
        shader="""
void main() {
  emitRGB(vec3(toNormalized(getDataValue(0)),
               toNormalized(getDataValue(1)),
               toNormalized(getDataValue(2))));
}
""")
    s.layers.append(
        name='b',
        layer=neuroglancer.LocalVolume(
            data=b,
            voxel_size=s.voxel_size,
        ))
    s.layers.append(
        name='big brain',
        layer=neuroglancer.Layer({
            'source': 'precomputed://https://neuroglancer.humanbrainproject.org/precomputed/BigBrainRelease.2015/8bit',
            'type': 'image'
        })
    )

print(viewer)
