from abjad import *
#from abjad.core import _Parser
import py
py.test.skip('skipping until _Parser is removed from codebase.')


## FORMAT ATTRIBUTE ##

def test_lilyfiletools__format_lilypond_value_and_attribute_01( ):
   t = _Parser( )
   f = t.format_attribute('color')
   assert f == "#'color"
   

def test_lilyfiletools__format_lilypond_value_and_attribute_02( ):
   '''format_attribute correctly replaces _ with -.'''
   t = _Parser( )
   f = t.format_attribute('a_b')
   assert f == "#'a-b"
   

def test_lilyfiletools__format_lilypond_value_and_attribute_03( ):
   '''format_attribute correctly replaces __ with " #'".'''
   t = _Parser( )
   f = t.format_attribute('a__b')
   assert f == "#'a #'b"
   

def test_lilyfiletools__format_lilypond_value_and_attribute_04( ):
   '''
   format_attribute correctly replaces both single underscore (_) and double 
   underscore (__) in the same string.'''
   t = _Parser( )
   f = t.format_attribute('a_b__x__y__z')
   assert f == "#'a-b #'x #'y #'z"
