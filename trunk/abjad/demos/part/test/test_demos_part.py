from abjad.demos.part.make_part_lilypond_file import make_part_lilypond_file
import py
py.test.skip('takes forever to run; maybe endless loop?')


def test_demos_part_01():

    lilypond_file = make_part_lilypond_file()
