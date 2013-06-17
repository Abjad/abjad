from abjad import *
from abjad.tools import iotools


def test_stringtools_snake_case_to_lower_camel_case_01():

    assert stringtools.snake_case_to_lower_camel_case('foo_bar_blah') == 'fooBarBlah'
