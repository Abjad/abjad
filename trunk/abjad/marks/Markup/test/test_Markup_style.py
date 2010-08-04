from abjad import *


def test_Markup_style_01( ):
   t = Markup('hello')
   assert t.format == r'\markup { hello }'


def test_Markup_style_02( ):
   t = Markup('"hello"')
   assert t.format == r'\markup { "hello" }'


def test_Markup_style_03( ):
   t = Markup(r'\upright "hello"')
   assert t.format == r'\markup { \upright "hello" }'


def test_Markup_style_04( ):
   t = Markup("(markup #:draw-line '(0 . -1))")
   t.style = 'scheme'
   assert t.format == "#(markup #:draw-line '(0 . -1))"
