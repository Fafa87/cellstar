import numpy as np
import scipy.misc

import cellstar

input_image = scipy.misc.imread("input_images/sample_brightfield.tif")
print ("Input image shape: {0} and dtype: {1}"
       .format(input_image.shape, input_image.dtype))

segmentator = cellstar.Segmentation(segmentation_precision=9, avg_cell_diameter=35)
segmentator.set_frame(input_image)
segmentation, snakes = segmentator.run_segmentation()

print ("Segmentation run successfully and returned labeled image of shape: {0} and dtype: {1}"
       .format(segmentation.shape, segmentation.dtype))

number_of_found_cells = len(np.unique(segmentation))-1
print ("Found {0} cells, saved at output_segmentation."
       .format(number_of_found_cells))

scipy.misc.imsave("output_segmentation/sample_brightfield_segmented.tif", segmentation)