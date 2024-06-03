# Class vtkfile for read and write operations

import os
from pathlib import Path
import pyvista as pv
import scipy as sp
import sys


class Vtkfile:
    data = None
    directory = None
    name = None
    cells = None

    def __init__(self, path=None):
        if path:
            self.read(path)

    def read(self, path):
        """Read vtk file from path and store attributes. """
        fullPath = Path(path).resolve()
        self.data = pv.read(fullPath)

        self.directory = str(fullPath.parent)
        self.name = str(fullPath.stem)
        self.cells = self.data.extract_cells(range(self.data.n_cells))

    def write(self, matfile, arrays, extractCells):
        """Write mat file using given arrays"""
        
        # Create empty dict for data
        matdata = dict()

        # Add points
        matdata["points"] = self.data.points

        # Add connectivity for different celltypes and increase node indices by 1 for Matlab
        if extractCells:
            for celltype in set(self.cells.celltypes):
                matdata[f"cells_{pv.CellType(celltype).name.lower()}"] = (
                    self.cells.cells_dict[celltype] + 1
                )
        else:
            matdata["celltypes"] = self.cells.celltypes
            matdata["offsets"] = self.cells.offset + 1
            matdata["connectivity"] = self.cells.cell_connectivity + 1

        # Add arrays
        for array in arrays:
            if array in self.data.array_names:
                matdata[array.replace("-", "_")] = self.data[array]
            else:
                print(f'Could not find array {array} in arrays. Skipping identifier.')

        sp.io.savemat(file_name=matfile, mdict=matdata, oned_as="column")
        print(f"Wrote {matfile}.")


def main():
    # Open vtkfile from first argument
    vtkfile = Vtkfile(sys.argv[1])

    # Read choices from additional arguments or 
    if len(sys.argv) > 2:
        arrays = sys.argv[2:]
    else:
        arrays = vtkfile.data.array_names

    # Write mat file at input location under same name
    vtkfile.write(f'{vtkfile.directory}{os.sep}{vtkfile.name}.mat', arrays, False)


if __name__ == "__main__":
    main()
