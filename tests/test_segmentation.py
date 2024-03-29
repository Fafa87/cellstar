# -*- coding: utf-8 -*-
"""
This file contains complete CellStar segmentation tests.
Date: 2013-2016
Website: http://cellstar-algorithm.org/
"""
import pathlib
import unittest

import imageio

from cellstar.segmentation import Segmentation
import cellstar.utils.debug_util
from tests.input_utils import *


class TestSegmentation(unittest.TestCase):
    def setUp(self):
        self.debug_image_path = cellstar.utils.debug_util.debug_image_path

    def test_no_objects(self):
        img = prepare_image((50, 50))

        segmentor = Segmentation(9, 10)
        segmentor.set_frame(img)
        segmentation, snakes = segmentor.run_segmentation()

        self.assertEqual(0, segmentation.max())
        self.assertEqual(0, len(snakes))

    def test_multiple_objects(self):
        img = prepare_image((50, 50))
        draw_cell(img, (10, 10), 6)
        draw_cell(img, (30, 15), 8)
        img = finish_image(img, gauss=1, noise=0)

        segmentor = Segmentation(9, 10)
        segmentor.set_frame(img)
        segmentation, snakes = segmentor.run_segmentation()

        self.assertEqual(2, segmentation.max())
        self.assertEqual(2, len(snakes))

    def test_mask_usage(self):
        img = prepare_image((80, 80))
        gt = np.zeros((80, 80), dtype=int)

        draw_very_weak_cell(img, (10, 10), 6)
        draw_disc(gt, (10, 10), 6, 1)

        draw_very_weak_cell(img, (30, 15), 8)
        draw_disc(gt, (30, 15), 6, 1)

        # very bright points
        img[50:70, 50:70] = 1
        img[50:70, 10:30] = 0

        segmentor = Segmentation(9, 10)
        segmentor.set_frame(img)
        segmentation, snakes = segmentor.run_segmentation()

        self.assertLess(segmentation.max(), 2)
        self.assertLess(len(snakes), 2)

        ignore_mask = (img == 1) | (img == 0)
        segmentor = Segmentation(9, 10)
        segmentor.set_frame(img)
        segmentor.set_mask(ignore_mask)

        segmentation, snakes = segmentor.run_segmentation()
        self.assertEqual(2, segmentation.max())
        self.assertEqual(2, len(snakes))

    def test_background_usage(self):
        img = prepare_image((80, 80))
        gt = np.zeros((80, 80), dtype=int)
        background = np.ones((80, 80))
        background = background * 0.5

        draw_cell(img, (10, 10), 6)
        draw_disc(gt, (10, 10), 6, 1)

        draw_cell(img, (30, 15), 8)
        draw_disc(gt, (30, 15), 6, 1)

        # background with cell looking noise
        draw_cell(img, (30, 40), 9)
        draw_cell(background, (30, 40), 9)
        img = finish_image(img, gauss=1, noise=0)

        segmentor = Segmentation(9, 14)
        segmentor.set_frame(img)
        segmentation, snakes = segmentor.run_segmentation()

        # background noise is returned as cell
        self.assertEqual(3, segmentation.max())
        self.assertEqual(3, len(snakes))

        segmentor = Segmentation(9, 14)
        segmentor.set_frame(img)
        segmentor.set_background(background)

        segmentation, snakes = segmentor.run_segmentation()
        self.assertEqual(2, segmentation.max())
        self.assertEqual(2, len(snakes))

    def test_large_image(self):
        img = prepare_image((300, 300))
        gt = np.zeros((300, 300), dtype=int)

        draw_cell(img, (40, 40), 30)
        draw_disc(gt, (40, 40), 30, 1)
        draw_cell(img, (150, 90), 25)
        draw_disc(gt, (150, 90), 25, 2)
        draw_cell(img, (180, 70), 20)
        draw_disc(gt, (180, 70), 20, 3)
        img = finish_image(img, gauss=2, noise=0)

        segmentor = Segmentation(11, 60)
        segmentor.set_frame(img)
        segmentation, snakes = segmentor.run_segmentation()

        self.assertEqual(3, segmentation.max())
        self.assertEqual(3, len(snakes))

        object_diffs = calculate_ious_per_object(segmentation, gt)
        self.assertLessEqual(0.75, min(object_diffs))

    def test_sample_image(self):
        input_image = imageio.imread(get_input("sample_brightfield.tif"))
        output_dir = pathlib.Path(prepare_output_dir("sample_brightfield"))
        cellstar.utils.debug_util.debug_image_path = str(output_dir)

        segmentator = Segmentation(segmentation_precision=9, avg_cell_diameter=35)
        segmentator.set_frame(input_image)
        segmentation, snakes = segmentator.run_segmentation()

        imageio.imsave(output_dir / "segmented.tif", (segmentation * 20).astype(np.uint8))

        self.assertGreaterEqual(segmentation.max(), 8)
        self.assertLessEqual(segmentation.max(), 9)

    def tearDown(self):
        cellstar.utils.debug_util.debug_image_path = self.debug_image_path