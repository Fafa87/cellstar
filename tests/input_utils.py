# -*- coding: utf-8 -*-
"""
This file contains method for input imagery creation for other unit tests..
Date: 2013-2016
Website: http://cellstar-algorithm.org/
"""

import numpy as np


def prepare_image(shape):
    img = np.zeros(shape)
    img.fill(0.5)
    return img


def draw_cell(img, center, radius):
    draw_disc(img, center, radius + 2, .8)
    draw_disc(img, center, radius, .3)


def draw_disc(img, center, radius, value):
    x, y = np.mgrid[0:img.shape[0], 0:img.shape[1]]
    distance = np.sqrt((x - center[0]) * (x - center[0]) + (y - center[1]) * (y - center[1]))
    img[distance <= radius] = value
