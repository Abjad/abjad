from abjad import *


def test_instrumenttools_MezzoSopranoVoice__tools_package_qualified_indented_repr_01():

    voice = instrumenttools.MezzoSopranoVoice()

    assert voice._tools_package_qualified_indented_repr == 'instrumenttools.MezzoSopranoVoice()'
