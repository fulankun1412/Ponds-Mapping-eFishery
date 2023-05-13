from PIL import Image
import math, shutil, requests, os
import pandas as pd
import os
import cv2, numpy as np

class GoogleMapsLayers:
  ROADMAP = "v"
  TERRAIN = "p"
  ALTERED_ROADMAP = "r"
  SATELLITE = "s"
  TERRAIN_ONLY = "t"
  HYBRID = "y"


class GoogleMapDownloader:
    """
        A class which generates high resolution google maps images given
        a longitude, latitude and zoom level
    """

    def __init__(self, lat, lng, zoom=12, layer=GoogleMapsLayers.ROADMAP):
        """
            GoogleMapDownloader Constructor
            Args:
                lat:    The latitude of the location required
                lng:    The longitude of the location required
                zoom:   The zoom level of the location required, ranges from 0 - 23
                        defaults to 12
        """
        self._lat = lat
        self._lng = lng
        self._zoom = zoom
        self._layer = layer

    def getXY(self):
        """
            Generates an X,Y tile coordinate based on the latitude, longitude
            and zoom level
            Returns:    An X,Y tile coordinate
        """

        tile_size = 256

        # Use a left shift to get the power of 2
        # i.e. a zoom level of 2 will have 2^2 = 4 tiles
        numTiles = 1 << self._zoom

        # Find the x_point given the longitude
        point_x = (tile_size / 2 + self._lng * tile_size / 360.0) * numTiles // tile_size

        # Convert the latitude to radians and take the sine
        sin_y = math.sin(self._lat * (math.pi / 180.0))

        # Calulate the y coorindate
        point_y = ((tile_size / 2) + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -(
        tile_size / (2 * math.pi))) * numTiles // tile_size

        return int(point_x), int(point_y)

    def generateImage(self, **kwargs):
        """
            Generates an image by stitching a number of google map tiles together.
            Args:
                start_x:        The top-left x-tile coordinate
                start_y:        The top-left y-tile coordinate
                tile_width:     The number of tiles wide the image should be -
                                defaults to 5
                tile_height:    The number of tiles high the image should be -
                                defaults to 5
            Returns:
                A high-resolution Goole Map image.
        """

        start_x = kwargs.get('start_x', None)
        start_y = kwargs.get('start_y', None)
        tile_width = kwargs.get('tile_width', 8)
        tile_height = kwargs.get('tile_height', 8)

        # Check that we have x and y tile coordinates
        if start_x == None or start_y == None:
            start_x, start_y = self.getXY()
        # Determine the size of the image
        width, height = 256 * tile_width, 256 * tile_height
        # Create a new image of the size require
        map_img = Image.new('RGB', (width, height))
        for x in range(-tile_width//2, tile_width//2):
            for y in range(-tile_height//2, tile_height//2):
                url = f'https://mt0.google.com/vt?lyrs={self._layer}&x=' + str(start_x + x) + \
                       '&y=' + str(start_y + y) + '&z=' + str(self._zoom)
                current_tile = str(x) + '-' + str(y)
                response = requests.get(url, stream=True)
                with open(current_tile, 'wb') as out_file: shutil.copyfileobj(response.raw, out_file)
                im = Image.open(current_tile)
                map_img.paste(im, ((x+tile_width//2) * 256, (y+tile_height//2) * 256))
                os.remove(current_tile)
        print('Image size (pix): ', map_img.size)
        return map_img

def main():
    # Create a new instance of GoogleMap Downloader

    gmd = GoogleMapDownloader(float(-7.675039), float(107.769191), 18, GoogleMapsLayers.SATELLITE)
    
    print("The tile coorindates are {}".format(gmd.getXY()))

    try:
        # Get the high resolution image
        img = gmd.generateImage()
    except IOError:
        print("Could not generate the image - try adjusting the zoom level and checking your coordinates")
    else:
        # Save the image to disk
        img.save("satellite-image.png")
        print("The map has successfully been created")

def main_main():
    # Create a new instance of GoogleMap Downloader
    os.makedirs("satteliteImages", exist_ok=True)
    df = pd.read_csv("mapData.csv")
    for i in range(len(df)):
        namaPemilik = str(df.iloc[i][0])
        coor = str(df.iloc[i][2])
        coor = coor.replace("(", "")
        coor = coor.replace(")", "")
        coor = coor.split(",")

        gmd = GoogleMapDownloader(float(coor[0]), float(coor[1]), 18, GoogleMapsLayers.SATELLITE)
        
        print("The tile coorindates are {}".format(gmd.getXY()))

        try:
            # Get the high resolution image
            img = gmd.generateImage()
        except IOError:
            print("Could not generate the image - try adjusting the zoom level and checking your coordinates")
        else:
            # Save the image to disk
            img.save(f"satelliteImages/{namaPemilik}.png")
            print("The map has successfully been created")


def getSatelliteImage(latitudes, longitudes, zoomLevel = 18):
    try:
        gmd = GoogleMapDownloader(latitudes, longitudes, zoomLevel, GoogleMapsLayers.SATELLITE)
    except:
        img = None
        isError = True
        message = "Could not generate the image - try adjusting the zoom level and checking your coordinates"
        return img, isError, message

    print("The tile coorindates are {}".format(gmd.getXY()))

    try:
        # Get the high resolution image
        img = gmd.generateImage()
        img = np.array(img) 
        # Convert RGB to BGR
        #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 
    except IOError:
        img = None
        isError = True
        message = "Could not generate the image - try adjusting the zoom level and checking your coordinates"
    else:
        # Save the image to disk
        isError = False
        message = "The map has successfully been created"

    return img, isError, message

if __name__ == "__main__":
    main()
