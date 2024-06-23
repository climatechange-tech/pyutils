#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import scipy.signal as ssig
import scipy.stats as ss
from scipy.cluster.vq import whiten

#-----------------------#
# Import custom modules #
#-----------------------#

import pytools.weather_and_climate.netcdf_handler as pyt_netcdf_handler
import pytools.arrays_and_lists.array_maths as pyt_array_maths

# Create aliases #
#----------------#

#------------------#
# Define functions #
#------------------#