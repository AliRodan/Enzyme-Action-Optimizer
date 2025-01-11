# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 18:20:58 2025

@author: aliro
"""

import numpy as np
from eao import EAO
from get_f import Get_F

def main():
    # Define your parameters
    EnzymeCount = 50
    f_name = 'F23'
    MaxIter = 500

    # Get the problem details (bounds, dimension, and objective function)
    lb, ub, dim, fobj = Get_F(f_name)

    # Call the optimizer
    OptimalCatalysis, BestSubstrate, conv_curve = EAO(
        EnzymeCount, 
        MaxIter, 
        lb, 
        ub, 
        dim, 
        fobj
    )

    # Display the result
    print(f"The best optimal value of the objective function found by EAO is : {OptimalCatalysis}")

if __name__ == "__main__":
    main()
