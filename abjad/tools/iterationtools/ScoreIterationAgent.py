# -*- encoding: utf-8 -*-
from abjad.tools import scoretools


class ScoreIterationAgent(object):
    r'''A wrapper around the Abjad score iterators.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client):
        self._client = client

    ### SPECIAL METHODS ###

    def __repr__(self):
        '''Interpreter representation of score iteration agent.

        ..  container:: example

            ::

                >>> staff = Staff("c'4 e'4 d'4 f'4")
                >>> iterate(staff[2:])
                ScoreIterationAgent(SliceSelection(Note("d'4"), Note("f'4")))

        Returns string.
        '''
        return '{}({})'.format(
            type(self).__name__,
            self._client,
            )

    ### PUBLIC METHODS ###

    def by_class(
        self,
        component_classes=None,
        reverse=False,
        start=0,
        stop=None,
        ):
        r'''Iterate components forward in `expr`.

        ::

            >>> staff = Staff()
            >>> staff.append(Measure((2, 8), "c'8 d'8"))
            >>> staff.append(Measure((2, 8), "e'8 f'8"))
            >>> staff.append(Measure((2, 8), "g'8 a'8"))

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 2/8
                    c'8
                    d'8
                }
                {
                    e'8
                    f'8
                }
                {
                    g'8
                    a'8
                }
            }

        ::

            >>> for note in iterate(staff).by_class(Note):
            ...     note
            ...
            Note("c'8")
            Note("d'8")
            Note("e'8")
            Note("f'8")
            Note("g'8")
            Note("a'8")

        Use optional `start` and `stop` keyword parameters to control
        start and stop indices of iteration:

        ::

            >>> for note in iterate(staff).by_class(Note):
            ...     note
            ...
            Note("f'8")
            Note("g'8")
            Note("a'8")

        ::

            >>> for note in iterate(staff).by_class(
            ...     Note, start=0, stop=3):
            ...     note
            ...
            Note("c'8")
            Note("d'8")
            Note("e'8")

        ::

            >>> for note in iterate(staff).by_class(
            ...     Note, start=2, stop=4):
            ...     note
            ...
            Note("e'8")
            Note("f'8")

        Yield right-to-left notes in `expr`:

        ::

            >>> staff = Staff()
            >>> staff.append(Measure((2, 8), "c'8 d'8"))
            >>> staff.append(Measure((2, 8), "e'8 f'8"))
            >>> staff.append(Measure((2, 8), "g'8 a'8"))

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 2/8
                    c'8
                    d'8
                }
                {
                    e'8
                    f'8
                }
                {
                    g'8
                    a'8
                }
            }

        ::

            >>> for note in iterate(staff).by_class(
            ...     Note, reverse=True):
            ...     note
            ...
            Note("a'8")
            Note("g'8")
            Note("f'8")
            Note("e'8")
            Note("d'8")
            Note("c'8")

        Use optional `start` and `stop` keyword parameters to control
        indices of iteration:

        ::

            >>> for note in iterate(staff).by_class(
            ...     Note, reverse=True, start=3):
            ...     note
            ...
            Note("e'8")
            Note("d'8")
            Note("c'8")

        ::

            >>> for note in iterate(staff).by_class(
            ...     Note, reverse=True, start=0, stop=3):
            ...     note
            ...
            Note("a'8")
            Note("g'8")
            Note("f'8")

        ::

            >>> for note in iterate(staff).by_class(
            ...     Note, reverse=True, start=2, stop=4):
            ...     note
            ...
            Note("f'8")
            Note("e'8")

        Iterates across different logical voices.

        Returns generator.
        '''
        from abjad.tools import spannertools

        component_classes = component_classes or scoretools.Component

        def component_iterator(expr, component_class, reverse=False):
            if isinstance(expr, component_class):
                yield expr
            if isinstance(expr, (list, tuple, spannertools.Spanner)) or \
                hasattr(expr, '_music'):
                if hasattr(expr, '_music'):
                    expr = expr._music
                if reverse:
                    expr = reversed(expr)
                for m in expr:
                    for x in component_iterator(
                        m, component_class, reverse=reverse):
                        yield x

        def subrange(iter, start=0, stop=None):
            # if start<0, then 'stop-start' gives a funny result
            # don not have to check stop>=start
            # because xrange(stop-start) already handles that
            assert 0 <= start

            try:
                # skip the first few elements, up to 'start' of them:
                for i in xrange(start):
                    # no yield to swallow the results
                    iter.next()

                # now generate (stop-start) elements
                # (or all elements if stop is none)
                if stop is None:
                    for x in iter:
                        yield x
                else:
                    for i in xrange(stop - start):
                        yield iter.next()
            except StopIteration:
                # this happens if we exhaust the list before
                # we generate a total of 'stop' elements
                pass

        return subrange(
            component_iterator(
                self._client,
                component_classes,
                reverse=reverse),
            start,
            stop,
            )
