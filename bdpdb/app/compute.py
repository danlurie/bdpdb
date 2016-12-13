from os import path
from nibabel import load, affines
from pandas import DataFrame, HDFStore
from numpy import ravel, ravel_multi_index, random, prod
#import numpy as np
#import pandas as pd
#import nibabel as nib
#from nilearn import image

def add_replace_patient_mask(patient_number, mask_path, store_path):
    """
    Add/replace a new/existing patient/mask to the damage database.
    
    Parameters
    ----------
    patient_number : str
    mask_path : str
        Path the patient's lesion mask. Must be in MNI space,
        with 2mm voxels, and have RPI orientation.
    store_path : str
        Path to a Pandas HDFSstore (e.g. file.h5)
    """
    # Check inputs
    assert isinstance(patient_number, str)
    assert path.exists(mask_path)
    
    # Load the mask image.
    mask_data = load(mask_path).get_data()
    
    # Open the HD5 store, add a column for the new patient, then close the store.
    store = HDFStore(store_path)
    data_df = store.get('df')
    data_df[patient_number] = mask_data.ravel()
    store.put('df', data_df, format='t')
    print(store.df.columns)
    store.flush()
    store.close()

def coordinate_search(mni_coordinates, img_shape, inverse_affine, store_path):
    """
    
    Parameters
    ----------
    coordinates : tuple
        MNI coordinates (x,y,z)
    img_shape : tuple
        Voxel dimensions of the 3D mask images to be searched.
    inverse_affine : array-like
        Mapping from MNI space to voxel-space.
    store_path : str
        Path to a Pandas HDFSstore (e.g. file.h5)
        
    Returns
    -------
    patients : array-like
        A list of patients with damage at the search coordinate.
        
    Notes
    -----
    Currently only able to handle 2mm resolution MNI coordinates.
    """

    voxel_coordinates = affines.apply_affine(inverse_affine, list(mni_coordinates))
    voxel_coordinates = [int(i) for i in voxel_coordinates]
    voxel_index = ravel_multi_index(voxel_coordinates, img_shape)
    
    restore = HDFStore(store_path)
    vox_row = restore.select('df', start=voxel_index, stop=voxel_index+1)
    res = vox_row.T.iloc[:,0] == 1
    patients = list(res[res == True].index)
    restore.close()
    
    return patients
"""
def generate_overlap_iamge(overlap_image_path):
    
    # Get an array containing the mask_paths for all patients in the database.
    mask_files = Patient.
    
    # Stack mask images
    mask_stack_img = image.concat_imgs(mask_files)
    
    # Sum the mask stack
    overlap_img = image.math_img("np.sum(img1, axis=-1)", img1=mask_stack_img)

    # Save the image
    overlap_img.to_filename(overlap_image_path)
"""
def test_rand():
    foo = random.rand(50)
    res = prod(foo)
    return res

if __name__ == '__main__':
    print("Nothing to see here, buddy.")

