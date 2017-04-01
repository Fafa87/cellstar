# -*- coding: utf-8 -*-
"""
This file contatins various experimental methods that were developed to improve original CellStar
but how not been yet proved to provide improvement.
Date: 2013-2016
Website: http://cellstar-algorithm.org/
"""

import numpy as np


def smooth_contour_new_max(self, radius, max_diff, points_number, f_tot):
    """
    Smoothing contour using greedy length cut. Rotating from min radius clockwise and anti.
    @type radius: np.ndarray
    @param max_diff: max change of ray length per iter.
    @type max_diff np.ndarray
    @type points_number int
    @param f_tot: quality function array
    @type f_tot: np.ndarray

    @rtype (np.ndarray, np.ndarray)
    @return (smoothed_radius, used_radius_bounds)
    """
    min_angle = radius.argmin()
    istart = min_angle

    xmins2 = np.copy(radius)
    xmaxs = np.copy(radius)

    changed = True

    def cut_rotate(start, step):
        last_ok = False
        iteration = 0
        any_cut = False
        while not (iteration >= points_number and last_ok):
            current = (start + iteration * step) % points_number
            previous = (current - 1 * step) % points_number

            if xmins2[current] - xmins2[previous] > max_diff[xmins2[previous]]:
                xmaxs[current] = xmins2[previous] + max_diff[xmins2[previous]]
                xmin = max(0, xmins2[previous] - max_diff[xmins2[previous]])
                f_tot_slice = f_tot[current, xmin:xmaxs[current] + 1]
                xmins2[current] = f_tot_slice.argmin() + xmin

                last_ok = False
                any_cut = True
            else:
                last_ok = True

            iteration += 1
        return (start + iteration * step) % points_number, any_cut

    current_position = istart
    while changed:
        changed = False

        current_position, any_cut = cut_rotate(current_position, 1)
        changed = changed or any_cut

        current_position, any_cut = cut_rotate(current_position, -1)
        changed = changed or any_cut

    return xmins2, xmaxs


def smooth_contour_turns(self, radius, max_diff, points_number, f_tot):
    """
    Smoothing contour using greedy length cut. Rotating from min radius clockwise and anti.
    @type radius: np.ndarray
    @param max_diff: max change of ray length per iter.
    @type max_diff np.ndarray
    @type points_number int
    @param f_tot: quality function array
    @type f_tot: np.ndarray

    @rtype (np.ndarray, np.ndarray)
    @return (smoothed_radius, used_radius_bounds)
    """
    min_angle = radius.argmin()
    istart = min_angle

    xmins2 = np.copy(radius)
    xmaxs = np.copy(radius)

    changed = True

    def cut_rotate(start, step):
        last_ok = False
        iteration = 0
        any_cut = False
        while not (iteration >= points_number and last_ok):
            current = (start + iteration * step) % points_number
            previous = (current - 1 * step) % points_number
            previous2 = (previous - 1 * step) % points_number

            expected_size = xmins2[previous]
            if iteration > 2:
                expected_size = max(expected_size, xmins2[previous] + xmins2[previous] - xmins2[previous2])

            if xmins2[current] - expected_size > max_diff[xmins2[previous]]:
                xmaxs[current] = expected_size + max_diff[xmins2[previous]]
                xmin = max(0, expected_size - max_diff[xmins2[previous]])
                f_tot_slice = f_tot[current, xmin:xmaxs[current] + 1]
                xmins2[current] = f_tot_slice.argmin() + xmin
                last_ok = False
                any_cut = True
            else:
                last_ok = True

            iteration += 1
        return (start + iteration * step) % points_number, any_cut

    current_position = istart
    while changed:
        changed = False

        current_position, any_cut = cut_rotate(current_position, 1)
        changed = changed or any_cut

        current_position, any_cut = cut_rotate(current_position, -1)
        changed = changed or any_cut

    return xmins2, xmaxs
