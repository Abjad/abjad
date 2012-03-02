from abjad.tools import sequencetools


def test_sequencetools_CyclicTree__repr_with_tools_package_01():

    cyclic_tree = sequencetools.CyclicTree([[1, 2, 3], [4, 5]])

    assert cyclic_tree._repr_with_tools_package == 'sequencetools.CyclicTree([[1, 2, 3], [4, 5]])'
