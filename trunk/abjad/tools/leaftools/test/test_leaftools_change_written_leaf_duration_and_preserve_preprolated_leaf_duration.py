from abjad import *


def test_leaftools_change_written_leaf_duration_and_preserve_preprolated_leaf_duration_01():

    n = Note("c'4")
    leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration(
      n, Duration(3, 16))
    assert n.format == "c'8. * 4/3"


def test_leaftools_change_written_leaf_duration_and_preserve_preprolated_leaf_duration_02():

    n = Note("c'4")
    leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration(
      n, Duration(7, 8))
    assert n.format == "c'2.. * 2/7"


def test_leaftools_change_written_leaf_duration_and_preserve_preprolated_leaf_duration_03():

    n = Note("c'4")
    leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration(
      n, Duration(15, 16))
    assert n.format == "c'2... * 4/15"
