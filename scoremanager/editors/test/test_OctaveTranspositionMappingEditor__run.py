# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_OctaveTranspositionMappingEditor__run_01():

    session = scoremanager.core.Session()
    editor = scoremanager.editors.OctaveTranspositionMappingEditor
    editor = editor(session=session)
    string = 'add source [A0, F#4] target 22 done'
    string += ' add source (F#4, C8] target 26 done done done'
    editor._run(pending_user_input=string)

    mapping = pitchtools.OctaveTranspositionMapping([
        ('[A0, F#4]', 22),
        ('(F#4, C8]', 26),
        ])
    assert editor.target == mapping


def test_OctaveTranspositionMappingEditor__run_02():
    r'''Named mapping.
    '''

    session = scoremanager.core.Session()
    editor = scoremanager.editors.OctaveTranspositionMappingEditor
    editor = editor(session=session)
    string = 'add source [A0, F#4] target 22 done'
    string +=  ' add source (F#4, C8] target 26 done done done'
    editor._run(pending_user_input=string)

    mapping = pitchtools.OctaveTranspositionMapping(
            [('[A0, F#4]', 22), ('(F#4, C8]', 26)],
            )

    assert editor.target == mapping
