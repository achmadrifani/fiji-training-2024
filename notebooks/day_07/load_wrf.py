import os
from netCDF4 import Dataset
import wrf
from wrf import getvar


def load_one_wrf(filename: str, varname: str):
    """
    Load a variable from a WRF file.

    Parameters:
    filename : str
        Path to the WRF file.
    varname : str
        Variable name to extract.

    Returns:
    xr.DataArray
        The extracted variable as an xarray DataArray.

    Raises:
    FileNotFoundError
        If the specified file does not exist.
    """
    # Check if the file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found")

    # Open the file
    ncfile = Dataset(filename)

    # Extract the variable
    var = getvar(ncfile, varname)

    return var


def load_all_wrf(folder_path: str, varname: str):
    """
    Load a variable from all WRF files in a folder and concatenate them over time.

    Parameters:
    folder_path : str
        Path to the folder containing the WRF files.
    varname : str
        Variable name to extract.

    Returns:
    xr.DataArray
        The concatenated variable over time from all WRF files.

    Raises:
    FileNotFoundError
        If the specified folder does not exist or contains no WRF files.
    ValueError
        If no valid WRF files are found in the specified folder.
    """
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Folder {folder_path} not found")

    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter for valid NetCDF files
    nc_files = [os.path.join(folder_path, f) for f in files if f.startswith('wrfout')]

    # Check if there are any NetCDF files in the folder
    if not nc_files:
        raise ValueError(f"No NetCDF files found in folder {folder_path}")

    # Open all NetCDF files
    ncfiles = [Dataset(file) for file in nc_files]

    # Extract and concatenate the variable over time
    var = getvar(ncfiles, varname, timeidx=wrf.ALL_TIMES, method="cat")

    return var


'''
Usage example
folder_path = 'D:/Projects/fiji-training-2024/data/wrf/'
slp = load_all_wrf(folder_path, 'slp')
'''