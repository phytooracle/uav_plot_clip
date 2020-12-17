#!/usr/bin/env python3
"""
Author : Emmanuel Gonzalez
Date   : 2020-12-17
Purpose: UAV plotclip
"""

import argparse
import os
import sys
import numpy as np
import rasterio
import rasterio.mask
import matplotlib.pyplot as plt
import geopandas as gpd
import multiprocessing


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('tif',
                        nargs='+',
                        metavar='str',
                        help='A positional argument')

    parser.add_argument('-g',
                        '--geojson',
                        help='GeoJSON of plot boundaries',
                        metavar='str',
                        type=str,
                        required=True)

    parser.add_argument('-c',
                        '--cpu',
                        help='CPUs for multiprocessing',
                        metavar='cpu',
                        type=int,
                        required=True)

    return parser.parse_args()


# --------------------------------------------------
def open_geojson(geojson_path):

    shp = gpd.read_file(geojson_path)

    geom_dict = {}
    cnt = 0

    for i, row in shp.iterrows():
        cnt += 1
        geom = row['geometry']
        plot_num = row['ID']

        geom_dict[cnt] = {
            'geometry': geom,
            'plot': plot_num
        }

    return geom_dict


# --------------------------------------------------
def process_image(image):

    args = get_args()

    f_name = os.path.splitext(os.path.basename(image))[-2]

    geom_dict = open_geojson(args.geojson)

    src = rasterio.open(image)
    array = src.read(1)

    for k, v in geom_dict.items():

        geom = v['geometry']
        plot = v['plot']

        out_dir = os.path.join(f_name, str(int(plot)))

        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)

        out_image, out_transform = rasterio.mask.mask(src, geom, crop=True, nodata=np.nan)
        out_meta = src.meta

        out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})


        with rasterio.open(f'{out_dir}/{plot}_plotclip.tif', "w", **out_meta) as dest:
            dest.write(out_image)


# --------------------------------------------------
def main():
    """Process images here"""

    args = get_args()
    with multiprocessing.Pool(args.cpu) as p:
        p.map(process_image, args.tif)

# --------------------------------------------------
if __name__ == '__main__':
    main()
