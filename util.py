# -*- coding: utf-8 -*-

# (c) 2015 David A. Thompson <thompdump@gmail.com>
#
# This file is part of Busca
#
# Busca is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Busca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Busca. If not, see <http://www.gnu.org/licenses/>.

import cv2
import numpy
import os

# configure logging
import logging
# define busca logger as the generic logger
lg=logging


# see http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
# Python 3.3 offers shutil.which()
def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


#
# circles

# circles: a listo f of numpy ndarray circles
def atCircles(img, circles, fn):
    for circle in circles:
        if numpyCircleP(circle):
            fn(circle)
        else:
            raise NotImplementedError("only numpy ndarray circles handled")
    return True


def circle_centers(circles):
    """Given a sequence of circles, return a sequence of tuples representing XY coordinates of the circle centers."""
    centers = []
    for circle in circles[0,:]:
        point = (circle[0],circle[1])
        centers.append(point)
    return centers


def circles_array_to_list(circles):
    circlesList = []
    for i in circles[0,:]:
        circlesList.append(i)
    return circlesList

# FIXME: need to do sanity checks (e.g., if img is grayscale, will it be problematic to use blue or red as a color?)


# circles: an array of ...?
def draw_circles(img, circles):
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(img, (i[0],i[1]), i[2], (0,255,0), 2)
        # draw the center of the circle
        cv2.circle(img, (i[0],i[1]), 2, (0,0,255), 3)


# circles: a list of circles (as returned by find_circles)
def draw_circles_2(img, circles, line_origin=(0,0)):
    if grayscale_p(img):
        color = 0
    else:
        color = (255,0,0)
    for i in circles:
        if numpyCircleP(i):
            print i
            cv2.circle(img, (i[0],i[1]), 20, color, 3)


# a circle object is a numpy ndarray where data is a tuple (x,y,radius); 
def numpyCircleP(x):
    # simpleCircleP
    # if isinstance(x,list) and len(x)==3:

    #print "numpyCircleP",x,type(x),x.shape
    if isinstance(x,numpy.ndarray):
        #print "is numpy.ndarray"
        if x.shape == (3,):
            return True
        else:
            return False
    else:
        return False
    return True


#
# rectangles    
def rectangleP(x):
    if isinstance(x, list) and len(x) == 4:
        return True
    else:
        return False


#
# lines
def lines_from_point(origin, points, img, color=(0,0,0)):
    """POINTS should be a sequence of tuples"""
    #print "points", points, "origin", origin
    for point in points:
        cv2.line(img, origin, point, color, 5)


#
# images
def grayscale_p(img):
    """Return a boolean indicating whether the image IMG is grayscale."""
    first_pixel = img[0,0]
    if isinstance(first_pixel, int):
        return True
    elif isinstance(first_pixel, numpy.uint8):
        return True
    else:
        return False


def px_per_cm(img, x_cm, y_cm):
    """Return pixels per centimeter for image IMG. X_CM and Y_CM are the physical dimensions of the reference image."""
    lg.debug("PX_PER_CM.00 img: %s x_cm: %s y_cm: %s",img,x_cm,y_cm)
    # IMG.SHAPE returns a tuple of 2 or 3 members depending on whether IMG is color or greyscale
    img_rows = img.shape[0]
    img_cols = img.shape[1]
    lg.debug("PX_PER_CM.10 img.shape[0]: %s img.shape[1]: %s",img.shape[0],img.shape[1])

    rows_per_cm = img_rows / y_cm
    cols_per_cm = img_cols / x_cm
    # print rows_per_cm, cols_per_cm
    assert numpy.allclose(round(rows_per_cm), round(cols_per_cm)), "Scaling appears to be different for X and Y dimensions."
    return numpy.mean([rows_per_cm, cols_per_cm])


# cv2 imread doesn't complain if the file passed as argument doesn't exist...
def sane_imread(file, flag):
    if os.path.isfile(file):
        return cv2.imread(file, flag)
    else:
        raise Exception('file does not exist:', file)


#
# points
def xy_arrays_to_xy_tuples(points_as_arrays):
    points_as_tuples=[]
    for point in points_as_arrays:
        point_as_tuple = (point[0],point[1])
        points_as_tuples.append(point_as_tuple)
    return points_as_tuples

#
# types

# type is a type object
def typeP (x,type):
    if type(x)==type:
        return True
    else:
        return False



#
# uncategorized

# test whether circle is in rectangle
# circle is a tuple (x,y,radius); 
# rectangle is a tuple [ x1,y1,x2,y2] ] where x1 < x2 and y1 < y2
def circleInRectangleP (circle, rectangle, centerP=True):
    #print "circleInRectangleP",circle,type(circle),rectangle

    # sanity checks
    assert numpyCircleP(circle),'circle should be a numpy circle'
    assert rectangleP(rectangle),'rectangle should be a list with 4 elements'
    if centerP:
        return pointInRectangleP( circle[0], circle[1], rectangle )
    else:
        raise NotImplementedError("centerP=false not handled")


