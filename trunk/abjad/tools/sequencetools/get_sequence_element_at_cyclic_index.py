from abjad.tools import mathtools


def get_sequence_element_at_cyclic_index(sequence, index):
    r'''.. versionadded:: 2.0

    Get `sequence` element at nonnegative cyclic `index`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> for index in range(10):
        ...     print '%s\t%s' % (index, sequencetools.get_sequence_element_at_cyclic_index('string', index))
        ...
        0  s
        1  t
        2  r
        3  i
        4  n
        5  g
        6  s
        7  t
        8  r
        9  i

    Get `sequence` element at negative cyclic `index`::

        abjad> for index in range(1, 11):
        ...     print '%s\t%s' % (-index, sequencetools.get_sequence_element_at_cyclic_index('string', -index))
        ...
        -1    g
        -2    n
        -3    i
        -4    r
        -5    t
        -6    s
        -7    g
        -8    n
        -9    i
        -10   r

    Return reference to `sequence` element.
    '''

    return sequence[mathtools.sign(index) * (abs(index) % len(sequence))]
