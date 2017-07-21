import argparse
import pandas as pd
from itertools import combinations
parser = argparse.ArgumentParser()

parser.add_argument('--pct_thresh', nargs=1, type=int)
parser.add_argument('--roi_stats', nargs='+')

assert len(roi_stats) >= 2, "Please specify at least two ROI coverage files"


# Get patient lists
for roi in roi_stats:
    # Load the CSV
    # Threshold the list
    # Grab any remaining patients
    # Return a set somehow? Maybe make this a function

# Create an array of the sets, or maybe a set of tuples, (name, set)
sets = BLAH
# Get the intersection of all ROIs

# Pairwise comparisons
for pair in combinations(sets, 2):
    # Create sets
    A = set(pair[0])
    B = pair[1]
    
    # A and B
    # A but not B
    # B but not A

# How best to save this data? As an array of long tuples? How to output them too...

# Compute sets
for roi in roi_stats:


