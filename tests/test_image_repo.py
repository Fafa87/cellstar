import os.path
import unittest

import imageio
import numpy as np
import numpy.testing as nptest

import cellstar.utils.params_util
import cellstar.core.image_repo
import cellstar.utils.debug_util

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

class TestImageRepo(unittest.TestCase):
    def setUp(self):
        self.debug_image_path = cellstar.utils.debug_util.debug_image_path

    def test_on_example_image(self):
        output_dir = prepare_output_dir("sample_brightfield")
        cellstar.utils.debug_util.debug_image_path = output_dir

        input_image = imageio.imread(get_input("sample_brightfield.tif"))

        parameters = cellstar.utils.params_util.default_parameters(9, 35)
        images = cellstar.core.image_repo.ImageRepo(input_image, parameters)
        cellstar.utils.debug_util.images_repo_save(images)

        expected_darker = imageio.imread(get_expected("sample_brightfield.tif", "darker"))
        nptest.assert_almost_equal(expected_darker, images.darker, decimal=2)
        expected_cell_content_mask = imageio.imread(get_expected("sample_brightfield.tif", "cell_content_mask"))
        expected_cell_content_mask = expected_cell_content_mask > 0
        differences = expected_cell_content_mask != images.cell_content_mask
        assert differences.mean() < 0.0001, differences.mean()

    def tearDown(self):
        cellstar.utils.debug_util.debug_image_path = self.debug_image_path