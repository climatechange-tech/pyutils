#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import itertools as it
from numpy import array as np_arr

#------------------#
# Define functions #
#------------------#

# Combinatorial operations #
#--------------------------#

def calc_all_unique_pairs(array_like, library="python-default"):    
    """
    Function to calculate all possible pairs, irrespective of the order,
    in a list or 1D array.
    
    Example
    -------
    arr = [1,7,4]
    
    Having 3 items in the list, there are fact(3) = 6 combinations
    Manually, one can deduce the following pairs:
    
    1-7, 1-4, 4-1, 7-1, 7-4, 4-7
    
    Since the order is unimportant, actual number of combos is fact(3) / 2 = 3.
    In this case, pairs number 3, 4 and 6 can be ruled out, remaining these combos:
        
    1-7, 1-4 and 4-7
    
    Programatically, this function is designed to store each possible
    pair in a tuple, conforming a list of them, so for this case
    the output would be:
        
    [(1,7), (1,4), (4,7)]
    
    Calculations can either be performed using standard Python procedures,
    or with the built-in 'itertools' library.
    
    Parameters
    ----------
    array_like : array-like of numbers, i.e. list or np.ndarray thereof.    
        Input data. In both cases it will be converted to a NumPy array,
        and if the latter's dimension is N > 1, it will also be flattened.
       
        Programatically, all types of data are allowed to co-exist
        in the array, being these simple or complex, which in that case
        converting to a NumPy array would result in an 'object' data type array.
        However, with no other context, the pairing would be nonsensical.

        In order to give some meaning to the pairing, object-type arrays
        are not allowed, else TypeError is raised.
        Numbers can be of type integer, float, complex
        or a combination among them.
            
    library : {'python-default', 'itertools'}
        Library to be used. Using 'itertools' built-in library
        the execution time is slightly improved.
            
    Returns
    -------
    TypeError
        If not all elements inside the array are of the same type.
    ValueError
        If an unsupported library is chosen.
    all_pair_combo_arr : list or numpy.array of tuples
        The resulting list or array (depending the library used) of tuples.    
    """
    
    # Input validations #
    #-#-#-#-#-#-#-#-#-#-#
    
    # Input array #
    array = np_arr(array_like)
    data_type = array.dtype

    if data_type == 'O':       
        raise TypeError("All elements of the array must either be of type"
                        "'int', 'float', 'complex', 'str' "
                        "or a combination of several of them.")
        
    else:
        dims = len(array.shape)
        if dims > 1:
            array = array.flatten()
    
    # Library #
    if library not in return_pairs_library_list:
        raise ValueError("Unsupported library. "
                         f"Choose one from {return_pairs_library_list}.")
    
    
    # Compute pairs of numbers #
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-
    
    all_pair_combo_arr = return_pairs_opt_dict.get(library)(array)
    return all_pair_combo_arr


#--------------------------#
# Parameters and constants #
#--------------------------#

# Supported options #
#-------------------#

# Method options #
return_pairs_library_list = ["python-default", "itertools-comb"]

# Switch case dictionaries #
#--------------------------#

# Pair combo calculation functions #
return_pairs_opt_dict = {
    return_pairs_library_list[0]: lambda arr: [(i, j) 
                                               for i_aux, i in enumerate(arr)
                                               for j in arr[i_aux+1:]],
    return_pairs_library_list[1]: lambda arr: list(it.combinations(arr, 2))
}
