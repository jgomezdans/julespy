# -*- coding: utf-8 -*-
from nose.tools import *
from julespy import *


@raises(IOError)
def test_do_parameter_file_no_file ( ):
    do_parameter_file ( "abc" )

def test_do_parameter_file_do_file_header ():
    ( header_names, parameters, p_list ) = do_parameter_file ( \
                    "/home/ucfajlg/JULES/JULES/" + \
                    "jules-cvs/PARAM/standard_pft_param.dat" )
    assert header_names == ['BT', 'NT', 'C3G', 'C4G', 'shrub']

def test_do_parameter_file_do_file_par_vals ():
    ( h, p, p_list ) = do_parameter_file ( \
                    "/home/ucfajlg/JULES/JULES/" + \
                    "jules-cvs/PARAM/standard_pft_param.dat" )
    assert p.has_key("rootd_ft")

def test_do_parameter_file_do_file_par_list ():
    (h, p, p_list ) = do_parameter_file ( "/home/ucfajlg/JULES/JULES/jules-cvs/PARAM/standard_pft_param.dat" )
    assert len(p_list) == 42
def test_write_parameter_file ():
    (h, p, p_list ) = do_parameter_file ( "/home/ucfajlg/JULES/JULES/jules-cvs/PARAM/standard_pft_param.dat" )
    write_parameter_file ( "/tmp/standard_pft_param.dat", h, p, p_list )
    fp = open( "/tmp/standard_pft_param.dat", 'r' )
    new_file = fp.read()
    fp.close()
    fp = open( "/home/ucfajlg/JULES/JULES/jules-cvs/PARAM/standard_pft_param.dat", 'r' )
    old_file = fp.read()
    fp.close()
    assert (new_file[0] == old_file[0]) and (new_file[1] == old_file[1])

def test_julespy_init():
    j = julespy( )

@raises(IOError)
def test_julespy_init_jules_exe():
    J = julespy( jules_cmd="/asrb")

@raises(IOError)
def test_julespy_init_jules_jin():
    J = julespy( jules_infile="/asrb" )

def test_julespy_modify_pft_params ( ):
    jules = julespy()
    jules.modify_params ( "pft",'lai', 'BT', 23 )
    assert jules.pft_parameters['lai'][0] == 23
    
def test_julespy_modify_pft_params2 ( ):
    jules = julespy()
    jules.modify_params ( "nonveg",'gs_nvg', 'urban', 23 )
    assert jules.nonveg_parameters['gs_nvg'][0] == 23


def test_julespy_modify_pft_params3 ( ):
    jules = julespy()
    jules.modify_params ( "trifid",'lai_max', 'BT', 23 )
    assert jules.trif_parameters['lai_max'][0] == 23
    
@raises (ValueError)
def test_julespy_modify_pft_params4 ( ):
    jules = julespy()
    jules.modify_params ( "urg",'lai_max', 'BT', 23 )
    
    
def test_julespy_modify_params_list ( ):
    jules = julespy()
    jules.modify_params ( "pft", ['lai', 'c3'], 'BT', [23,24] )
    assert (jules.pft_parameters['lai'][0] == 23) and \
           (jules.pft_parameters['c3'][0] == 24)

@raises (TypeError)           
def test_julespy_modify_params_list1 ( ):
               jules = julespy()
               jules.modify_params ( "pft", ['lai', 'c3'], 'BT', 23 )

@raises (ValueError)
def test_julespy_modify_params_list2 ( ):
                   jules = julespy()
                   jules.modify_params ( "pft", ['lai', 'c3'], 'BT', [23] )

def test_julespy_call_jules():
    jules = julespy()
    output = jules.call_jules()
    assert output.find("End")>=0

def test_process_jules_output():
    output = process_jules_output (\
        "/home/ucfajlg/JULES/JULES/jules-cvs/OUTPUT/loobos.p2.01d.asc")
    assert type(output) == dict