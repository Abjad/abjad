from abjad import *


def test_Markup___init____01( ):
   '''Init with string.'''

   markup = markuptools.Markup('foo')

   assert markup.contents == 'foo'


def test_Markup___init____02( ):
   '''Init with other markup instance.'''

   markup_1 = markuptools.Markup('foo')
   markup_2 = markuptools.Markup(markup_1)
   
   assert markup_1.contents == 'foo'
   assert markup_2.contents == 'foo'
