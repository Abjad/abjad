from abjad.tools.spannertools.Spanner import Spanner


def all_are_spanners(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad spanners::

        abjad> voice = Voice("c'8 d'8 e'8 f'8")
        abjad> spanner = spannertools.BeamSpanner(voice[:2])

    ::

        abjad> spannertools.all_are_spanners([spanner])
        True

    True when `expr` is an empty sequence::

        abjad> spannertools.all_are_spanners([])
        True

    Otherwise false::

        abjad> spannertools.all_are_spanners('foo')
        False

    Return boolean.
    '''

    return all([isinstance(x, Spanner) for x in expr])
