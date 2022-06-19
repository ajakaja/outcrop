#!/usr/bin/env python3

from wand.image import Image
import sys
import math
import os
import argparse

parser = argparse.ArgumentParser(description='Add padding around photos in a given aspect ratio for happier printing')
parser.add_argument('filename', help='file to be processed')
parser.add_argument('aspect ratio', help="desired aspect ratio, formatted like '8x10'")
parser.add_argument('-c', '--color', default='white', help='padding color which will be added around the edges')
parser.add_argument('-p', '--padding', default=None, help='extra padding (in px) which will be added on all sides', type=int)
args = parser.parse_args()

filename = args.filename
filename_base = os.path.splitext(filename)[0]
aspect_ratio = vars(args)["aspect ratio"]
color = args.color
padding = args.padding or 0

ratio_parts = aspect_ratio.split('x')
assert len(ratio_parts) == 2
ratio1 = float(ratio_parts[0])
ratio2 = float(ratio_parts[1])
if ratio1 > ratio2:
    ratio = ratio1 / ratio2
else:
    ratio = ratio2 / ratio1

if padding > 0:
    print(f'Resizing {filename} to aspect ratio {ratio1}:{ratio2} with {color} background and {padding}px padding')
else:
    print(f'Resizing {filename} to aspect ratio {ratio1}:{ratio2} with {color} background')

with Image(filename=filename) as img:

    old_width, old_height = img.size
    width = old_width + 2 * padding
    height = old_height + 2 * padding

    # get best dimensions to fit in this aspect ratio
    new_width = width
    new_height = height
    x_offset = padding
    y_offset = padding

    if width > height:
        # width will be the larger side
        if width < height * ratio:
            new_width = math.floor(height * ratio)
            x_offset += math.floor((new_width - width) / 2)
        else:
            new_height = math.floor(width/ratio)
            y_offset += math.floor((new_height - height) / 2)
    else:
        # height will be the larger side
        if height < width * ratio:
            new_height = math.floor(width * ratio)
            y_offset += math.floor((new_height - height) / 2)
        else:
            new_width = math.floor(height/ratio)
            x_offset += math.floor((new_width - width) / 2)


    print(f'Resizing from {old_width, old_height} to {new_width, new_height}')
    print(f'Positioning image with offset of {x_offset, y_offset}')

    canvas = Image(width=new_width, height=new_height, pseudo=f'canvas:{color}')

    canvas.composite(img, left=x_offset, top=y_offset)
    if padding > 0:
        canvas.save(filename=f'{filename_base}-{aspect_ratio}+{padding}.png')
    else:
        canvas.save(filename=f'{filename_base}-{aspect_ratio}.png')


