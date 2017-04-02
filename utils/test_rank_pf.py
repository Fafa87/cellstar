# -*- coding: utf-8 -*-
"""
Script used for external testing of ranking parameter fitting process.
Date: 2013-2016
Website: http://cellstar-algorithm.org/
"""

import logging
import sys

import numpy as np

import cellstar.parameter_fitting.pf_rank_process as pf_rank
import cellstar.tests.test_contour_pf as test_pf
import cellstar.utils.debug_util as debug_util
from cellstar.segmentation import Segmentation
from cellstar.tests.test_contour_pf import try_load_image, image_to_label, gt_label_to_snakes


def test_rank_pf(image_path, mask_path, precision, avg_cell_diameter, method, initial_params=None, options=None, callback_progress=None):
    frame = try_load_image(image_path)

    if options == 'invert':
        frame = 1 - frame

    gt_image = np.array(try_load_image(mask_path) * 255, dtype=int)

    gt_mask = image_to_label(gt_image)

    gt_snakes = gt_label_to_snakes(gt_mask)
    pf_rank.callback_progress = callback_progress
    if method == "mp" or method == "mp_superfit":
        return pf_rank.run_multiprocess(frame, gt_snakes, precision, avg_cell_diameter, 'brutemaxbasin',
                                        initial_params=initial_params)
    else:
        return pf_rank.run_singleprocess(frame, gt_snakes, precision, avg_cell_diameter, method,
                                         initial_params=initial_params)


if __name__ == "__main__":
    if len(sys.argv) < 7:
        print "Usage: <script> base_path image_path mask_path precision avg_cell_diameter method {image_result_path}"
        print "Given: " + " ".join(sys.argv)
        sys.exit(-1)

    # from cellstar.core.snake import Snake
    # from cellstar.tests.experiments import smooth_contour_turns
    # Snake.smooth_contour = smooth_contour_turns

    pf_rank.get_max_workers = lambda: 2
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger = logging.getLogger('cellstar.parameter_fitting')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    test_pf.default_data_path = sys.argv[1]

    precision = int(sys.argv[4])
    avg_cell_diameter = float(sys.argv[5])

    image_result_path = None
    if len(sys.argv) >= 8:
        image_result_path = sys.argv[7]

    # complete_params = default_parameters(segmentation_precision=precision, avg_cell_diameter=avg_cell_diameter)
    complete_params, _, _ = test_rank_pf(sys.argv[2], sys.argv[3], precision, avg_cell_diameter, sys.argv[6])

    print "Best_params:", complete_params
    print
    print "CellProfiler autoparams:", Segmentation.encode_auto_params_from_all_params(complete_params)

    debug_util.DEBUGING = True
    if image_result_path is not None:
        test_pf.test_parameters(sys.argv[2], sys.argv[3], precision, avg_cell_diameter, complete_params,
                                image_result_path)
