# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_OctaveTranspositionMappingComponentEditor_run_01():

    editor = scoremanager.editors.OctaveTranspositionMappingComponentEditor()
    string = 'source [A0, C8] target -18 q'
    editor._run(pending_user_input=string)

    assert editor.target == \
        pitchtools.OctaveTranspositionMappingComponent('[A0, C8]', -18)
