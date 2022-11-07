import os.path
import unittest

import imageio
import numpy as np
import numpy.testing as nptest

import cellstar.utils.params_util
import cellstar.core.image_repo

TESTS = os.path.dirname(__file__)


def get_input(sample_file):
    return os.path.join(TESTS, "data", sample_file)


def get_expected(sample_file, name):
    sample_name = os.path.splitext(sample_file)[0]
    return os.path.join(TESTS, "expected", sample_name, name + ".tif")


class TestImageRepo(unittest.TestCase):
    def test_on_example_image(self):
        input_image = imageio.imread(get_input("sample_brightfield.tif"))

        parameters = cellstar.utils.params_util.default_parameters(9, 35)
        images = cellstar.core.image_repo.ImageRepo(input_image, parameters)

        expected_darker = imageio.imread(get_expected("sample_brightfield.tif", "darker"))
        nptest.assert_almost_equal(expected_darker, images.darker, decimal=2)
        expected_cell_content_mask = imageio.imread(get_expected("sample_brightfield.tif", "cell_content_mask"))
        expected_cell_content_mask = expected_cell_content_mask > 0
        differences = expected_cell_content_mask != images.cell_content_mask
        assert differences.mean() < 0.0001
