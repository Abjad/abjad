from abjad import *


def test_Markup___init____01( ):
   '''Init markup with string.
   '''

   markup = markuptools.Markup('foo')

   assert markup.contents_string == 'foo'


def test_Markup___init____02( ):
   '''Init markup with other markup instance.
   '''

   markup_1 = markuptools.Markup('foo')
   markup_2 = markuptools.Markup(markup_1)
   
   assert markup_1.contents_string == 'foo'
   assert markup_2.contents_string == 'foo'


def test_Markup___init____03( ):
   '''Init markup with nonstring and nonmarkup instance.
   '''

   markup = markuptools.Markup(27)

   assert markup.contents_string == '27'
