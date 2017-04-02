# -*- coding: utf-8 -*-
"""
Script used for external testing of entire parameter fitting process.
Date: 2013-2016
Website: http://cellstar-algorithm.org/
"""


import logging
import sys

import cellstar.parameter_fitting.pf_process as pf_process
import cellstar.parameter_fitting.pf_rank_process as pf_rank
import cellstar.utils.debug_util as debug_util
from cellstar.segmentation import Segmentation

import cellstar.tests.test_contour_pf as test_pf
from cellstar.tests.test_rank_pf import test_rank_pf

logger = logging.getLogger(__name__)

def show_progress(fraction):
    print "Progress {0:.1f}%".format(fraction * 100)

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print "Usage: <script> base_path image_path mask_path precision avg_cell_diameter method {image_result_path} {-O options}"
        print "Given: " + " ".join(sys.argv)
        sys.exit(-1)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger = logging.getLogger('cellstar.parameter_fitting')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    method = sys.argv[6]

    workers_num = 2
    callback_progress = None
    if method == "mp_superfit":
        workers_num = 6
        callback_progress = show_progress
    pf_process.get_max_workers = lambda: workers_num
    pf_rank.get_max_workers = lambda: workers_num

    image_result_path = None
    options = None
    if len(sys.argv) >= 8:
        if sys.argv[7] == '-O':
            options = sys.argv[8]
        else:
            image_result_path = sys.argv[7]

    if len(sys.argv) >= 9:
        if sys.argv[8] == '-O':
            options = sys.argv[9]

    #from cellstar.core.snake import Snake
    #from cellstar.tests.experiments import smooth_contour_turns
    #Snake.smooth_contour = smooth_contour_turns

    test_pf.default_data_path = sys.argv[1]
    image_path = sys.argv[2]
    mask_path = sys.argv[3]
    precision = int(sys.argv[4])
    avg_cell_diameter = float(sys.argv[5])

    #from cellstar.utils.params_util import default_parameters
    #default = default_parameters(segmentation_precision=precision, avg_cell_diameter=avg_cell_diameter)

    #complete_params = full_params_contour
    full_params_contour, _, _ = test_pf.test_pf(image_path, mask_path, precision, avg_cell_diameter, method, options=options, callback_progress=callback_progress)
    complete_params, _, _ = test_rank_pf(image_path, mask_path, precision, avg_cell_diameter, method, initial_params=full_params_contour, options=options, callback_progress=callback_progress)

    #complete_params["segmentation"]["ranking"]["stickingWeight"] = 60.0

    print "Best_params:", complete_params
    print
    print "CellProfiler autoparams:", Segmentation.encode_auto_params_from_all_params(complete_params)

    debug_util.DEBUGING = True
    test_pf.test_parameters(image_path, mask_path, precision, avg_cell_diameter, complete_params, image_result_path, options=options)