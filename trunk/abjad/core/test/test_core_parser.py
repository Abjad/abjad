from abjad import *
from abjad.core.parser import _Parser


### FORMAT ATTRIBUTE ###

def test_core_parser_01( ):
   t = _Parser( )
   f = t.formatAttribute('color')
   assert f == "#'color"
   

def test_core_parser_02( ):
   '''formatAttribute correctly replaces _ with -.'''
   t = _Parser( )
   f = t.formatAttribute('a_b')
   assert f == "#'a-b"
   

def test_core_parser_03( ):
   '''formatAttribute correctly replaces __ with " #'".'''
   t = _Parser( )
   f = t.formatAttribute('a__b')
   assert f == "#'a #'b"
   

def test_core_parser_04( ):
   '''
   formatAttribute correctly replaces both single underscore (_) and double 
   underscore (__) in the same string.'''
   t = _Parser( )
   f = t.formatAttribute('a_b__x__y__z')
   assert f == "#'a-b #'x #'y #'z"
   

