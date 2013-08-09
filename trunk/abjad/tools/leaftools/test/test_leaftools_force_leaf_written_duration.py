# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_force_leaf_written_duration_01():

    note = Note("c'4")
    leaftools.force_leaf_written_duration(
      note, Duration(3, 16))
    assert note.lilypond_format == "c'8. * 4/3"


def test_leaftools_force_leaf_written_duration_02():

    note = Note("c'4")
    leaftools.force_leaf_written_duration(
      note, Duration(7, 8))
    assert note.lilypond_format == "c'2.. * 2/7"


def test_leaftools_force_leaf_written_duration_03():

    note = Note("c'4")
    leaftools.force_leaf_written_duration(
      note, Duration(15, 16))
    assert note.lilypond_format == "c'2... * 4/15"
