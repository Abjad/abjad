# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_OctaveTranspositionMappingEditor_run_01():

    editor = scoremanager.editors.OctaveTranspositionMappingEditor()
    editor._run(pending_user_input='add source [A0, F#4] target 22 done add source (F#4, C8] target 26 done done done')

    mapping = pitchtools.OctaveTranspositionMapping([('[A0, F#4]', 22), ('(F#4, C8]', 26)])
    assert editor.target == mapping


def test_OctaveTranspositionMappingEditor_run_02():
    r'''Named mapping.
    '''

    editor = scoremanager.editors.OctaveTranspositionMappingEditor()
    editor._run(pending_user_input='id piccolo~second~octave '
        'add source [A0, F#4] target 22 done '
        'add source (F#4, C8] target 26 done done done ')

    mapping = pitchtools.OctaveTranspositionMapping(
            [('[A0, F#4]', 22), ('(F#4, C8]', 26)],
            custom_identifier='piccolo second octave')

    assert editor.target == mapping


def test_OctaveTranspositionMappingEditor_run_03():
    r'''Name only.
    '''

    editor = scoremanager.editors.OctaveTranspositionMappingEditor()
    editor._run(pending_user_input='id piccolo~second~octave done')

    mapping = pitchtools.OctaveTranspositionMapping(
        custom_identifier='piccolo second octave')
    assert editor.target == mapping
