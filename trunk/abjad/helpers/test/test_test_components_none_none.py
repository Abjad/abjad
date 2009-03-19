from abjad.helpers.test_components import _test_components
from abjad import *


def test_test_components_none_none_01( ):
   t = scale(4)
   assert _test_components(t)


def test_test_components_none_none_02( ):
   t = Staff(scale(4)) * 4
   assert _test_components(t)


def test_test_components_none_none_03( ):
   t = range(4)
   assert not _test_components(t)


def test_test_components_none_none_04( ):
   t = [ ]
   assert _test_components(t)
