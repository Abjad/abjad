from abjad.tools import sequencetools


def test_sequencetools_CyclicTree__repr_with_tools_package_01():

    cyclic_tree = sequencetools.CyclicTree([[1, 2, 3], [4, 5]])

    assert cyclic_tree._tools_package_qualified_repr == 'sequencetools.CyclicTree([[1, 2, 3], [4, 5]])'
