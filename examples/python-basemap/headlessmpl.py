#!/usr/bin/env python
"""
.. module::headlessmpl
    :platform: GNU/Linux, Windows, Mac
    :synopsis:  A Module for matplotlib figures which only output pixmaps

.. moduleauthor::Lachlan McCalman <lachlan.mccalman@nicta.com.au>

"""
#Built-in Imports
import logging
#3rd-party Imports
import numpy as np
import PIL as pil
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

log = logging.getLogger(__name__)


def figure(width, height, dpi=96, bgcolor='black'):
    """A headless MPL figure for generating pixmaps
    :param width: the width of the resultant image in pixels
    :type width: int
    :param height: the height of the resultant image in pixels
    :type height: int
    :returns: A dictionary with label keys and RGB values
    """
    fig_width = width / float(dpi)
    fig_height = height / float(dpi)
    fig = Figure(figsize=(fig_width, fig_height), dpi=dpi, facecolor=bgcolor)
    fig.subplots_adjust(left=0.0,right=1.0,top=1.0,bottom=0.0,wspace=0.0,hspace=0.0)
    return fig


def figure_to_pixmap(figure):
    """Get a pixmap from a headless MPL figure
    :param figure: a headless (or any other) matplotlib figure object
    :type filename: matplotlib.figure.Figure
    :returns: 3D numpy uint8 array of pixel values (the image)
    """
    canvas = FigureCanvasAgg(figure)
    canvas.draw()
    w, h = canvas.get_width_height()
    pixmap_string = canvas.tostring_argb()
    #line up the channels right
    pix_array = np.fromstring(pixmap_string, dtype=np.uint8)
    pix_array.shape = (w, h, 4)
    # pix_array = pix_array[:, :, ::-1]
    swapped_array = np.zeros(pix_array.shape, dtype=np.uint8)
    swapped_array[:,:,3] = pix_array[:,:,0]
    swapped_array[:,:,0] = pix_array[:,:,1]
    swapped_array[:,:,1] = pix_array[:,:,2]
    swapped_array[:,:,2] = pix_array[:,:,3]
    return swapped_array


def figure_to_file(figure, filename):
    """Write an mpl figure directly to a file"""
    pixel_array = figure_to_pixmap(figure)
    new_shape = (pixel_array.shape[1], pixel_array.shape[0], -1)
    pixel_array = pixel_array.reshape(new_shape)
    image = pil.Image.fromarray(pixel_array)
    image.save(filename)
