# -*- coding: utf-8 -*-
"""
This file contains CellStar fitting tests.
Date: 2013-2016
Website: http://cellstar-algorithm.org/
"""
import random
import unittest

import numpy as np
import scipy.ndimage as image

from cellstar.parameter_fitting.pf_runner import run_pf, run_rank_pf
import cellstar.parameter_fitting.pf_auto_params as params
from cellstar.parameter_fitting.pf_snake import PFSnake
from cellstar.parameter_fitting.pf_rank_snake import PFRankSnake

import cellstar.parameter_fitting.pf_process as process
import cellstar.parameter_fitting.pf_rank_process as rank_process

from cellstar.segmentation import Segmentation
from tests.input_utils import *


class TestFitting(unittest.TestCase):
    def setUp(self):
        random.seed(44)
        np.random.seed(44)

    def test_contour_fitting(self):
        process.SEARCH_LENGTH_NORMAL = 20

        img = prepare_image((80, 80))
        gt = np.zeros((80,80), dtype=int)
        draw_weak_cell(img, (60, 20), 12)
        draw_disc(gt, (60, 20), 14, 1)
        draw_weak_cell(img, (40, 25), 8)
        draw_disc(gt, (40, 25), 8, 2)
        draw_weak_cell(img, (30, 40), 9)
        draw_disc(gt, (30, 40), 9, 3)
        img = finish_image(img)

        cellstar = Segmentation(11, 20)

        # break parameters
        weights = cellstar.parameters["segmentation"]["stars"]["sizeWeight"]
        encoded = params.pf_parameters_encode(cellstar.parameters)
        one_params = [0.5 for k in encoded]
        one_params[3] = 0.001
        one_decoded = params.pf_parameters_decode(one_params, weights)
        broken_params = PFSnake.merge_parameters(cellstar.parameters, one_decoded)

        cellstar.parameters = broken_params

        cellstar.set_frame(img)
        segmentation, snakes = cellstar.run_segmentation()

        # fail miserably (not all snakes are found)
        self.assertGreater(3, segmentation.max())
        self.assertGreater(3, len(snakes))

        new_params, _ = run_pf(img, None, None, gt, cellstar.parameters, 11, 20)
        cellstar = Segmentation(11, 20)
        cellstar.parameters = new_params
        cellstar.set_frame(img)

        segmentation2, snakes2 = cellstar.run_segmentation()

        self.assertLessEqual(3, segmentation2.max())
        self.assertLessEqual(3, len(snakes2))

        # find best 3 objects
        best3 = get_best_mask(segmentation2, 3)
        segmentation_quality = calculate_diff_fraction(best3, gt)
        self.assertLessEqual(0.65, segmentation_quality)

    def test_rank_fitting(self):
        img = prepare_image((80, 80))
        gt = np.zeros((80, 80), dtype=int)
        draw_weak_cell(img, (60, 20), 12)
        draw_disc(gt, (60, 20), 10, 1)
        draw_weak_cell(img, (40, 25), 8)
        draw_disc(gt, (40, 25), 6, 2)
        draw_weak_cell(img, (30, 40), 9)
        draw_disc(gt, (30, 40), 7, 3)
        img = finish_image(img)

        cellstar = Segmentation(11, 20)

        # break parameters
        encoded = params.pf_rank_parameters_encode(cellstar.parameters)
        one_params = [0.1 for k in encoded]
        one_decoded = params.pf_rank_parameters_decode(one_params)
        broken_params = PFRankSnake.merge_rank_parameters(cellstar.parameters, one_decoded)

        cellstar.parameters = broken_params

        cellstar.set_frame(img)
        segmentation, snakes = cellstar.run_segmentation()

        # fail miserably (best snakes are nowhere close)
        best3 = get_best_mask(segmentation, 3)
        segmentation_quality = calculate_diff_fraction(best3, gt)
        self.assertLessEqual(segmentation_quality, 0.01)
        cells_inside_gt_mask = np.count_nonzero((best3 > 0) & (gt > 0)) / np.count_nonzero((best3 > 0))
        self.assertLessEqual(cells_inside_gt_mask, 0.1)

        new_params, _ = run_rank_pf(img, None, None, gt, cellstar.parameters)
        cellstar = Segmentation(11, 20)
        cellstar.parameters = new_params
        cellstar.set_frame(img)

        segmentation2, snakes2 = cellstar.run_segmentation()

        self.assertLessEqual(3, segmentation2.max())
        self.assertLessEqual(3, len(snakes2))

        # find best 3 objects
        best3 = get_best_mask(segmentation2, 3)
        snake3 = snakes2[:3]
        segmentation_quality = calculate_diff_fraction(best3, gt)
        self.assertLessEqual(0.3, segmentation_quality)  # there was no contour fitting

        object_diffs = calculate_diffs_per_object(best3, gt)
        self.assertLessEqual(0.2, min(object_diffs))

        # check how much resulting snakes are inside ground truth
        cells_inside_gt_mask = np.count_nonzero((best3 > 0) & (gt > 0)) / np.count_nonzero((best3 > 0))
        self.assertLessEqual(0.9, cells_inside_gt_mask)
