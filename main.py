import sys
import numpy as np
from PIL import Image

import alg
from alg import BucketSorting

import fmt
from fmt import ColorMode

# arguments
img_path = sys.argv[1]
n = int(sys.argv[2])

# load the image into a numpy array
img = Image.open(img_path).convert("RGB")
pixels = np.array(img.getdata())

"""
# get colors from the bucket algorithm
bucket_colors_channel = alg.buckets(pixels, n, BucketSorting.CHANNEL)
bucket_colors_brightness = alg.buckets(pixels, n, BucketSorting.BRIGHTNESS)

fmt.table({
    "Channel RGB": [{"color": color, "fmt": ColorMode.RGB} for color in bucket_colors_channel],
    "Channel HEX": [{"color": color, "fmt": ColorMode.HEX} for color in bucket_colors_channel],
    "Brightness RGB": [{"color": color, "fmt": ColorMode.RGB} for color in bucket_colors_brightness],
    "Brightness HEX": [{"color": color, "fmt": ColorMode.HEX} for color in bucket_colors_brightness],
})
"""

alg.rgb_cubic_hist(pixels, n, 8)
