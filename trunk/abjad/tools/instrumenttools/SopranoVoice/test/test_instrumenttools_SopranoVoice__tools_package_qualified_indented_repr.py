from abjad import *


def test_instrumenttools_SopranoVoice__tools_package_qualified_indented_repr_01():

    voice = instrumenttools.SopranoVoice()

    assert voice._tools_package_qualified_indented_repr == 'instrumenttools.SopranoVoice()'
