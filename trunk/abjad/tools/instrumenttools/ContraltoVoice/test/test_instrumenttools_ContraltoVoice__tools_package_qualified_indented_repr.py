from abjad import *


def test_instrumenttools_ContraltoVoice__tools_package_qualified_indented_repr_01():

    voice = instrumenttools.ContraltoVoice()

    assert voice._tools_package_qualified_indented_repr == 'instrumenttools.ContraltoVoice()'

