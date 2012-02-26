def all_are_pairs_of_types(expr, first_type, second_type):
    '''True when `expr` is a sequence whose members are all sequences of length 2,
    and where the first member of each pair is an instance of `first_type` and
    where the second member of each pair is an instance of `second_type`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.all_are_pairs_of_types([(1., 'a'), (2.1, 'b'), (3.45, 'c')], float, str)
        True

    True when `expr` is an empty sequence::

        abjad> sequencetools.all_are_pairs_of_types([], float, str)
        True

    False otherwise::

        abjad> sequencetools.all_are_pairs_of_types('foo', float, str)
        False

    Return boolean.
    '''
    
    try:
        return all([len(x) == 2 and \
            isinstance(x[0], first_type) and \
            isinstance(x[1], second_type) for x in expr])
    except TypeError:
        return False
