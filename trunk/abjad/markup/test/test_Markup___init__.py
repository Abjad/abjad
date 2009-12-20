from abjad import *


def test_Markup___init___01( ):
   '''Init with string.'''

   markup = Markup('foo')

   assert markup.contents == 'foo'


def test_Markup___init___02( ):
   '''Init with other markup instance.'''

   markup_1 = Markup('foo')
   markup_2 = Markup(markup_1)
   
   assert markup_1.contents == 'foo'
   assert markup_2.contents == 'foo'
