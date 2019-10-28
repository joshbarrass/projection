import math

try:
    import numpy as np
    have_numpy = True
except ImportError:
    have_numpy = False

class Screen(object):
    def __init__(self, size, fov):
        self.size = size
        self.set_fov(fov)

    def set_fov(self, fov):
        self.fov = fov
        self.fov_rad = math.radians(fov)
        width = self.size[0]
        self.z = width/(2*math.tan(self.fov_rad/2))

    def transform_coords(self, coords, add=True):
        """coord can be numpy array or any other iterable containing
3D coordinates"""
        isarray = isinstance(coords, np.ndarray)
        if isarray:
            if len(coords.shape) != 2 or coords.shape[1] != 3:
                raise TypeError("coords must contain 3D coordinates")
        else:
            if len(coords[0]) != 3:
                raise TypeError("coords must contain 3D coordiantes")

        if isarray:
            zeros = np.zeros(coords.shape)
            coords = coords.astype("float64")
            if add:
                coords[:,2] += self.z
            mask = coords[:,2]>0
            trans = coords[mask]
            zeros[mask] = trans*(self.z/trans[:,2])[:,None]
            return zeros
        # else:
        for i in range(len(coords)):
            if add:
                coords[i][2] += self.z
            if coords[i][2] <= 0:
                coords[i] = [inf, inf, inf]
        return [(c[0]*(self.z/c[2]), c[1]*(self.z/c[2]), self.z) if c[2] > 0 else (0,0,0) for c in coords]
