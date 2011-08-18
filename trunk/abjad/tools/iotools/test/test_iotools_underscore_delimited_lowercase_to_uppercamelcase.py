from abjad import *
from abjad.tools import iotools


def test_iotools_underscore_delimited_lowercase_to_uppercamelcase_01():

    assert iotools.underscore_delimited_lowercase_to_uppercamelcase('foo_bar_blah') == 'FooBarBlah'
