from abjad import *
from abjad.core.parser import _Parser


## FORMAT ATTRIBUTE ##

def test_core_parser_01( ):
   t = _Parser( )
   f = t.format_attribute('color')
   assert f == "#'color"
   

def test_core_parser_02( ):
   '''format_attribute correctly replaces _ with -.'''
   t = _Parser( )
   f = t.format_attribute('a_b')
   assert f == "#'a-b"
   

def test_core_parser_03( ):
   '''format_attribute correctly replaces __ with " #'".'''
   t = _Parser( )
   f = t.format_attribute('a__b')
   assert f == "#'a #'b"
   

def test_core_parser_04( ):
   '''
   format_attribute correctly replaces both single underscore (_) and double 
   underscore (__) in the same string.'''
   t = _Parser( )
   f = t.format_attribute('a_b__x__y__z')
   assert f == "#'a-b #'x #'y #'z"
