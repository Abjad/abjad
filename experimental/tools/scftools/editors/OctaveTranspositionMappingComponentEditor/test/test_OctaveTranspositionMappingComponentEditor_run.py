from abjad.tools import pitchtools
from experimental import *


def test_OctaveTranspositionMappingComponentEditor_run_01():

    editor = scftools.editors.OctaveTranspositionMappingComponentEditor()
    editor.run(user_input='source [A0, C8] target -18 q')

    assert editor.target == pitchtools.OctaveTranspositionMappingComponent('[A0, C8]', -18)
