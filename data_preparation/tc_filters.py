from procgraph import  simple_block
import numpy as np

@simple_block
def middle(gray):
    h, _ = gray.shape
    j = int(h / 2)
    y = gray[j, :]
    return y
    
    
@simple_block
def center(gray):
    _, w = gray.shape
    i = int(w / 2)
    y = gray[:, i]
    return y


@simple_block
def midcen(gray):
    mid = middle(gray)
    cen = center(gray)
    midcen = np.hstack((mid[::2], cen[::2]))
    return midcen

@simple_block
def grid24(gray): return grid(gray, 24)

@simple_block
def grid16(gray): return grid(gray, 16)

@simple_block
def grid8(gray): return grid(gray, 8)

@simple_block
def grid20(gray): return grid(gray, 20)

def grid(gray, interval):
    """ Extract a grid of pixels"""
    h, w = gray.shape
    x = range(0, h, interval)
    y = range(0, w, interval)
    return gray[x, :][:, y]

@simple_block
def patch32(gray):
    x, y = 200, 200
    w, h = 32, 32
    return gray[x:x + w,
                y:y + h]

@simple_block
def patch32s4(gray):
    x, y = 200, 200
    w, h = 32, 32
    s = 4
    return gray[x:x + w * s:s,
                y:y + h * s:s]
    
    
    
    
