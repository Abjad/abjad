# -*- encoding: utf-8 -*-
from abjad.demos.part.make_part_lilypond_file import make_part_lilypond_file


def test_demos_part_01():

    lilypond_file = make_part_lilypond_file()
    assert len(format(lilypond_file))
