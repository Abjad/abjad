from abjad import *
from abjad.tools import datastructuretools
import py


def test_ImmutableDictionary___setattr___01():

    dictionary = datastructuretools.ImmutableDictionary({'color': 'red'})

    assert py.test.raises(Exception, "dictionary.flavor = 'cherry'")
