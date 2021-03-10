#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
##                    Code to create grid for garden simulation               ##
################################################################################
# Copyright (c) 2020 Adam Galindo                                             ##
#                                                                             ##
# Permission is hereby granted, free of charge, to any person obtaining a copy##
# of this software and associated documentation files (the "Software"),to deal##
# in the Software without restriction, including without limitation the rights##
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell   ##
# copies of the Software, and to permit persons to whom the Software is       ##
# furnished to do so, subject to the following conditions:                    ##
#                                                                             ##
# Licenced under GPLv3                                                        ##
# https://www.gnu.org/licenses/gpl-3.0.en.html                                ##
#                                                                             ##
# The above copyright notice and this permission notice shall be included in  ##
# all copies or substantial portions of the Software.                         ##
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################

import sys
from tkinter import *
from tkinter import filedialog


# Maximum and default grid size
MAX_N, DEFAULT_N = 26, 10
# The "default" colour for an unfilled grid cell
UNFILLED = '#fff'

# The colour palette
colours = (UNFILLED, 'red', 'green', 'blue', 'cyan', 'orange', 'yellow',
               'magenta', 'brown', 'black')
ncolours = len(colours)

from plants import *

#plants_list = IntercroppingRelationships()
#for each in plants_list.plant_info:



# TKinter code based on https://github.com/scipython/colouring-grid
# A simple colouring grid app, with load/save functionality.
# Christian Hill, August 2018.

class CreateGardenGrid():
    def __new__(cls, *args):
        pass

    def __init__(self , cls , grid_size_n : int, filename : str):
        # SIZE is the grid image size, including padding around all sides of PAD.
        self.SIZE = 1280
        self.PAD = 1024
        # output SVG image filename, size of the grid within the image.
        self.filename = 'blank_grid-{n}x{n}.svg'.format(n=n)
        self.c_size = (self.SIZE - 2*self.PAD) / n

    def svg_preamble(self, height, width):
        line1 = '<?xml version="1.0" encoding="utf-8"?>\n'
        line2 = '<svg xmlns="http://www.w3.org/2000/svg"\n      '
        line3 = 'xmlns:xlink="http://www.w3.org/1999/xlink" width="{}" height="{}" >'.format(height, width)
        block1 = """<defs>
<style type="text/css"><![CDATA[
line {
        stroke-width: 1px;
        stroke: #888;
     }
    ]]></style>
</defs>
"""         
        data_required = ''' {}{}{}{}'''.format(line1,line2,line3,block1)
        return data_required

    def get_letter_coord(self, i):
        """Return the letter A, B, C, ... corresponding to i = 1, 2, 3, ..."""
        return chr(i+64)

    def createimagefile(self, filename, stuff):
        new_image_file = open(filename, 'w')
        new_image_file.write(self.svg_preamble(stuff))
        # We need n+1 lines to mark out n cells and two nested loops; write both
        # coordinate labels in the outer loop.
            v = self.PAD // 2
            for i in range(n+1):
                if i:
                    u = self.PAD + self.c_size*(i-0.5)
                    print('<text x="{}" y="{}" text-anchor="middle" '
                        'dominant-baseline="central">{}</text>'.format(u, SIZE-v,
                        self.get_letter_coord(i)), file=fo)
                    print('<text x="{}" y="{}" text-anchor="middle" '
                        'dominant-baseline="central">{}</text>'.format(v, SIZE-u,
                        str(i)), file=fo)
                for j in range(n+1):
                    x1 = x2 = self.PAD + i*self.c_size
                    y1, y2 = self.PAD, self.SIZE-self.PAD
                    print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(
                        x1, y1, x2, y2), file=fo)
                    print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(
                        y1, x1, y2, x2), file=fo)
            print('</svg>', file=fo)

def get_goodneighbors(plant_name:str):
    intercrop_list = IntercroppingRelationships()
    for plant in intercrop_list.plant_info:
        if plant.key == plant_name:
            pass


