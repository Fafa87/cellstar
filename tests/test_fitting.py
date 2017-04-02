# -*- coding: utf-8 -*-
"""
This file contains CellStar fitting tests.
Date: 2013-2016
Website: http://cellstar-algorithm.org/
"""

import unittest

import numpy as np

from cellstar.segmentation import Segmentation
from cellstar.parameter_fitting.pf_runner import run_pf, run_rank_pf
from input_utils import *


class TestFitting(unittest.TestCase):
    def test_contour_fitting(self):
        self.fail("TODO")
        img = self.prepare_image((50,50))
        self.draw_cell(img, (10, 10), 6)
        self.draw_cell(img, (30, 15), 8)

        cellstar = Segmentation(9, 10)
        cellstar.set_frame(img)
        segmentation, snakes = cellstar.run_segmentation()

        self.assertEqual(2, segmentation.max())
        self.assertEqual(2, len(snakes))

    def test_rank_fitting(self):
        self.fail("TODO")
        img = self.prepare_image((50,50))
        self.draw_cell(img, (10, 10), 6)
        self.draw_cell(img, (30, 15), 8)

        cellstar = Segmentation(9, 10)
        cellstar.set_frame(img)
        segmentation, snakes = cellstar.run_segmentation()

        self.assertEqual(2, segmentation.max())
        self.assertEqual(2, len(snakes))
