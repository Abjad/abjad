from abjad import *


def test_markup_01( ):
   t = Markup('hello')
   assert t.format == r'\markup{hello}'


def test_markup_02( ):
   t = Markup('"hello"')
   assert t.format == r'\markup{"hello"}'


def test_markup_03( ):
   t = Markup(r'\upright "hello"')
   assert t.format == r'\markup{\upright "hello"}'
