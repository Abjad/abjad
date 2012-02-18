def all_are_pairs(expr):
    '''True when `expr` is a sequence whose members are all sequences of length 2::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.all_are_pairs([(1, 2), (3, 4), (5, 6), (7, 8)])
        True

    True when `expr` is an empty sequence::

        abjad> sequencetools.all_are_pairs([])
        True

    False otherwise::

        abjad> sequencetools.all_are_pairs('foo')
        False

    Return boolean.
    '''

    try:
        return all([len(x) == 2 for x in expr])
    except TypeError:
        return False
