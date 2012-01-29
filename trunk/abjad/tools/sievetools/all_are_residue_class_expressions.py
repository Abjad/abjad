from abjad.tools.sievetools.ResidueClassExpression import ResidueClassExpression


def all_are_residue_class_expressions(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad residue class expressions::

        abjad> from abjad.tools import sievetools

    ::

        abjad> sieve = sievetools.ResidueClass(3, 0) | sievetools.ResidueClass(2, 0)

    ::

        abjad> sieve
        {ResidueClass(2, 0) | ResidueClass(3, 0)}

    ::

        abjad> sievetools.all_are_residue_class_expressions([sieve])
        True

    True when `expr` is an empty sequence::

        abjad> sievetools.all_are_residue_class_expressions([])
        True

    Otherwise false::

        abjad> sievetools.all_are_residue_class_expressions('foo')
        False

    Return boolean.
    '''

    return all([isinstance(x, ResidueClassExpression) for x in expr])
