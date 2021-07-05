import numpy as np

"""This file is where all our default parameters will be placed.
"""

# Smoothing window
SMOOTHING_WINDOW = 7

# The number of days we use to calculate R_0
R0_WINDOW = 14

# The serial interval, an empirically measured number that is the number
# of days it takes a person who has just gotten COVID-19 to be come
# infections. Right now I have set that number to be 5.2 (taken from a
# a paper of which I will give a reference to).
SERIAL_INT = 5.2

# A Boolean that determines whether we want to include data for not just
# the subregions within a region, but also for the whole region as well.
# See below. 
TOTAL = False

#####################################################################
# Modify this to suit the state you want to use this for in Malaysia.
# Currently "REGION" is set to Penang and "SUBREGIONS" is the list of
# districts in Penang. 
#####################################################################
REGION = 'Penang'
SUBREGIONS = ['Timur Laut', 'Barat Daya', 'Seberang Perai Utara',
              'Seberang Perai Tengah', 'Seberang Perai Selatan']
if TOTAL:
    SUBREGIONS += [REGION]

