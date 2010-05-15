# -*- coding: utf-8 -*-
from nose.tools import *
from julespy import *


@raises(IOError)
def test_do_parameter_file_no_file ( ):
    do_parameter_file ( "abc" )

def test_do_parameter_file_do_file_header ():
    ( header_names, parameters ) = do_parameter_file ( \
                    "/home/ucfajlg/JULES/JULES/" + \
                    "jules-cvs/PARAM/standard_pft_param.dat" )
    assert header_names == ['BT', 'NT', 'C3G', 'C4G', 'shrub']

def test_do_parameter_file_do_file_par_vals ():
    ( h, p) = do_parameter_file ( \
                    "/home/ucfajlg/JULES/JULES/" + \
                    "jules-cvs/PARAM/standard_pft_param.dat" )
    assert p.has_key("rootd_ft") 
    