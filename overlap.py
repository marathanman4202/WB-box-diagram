# From stackoverflow suggestion at
# http://stackoverflow.com/questions/16691524/calculating-the-overlap-distance-of-two-1d-line-segments
def overlap(min1, max1, min2, max2):
    """
    Find overlapping length of two 1D lines denoted by (min1, max1)
    and (min2, max2). 
    """
    return max(0, min(max1, max2) - max(min1, min2))