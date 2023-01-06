import unittest

import numpy as np

from tests.input_utils import calculate_ious_per_object


class TestInputUtils(unittest.TestCase):
    def test_calculate_ious_per_object(self):
        seg = np.zeros((60, 30), dtype=np.uint8)
        gt = np.zeros((60, 30), dtype=np.uint8)

        gt[1, 1] = 1
        gt[1:4, 3:5] = 2
        gt[5, 2] = 4
        gt[4:6, 4] = 5

        seg[2, 1] = 1
        seg[4:6, 1:5] = 4
        seg[1:3, 3:5] = 3
        seg[3, 3:5] = 2

        res = calculate_ious_per_object(seg, gt)
        self.assertListEqual(res, [0, 1.0/3, 2.0/3, 1.0/4, 0])

        res = calculate_ious_per_object(gt, seg)
        self.assertListEqual(res, [0, 2.0/3, 0, 1.0/8, 1.0/4])
