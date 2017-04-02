# -*- coding: utf-8 -*-
"""
This file contains complete CellStar segmentation tests.
Date: 2013-2016
Website: http://cellstar-algorithm.org/
"""

import unittest

from cellstar.segmentation import Segmentation
from input_utils import *


class TestSegmentation(unittest.TestCase):
    def test_no_objects(self):
        img = prepare_image((50, 50))

        cellstar = Segmentation(9, 10)
        cellstar.set_frame(img)
        segmentation, snakes = cellstar.run_segmentation()

        self.assertEqual(0, segmentation.max())
        self.assertEqual(0, len(snakes))

    def test_multiple_objects(self):
        img = prepare_image((50, 50))
        draw_cell(img, (10, 10), 6)
        draw_cell(img, (30, 15), 8)

        cellstar = Segmentation(9, 10)
        cellstar.set_frame(img)
        segmentation, snakes = cellstar.run_segmentation()

        self.assertEqual(2, segmentation.max())
        self.assertEqual(2, len(snakes))
