from abjad import *


def test_instrumenttools_BaritoneVoice__tools_package_qualified_indented_repr_01():

    voice = instrumenttools.BaritoneVoice()

    assert voice._tools_package_qualified_indented_repr == 'instrumenttools.BaritoneVoice()'
