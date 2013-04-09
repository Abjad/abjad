from abjad import *
from abjad.tools.pitchtools import NamedChromaticPitch
import scftools


def test_PitchRangeEditor_run_01():

    editor = scftools.editors.PitchRangeEditor()
    editor.run(user_input="1 [F#3, C5) q")
    assert editor.target == pitchtools.PitchRange('[F#3, C5)')

    editor = scftools.editors.PitchRangeEditor()
    editor.run(user_input='1 (A0, C8] q')
    assert editor.target == pitchtools.PitchRange('(A0, C8]')


def test_PitchRangeEditor_run_02():
    '''Quit, score, studio & junk all work.

    Note that back doesn't yet work here
    because 'b' interprets as named chromatic pitch.
    '''

    editor = scftools.editors.PitchRangeEditor()
    editor.run(user_input='q')
    assert editor.ts == (2,)

    editor = scftools.editors.PitchRangeEditor()
    editor.run(user_input='sco q')
    assert editor.ts == (4, (0, 2))

    editor = scftools.editors.PitchRangeEditor()
    editor.run(user_input='stu')
    assert editor.ts == (2,)

    editor = scftools.editors.PitchRangeEditor()
    editor.run(user_input='foo q')
    assert editor.ts == (4, (0, 2))