# FIXME: ensure containing algorithm uses this correctly
# note that 'in' doesn't include rectangle boundary itself
def pointInRectangleP (x, y, rectangle):
    if x < rectangle[2] and x > rectangle[0]:
        if y < rectangle[3] and y > rectangle[1]:
            #print "TRUE"
            return True
        else:
            return False
    else:
        return False


# FIXME?
# fundamentally, this could be simplified as findCornerPoint -- given a series of points, find the upper-left-most, upper-right-most, lower-left-most, or lower-right-most point

# centerP: if centerP is true, find upper-left-most circle where center of circle is within rectangle



# CIRCLES is of type <type 'numpy.ndarray'>
# OLD:  CIRCLES is a list of numpy circle objects (intuitively convenient)
#   (don't implement circles as...: opencv generates: a numpy ndarray with the shape (1,N,3) )
# a numpy circle object: 
#   a numpy ndarray where data is a tuple (x,y,radius); 

# RECTANGLE is a tuple [ x1,y1,x2,y2] ] where x1 < x2 and y1 < y2
# FACTOR is an internal variable (the algorithm uses upper left hand rectangle size dependent on factor)
# CORNER: 8 (upper-left), 4 (upper-right), 2 (lower-left), 1 (lower-right) 
# RECURSE_COUNT: an integer; used internally to limit excessive recursion
def findCornerCircle (circles, rectangle, corner, centerP=True, error_p=True, factor=2, oldFactor=1, recurse_count=0):
    lg.debug("FINDCORNERCIRCLE.00: circles: %s %s %s",circles,rectangle,corner)
    # print("findCornerCircle.00", , corner, oldFactor, factor,recurse_count)
    # print type(circles)
    # print len(circles)
    assert recurse_count<20
    assert isinstance(circles, numpy.ndarray)

    # sanity conversion for python's math madness with integer division in python 2.x
    factor=float(factor)
    oldFactor=float(oldFactor)
    # begin by searching in rectangle anchored in the upper-left-hand corner; expand or contract rectangle as needed...
    xdelta=(rectangle[2]-rectangle[0])/factor
    ydelta=(rectangle[3]-rectangle[1])/factor
    lg.debug("FINDCORNERCIRCLE.20")
    if corner==8:# ul
        searchRectangle = [rectangle[0], rectangle[1], rectangle[0]+xdelta, rectangle[1]+ydelta]
    elif corner==4:# ur
        searchRectangle = [rectangle[0]+xdelta, rectangle[1], rectangle[2], rectangle[3]-ydelta]
    elif corner==2:# ll
        searchRectangle = [rectangle[0], rectangle[3]-ydelta, rectangle[0]+xdelta, rectangle[3]]
    elif corner==1:# lr
        searchRectangle = [rectangle[0]+xdelta, rectangle[1]+ydelta, rectangle[2], rectangle[3]]
    lg.debug("FINDCORNERCIRCLE.40")        
    #print "searchRectangle",searchRectangle    
    # new circles of interest
    circleSet=[]
    for circle in circles:
        #print "CIRCLE",circle
        if circleInRectangleP(circle, searchRectangle, centerP):
            circleSet.append(circle)
    #print "DONE"
    lg.debug("FINDCORNERCIRCLE.50")
    # give up if we apparently have searched virtually the whole rectangle and nothing shows up...
    if (factor-1.0) < 0.01:
        #print "NONE"
        return []
    # handle different circleSet possibilities

    #print "circleSet",circleSet
    lg.debug("FINDCORNERCIRCLE.60")

    if len(circleSet)==0:
        # make search rectangle bigger
        newFactor=(oldFactor+factor)/2
        finalCircle=findUpperLeftMostCircle(circles, rectangle, True, newFactor, oldFactor, recurse_count+1)
    elif len(circleSet)==1:
        #print "SINGLE",circleSet[0]
        finalCircle=circleSet[0]
    else:
        #print "Lots of circles..."
        finalCircle=findUpperLeftMostCircle(circleSet, searchRectangle, True, 2, 1, recurse_count+1)
    #print type(finalCircle)
    lg.debug("FINDCORNERCIRCLE.90")
    assert numpyCircleP(finalCircle), "Couldn't find circle"
    lg.debug("FINDCORNERCIRCLE.A0")
    return finalCircle


def findUpperLeftMostCircle(circles,rectangle,centerP=True,factor=2,oldFactor=1,recurse_count=0):
    findCornerCircle(circles, rectangle, 8, centerP, factor, oldFactor, recurse_count)
