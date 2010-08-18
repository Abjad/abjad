from abjad import *


def test_Markup_style_01( ):
   t = markuptools.Markup('hello')
   assert t.format == r'\markup { hello }'


def test_Markup_style_02( ):
   t = markuptools.Markup('"hello"')
   assert t.format == r'\markup { "hello" }'


def test_Markup_style_03( ):
   t = markuptools.Markup(r'\upright "hello"')
   assert t.format == r'\markup { \upright "hello" }'


def test_Markup_style_04( ):
   t = markuptools.Markup("(markup #:draw-line '(0 . -1))", style = 'scheme')
   #t.style = 'scheme'
   assert t.format == "#(markup #:draw-line '(0 . -1))"
