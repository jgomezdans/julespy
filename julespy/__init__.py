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
    fin = open ( parameter_file, 'r' )
    read_line = fin.readline().strip().split("!")[0]
    header_names = [ i.lstrip ().rstrip().lstrip("'").rstrip("'") \
                        for i in read_line.split(",") ]
    parameters = {}
    parameter_list = []
    while True:
        read_line = fin.readline()
        if not read_line:
            break
        if read_line[0] == "#":
            continue
        try:
            [par_vals, par_name ] = read_line.strip("\n").split("!")
        except ValueError:
            continue
        for i in par_vals.split(","):
            try:
                parameter_list.index ( par_name.lstrip().rstrip() )
            except:
                parameter_list.append ( par_name.lstrip().rstrip() )
            try:
                parameters.setdefault( par_name.lstrip().rstrip(), []).append(\
                     float(i.lstrip ().rstrip().lstrip("'").rstrip("'") ))
            except ValueError:
                #Groan...
                parameters.setdefault( par_name.lstrip().rstrip(), []).append(\
                    float( int(\
                        i.lstrip ().rstrip().lstrip("'").rstrip("'") ) ))
    fin.close()
    return ( header_names, parameters, parameter_list )

def write_parameter_file ( fname, header, parameters, parameter_list ):
    """
    A function to write JULES parameter files out. These files are made up of

    1. A header with eg PFT names running across the top
    2. The values under each header
    3. A fortran comment synbol (!) and the parameter name
    4. Some random stuff preceded by a #
    """
    f_out = open ( fname, 'w' )
    header_txt =  ",".join( [ "%7s"%str("'%s'"%h) for h in header ] )
    header_txt += "    !  pftName \n"
    f_out.write ( header_txt )
    for p in parameter_list:
        p_txt = ", ".join( [ str("%6.2f"%h) for h in parameters[p] ] )
        p_txt += ("     !  %s\n"%p)
        f_out.write ( p_txt )
    f_out.write ("# A nice file written out by the julespy system!")
    f_out.close()
        

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
    