class GridApp:
    """The main class representing a grid of coloured cells."""
    def __init__(self, master, n, width=600, height=600, pad=5):
        """Initialize a grid and the Tk Frame on which it is rendered."""
        # Number of cells in each dimension.
        self.n = n
        self.width, self.height = width, height
        palette_height = 40
        # Padding stuff: xsize, ysize is the cell size in pixels (without pad).
        npad = n + 1
        self.pad = pad
        xsize = (width - npad*pad) / n
        ysize = (height - npad*pad) / n
        # Canvas dimensions for the cell grid and the palette.
        c_width, c_height = width, height
        p_pad = 5
        p_width = p_height = palette_height - 2*p_pad

        # The main frame onto which we draw the App's elements.
        frame = Frame(master)
        frame.pack()

        # The palette for selecting colours.
        self.palette_canvas = Canvas(master, width=c_width,
                                     height=palette_height)
        self.palette_canvas.pack()

        # Add the colour selection rectangles to the palette canvas.
        self.palette_rects = []
        for i in range(self.ncolours):
            x, y = p_pad * (i+1) + i*p_width, p_pad
            rect = self.palette_canvas.create_rectangle(x, y,
                            x+p_width, y+p_height, fill=self.colours[i])
            self.palette_rects.append(rect)
        # ics is the index of the currently selected colour.
        self.ics = 0
        self.select_colour(self.ics)

        # The canvas onto which the grid is drawn.
        self.w = Canvas(master, width=c_width, height=c_height)
        self.w.pack()

        # Add the cell rectangles to the grid canvas.
        self.cells = []
        for iy in range(n):
            for ix in range(n):
                xpad, ypad = pad * (ix+1), pad * (iy+1) 
                x, y = xpad + ix*xsize, ypad + iy*ysize
                rect = self.w.create_rectangle(x, y, x+xsize,
                                           y+ysize, fill=UNFILLED)
                self.cells.append(rect)

        # Load and save image buttons
        b_load = Button(frame, text='open', command=self.load_image)
        b_load.pack(side=RIGHT, padx=pad, pady=pad)
        b_save = Button(frame, text='save', command=self.save_by_colour)
        b_save.pack(side=RIGHT, padx=pad, pady=pad)
        # Add a button to clear the grid
        b_clear = Button(frame, text='clear', command=self.clear_grid)
        b_clear.pack(side=LEFT, padx=pad, pady=pad)

        def palette_click_callback(event):
            """Function called when someone clicks on the palette canvas."""
            x, y = event.x, event.y

            # Did the user click a colour from the palette?
            if p_pad < y < p_height + p_pad:
                # Index of the selected palette rectangle (plus padding)
                ic = x // (p_width + p_pad)
                # x-position with respect to the palette rectangle left edge
                xp = x - ic*(p_width + p_pad) - p_pad
                # Is the index valid and the click within the rectangle?
                if ic < self.ncolours and 0 < xp < p_width:
                    self.select_colour(ic)
        # Bind the palette click callback function to the left mouse button
        # press event on the palette canvas.
        self.palette_canvas.bind('<ButtonPress-1>', palette_click_callback)

        def w_click_callback(event):
            """Function called when someone clicks on the grid canvas."""
            x, y = event.x, event.y

            # Did the user click a cell in the grid?
            # Indexes into the grid of cells (including padding)
            ix = int(x // (xsize + pad))
            iy = int(y // (ysize + pad))
            xc = x - ix*(xsize + pad) - pad
            yc = y - iy*(ysize + pad) - pad
            if ix < n and iy < n and 0 < xc < xsize and 0 < yc < ysize:
                i = iy*n+ix
                self.w.itemconfig(self.cells[i], fill=self.colours[self.ics])
        # Bind the grid click callback function to the left mouse button
        # press event on the grid canvas.
        self.w.bind('<ButtonPress-1>', w_click_callback)

    def select_colour(self, i):
        """Select the colour indexed at i in the colours list."""

        self.palette_canvas.itemconfig(self.palette_rects[self.ics],
                                       outline='black', width=1)
        self.ics = i
        self.palette_canvas.itemconfig(self.palette_rects[self.ics],
                                       outline='black', width=5)

    def _get_cell_coords(self, i):
        """Get the <letter><number> coordinates of the cell indexed at i."""

        # The horizontal axis is labelled A, B, C, ... left-to-right;
        # the vertical axis is labelled 1, 2, 3, ... bottom-to-top.
        iy, ix = divmod(i, self.n)
        return '{}{}'.format(chr(ix+65), self.n-iy)

    def save_by_colour(self):
        """Output a list of cell coordinates, sorted by cell colour."""

        # When we save the list of coordinates with each colour it looks
        # better if we limit the number of coordinates on each line of output.
        MAX_COORDS_PER_ROW = 12

        def _get_coloured_cells_dict():
            """Return a dictionary of cell coordinates and their colours."""

            coloured_cell_cmds = {}
            for i, rect in enumerate(self.cells):
                c = self.w.itemcget(rect, 'fill')
                if c == UNFILLED:
                    continue
                coloured_cell_cmds[self._get_cell_coords(i)] = c
            return coloured_cell_cmds

        def _output_coords(coords):
            """Sort the coords into column (by letter) and row (by int)."""

            coords.sort(key=lambda e: (e[0], int(e[1:])))
            nrows = len(coords) // MAX_COORDS_PER_ROW + 1
            for i in range(nrows):
                print(', '.join(
                      coords[i*MAX_COORDS_PER_ROW:(i+1)*MAX_COORDS_PER_ROW]),
                      file=fo)

        # Create a dictionary of colours (the keys) and a list of cell
        # coordinates with that colour (the value).
        coloured_cell_cmds = _get_coloured_cells_dict()
        cell_colours = {}
        for k, v in coloured_cell_cmds.items():
            cell_colours.setdefault(v, []).append(k)

        # Get a filename from the user and open a file with that name.
        with filedialog.asksaveasfile(mode='w',defaultextension=".grid") as fo:
            if not fo:
                return

            self.filename = fo.name
            print('Writing file to', fo.name)
            for colour, coords in cell_colours.items():
                print('{}\n{}'.format(colour,'-'*len(colour)), file=fo)
                _output_coords(coords)
                print('\n', file=fo)

    def clear_grid(self):
        """Reset the grid to the background "UNFILLED" colour."""

        for cell in self.cells:
            self.w.itemconfig(cell, fill=UNFILLED)
        
    def load_image(self):
        """Load an image from a provided file."""

        def _coords_to_index(coords):
            """
            Translate from the provided coordinate (e.g. 'A1') to an index
            into the grid cells list.
            """

            ix = ord(coords[0])-65
            iy = self.n - int(coords[1:])
            return iy*self.n + ix

        self.filename = filedialog.askopenfilename(filetypes=(
                ('Grid files', '.grid'),
                ('Text files', '.txt'),
                ('All files', '*.*')))
        if not self.filename:
            return
        print('Loading file from', self.filename)
        self.clear_grid()
        # Open the file and read the image, setting the cell colours as we go.
        with open(self.filename) as fi:
            for line in fi.readlines():
                line = line.strip()
                if line in self.colours:
                    this_colour = line
                    continue
                if not line or line.startswith('-'):
                    continue
                coords = line.split(',')
                if not coords:
                    continue
                for coord in coords:
                    i = _coords_to_index(coord.strip())
                    self.w.itemconfig(self.cells[i], fill=this_colour)

# Get the grid size from the command line, if provided
try:
    n = int(sys.argv[1])
except IndexError:
    n = DEFAULT_N
except ValueError:
    print('Usage: {} <n>\nwhere n is the grid size.'.format(sys.argv[0]))
    sys.exit(1)
if n < 1 or n > MAX_N:
    print('Minimum n is 1, Maximum n is {}'.format(MAX_N))
    sys.exit(1)

# Set the whole thing running
root = Tk()
grid = GridApp(root, n, 600, 600, 5)
root.mainloop()
