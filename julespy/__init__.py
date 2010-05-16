#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Interface with JULES.
---------------------

The module provides a wrapper to easily call the JULES model.
"""

import os

def process_jules_output ( fname ):
    """
    A function to process JULES output files. It reads the text files, bagging
    all the parameter names (and levels), and collects the data for each 
    timestep. The output is a dictionary, with the timestep as keys (this 
    probably needs some clever work to make it easier to find stuff), and 
    a subsequent dictionary with the parameters.

    :param fname: The filename of the JULES output file that will be processed.
    """
    import numpy
    from copy import deepcopy
    var_dict = {}
    output = {}
    with open( fname,'r') as jules_out:
        while True:
            read_line = jules_out.readline()
            if not read_line:
                break

            if (read_line.find("S")==0) or (read_line.find("M")==0) or \
                                        (read_line.find("A")==0)  :
                # First, get variable names and number of levels
                split_string = read_line.split()
                var_dict[ split_string[2].strip() ] = \
                            numpy.zeros((int(split_string[1])))
                print "Variable: ", split_string[2]
            elif read_line.find ("timestep")==0:
                #Aaaahhh, a timestep!
                # Get the timestep
                split_string = read_line.split()
                tstep = ''.join(split_string[-2:])
                #Empty dictionary for this timestep
                output[tstep] = deepcopy( var_dict )
                # For each variable
                for var in var_dict.iterkeys():
                    #How many labels for this variable?
                    for i in xrange(var_dict[var].shape[0]):
                        # Read value and store
                        read_line = jules_out.readline().strip()
                        output[tstep][var][i] = float(read_line)

    return output

def do_parameter_file ( parameter_file ):
    """
    A function to read and process JULES parameter files. The output
    is a list with the headers (usually, PFTs or non-vegetated surface types)
    and a dictionary, with the parameter names as keys, and a dictionary of
    parameter values stored in the same order as the headers.

    :param parameter_file: The JULES parameter file
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

    :param fname: The parameter filename.
    :param header: A list with the parameter headers in order
    :param parameters: The parameters dictionary. Each entry is a list with the value for each header.
    :param parameter_list: A list with the order of the parameters in the file. Not sure this is actually needed...
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
    def __init__ ( self, jules_infile = "point_loobos.jin", \
                         jules_cmd = "jules.exe", \
                         pft_params_file = "standard_pft_param.dat", \
                         nonveg_params_file = \
                                        "standard_nonveg_param.dat", \
                         trif_params_file = \
                                        "standard_trif_param.dat" ):
        """
        The constructor.
        """
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

        # Read JULES parameter files
        ( self.pft_names, self.pft_parameters, self.pft_para_list ) = \
            do_parameter_file ( pft_params_file )

        ( self.nonveg_names, self.nonveg_parameters, \
                self.nonveg_para_list ) = \
                do_parameter_file ( nonveg_params_file )

        ( self.trif_names, self.trif_parameters, self.trif_para_list ) = \
            do_parameter_file ( trif_params_file )

    def modify_params ( self, ptype, param, pft, new_val ):
        """
        A method to modify parameters. Given that parameters are either
        pft, trifid or non-vegetation parameters, this has to be specified
        in the ptype argument. Then, the parameter (or parameters, stick them
        on a list), the pft to which they apply, and the actual value (or
        values if you have a list).

        :param ptype: The type of parameter. For this version, this can either be ``pft``, ``nonveg`` or ``trifid``.
        :param param: Parameter name (or names if this is a list)
        :param pft: PFT to which the changes will be applied to.
        :param new_val: New value, or values if a list. If it is a list, make sure that the order is the same as in param.
        
        """
        if ptype.lower() == "pft":
            paramset = self.pft_parameters
            paramlist = self.pft_names
        elif ptype.lower() == "trifid":
            paramset = self.trif_parameters
            paramlist = self.trif_names
        elif ptype.lower() == "nonveg":
            paramset = self.nonveg_parameters
            paramlist = self.nonveg_names
        else:
            raise ValueError, "ptype has to be either 'pft', " + \
                              "'trifid' or 'nonveg'"
        if (type ( param ) == list):
            if type(new_val) != list :
                raise TypeError, "new_val has to be a list if param is a list."
            if len(new_val) != len(param):
                raise ValueError, "new_val must have the same length as param"
            for (i, p) in enumerate( param ):
                paramset[p][paramlist.index(pft)] = new_val[i]
        else:
            paramset[param][paramlist.index(pft)] = new_val

    def call_jules ( self ):
        """
        Calls JULES, creating a JIN file that points to parameter
        files created on the run. The output of the model is saved
        in some text files that is specifid in the JIN file

        TODO Provide the ability to change drivers
        """
        from subprocess import Popen, PIPE, STDOUT
        import tempfile
        
        
        # Create the PFT, TRIFID and NONVEG temporary files
        pft_fd, pft_path = tempfile.mkstemp()
        trifid_fd, trifid_path = tempfile.mkstemp()
        nonveg_fd, nonveg_path = tempfile.mkstemp()
        # Save parameters to these files
        write_parameter_file ( pft_path, self.pft_names, \
                self.pft_parameters, self.pft_para_list  )
        write_parameter_file ( trifid_path, self.trif_names, \
                self.trif_parameters, self.trif_para_list )
        write_parameter_file ( nonveg_path, self.nonveg_names, \
                self.nonveg_parameters, self.nonveg_para_list )
        # Now, read the file
        file_in = open( self.jules_infile, 'r' )
        jules_jin = file_in.read()
        file_in.close()

        # Modify the locations of temporary files
        jules_jin = jules_jin.replace( "**PFTPARAMETERS**", \
                                        "%s"%pft_path )
        jules_jin = jules_jin.replace( "**NONVEGPARAMETERS**", \
                                        "%s"%nonveg_path )
        jules_jin = jules_jin.replace ( "**TRIFIDPARAMETERS**", \
                                        "%s"%trifid_path )

        # Launch JULES with new parametrisation
        # Pass jules_jin as stdin, and pipe stderr and stdout to
        # a python variable.
        cmd_line = "" + self.jules_cmd
        p = Popen ( cmd_line, stdout=PIPE, stdin=PIPE, stderr=STDOUT )
        p.stdin.write( jules_jin )
        output = p.communicate()[0]
        p.stdin.close()
        # Remove temporary files
        os.remove ( pft_path )
        os.remove ( nonveg_path )
        os.remove ( trifid_path )
        return output


