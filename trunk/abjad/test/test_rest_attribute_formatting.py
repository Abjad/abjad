from abjad import *


def test_rest_attribute_formatting_01( ):
   '''Rests format arbitrary LilyPond attributes.'''
   t = Rest((1, 4))
   t.color = 'red'
   assert t.format == "\\once \\override Rest #'color = #red\nr4"


def test_rest_attribute_formatting_02( ):
   '''Rests format arbitrarily many LilyPond attributes.'''
   t = Rest((1, 4))
   t.color = 'red'
   t.staff_position = -6
   assert t.format == "\\once \\override Rest #'color = #red\n\\once \\override Rest #'staff-position = #-6\nr4"


def test_rest_atrribute_formatting_03( ):
   '''Clear LilyPond attributes on rests one at a time with None.'''
   t = Rest((1, 4))
   t.color = 'red'
   t.color = None
   assert t.format == 'r4'


def test_rest_attribute_formatting_04( ):
   '''Clear all LilyPond attributes on rests with rest.clear( ).'''
   t = Rest((1, 4))
   t.color = 'red'
   t.color = None
   t.clear( )
   assert t.format == 'r4'
