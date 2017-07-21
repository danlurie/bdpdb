import os
import sys
import numpy as np
import pandas as pd
import nibabel as nib

def roi_search(roi_path, store_path, out_dir):
    """
    Parameters
    ----------
    roi_path : str
        Path to a 3D ROI file in the same space as the patient masks.
    store_path : str
        Path to a Pandas HDFSstore (e.g. file.h5) containing mask data.
    out_dir : str
        Path to the directory where the output CSV should be written.
    """
    # Load ROI
    roi_img = nib.load(roi_path)
    roi_data = roi_img.get_data()
    # Get ROI voxels
    roi_data_flat = roi_data.ravel()
    roi_voxels = np.nonzero(roi_data_flat)[0]
    # Load the mask store
    restore = pd.HDFStore(store_path)
    restore_df = restore.select('df')
    # Run the search
    roi_res = restore_df.iloc[roi_voxels,:]
    vox_counts = roi_res.sum(axis=0)
    has_damage = vox_counts[vox_counts > 0]
    damage_pcts = (has_damage / roi_voxels.shape) * 100
    # Create and write the output file
    out_df = pd.concat([has_damage.astype(int), damage_pcts], axis=1)
    out_df.columns = ['num_vox', 'pct_roi']
    out_path = os.path.join(out_dir, os.path.basename(roi_path).rstrip('.nii.gz')+'.csv')
    out_df.to_csv(out_path, index_label='patient')
    # Close the store
    restore.close()

if __name__ == "__main__":
    STORE_PATH = '/home/despoB/dlurie/Projects/bdpdb/notebooks/mask_data.h5'

    roi_path, out_dir = sys.argv[1:]
    
    print("Calculating overlap for "+roi_path)

    roi_search(roi_path, STORE_PATH, out_dir)

