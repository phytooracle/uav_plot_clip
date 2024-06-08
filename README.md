# UAV Plot Clip

This repository clips plots from drone imagery.

## Inputs
The scripts takes in a GeoJSON and TIF image/s to clip. Please ensure that both are in the same coordinate reference system.

## Outputs
The script will output a subdirectory for each plot polygon in the GeoJSON. Within each subdirectory, an image containing only the polygon area is saved.

## Arguments and Flags

* **Positional Arguments:** 
    * **Path/s to a TIF image:** 'tif'
    
* **Required Arguments:**
    * **GeoJSON:** '-g', '--geojson'
    * **Central processing unit (CPU):** '-c', '--cpu'
