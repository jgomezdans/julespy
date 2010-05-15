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
 ###           try:
            parameters.setdefault( par_name.lstrip().rstrip(), []).append(\
                     float(i.lstrip ().rstrip().lstrip("'").rstrip("'") ))
            #except ValueError:
                ##Groan...
                #parameters.setdefault( par_name.lstrip().rstrip(), []).append(\
                    #float( int(\
                        #i.lstrip ().rstrip().lstrip("'").rstrip("'") ) ))
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
        

class julespy:
    """
    A class to call JULES, varying stuff like PFT parameters and the like.
    """
    def __init__ ( self, jules_infile = "point_loobos_example.jin", \
                         jules_outfile = "OUTPUT/loobos.tstep.30m.asc", \
                         jules_cmd = "jules.exe", \
                         pft_params_file = "standard_pft_param.dat", \
                         nonveg_params_file = \
                                        "standard_nonveg_param.dat", \
                         trif_params_file = \
                                        "standard_trif_param.dat" ):
        if not os.environ.has_key ( "JULES_DIR" ):
            raise  RuntimeError, "You need to set the JULES_DIR " + \
                                 "environment variable"
        else:
            self.jules_dir = os.environ['JULES_DIR']
            
        if os.path.exists ( os.path.join( self.jules_dir, jules_cmd) ):
            self.jules_cmd = os.path.join( self.jules_dir, jules_cmd)
        else:
            raise IOError, "No JULES executable in %s" % \
                            (os.path.join( self.jules_dir, jules_cmd))

        if os.path.exists ( os.path.join( self.jules_dir, jules_infile) ):
            self.jules_infile = os.path.join ( self.jules_dir, jules_infile )
        else:
            raise IOError, "JULES infile (jin) %s doesn't seem to exist" % \
                            (os.path.join( self.jules_dir, jules_infile))

        self.jules_outfile = jules_outfile
        # Read JULES parameter files
        ( self.pft_names, self.pft_parameters, self.pft_para_list ) = \
            do_parameter_file ( pft_params_file )

        ( self.nonveg_names, self.nonveg_parameters, \
                self.nonveg_para_list ) = \
                do_parameter_file ( nonveg_params_file )

        ( self.trif_names, self.trif_parameters, self.trif_para_list ) = \
            do_parameter_file ( trif_params_file )

    def modify_pft_params ( self, param, pft, new_val ):
        if (type ( param ) == list):
            if type(new_val) != list :
                raise TypeError, "new_val has to be a list if param is a list."
            if len(new_val) != len(param):
                raise ValueError, "new_val must have the same length as param"
            for (i, p) in enumerate( param ):
                self.pft_parameters[p][self.pft_names.index(pft)] = new_val[i]
        else:
            self.pft_parameters[param][self.pft_names.index(pft)] = new_val
