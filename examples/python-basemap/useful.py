import numpy as np
from mpl_toolkits.basemap import Basemap

def remove_figure_borders(figure):
    figure.patch.set_alpha(0)
    axes = figure.gca()
    axes.set_frame_on(False)
    axes.set_xticks([])
    axes.set_yticks([])
    axes.axis('off')

def basemap_data(axes, draw_map=False, draw_bg=False, draw_coastlines=False,
        draw_states=False):
    """Add coastlines, satellite background etc"""
    min_point = np.array([axes.get_xlim()[0], axes.get_ylim()[0]])
    max_point = np.array([axes.get_xlim()[1], axes.get_ylim()[1]])
    globe = Basemap(projection='cyl', llcrnrlon=min_point[0],
            llcrnrlat=min_point[1], urcrnrlon=max_point[0],
            urcrnrlat=max_point[1], resolution='i', area_thresh=1000,
            ax=axes, suppress_ticks=False, fix_aspect=False)
    if draw_map:
        globe.drawmapboundary()
    if draw_bg:
        globe.bluemarble()
    if draw_coastlines:
        globe.drawcoastlines()
    if draw_states:
        globe.drawstates()
        globe.drawcountries()
    return axes

def histogram_cutoffs(data, alpha_data,
        low_cutoff=0.001, high_cutoff=0.999):
    """Finds correct exposure based on the intensity histogram"""
    input_data = data.flatten()
    input_weights = alpha_data.flatten()
    input_data = np.extract(input_weights == 1.0, input_data)
    hist, bin_edges = np.histogram(input_data, bins=256, density=True)
    cumulative_hist = np.cumsum(hist / np.sum(hist))
    low_index = np.argmax(cumulative_hist >= low_cutoff)
    high_index = np.argmax(cumulative_hist >= high_cutoff)
    low_value = bin_edges[low_index]
    high_value = bin_edges[high_index]
    return low_value, high_value


def set_matplotlib_colors(axes, background='black', foreground='white'):
    """Set the colors of the matplotlib axes, background and labels
    """
    axes.patch.set_facecolor(background)
    legend = axes.get_legend()
    if legend:
        legend.legendPatch.set_facecolor(background)
        legend.get_title().set_color(foreground)
        legend.legendPatch.set_edgecolor('none')
        labels = legend.get_texts()
        for lab in labels:
            lab.set_color(foreground)
    for t in axes.get_xticklines():
        t.set_color(foreground)
    for t in axes.get_yticklines():
        t.set_color(foreground)
    for s in axes.spines:
        axes.spines[s].set_edgecolor(foreground)
    for t in axes.xaxis.get_major_ticks():
        t.label1.set_color(foreground)
    for t in axes.yaxis.get_major_ticks():
        t.label1.set_color(foreground)
    axes.axes.xaxis.label.set_color(foreground)
    axes.axes.yaxis.label.set_color(foreground)
    axes.axes.xaxis.get_offset_text().set_color(foreground)
    axes.axes.yaxis.get_offset_text().set_color(foreground)
    axes.axes.title.set_color(foreground)
    for t in axes.get_xticklabels():
        t.set_color(foreground)
    for t in axes.get_yticklabels():
        t.set_color(foreground)
