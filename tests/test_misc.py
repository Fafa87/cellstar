import math
import unittest

import matplotlib
import numpy as np
from matplotlib.path import Path

print (matplotlib.__version__)

from cellprofiler.cpmath.cpmorphology import polygon_lines_to_mask

from PIL import Image, ImageDraw

class MyTestCase(unittest.TestCase):
    def generate_circle(self):
        angles = np.linspace(0, 2 * math.pi, 90)
        px = 110 + 100 * np.cos(angles)
        py = 70 + 50 * np.sin(angles)
        return py, px, (20,121), (10,211)

    def generate_mini_circle(self):
        angles = np.linspace(0, 2 * math.pi, 90)
        px = 11 + 10 * np.cos(angles)
        py = 7 + 5 * np.sin(angles)
        return py, px, (2,13), (1,22)

    def get_polygon_path(self, polygon_x, polygon_y):
        vertices = zip(polygon_x, polygon_y)
        p = Path(vertices, None, closed=True, readonly=True)
        return p

    def get_in_polygon(self, x1, x2, y1, y2, path):
        x, y = np.meshgrid(np.arange(x1, x2), np.arange(y1, y2))
        x, y = x.flatten(), y.flatten()
        pts = np.vstack((x, y)).T

        # Find points that belong to snake in minimal rectangle
        grid = path.contains_points(pts)
        return grid

    def mask_by_matplotlib(self, ys, xs, yslice, xslice):
        xs = np.round(xs)
        ys = np.round(ys)

        poly = self.get_polygon_path(xs, ys)
        grid = self.get_in_polygon(xslice[0], xslice[1], yslice[0], yslice[1], poly)
        grid = grid.reshape(yslice[1] - yslice[0], xslice[1] - xslice[0])
        return grid

    def mask_by_pil(self, ys, xs, yslice, xslice):
        xs = np.round(xs)
        ys = np.round(ys)

        rxs = xs - xslice[0]
        rys = ys - yslice[0]

        lx = xslice[1] - xslice[0]
        ly = yslice[1] - yslice[0]
        img = Image.new('L', (lx, ly), 0)
        ImageDraw.Draw(img).polygon(zip(rxs, rys), outline=1, fill=1)
        return np.array(img) != 0

    def mask_by_pil_noImageDraw(self, ys, xs, yslice, xslice):
        rxs = xs - xslice[0]
        rys = ys - yslice[0]

        lx = xslice[1] - xslice[0]
        ly = yslice[1] - yslice[0]
        rxys = zip(rxs, rys)

        img = Image.new('L', (lx, ly), 0)
        draw = Image.core.draw(img.im, 0)
        ink = draw.draw_ink(1, "white")
        draw.draw_polygon(rxys, ink, 1)
        draw.draw_polygon(rxys, ink, 0)
        return np.array(img) != 0

    def mask_by_cpmorph(self, ys, xs, yslice, xslice):
        rxs = xs - xslice[0]
        rys = ys - yslice[0]

        lx = xslice[1] - xslice[0]
        ly = yslice[1] - yslice[0]

        px1 = rxs
        px2 = np.append(rxs[1:], rxs[0])
        py1 = rys
        py2 = np.append(rys[1:], rys[0])

        return polygon_lines_to_mask(py1, px1, py2, px2, (ly, lx))

    def test_matplotlib(self):
        py, px, sy, sx = self.generate_circle()
        for k in range(50):
            self.mask_by_matplotlib(py, px, sy, sx)

        self.assertEqual(True, True)

    def test_pil(self):
        py, px, sy, sx = self.generate_circle()
        for k in range(50):
            self.mask_by_pil(py, px, sy, sx)

        self.assertEqual(True, True)

    def test_pil_noImageDraw(self):
        py, px, sy, sx = self.generate_circle()
        for k in range(50):
            self.mask_by_pil_noImageDraw(py, px, sy, sx)

        self.assertEqual(True, True)

    def test_cp(self):
        py, px, sy, sx = self.generate_circle()
        for k in range(50):
            self.mask_by_cpmorph(py, px, sy, sx)

        self.assertEqual(True, True)

    def test_compare(self):
        py, px, sy, sx = self.generate_mini_circle()

        mask_org = self.mask_by_matplotlib(py, px, sy, sx)

        mask_pil = self.mask_by_pil(py, px, sy, sx)

        mask_cp = self.mask_by_cpmorph(py, px, sy, sx)

        self.assertTrue((mask_org == mask_cp).all())
        self.assertTrue((mask_org == mask_pil).all())

    def time_it(self, func, image, size):
        import time
        start = time.clock()
        res = func(image, size)
        elapsed = time.clock() - start
        print func, size, "elapsed:", elapsed
        return res

    def test_image_blur(self):
        import cell_star.utils.image_util as image_util
        import cell_star.utils.debug_util as debug_util

        def image_smooth_old(a,b):
            return image_util.image_smooth(a,b,False)

        debug_util.debug_image_path = r"D:\Fafa\Drozdze\CellProfilerOutput"
        debug_util.DEBUGING = True
        image = image_util.load_image(r"D:\Fafa\Drozdze\CellProfilerOutput\TS10_A_4M_fulk_flatten_light_megafit_rand2B\Point0000_Seq00000000.tif\brighter.tif")
        #image = image_util.load_image(r"D:\Fafa\Drozdze\CellStarTesting\Data\Speeder\frames\Horde_1_1K_frame.tif")

        # think about image_smooth too! there fft should work much better!
        smooth1 = self.time_it(image_smooth_old,image, 1)
        smooth7 = self.time_it(image_smooth_old,image, 8)
        smooth20 = self.time_it(image_smooth_old,image, 20)
        #smooth40 = self.time_it(image_smooth_old,image, 40)
        #smooth60 = self.time_it(image_smooth_old,image, 60)

        debug_util.image_save(smooth20, "smooth20")
        #debug_util.image_save(smooth40, "smooth40")
        #debug_util.image_save(smooth60, "smooth60")

        smooth1 = self.time_it(image_util.image_smooth,image, 1)
        smooth7 = self.time_it(image_util.image_smooth,image, 8)
        smooth20 = self.time_it(image_util.image_smooth,image, 20)
        smooth40 = self.time_it(image_util.image_smooth,image, 40)
        smooth60 = self.time_it(image_util.image_smooth,image, 60)

        debug_util.image_save(smooth20, "smooth20fft")
        debug_util.image_save(smooth40, "smooth40fft")
        debug_util.image_save(smooth60, "smooth60fft")

        #blur32 = self.time_it(image_util.image_blur,image, 32)
        #blur64 = self.time_it(image_util.image_blur,image, 64)
        #blur128 = self.time_it(image_util.image_blur,image, 128)

        #debug_util.image_save(blur32, "blur32")
        #debug_util.image_save(blur64, "blur64")
        #debug_util.image_save(blur128, "blur128")

        #blur1 = self.time_it(image_util.image_blur_old,image, 1)
        #blur7 = self.time_it(image_util.image_blur_old,image, 8)
        #blur32 = self.time_it(image_util.image_blur_old,image, 32)
        #blur64 = self.time_it(image_util.image_blur_old,image, 64)
        #blur128 = self.time_it(image_util.image_blur_old,image, 128)

        #debug_util.image_save(blur32, "blur32b")
        #debug_util.image_save(blur64, "blur64b")
        #debug_util.image_save(blur128, "blur128b")

        blur1 = self.time_it(image_util.image_blur,image, 1)
        blur7 = self.time_it(image_util.image_blur,image, 8)
        blur32 = self.time_it(image_util.image_blur,image, 32)
        blur64 = self.time_it(image_util.image_blur,image, 64)
        blur128 = self.time_it(image_util.image_blur,image, 128)

        debug_util.image_save(blur32, "blur32fft")
        debug_util.image_save(blur64, "blur64fft")
        debug_util.image_save(blur128, "blur128fft")

        # TODO write test that created blurred brighter / darker and see if it


def start_manual_identify():
    from cellprofiler.gui.editobjectsdlg import EditObjectsDialog
    from wx import OK
    import wx

    app = wx.App(0)

    input_image = np.zeros((400,400), float)
    input_image[100:150,100:150] = 0.5
    input_image[40:50,170:179] = 0.7

    edit_labels = [np.zeros((400,400), int)]

    ## two next lines are hack from Lee
    edit_labels[0][0, 0] = 1
    edit_labels[0][-2, -2] = 1
    with EditObjectsDialog(
            input_image, edit_labels, False, "Maluj") as dialog_box:
        # hack into editobjects dlg
        import cellprofiler.modules.yeast_cell_segmentation as YS
        YS.hack_add_from_file_into_EditObjects(dialog_box)
        result = dialog_box.ShowModal()
        if result != OK:
            return None
        labels = dialog_box.labels[0]
    ## two next lines are hack from Lee
    labels[0, 0] = 0
    labels[-2, -2] = 0



if __name__ == '__main__':
    start_manual_identify()
    #unittest.main()
