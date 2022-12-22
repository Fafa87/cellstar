# -*- coding: utf-8 -*-
"""
This file contains method for input imagery creation for other unit tests..
Date: 2013-2016
Website: http://cellstar-algorithm.org/
"""
import os

import numpy as np
import scipy.ndimage as image

import cellstar.utils.debug_util as debug_util


def turn_on_debug():
    debug_util.DEBUGING = True


def turn_off_debug():
    debug_util.DEBUGING = False


TESTS = os.path.dirname(__file__)


def get_input(sample_file):
    return os.path.join(TESTS, "data", sample_file)


def get_expected(sample_file, name):
    sample_name = os.path.splitext(sample_file)[0]
    return os.path.join(TESTS, "expected", sample_name, name + ".tif")


def prepare_output_dir(sample_file):
    sample_name = os.path.splitext(sample_file)[0]
    output_dir = os.path.join(TESTS, "output", sample_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def prepare_image(shape):
    img = np.zeros(shape)
    img.fill(0.5)
    return img


def finish_image(img, gauss=3, noise=0.01):
    img = image.gaussian_filter(img, gauss)
    img = img + np.random.normal(0, noise, img.shape)
    return img


def draw_cell(img, center, radius):
    draw_disc(img, center, radius + 2, .8)
    draw_disc(img, center, radius + 1, .6)
    draw_disc(img, center, radius, .3)


def draw_weak_cell(img, center, radius):
    draw_disc(img, center, radius + 2, .8)
    draw_disc(img, center, radius, .45)


def draw_very_weak_cell(img, center, radius):
    draw_disc(img, center, radius + 2, .55)
    draw_disc(img, center, radius, .45)


def draw_disc(img, center, radius, value):
    x, y = np.mgrid[0:img.shape[0], 0:img.shape[1]]
    distance = np.sqrt((x - center[0]) * (x - center[0]) + (y - center[1]) * (y - center[1]))
    img[distance <= radius] = value


def get_best_mask(seg, num):
    """
    @type seg: np.ndarray
    """
    res = seg.copy()
    res[seg > num] = 0
    return res


def calculate_diff_fraction(seg, gt):
    """
    @type seg: np.ndarray
    @type gt: np.ndarray
    """
    return (float(np.count_nonzero(seg & gt))) / np.count_nonzero(seg | gt)


def calculate_diffs_per_object(seg, gt):
    """
    @type seg: np.ndarray
    @type gt: np.ndarray
    """
    ids = range(1, max(seg.max(), gt.max()) + 1)
    seg_masks = [seg == i for i in ids]
    gt_masks = [gt == i for i in ids]

    res = []
    for s in seg_masks:
        if len(gt_masks) > 0:
            diffs = [calculate_diff_fraction(s, g) for g in gt_masks]
            best_id = np.argmax(diffs)
            if diffs[best_id] == 0:
                res.append(0)
                continue
            res.append(diffs[best_id])
            gt_masks.pop(best_id)
        else:
            res.append(0)
    return res
