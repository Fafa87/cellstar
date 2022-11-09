CellStar
========
.. image:: https://github.com/Fafa87/docs/actions/workflows/run_tests.yml/badge.svg
.. image:: https://img.shields.io/pypi/v/cellstar.svg 
   :target: https://pypi.org/project/CellStar/
.. image:: https://img.shields.io/pypi/pyversions/cellstar
   :target: https://pypi.org/project/CellStar/
.. image:: https://img.shields.io/badge/platform-windows%20%7C%20osx%20%7C%20ubuntu-lightgrey
   :target: https://pypi.org/project/CellStar/


Introduction
------------
Automatic tracking of cells in time-lapse microscopy is required to investigate a multitude of biological questions. To limit manipulations during cell line preparation and phototoxicity during imaging, brightfield imaging is often considered. Since the segmentation and tracking of cells in brightfield images is considered to be a difficult and complex task, a number of software solutions have been already developed.
 
CellStar is one of such algorithms. It is optimized to segment and track images of budding yeast cells growing in monolayer (e.g. images from microfluidic chambers), however the algorithm can be also used to track other round objects (in brightfield as well as fluorescent images).

The important part of that solution is parameter fitting mechanism which allows to train and use CellStar for many different types of imagery.

Please visit our website http://www.cellstar-algorithm.org/ for more details.

Distributions
-------------
There are three ways of using CellStar:

- python package https://github.com/Fafa87/cellstar (pip install cellstar)

- plugin for CellProfiler 2.2 http://cellstar-algorithm.strikingly.com/#download

- matlab version for manual curation http://cellstar-algorithm.strikingly.com/#download

The plugin package includes not only the plugin itself but also examples of its usage to guide users on how to achieve best segmentation on a given type of imagery.

How to use package
------------------

.. code-block:: python

    import cellstar
    input_image = imageio.imread("input_images/sample_brightfield.tif")
    segmentator = cellstar.Segmentation(segmentation_precision=9, avg_cell_diameter=35)
    segmentator.set_frame(input_image)
    segmentation, snakes = segmentator.run_segmentation()

See and run examples/use_cellstar.py as well as tests for more details.

Wide range of example usages
----------------------------
During the testing phase of our plugin it turned out that combining parameter fitting and CellProfiler pipeline flow can result in a very flexible solution. In order to show that and also provide a quick starting point for users the `Official user guide <https://drive.google.com/file/d/0B3to8FwFxuTHNnJZbXRIdTdWTFE/view>`_ was prepared.

It contains the ready to use segmentation solution for a wide range of various imagery which includes:

- complete pipeline description

- method selection discussions

- CellProfiler Analyst usage for advanced filtering

The pipelines listed in the document along with the actual imagery are available as a part of plugin version. Every case can be easily to recreate the results.

.. image:: https://user-images.githubusercontent.com/9865688/62827684-7ca28f80-bbd4-11e9-9ff7-f9ee7591d732.png
