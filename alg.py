import numpy as np
from enum import Enum
from PIL import Image

import fmt


# ways in which to sort the pixels in `bucket`
BucketSorting = Enum('BucketSorting', ['BRIGHTNESS', 'CHANNEL'])


def buckets(pixels, n, sorting):
    """
    generate colors from an image using buckets.

    Args:
    - `pixels`: A numpy array of the pixels of the image. The array should have
        shape `(N, 3)` where `N` is the number of pixels in the image.
    - `n`: The number of buckets to use.
    - `sorting`: Either `BRIGHTNESS` or `CHANNEL`. If `BRIGHTNESS` is used, the
        pixels of the array will be sorted according to their brightness, otherwise
        they will be sorted solely on the brightest channel.
    """

    # find the largest range
    ranges = np.amax(pixels, axis=0) - np.amin(pixels, axis=0)
    widest = np.argmax(ranges)

    # array sorting technique
    predicate = np.sum(
        pixels, axis=1) if sorting == BucketSorting.BRIGHTNESS else pixels[:, widest]

    # sort the array of pixels
    order = np.argsort(predicate)
    sorted_pixels = pixels[order]

    # bucket pixels
    buckets = np.array_split(sorted_pixels, n)

    # find minimum bucket size
    size = min(map(lambda bucket: bucket.shape[0], buckets))

    # shave off buckets to make array regular
    buckets = np.array([bucket[:size] for bucket in buckets])

    # compute colors by averaging each channel of each bucket
    means = np.mean(buckets, axis=1)
    colors = np.rint(means).astype(int)

    return colors


def rgb_cubic_hist(pixels, n, k):

    num_buckets = round(255 / k)

    # # Note: maybe floor or ceil might be another parameter?
    # pixels = pixels / k
    # pixels = np.rint(pixels).astype(int)

    # print(pixels)

    a = np.array([
        [1, 1, 4],
        [3, 2, 1],
        [1, 1, 1],
        [2, 3, 2],
        [1, 1, 1]
    ])

    # sorts on columns, so need to transpose
    order = np.lexsort(a.T)
    sorted_a = a[order]

    # diff = np.diff(sorted_a, axis=0)
    # thing = np.any(diff)

    # print(thing)

    # np.diff()
