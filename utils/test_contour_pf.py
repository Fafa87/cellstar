# -*- coding: utf-8 -*-
"""
Script used for external testing of contour parameter fitting process.
Date: 2013-2016
Website: http://cellstar-algorithm.org/
"""

import logging
import sys

import numpy as np

import cellstar.parameter_fitting.pf_process as pf_process
from cellstar.parameter_fitting.pf_process import run
from cellstar.parameter_fitting.pf_runner import gt_label_to_snakes, image_to_label
from cellstar.segmentation import Segmentation
from cellstar.utils import image_util, debug_util
from cellstar.utils.debug_util import image_show, image_save

global default_data_path
default_data_path = "."


def try_load_image(image_path):
    return image_util.load_image(default_data_path + image_path)


#
#
# VISUALIZATION
#
#

def test_trained_parameters(image, star_params, ranking_params, precision, avg_cell_diameter, output_name=None):
    seg = Segmentation(segmentation_precision=precision, avg_cell_diameter=avg_cell_diameter)
    for k, v in star_params.iteritems():
        seg.parameters["segmentation"]["stars"][k] = v
    for k, v in ranking_params.iteritems():
        seg.parameters["segmentation"]["ranking"][k] = v

    seg.set_frame(image)
    seg.run_segmentation()
    if output_name is None:
        image_show(seg.images.segmentation, 1)
    else:
        image_save(seg.images.segmentation, output_name)


#
#
# TESTING HELPERS
#
#

def test_pf(image_path, mask_path, precision, avg_cell_diameter, method, initial_params=None, options=None, callback_progress=None):
    frame = try_load_image(image_path)

    if options == 'invert':
        frame = 1 - frame

    gt_image = np.array(try_load_image(mask_path) * 255, dtype=int)

    gt_mask = image_to_label(gt_image)

    gt_snakes = gt_label_to_snakes(gt_mask)

    pf_process.callback_progress = callback_progress
    return run(frame, gt_snakes, precision, avg_cell_diameter, method, initial_params=initial_params)


def test_parameters(image_path, mask_path, precision, avg_cell_diameter, params, output_path=None, options=None):
    frame = try_load_image(image_path)

    if options == 'invert':
        frame = 1 - frame
    # gt_image = np.array(try_load_image(mask_path) * 255, dtype=int)

    # cropped_image, cropped_gt_label = cropped_to_gt(avg_cell_diameter, frame, gt_image)
    # gt_snakes = gt_label_to_snakes(cropped_gt_label)

    output_name = None
    if output_path is not None:
        debug_util.debug_image_path = output_path
        output_name = "trained"

    test_trained_parameters(frame, params["segmentation"]["stars"], params["segmentation"]["ranking"], precision,
                            avg_cell_diameter, output_name)


if __name__ == "__main__":
    if len(sys.argv) < 7:
        print "Usage: <script> base_path image_path mask_path precision avg_cell_diameter method {image_result_path}"
        print "Given: " + " ".join(sys.argv)
        sys.exit(-1)

    # from cellstar.core.snake import Snake
    # from cellstar.tests.experiments import smooth_contour_turns
    # Snake.smooth_contour = smooth_contour_turns

    pf_process.get_max_workers = lambda: 2
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger = logging.getLogger('cellstar.parameter_fitting')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    default_data_path = sys.argv[1]
    precision = int(sys.argv[4])
    avg_cell_diameter = float(sys.argv[5])

    image_result_path = None
    if len(sys.argv) >= 8:
        image_result_path = sys.argv[7]

    complete_params, _, _ = test_pf(sys.argv[2], sys.argv[3], precision, avg_cell_diameter, sys.argv[6])

    print "Best_params:", complete_params
    print
    print "CellProfiler autoparams:", Segmentation.encode_auto_params_from_all_params(complete_params)

    debug_util.DEBUGING = True
    if image_result_path is not None:
        test_parameters(sys.argv[2], sys.argv[3], precision, avg_cell_diameter, complete_params, image_result_path)
