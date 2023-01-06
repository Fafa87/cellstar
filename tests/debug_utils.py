# -*- coding: utf-8 -*-
"""
This file contains method for debug tools in unit tests.
Date: 2013-2023
Website: http://cellstar-algorithm.org/
"""

import cellstar.utils.debug_util as debug_util


def turn_on_debug():
    debug_util.DEBUGING = True


def turn_off_debug():
    debug_util.DEBUGING = False
