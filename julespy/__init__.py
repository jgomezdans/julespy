#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interface with JULES.

Build a JULES infile, run JULES and get the return the output.

Heavily based on MdeKauwe's version.
"""

import os
import sys

def do_parameter_file ( parameter_file ):
    """
    A function to read and process JULES parameter files. The output
    is a list with the headers (usually, PFTs or non-vegetated surface types)
    and a dictionary, with the parameter names as keys, and a dictionary of
    parameter values stored in the same order as the headers.
    """
    if not os.path.exists ( parameter_file ):
        raise IOError, "Input file doesn't exist!"
    fp = open ( parameter_file, 'r' )
    L = fp.readline().strip().split("!")[0]
    header_names = [ i.lstrip ().rstrip().lstrip("'").rstrip("'") \
                        for i in L.split(",") ]
    parameters = {}
    while True:
        L = fp.readline()
        if not L: break
        if L[0]=="#": continue
        try:
            [par_vals, par_name ] = L.strip("\n").split("!")
        except ValueError:
            continue
        for i in par_vals.split(","):
            try:
                parameters[ par_name.lstrip().rstrip() ] = \
                     float(i.lstrip ().rstrip().lstrip("'").rstrip("'") )
            except:
                #Groan...
                parameters[ par_name.lstrip().rstrip() ] = \
                    float( int(i.lstrip ().rstrip().lstrip("'").rstrip("'") ) )
    fp.close()
    return ( header_names, parameters )

######class julespy:
    ######"""
    ######A class to call JULES, varying stuff like PFT parameters and the like.
    ######"""
    ######def __init__ ( self, jules_infile = "./point_looblos.jin", \
                         ######jules_outfile = "./OUTPUT/loobos.tstep.30m.asc", \
                         ######jules_cmd = "./jules.exe", \
                         ######pft_params_file = "standard_pft_param.dat", \
                         ######standard_nonveg_params_file = \
                                        ######"standard_nonveg_param.dat", \
                         ######standard_trif_params_file = \
                                        ######"standard_trif_param.dat" ):

 
        ######if os.path.exists ( jules_comd ):
            ######self.jules_cmd = jules_cmd
        ######else:
            ######print "No JULES executable in %s"%jules_cmd
            ######sys.exit(-1)

        ######if os.path.exists ( jules_infile ):
            ######self.jules_infile = jules_infile
        ######else:
            ######print "JULES infile (jin) %s doens't seem to exist"%jules_infile
            ######sys.exit(-1)

        ######self.jules_outfile = jules_outfile

        ######self._get_parameters ( self, pft_params_file, \
                                     ######standard_nonveg_params_file, \
                                     ######standard_trif_params_file )

    ######def _get_parameters ( self, pft_params_file, standard_nonveg_params_file, \
                                ######standard_trif_params_file ):
        ######"""
        ######This method gets the parameter values in dictionaries for easy
        ######manipulation.
        ######"""
        ####### First, PFT parameter files

    
    ######def update_pft_parameters ( self, parameter_list, parameter_vals ):
        ######print "there"

######if __name__ == "__main__":
    ######print "here"
    