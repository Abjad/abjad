# -*- coding: utf-8 -*-
from __future__ import print_function
import collections
from abjad.tools import abctools
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate


class IterationAgent(abctools.AbjadObject):
    r'''Iteration agent.

    ..  container:: example

        **Example.** Iterates components:

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4
                e'4
                d'4
                f'4
            }

        ::

            >>> for component in iterate(staff).by_class():
            ...     component
            Staff("c'4 e'4 d'4 f'4")
            Note("c'4")
            Note("e'4")
            Note("d'4")
            Note("f'4")

    ..  container:: example

        **Example 2.** Iterates leaves:

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4
                e'4
                d'4
                f'4
            }

        ::

            >>> for leaf in iterate(staff).by_leaf():
            ...     leaf
            Note("c'4")
            Note("e'4")
            Note("d'4")
            Note("f'4")

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client=None):
        self._client = client

    ### PRIVATE METHODS ###

    def _by_components_and_grace_containers(self, prototype=None):
        prototype = prototype or scoretools.Leaf
        if getattr(self._client, '_grace', None) is not None:
            for component in self._client._grace:
                for x in iterate(component)._by_components_and_grace_containers(
                    prototype,
                    ):
                    yield x
        if isinstance(self._client, prototype):
            yield self._client
        if getattr(self._client, '_after_grace', None) is not None:
            for component in self._client._after_grace:
                for x in iterate(component)._by_components_and_grace_containers(
                    prototype,
                    ):
                    yield x
        if isinstance(self._client, (list, tuple)):
            for component in self._client:
                for x in iterate(component)._by_components_and_grace_containers(
                    prototype,
                    ):
                    yield x
        if hasattr(self._client, '_music'):
            for component in self._client._music:
                for x in iterate(component)._by_components_and_grace_containers(
                    prototype,
                    ):
                    yield x

    ### PUBLIC METHODS ###

    def by_class(
        self,
        prototype=None,
        pitched=None,
        reverse=False,
        start=0,
        stop=None,
        with_grace_notes=False,
        ):
        r'''Iterates by class.

        ..  container:: example

            **Example 1.** Iterates notes:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 8), "c'8 d'8"))
                >>> staff.append(Measure((2, 8), "e'8 f'8"))
                >>> staff.append(Measure((2, 8), "g'8 a'8"))
                >>> show(staff) # doctest: +SKIP

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

                >>> for note in iterate(staff).by_class(prototype=Note):
                ...     note
                ...
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Note("g'8")
                Note("a'8")

        ..  container:: example

            **Example 2.** Constrains iteration by index:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 8), "c'8 d'8"))
                >>> staff.append(Measure((2, 8), "e'8 f'8"))
                >>> staff.append(Measure((2, 8), "g'8 a'8"))
                >>> show(staff) # doctest: +SKIP

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
                ...     prototype=Note,
                ...     start=0,
                ...     stop=3,
                ...     ):
                ...     note
                ...
                Note("c'8")
                Note("d'8")
                Note("e'8")

            ::

                >>> for note in iterate(staff).by_class(
                ...     prototype=Note,
                ...     start=2,
                ...     stop=4,
                ...     ):
                ...     note
                ...
                Note("e'8")
                Note("f'8")

        ..  container:: example

            **Example 3.** Reverses direction of iteration:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 8), "c'8 d'8"))
                >>> staff.append(Measure((2, 8), "e'8 f'8"))
                >>> staff.append(Measure((2, 8), "g'8 a'8"))
                >>> show(staff) # doctest: +SKIP

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
                ...     prototype=Note,
                ...     reverse=True,
                ...     ):
                ...     note
                ...
                Note("a'8")
                Note("g'8")
                Note("f'8")
                Note("e'8")
                Note("d'8")
                Note("c'8")

        ..  container:: example

            **Example 5.** Iterates with grace notes:

            ::

                >>> voice = Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> grace_notes = [Note("cf''16"), Note("bf'16")]
                >>> grace = scoretools.GraceContainer(
                ...     grace_notes,
                ...     kind='grace',
                ...     )
                >>> attach(grace, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'8 [
                    \grace {
                        cf''16
                        bf'16
                    }
                    d'8
                    e'8
                    f'8 ]
                }

            ::

                >>> for component in iterate(voice).by_class(
                ...     with_grace_notes=True,
                ...     ):
                ...     component
                Voice("c'8 d'8 e'8 f'8")
                Note("c'8")
                Note("cf''16")
                Note("bf'16")
                Note("d'8")
                Note("e'8")
                Note("f'8")

        ..  container:: example

            **Example 5.** Iterates with both grace notes and after grace
            notes:

            ::

                >>> voice = Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> grace_notes = [Note("cf''16"), Note("bf'16")]
                >>> grace = scoretools.GraceContainer(
                ...     grace_notes,
                ...     kind='grace',
                ...     )
                >>> attach(grace, voice[1])
                >>> after_grace_notes = [Note("af'16"), Note("gf'16")]
                >>> after_grace = scoretools.GraceContainer(
                ...     after_grace_notes,
                ...     kind='after')
                >>> attach(after_grace, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'8 [
                    \grace {
                        cf''16
                        bf'16
                    }
                    \afterGrace
                    d'8
                    {
                        af'16
                        gf'16
                    }
                    e'8
                    f'8 ]
                }

            ::

                >>> for leaf in iterate(voice).by_class(with_grace_notes=True):
                ...     leaf
                ...
                Voice("c'8 d'8 e'8 f'8")
                Note("c'8")
                Note("cf''16")
                Note("bf'16")
                Note("d'8")
                Note("af'16")
                Note("gf'16")
                Note("e'8")
                Note("f'8")

        ..  container:: example

            **Example 6.** Iterates pitched components:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                >>> staff.append(Measure((2, 8), "af'8 r8"))
                >>> staff.append(Measure((2, 8), "r8 gf'8"))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 2/8
                        <c' bf'>8
                        <g' a'>8
                    }
                    {
                        af'8
                        r8
                    }
                    {
                        r8
                        gf'8
                    }
                }

            ::

                >>> for leaf in iterate(staff).by_class(pitched=True):
                ...     leaf
                ...
                Chord("<c' bf'>8")
                Chord("<g' a'>8")
                Note("af'8")
                Note("gf'8")

        ..  container:: example

            **Example 7.** Iterates nonpitched components:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                >>> staff.append(Measure((2, 8), "af'8 r8"))
                >>> staff.append(Measure((2, 8), "r8 gf'8"))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 2/8
                        <c' bf'>8
                        <g' a'>8
                    }
                    {
                        af'8
                        r8
                    }
                    {
                        r8
                        gf'8
                    }
                }

            ::

                >>> for leaf in iterate(staff).by_class(pitched=False):
                ...     leaf
                ...
                <Staff{3}>
                Measure((2, 8), "<c' bf'>8 <g' a'>8")
                Measure((2, 8), "af'8 r8")
                Rest('r8')
                Measure((2, 8), "r8 gf'8")
                Rest('r8')

        Returns generator.
        '''
        prototype = prototype or scoretools.Component
        if with_grace_notes:
            if reverse:
                message = 'reverse grace iteration not yet implemented.'
                raise NotImplementedError(message)
            if not start == 0 or stop is not None:
                message = 'indexed grace iteration not yet implemented.'
                raise NotImplementedError(message)
            return self._by_components_and_grace_containers(
                prototype=prototype
                )
        pitched_prototype = (scoretools.Note, scoretools.Chord)

        def component_iterator(expr, prototype, reverse=False):
            if isinstance(expr, prototype):
                if pitched is None:
                    yield expr
                elif pitched is True and isinstance(expr, pitched_prototype):
                    yield expr
                elif (
                    pitched is not True and not
                    isinstance(expr, pitched_prototype)
                    ):
                    yield expr
            if (
                isinstance(expr, (list, tuple, spannertools.Spanner)) or
                hasattr(expr, '_music')
                ):
                if hasattr(expr, '_music'):
                    expr = expr._music
                if reverse:
                    expr = reversed(expr)
                for component in expr:
                    for x in component_iterator(
                        component,
                        prototype,
                        reverse=reverse,
                        ):
                        yield x

        def subrange(iter, start=0, stop=None):
            # if start<0, then 'stop-start' gives a funny result
            # don not have to check stop>=start
            # because range(stop-start) already handles that
            assert 0 <= start
            try:
                # skip the first few elements, up to 'start' of them:
                for i in range(start):
                    # no yield to swallow the results
                    next(iter)
                # now generate (stop-start) elements
                # (or all elements if stop is none)
                if stop is None:
                    for x in iter:
                        yield x
                else:
                    for i in range(stop - start):
                        yield next(iter)
            except StopIteration:
                # this happens if we exhaust the list before
                # we generate a total of 'stop' elements
                pass
        return subrange(
            component_iterator(
                self._client,
                prototype,
                reverse=reverse
                ),
            start,
            stop,
            )

    def by_leaf(
        self,
        prototype=None,
        pitched=None,
        reverse=False,
        start=0,
        stop=None,
        with_grace_notes=False,
        ):
        r'''Iterates by leaf.

        ..  container:: example

            **Example 1.** Iterates leaves:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                >>> staff.append(Measure((2, 8), "af'8 r8"))
                >>> staff.append(Measure((2, 8), "r8 gf'8"))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 2/8
                        <c' bf'>8
                        <g' a'>8
                    }
                    {
                        af'8
                        r8
                    }
                    {
                        r8
                        gf'8
                    }
                }

            ::

                >>> for leaf in iterate(staff).by_leaf():
                ...     leaf
                ...
                Chord("<c' bf'>8")
                Chord("<g' a'>8")
                Note("af'8")
                Rest('r8')
                Rest('r8')
                Note("gf'8")

        ..  container:: example

            **Example 2.** Constrains iteration by index:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                >>> staff.append(Measure((2, 8), "af'8 r8"))
                >>> staff.append(Measure((2, 8), "r8 gf'8"))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 2/8
                        <c' bf'>8
                        <g' a'>8
                    }
                    {
                        af'8
                        r8
                    }
                    {
                        r8
                        gf'8
                    }
                }

            ::

                >>> for leaf in iterate(staff).by_leaf(start=0, stop=3):
                ...     leaf
                ...
                Chord("<c' bf'>8")
                Chord("<g' a'>8")
                Note("af'8")

            ::

                >>> for leaf in iterate(staff).by_leaf(start=2, stop=4):
                ...     leaf
                ...
                Note("af'8")
                Rest('r8')

        ..  container:: example

            **Example 3.** Reverses direction of iteration:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                >>> staff.append(Measure((2, 8), "af'8 r8"))
                >>> staff.append(Measure((2, 8), "r8 gf'8"))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 2/8
                        <c' bf'>8
                        <g' a'>8
                    }
                    {
                        af'8
                        r8
                    }
                    {
                        r8
                        gf'8
                    }
                }

            ::

                >>> for leaf in iterate(staff).by_leaf(reverse=True):
                ...     leaf
                ...
                Note("gf'8")
                Rest('r8')
                Rest('r8')
                Note("af'8")
                Chord("<g' a'>8")
                Chord("<c' bf'>8")

        ..  container:: example

            **Example 4.** Iterates with grace notes:

            ::

                >>> voice = Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> grace_notes = [Note("cf''16"), Note("bf'16")]
                >>> grace = scoretools.GraceContainer(
                ...     grace_notes,
                ...     kind='grace',
                ...     )
                >>> attach(grace, voice[1])
                >>> after_grace_notes = [Note("af'16"), Note("gf'16")]
                >>> after_grace = scoretools.GraceContainer(
                ...     after_grace_notes,
                ...     kind='after')
                >>> attach(after_grace, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'8 [
                    \grace {
                        cf''16
                        bf'16
                    }
                    \afterGrace
                    d'8
                    {
                        af'16
                        gf'16
                    }
                    e'8
                    f'8 ]
                }

            ::

                >>> for leaf in iterate(voice).by_leaf(with_grace_notes=True):
                ...     leaf
                ...
                Note("c'8")
                Note("cf''16")
                Note("bf'16")
                Note("d'8")
                Note("af'16")
                Note("gf'16")
                Note("e'8")
                Note("f'8")

        ..  container:: example

            **Example 5.** Iterates pitched leaves:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                >>> staff.append(Measure((2, 8), "af'8 r8"))
                >>> staff.append(Measure((2, 8), "r8 gf'8"))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 2/8
                        <c' bf'>8
                        <g' a'>8
                    }
                    {
                        af'8
                        r8
                    }
                    {
                        r8
                        gf'8
                    }
                }

            ::

                >>> for leaf in iterate(staff).by_leaf(pitched=True):
                ...     leaf
                ...
                Chord("<c' bf'>8")
                Chord("<g' a'>8")
                Note("af'8")
                Note("gf'8")

        ..  container:: example

            **Example 6.** Iterates nonpitched leaves:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                >>> staff.append(Measure((2, 8), "af'8 r8"))
                >>> staff.append(Measure((2, 8), "r8 gf'8"))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 2/8
                        <c' bf'>8
                        <g' a'>8
                    }
                    {
                        af'8
                        r8
                    }
                    {
                        r8
                        gf'8
                    }
                }

            ::

                >>> for leaf in iterate(staff).by_leaf(pitched=False):
                ...     leaf
                ...
                Rest('r8')
                Rest('r8')

        Returns generator.
        '''
        prototype = prototype or scoretools.Leaf
        return self.by_class(
            prototype=prototype,
            pitched=pitched,
            reverse=reverse,
            start=start,
            stop=stop,
            with_grace_notes=with_grace_notes,
            )

    def by_leaf_pair(self):
        r'''Iterates by leaf pair.

        ..  container:: example

            **Example 1.** Iterates leaf pairs:

            ::

                >>> score = Score([])
                >>> score.append(Staff("c'8 d'8 e'8 f'8 g'4"))
                >>> score.append(Staff("c4 a,4 g,4"))
                >>> attach(Clef('bass'), score[1])
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        c'8
                        d'8
                        e'8
                        f'8
                        g'4
                    }
                    \new Staff {
                        \clef "bass"
                        c4
                        a,4
                        g,4
                    }
                >>

            ::

                >>> for leaf_pair in iterate(score).by_leaf_pair():
                ...        leaf_pair
                (Note("c'8"), Note('c4'))
                (Note("c'8"), Note("d'8"))
                (Note('c4'), Note("d'8"))
                (Note("d'8"), Note("e'8"))
                (Note("d'8"), Note('a,4'))
                (Note('c4'), Note("e'8"))
                (Note('c4'), Note('a,4'))
                (Note("e'8"), Note('a,4'))
                (Note("e'8"), Note("f'8"))
                (Note('a,4'), Note("f'8"))
                (Note("f'8"), Note("g'4"))
                (Note("f'8"), Note('g,4'))
                (Note('a,4'), Note("g'4"))
                (Note('a,4'), Note('g,4'))
                (Note("g'4"), Note('g,4'))

        Iterates leaf pairs left-to-right and top-to-bottom.

        Returns generator.
        '''
        vertical_moments = self.by_vertical_moment()
        for moment_1, moment_2 in \
            sequencetools.iterate_sequence_nwise(vertical_moments):
            for pair in sequencetools.yield_all_unordered_pairs_of_sequence(
                moment_1.start_leaves):
                yield pair
            pairs = sequencetools.yield_all_pairs_between_sequences(
                moment_1.leaves, moment_2.start_leaves)
            for pair in pairs:
                yield pair
        else:
            for pair in sequencetools.yield_all_unordered_pairs_of_sequence(
                moment_2.start_leaves):
                yield pair

    def by_logical_tie(
        self,
        nontrivial=False,
        pitched=False,
        reverse=False,
        parentage_mask=None,
        with_grace_notes=False,
        ):
        r'''Iterates by logical tie.

        ..  container:: example

            **Example 1.** Iterates logical ties:

            ::

                >>> staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4 ~
                    \times 2/3 {
                        c'16
                        d'8
                    }
                    e'8
                    f'4 ~
                    f'16
                }

            ::

                >>> for logical_tie in iterate(staff).by_logical_tie():
                ...     logical_tie
                ...
                LogicalTie([Note("c'4"), Note("c'16")])
                LogicalTie([Note("d'8")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("f'4"), Note("f'16")])

        ..  container:: example

            **Example 2.** Reverses direction of iteration:

            ::

                >>> staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4 ~
                    \times 2/3 {
                        c'16
                        d'8
                    }
                    e'8
                    f'4 ~
                    f'16
                }

            ::

                >>> for logical_tie in iterate(staff).by_logical_tie(reverse=True):
                ...     logical_tie
                ...
                LogicalTie([Note("f'4"), Note("f'16")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("d'8")])
                LogicalTie([Note("c'4"), Note("c'16")])

        ..  container:: example

            **Example 3.** Iterates pitched logical ties:

            ::

                >>> staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4 ~
                    \times 2/3 {
                        c'16
                        d'8
                    }
                    e'8
                    f'4 ~
                    f'16
                }

            ::

                >>> for logical_tie in iterate(staff).by_logical_tie(pitched=True):
                ...     logical_tie
                ...
                LogicalTie([Note("c'4"), Note("c'16")])
                LogicalTie([Note("d'8")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("f'4"), Note("f'16")])

        ..  container:: example

            **Example 4.** Iterates nontrivial logical ties:

            ::

                >>> staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4 ~
                    \times 2/3 {
                        c'16
                        d'8
                    }
                    e'8
                    f'4 ~
                    f'16
                }

            ::

                >>> for logical_tie in iterate(staff).by_logical_tie(nontrivial=True):
                ...     logical_tie
                ...
                LogicalTie([Note("c'4"), Note("c'16")])
                LogicalTie([Note("f'4"), Note("f'16")])

        ..  container:: example

            **Example 5.** Iterates logical ties masked by parentage.

            ..  note::

                When iterating logical ties in a container, the yielded logical
                ties may contain leaves outside that container's parentage. By
                specifying a parentage mask, composers can constrain the
                contents of the yielded logical ties to only those leaves
                actually within the parentage of the container under iteration.

            ::

                >>> staff = Staff("{ c'1 ~ } { c'2 d'2 ~ } { d'1 }")
                >>> for logical_tie in iterate(staff[1]).by_logical_tie():
                ...     logical_tie
                ...
                LogicalTie([Note("c'1"), Note("c'2")])
                LogicalTie([Note("d'2"), Note("d'1")])

            ::

                >>> for logical_tie in iterate(staff[1]).by_logical_tie(
                ...     parentage_mask=staff[1]):
                ...     logical_tie
                ...
                LogicalTie([Note("c'2")])
                LogicalTie([Note("d'2")])

        ..  container:: example

            **Example 6.** Iterates logical ties with grace notes:

            ::

                >>> voice = Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> grace_notes = [Note("cf''16"), Note("bf'16")]
                >>> grace = scoretools.GraceContainer(
                ...     grace_notes,
                ...     kind='grace',
                ...     )
                >>> attach(grace, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'8 [
                    \grace {
                        cf''16
                        bf'16
                    }
                    d'8
                    e'8
                    f'8 ]
                }

            ::

                >>> for logical_tie in iterate(voice).by_logical_tie(
                ...     with_grace_notes=True,
                ...     ):
                ...     logical_tie
                LogicalTie([Note("c'8")])
                LogicalTie([Note("cf''16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Note("d'8")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("f'8")])

        ..  container:: example

            **Example 7.** Iterates logical ties with after grace notes:

            ::

                >>> voice = Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> after_grace_notes = [Note("af'16"), Note("gf'16")]
                >>> after_grace = scoretools.GraceContainer(
                ...     after_grace_notes,
                ...     kind='after')
                >>> attach(after_grace, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'8 [
                    \afterGrace
                    d'8
                    {
                        af'16
                        gf'16
                    }
                    e'8
                    f'8 ]
                }

            ::

                >>> for logical_tie in iterate(voice).by_logical_tie(
                ...     with_grace_notes=True,
                ...     ):
                ...     logical_tie
                LogicalTie([Note("c'8")])
                LogicalTie([Note("d'8")])
                LogicalTie([Note("af'16")])
                LogicalTie([Note("gf'16")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("f'8")])

        ..  container:: example

            **Example 8.** Iterates logical ties with both grace notes and
            after grace notes:

            ::

                >>> voice = Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> grace_notes = [Note("cf''16"), Note("bf'16")]
                >>> grace = scoretools.GraceContainer(
                ...     grace_notes,
                ...     kind='grace',
                ...     )
                >>> attach(grace, voice[1])
                >>> after_grace_notes = [Note("af'16"), Note("gf'16")]
                >>> after_grace = scoretools.GraceContainer(
                ...     after_grace_notes,
                ...     kind='after')
                >>> attach(after_grace, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'8 [
                    \grace {
                        cf''16
                        bf'16
                    }
                    \afterGrace
                    d'8
                    {
                        af'16
                        gf'16
                    }
                    e'8
                    f'8 ]
                }

            ::

                >>> for logical_tie in iterate(voice).by_logical_tie(
                ...     with_grace_notes=True,
                ...     ):
                ...     logical_tie
                ...
                LogicalTie([Note("c'8")])
                LogicalTie([Note("cf''16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Note("d'8")])
                LogicalTie([Note("af'16")])
                LogicalTie([Note("gf'16")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("f'8")])

        Returns generator.
        '''
        from abjad.tools import selectiontools
        nontrivial = bool(nontrivial)
        prototype = scoretools.Leaf
        if pitched:
            prototype = (scoretools.Chord, scoretools.Note)
        leaf, yielded = None, False
        if not reverse:
            for leaf in self.by_class(
                prototype=prototype,
                with_grace_notes=with_grace_notes,
                ):
                yielded = False
                tie_spanners = leaf._get_spanners(spannertools.Tie)
                if not tie_spanners or \
                    tuple(tie_spanners)[0]._is_my_last_leaf(leaf):
                    logical_tie = leaf._get_logical_tie()
                    if parentage_mask:
                        logical_tie = selectiontools.LogicalTie(
                            x for x in logical_tie
                            if parentage_mask in x._get_parentage()
                            )
                        if not logical_tie:
                            continue
                    if not nontrivial or not logical_tie.is_trivial:
                        yielded = True
                        yield logical_tie
            if leaf is not None and not yielded:
                if tie_spanners and \
                    tuple(tie_spanners)[0]._is_my_first_leaf(leaf):
                    logical_tie = leaf._get_logical_tie()
                    if parentage_mask:
                        logical_tie = selectiontools.LogicalTie(
                            x for x in logical_tie
                            if parentage_mask in x._get_parentage()
                            )
                        if not logical_tie:
                            return
                    if not nontrivial or not logical_tie.is_trivial:
                        yield logical_tie
        else:
            for leaf in self.by_class(
                prototype,
                reverse=True,
                with_grace_notes=with_grace_notes,
                ):
                yielded = False
                tie_spanners = leaf._get_spanners(spannertools.Tie)
                if not(tie_spanners) or \
                    tuple(tie_spanners)[0]._is_my_first_leaf(leaf):
                    logical_tie = leaf._get_logical_tie()
                    if parentage_mask:
                        logical_tie = selectiontools.LogicalTie(
                            x for x in logical_tie
                            if parentage_mask in x._get_parentage()
                            )
                        if not logical_tie:
                            continue
                    if not nontrivial or not logical_tie.is_trivial:
                        yielded = True
                        yield logical_tie
            if leaf is not None and not yielded:
                if tie_spanners and \
                    tuple(tie_spanners)[0]._is_my_last_leaf(leaf):
                    logical_tie = leaf._get_logical_tie()
                    if parentage_mask:
                        logical_tie = selectiontools.LogicalTie(
                            x for x in logical_tie
                            if parentage_mask in x._get_parentage()
                            )
                        if not logical_tie:
                            return
                    if not nontrivial or not logical_tie.is_trivial:
                        yield logical_tie

    def by_logical_voice(
        self,
        prototype,
        logical_voice,
        reverse=False,
        ):
        r'''Iterates by logical voice.

        ..  container:: example

            **Example 1.** Iterates notes in logical voice 1:

            ::

                >>> container_1 = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])
                >>> container_1.is_simultaneous = True
                >>> container_1[0].name = 'voice 1'
                >>> override(container_1[0]).stem.direction = Down
                >>> container_1[1].name = 'voice 2'
                >>> container_2 = Container([Voice("g'8 a'8"), Voice("b'8 c''8")])
                >>> container_2.is_simultaneous = True
                >>> container_2[0].name = 'voice 1'
                >>> override(container_2[0]).stem.direction = Down
                >>> container_2[1].name = 'voice 2'
                >>> staff = Staff([container_1, container_2])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    <<
                        \context Voice = "voice 1" \with {
                            \override Stem.direction = #down
                        } {
                            c'8
                            d'8
                        }
                        \context Voice = "voice 2" {
                            e'8
                            f'8
                        }
                    >>
                    <<
                        \context Voice = "voice 1" \with {
                            \override Stem.direction = #down
                        } {
                            g'8
                            a'8
                        }
                        \context Voice = "voice 2" {
                            b'8
                            c''8
                        }
                    >>
                }

            ::

                >>> selector = select().by_leaf(flatten=True)
                >>> leaves = selector(staff)
                >>> leaf = leaves[0]
                >>> signature = inspect_(leaf).get_parentage().logical_voice
                >>> for note in iterate(staff).by_logical_voice(Note, signature):
                ...     note
                ...
                Note("c'8")
                Note("d'8")
                Note("g'8")
                Note("a'8")

        Returns generator.
        '''
        if isinstance(self._client, prototype) and \
            self._client._get_parentage().logical_voice == \
                logical_voice:
            yield self._client
        if not reverse:
            if isinstance(self._client, (list, tuple)):
                for component in self._client:
                    for x in iterate(component).by_logical_voice(
                        prototype,
                        logical_voice,
                        ):
                        yield x
            if hasattr(self._client, '_music'):
                for component in self._client._music:
                    for x in iterate(component).by_logical_voice(
                        prototype,
                        logical_voice,
                        ):
                        yield x
        else:
            if isinstance(self._client, (list, tuple)):
                for component in reversed(self._client):
                    for x in iterate(component).by_logical_voice(
                        prototype,
                        logical_voice,
                        reverse=True,
                        ):
                        yield x
            if hasattr(self._client, '_music'):
                for component in reversed(self._client._music):
                    for x in iterate(component).by_logical_voice(
                        prototype,
                        logical_voice,
                        reverse=True,
                        ):
                        yield x

    def by_logical_voice_from_component(
        self,
        prototype=None,
        reverse=False,
        ):
        r'''Iterates by logical voice from client.

        ..  container:: example

            **Example 1.** Iterates from first leaf in score:

            ::

                >>> container_1 = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])
                >>> container_1.is_simultaneous = True
                >>> container_1[0].name = 'voice 1'
                >>> override(container_1[0]).stem.direction = Down
                >>> container_1[1].name = 'voice 2'
                >>> container_2 = Container([Voice("g'8 a'8"), Voice("b'8 c''8")])
                >>> container_2.is_simultaneous = True
                >>> container_2[0].name = 'voice 1'
                >>> override(container_2[0]).stem.direction = Down
                >>> container_2[1].name = 'voice 2'
                >>> staff = Staff([container_1, container_2])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    <<
                        \context Voice = "voice 1" \with {
                            \override Stem.direction = #down
                        } {
                            c'8
                            d'8
                        }
                        \context Voice = "voice 2" {
                            e'8
                            f'8
                        }
                    >>
                    <<
                        \context Voice = "voice 1" \with {
                            \override Stem.direction = #down
                        } {
                            g'8
                            a'8
                        }
                        \context Voice = "voice 2" {
                            b'8
                            c''8
                        }
                    >>
                }

            ::

                >>> selector = select().by_leaf(flatten=True)
                >>> leaves = selector(staff)
                >>> leaf = leaves[0]
                >>> for x in iterate(leaf).by_logical_voice_from_component(Note):
                ...     x
                ...
                Note("c'8")
                Note("d'8")
                Note("g'8")
                Note("a'8")

        ..  container:: example

            **Example 2.** Iterates from second leaf in score:

            ::

                >>> container_1 = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])
                >>> container_1.is_simultaneous = True
                >>> container_1[0].name = 'voice 1'
                >>> override(container_1[0]).stem.direction = Down
                >>> container_1[1].name = 'voice 2'
                >>> container_2 = Container([Voice("g'8 a'8"), Voice("b'8 c''8")])
                >>> container_2.is_simultaneous = True
                >>> container_2[0].name = 'voice 1'
                >>> override(container_2[0]).stem.direction = Down
                >>> container_2[1].name = 'voice 2'
                >>> staff = Staff([container_1, container_2])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    <<
                        \context Voice = "voice 1" \with {
                            \override Stem.direction = #down
                        } {
                            c'8
                            d'8
                        }
                        \context Voice = "voice 2" {
                            e'8
                            f'8
                        }
                    >>
                    <<
                        \context Voice = "voice 1" \with {
                            \override Stem.direction = #down
                        } {
                            g'8
                            a'8
                        }
                        \context Voice = "voice 2" {
                            b'8
                            c''8
                        }
                    >>
                }

            ::

                >>> leaf = leaves[1]
                >>> for x in iterate(leaf).by_logical_voice_from_component(Note):
                ...     x
                ...
                Note("d'8")
                Note("g'8")
                Note("a'8")

        ..  container:: example

            **Example 3.** Iterates all components in logical voice:

            ::

                >>> container_1 = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])
                >>> container_1.is_simultaneous = True
                >>> container_1[0].name = 'voice 1'
                >>> override(container_1[0]).stem.direction = Down
                >>> container_1[1].name = 'voice 2'
                >>> container_2 = Container([Voice("g'8 a'8"), Voice("b'8 c''8")])
                >>> container_2.is_simultaneous = True
                >>> container_2[0].name = 'voice 1'
                >>> override(container_2[0]).stem.direction = Down
                >>> container_2[1].name = 'voice 2'
                >>> staff = Staff([container_1, container_2])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    <<
                        \context Voice = "voice 1" \with {
                            \override Stem.direction = #down
                        } {
                            c'8
                            d'8
                        }
                        \context Voice = "voice 2" {
                            e'8
                            f'8
                        }
                    >>
                    <<
                        \context Voice = "voice 1" \with {
                            \override Stem.direction = #down
                        } {
                            g'8
                            a'8
                        }
                        \context Voice = "voice 2" {
                            b'8
                            c''8
                        }
                    >>
                }

            ::

                >>> leaf = leaves[0]
                >>> for x in iterate(leaf).by_logical_voice_from_component():
                ...     x
                ...
                Note("c'8")
                Voice("c'8 d'8")
                Note("d'8")
                Voice("g'8 a'8")
                Note("g'8")
                Note("a'8")

        ..  container:: example

            **Example 4.** Reverses direction of iteration:

            ::

                >>> container_1 = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])
                >>> container_1.is_simultaneous = True
                >>> container_1[0].name = 'voice 1'
                >>> override(container_1[0]).stem.direction = Down
                >>> container_1[1].name = 'voice 2'
                >>> container_2 = Container([Voice("g'8 a'8"), Voice("b'8 c''8")])
                >>> container_2.is_simultaneous = True
                >>> container_2[0].name = 'voice 1'
                >>> override(container_2[0]).stem.direction = Down
                >>> container_2[1].name = 'voice 2'
                >>> staff = Staff([container_1, container_2])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    <<
                        \context Voice = "voice 1" \with {
                            \override Stem.direction = #down
                        } {
                            c'8
                            d'8
                        }
                        \context Voice = "voice 2" {
                            e'8
                            f'8
                        }
                    >>
                    <<
                        \context Voice = "voice 1" \with {
                            \override Stem.direction = #down
                        } {
                            g'8
                            a'8
                        }
                        \context Voice = "voice 2" {
                            b'8
                            c''8
                        }
                    >>
                }

            ::

                >>> leaf = leaves[-1]
                >>> for x in iterate(leaf).by_logical_voice_from_component(
                ...     Note,
                ...     reverse=True,
                ...     ):
                ...     x
                Note("c''8")
                Note("b'8")
                Note("f'8")
                Note("e'8")

            ::

                >>> leaf = leaves[-1]
                >>> for x in iterate(leaf).by_logical_voice_from_component(
                ...     reverse=True,
                ...     ):
                ...     x
                Note("c''8")
                Voice("b'8 c''8")
                Note("b'8")
                Voice("e'8 f'8")
                Note("f'8")
                Note("e'8")

        Returns generator.
        '''
        # set default class
        if prototype is None:
            prototype = scoretools.Component
        # save logical voice signature of input component
        signature = self._client._get_parentage().logical_voice
        # iterate component depth-first allowing to crawl UP into score
        if not reverse:
            for x in iterate(self._client).depth_first(
                capped=False):
                if isinstance(x, prototype):
                    if x._get_parentage().logical_voice == signature:
                        yield x
        else:
            for x in iterate(self._client).depth_first(
                capped=False, direction=Right):
                if isinstance(x, prototype):
                    if x._get_parentage().logical_voice == signature:
                        yield x

    def by_run(self, prototype=None):
        r'''Iterates by run.

        ..  container:: example

            **Example 1.** Iterates runs of notes and chords at only the
            top level of score:

            ::

                >>> staff = Staff(r"\times 2/3 { c'8 d'8 r8 }")
                >>> staff.append(r"\times 2/3 { r8 <e' g'>8 <f' a'>8 }")
                >>> staff.extend("g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \times 2/3 {
                        c'8
                        d'8
                        r8
                    }
                    \times 2/3 {
                        r8
                        <e' g'>8
                        <f' a'>8
                    }
                    g'8
                    a'8
                    r8
                    r8
                    <b' d''>8
                    <c'' e''>8
                }

            ::

                >>> for group in iterate(staff[:]).by_run((Note, Chord)):
                ...     group
                ...
                (Note("g'8"), Note("a'8"))
                (Chord("<b' d''>8"), Chord("<c'' e''>8"))

        ..  container:: example

            **Example 2.** Iterates runs of notes and chords at all levels of
            score:

            ::

                >>> staff = Staff(r"\times 2/3 { c'8 d'8 r8 }")
                >>> staff.append(r"\times 2/3 { r8 <e' g'>8 <f' a'>8 }")
                >>> staff.extend("g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \times 2/3 {
                        c'8
                        d'8
                        r8
                    }
                    \times 2/3 {
                        r8
                        <e' g'>8
                        <f' a'>8
                    }
                    g'8
                    a'8
                    r8
                    r8
                    <b' d''>8
                    <c'' e''>8
                }

            ::

                >>> leaves = iterate(staff).by_class(scoretools.Leaf)

            ::

                >>> for group in iterate(leaves).by_run((Note, Chord)):
                ...     group
                ...
                (Note("c'8"), Note("d'8"))
                (Chord("<e' g'>8"), Chord("<f' a'>8"), Note("g'8"), Note("a'8"))
                (Chord("<b' d''>8"), Chord("<c'' e''>8"))

        Returns generator.
        '''
        from abjad.tools import selectiontools
        if not isinstance(prototype, collections.Sequence):
            prototype = (prototype,)
        sequence = selectiontools.Selection(self._client)
        current_group = ()
        for group in sequence.group_by(type):
            if isinstance(group[0], prototype):
                current_group = current_group + group
            elif current_group:
                yield current_group
                current_group = ()
        if current_group:
            yield current_group

    def by_semantic_voice(
        self,
        reverse=False,
        start=0,
        stop=None,
        ):
        r'''Iterates by semantic voice.

        ..  todo:: Deprecated. Use ``IterationAgent.by_class(Voice)`` instead.

        ..  container:: example

            **Example 1.** Iterates semantic voices:

            ::

                >>> pairs = [(3, 8), (5, 16), (5, 16)]
                >>> measures = scoretools.make_spacer_skip_measures(pairs)
                >>> time_signature_voice = Voice(measures)
                >>> time_signature_voice.name = 'TimeSignatureVoice'
                >>> time_signature_voice.is_nonsemantic = True
                >>> music_voice = Voice("c'4. d'4 e'16 f'4 g'16")
                >>> music_voice.name = 'MusicVoice'
                >>> staff = Staff([time_signature_voice, music_voice])
                >>> staff.is_simultaneous = True
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff <<
                    \context Voice = "TimeSignatureVoice" {
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 5/16
                            s1 * 5/16
                        }
                        {
                            s1 * 5/16
                        }
                    }
                    \context Voice = "MusicVoice" {
                        c'4.
                        d'4
                        e'16
                        f'4
                        g'16
                    }
                >>

                >>> for voice in iterate(staff).by_semantic_voice():
                ...   voice
                ...
                Voice("c'4. d'4 e'16 f'4 g'16")

        ..  container:: example

            **Example 2.** Reverses direction of iteration:

            ::

                >>> pairs = [(3, 8), (5, 16), (5, 16)]
                >>> measures = scoretools.make_spacer_skip_measures(pairs)
                >>> time_signature_voice = Voice(measures)
                >>> time_signature_voice.name = 'TimeSignatureVoice'
                >>> time_signature_voice.is_nonsemantic = True
                >>> music_voice = Voice("c'4. d'4 e'16 f'4 g'16")
                >>> music_voice.name = 'MusicVoice'
                >>> staff = Staff([time_signature_voice, music_voice])
                >>> staff.is_simultaneous = True
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff <<
                    \context Voice = "TimeSignatureVoice" {
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 5/16
                            s1 * 5/16
                        }
                        {
                            s1 * 5/16
                        }
                    }
                    \context Voice = "MusicVoice" {
                        c'4.
                        d'4
                        e'16
                        f'4
                        g'16
                    }
                >>

            ::

                >>> for voice in iterate(staff).by_semantic_voice(reverse=True):
                ...   voice
                ...
                Voice("c'4. d'4 e'16 f'4 g'16")

        Returns generator.
        '''
        for voice in self.by_class(
            scoretools.Voice,
            reverse=reverse,
            start=start,
            stop=stop,
            ):
            if not voice.is_nonsemantic:
                yield voice

    def by_spanner(
        self,
        prototype=None,
        reverse=False,
        ):
        r'''Iterates by spanner.

        ..  container:: example

            **Example 1.** Iterates spanners:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 f'8 b'8 c''8")
                >>> attach(Slur(), staff[:4])
                >>> attach(Slur(), staff[4:])
                >>> attach(Beam(), staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 [ (
                    d'8
                    e'8
                    f'8 )
                    g'8 (
                    a'8
                    f'8
                    b'8
                    c''8 ] )
                }

            ::

                >>> for spanner in iterate(staff).by_spanner():
                ...     spanner
                ...
                Beam("c'8, d'8, ... [5] ..., b'8, c''8")
                Slur("c'8, d'8, e'8, f'8")
                Slur("g'8, a'8, f'8, b'8, c''8")

        ..  container:: example

            **Example 2.** Reverses direction of iteration:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 f'8 b'8 c''8")
                >>> attach(Slur(), staff[:4])
                >>> attach(Slur(), staff[4:])
                >>> attach(Beam(), staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 [ (
                    d'8
                    e'8
                    f'8 )
                    g'8 (
                    a'8
                    f'8
                    b'8
                    c''8 ] )
                }

            ::

                >>> for spanner in iterate(staff).by_spanner(reverse=True):
                ...     spanner
                ...
                Beam("c'8, d'8, ... [5] ..., b'8, c''8")
                Slur("g'8, a'8, f'8, b'8, c''8")
                Slur("c'8, d'8, e'8, f'8")

        Returns generator.
        '''
        visited_spanners = set()
        for component in self.by_class(reverse=reverse):
            spanners = inspect_(component).get_spanners(prototype=prototype)
            spanners = sorted(spanners,
                key=lambda x: (
                    type(x).__name__,
                    inspect_(x).get_timespan(),
                    ),
                )
            for spanner in spanners:
                if spanner in visited_spanners:
                    continue
                visited_spanners.add(spanner)
                yield spanner

    # TODO: optimize to avoid behind-the-scenes full-score traversal.
    def by_timeline(self, prototype=None, reverse=False):
        r'''Iterates by timeline.

        ..  container:: example

            **Example 1.** Iterates leaves by timeline.

            ::

                >>> score = Score([])
                >>> score.append(Staff("c'4 d'4 e'4 f'4"))
                >>> score.append(Staff("g'8 a'8 b'8 c''8"))
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                    \new Staff {
                        g'8
                        a'8
                        b'8
                        c''8
                    }
                >>

            ::

                >>> for leaf in iterate(score).by_timeline():
                ...     leaf
                ...
                Note("c'4")
                Note("g'8")
                Note("a'8")
                Note("d'4")
                Note("b'8")
                Note("c''8")
                Note("e'4")
                Note("f'4")

        ..  container:: example

            **Example 2.** Reverses direction of iteration:

            ::

                >>> score = Score([])
                >>> score.append(Staff("c'4 d'4 e'4 f'4"))
                >>> score.append(Staff("g'8 a'8 b'8 c''8"))
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                    \new Staff {
                        g'8
                        a'8
                        b'8
                        c''8
                    }
                >>

            ::

                >>> for leaf in iterate(score).by_timeline(reverse=True):
                ...     leaf
                ...
                Note("f'4")
                Note("e'4")
                Note("d'4")
                Note("c''8")
                Note("b'8")
                Note("c'4")
                Note("a'8")
                Note("g'8")

        ..  container:: example

            **Example 3.** Iterates with grace notes:

            ::

                >>> voice = Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> grace_notes = [Note("cf''16"), Note("bf'16")]
                >>> grace = scoretools.GraceContainer(
                ...     grace_notes,
                ...     kind='grace',
                ...     )
                >>> attach(grace, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'8 [
                    \grace {
                        cf''16
                        bf'16
                    }
                    d'8
                    e'8
                    f'8 ]
                }

            ::

                >>> for component in iterate(voice).by_timeline():
                ...     component
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Note("f'8")

            ..  todo:: Incorrect because grace notes are not included.

        Iterates leaves when `prototype` is none.
        '''
        prototype = prototype or scoretools.Leaf
        if isinstance(self.client, scoretools.Component):
            components = [self.client]
        else:
            components = list(self.client)
        if not reverse:
            while components:
                current_start_offset = min(
                    _._get_timespan().start_offset
                    for _ in components
                    )
                components.sort(
                    key=lambda x: x._get_parentage(with_grace_notes=True).score_index,
                    reverse=True,
                    )
                components_to_process = components[:]
                components = []
                while components_to_process:
                    component = components_to_process.pop()
                    start_offset = component._get_timespan().start_offset
                    #print('    COMPONENT:', component)
                    if current_start_offset < start_offset:
                        components.append(component)
                        #print('        TOO EARLY')
                        continue
                    if isinstance(component, prototype):
                        #print('        YIELDING', component)
                        yield component
                    sibling = component._get_sibling(1)
                    if sibling is not None:
                        #print('        SIBLING:', sibling)
                        components.append(sibling)
                    if not isinstance(component, scoretools.Container):
                        continue
                    if not len(component):
                        continue
                    if not component.is_simultaneous:
                        components_to_process.append(component[0])
                    else:
                        components_to_process.extend(reversed(component))
        else:
            while components:
                #print('STEP')
                #print()
                current_stop_offset = max(
                    _._get_timespan().stop_offset
                    for _ in components
                    )
                components.sort(
                    key=lambda x: x._get_parentage(with_grace_notes=True).score_index,
                    reverse=True,
                    )
                components_to_process = components[:]
                components = []
                while components_to_process:
                    component = components_to_process.pop()
                    stop_offset = component._get_timespan().stop_offset
                    #print('\tCOMPONENT:', component)
                    if stop_offset < current_stop_offset:
                        components.insert(0, component)
                        continue
                    if isinstance(component, prototype):
                        yield component
                    sibling = component._get_sibling(-1)
                    if sibling is not None:
                        components.insert(0, sibling)
                    if not isinstance(component, scoretools.Container):
                        continue
                    if not len(component):
                        continue
                    if not component.is_simultaneous:
                        components_to_process.append(component[-1])
                    else:
                        components_to_process.extend(reversed(component))

    def by_timeline_and_logical_tie(
        self,
        nontrivial=False,
        pitched=False,
        reverse=False,
        ):
        r'''Iterates by timeline and logical tie.

        ..  container:: example

            ::

                >>> score = Score([])
                >>> score.append(Staff("c''4 ~ c''8 d''8 r4 ef''4"))
                >>> score.append(Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8"))
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        c''4 ~
                        c''8
                        d''8
                        r4
                        ef''4
                    }
                    \new Staff {
                        r8
                        g'4. ~
                        g'8
                        r16
                        f'8. ~
                        f'8
                    }
                >>

            ::

                >>> for logical_tie in iterate(score).by_timeline_and_logical_tie():
                ...     logical_tie
                ...
                LogicalTie([Note("c''4"), Note("c''8")])
                LogicalTie([Rest('r8')])
                LogicalTie([Note("g'4."), Note("g'8")])
                LogicalTie([Note("d''8")])
                LogicalTie([Rest('r4')])
                LogicalTie([Rest('r16')])
                LogicalTie([Note("f'8."), Note("f'8")])
                LogicalTie([Note("ef''4")])

        ..  container:: example

            **Example 2.** Reverses direction of iteration:

            ::

                >>> score = Score([])
                >>> score.append(Staff("c''4 ~ c''8 d''8 r4 ef''4"))
                >>> score.append(Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8"))
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        c''4 ~
                        c''8
                        d''8
                        r4
                        ef''4
                    }
                    \new Staff {
                        r8
                        g'4. ~
                        g'8
                        r16
                        f'8. ~
                        f'8
                    }
                >>

            ::

                >>> for logical_tie in iterate(score).by_timeline_and_logical_tie(
                ...     reverse=True,
                ...     ):
                ...     logical_tie
                ...
                LogicalTie([Note("ef''4")])
                LogicalTie([Note("f'8."), Note("f'8")])
                LogicalTie([Rest('r4')])
                LogicalTie([Rest('r16')])
                LogicalTie([Note("g'4."), Note("g'8")])
                LogicalTie([Note("d''8")])
                LogicalTie([Note("c''4"), Note("c''8")])
                LogicalTie([Rest('r8')])

        ..  container:: example

            **Example 3.** Iterates pitched logical ties by timeline:

            ::

                >>> for logical_tie in iterate(score).by_timeline_and_logical_tie(
                ...     pitched=True,
                ...     ):
                ...     logical_tie
                ...
                LogicalTie([Note("c''4"), Note("c''8")])
                LogicalTie([Note("g'4."), Note("g'8")])
                LogicalTie([Note("d''8")])
                LogicalTie([Note("f'8."), Note("f'8")])
                LogicalTie([Note("ef''4")])

        ..  container:: example

            **Example 4.** Iterates nontrivial logical ties by timeline:

            ::

                >>> for logical_tie in iterate(score).by_timeline_and_logical_tie(
                ...     nontrivial=True,
                ...     ):
                ...     logical_tie
                ...
                LogicalTie([Note("c''4"), Note("c''8")])
                LogicalTie([Note("g'4."), Note("g'8")])
                LogicalTie([Note("f'8."), Note("f'8")])

        '''
        visited_logical_ties = set()
        iterator = self.by_timeline(
            prototype=scoretools.Leaf,
            reverse=reverse,
            )
        for leaf in iterator:
            logical_tie = leaf._get_logical_tie()
            if logical_tie in visited_logical_ties:
                continue
            if nontrivial and logical_tie.is_trivial:
                continue
            if pitched and not logical_tie.is_pitched:
                continue
            visited_logical_ties.add(logical_tie)
            yield logical_tie

    # TODO: optimize to avoid behind-the-scenes full-score traversal
    def by_timeline_from_component(
        self,
        prototype=None,
        reverse=False,
        ):
        r'''Iterates from client by timeline.

        ..  container:: example

            **Example 1.** Iterates from note by timeline:

            ::

                >>> score = Score([])
                >>> score.append(Staff("c'4 d'4 e'4 f'4"))
                >>> score.append(Staff("g'8 a'8 b'8 c''8"))
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                    \new Staff {
                        g'8
                        a'8
                        b'8
                        c''8
                    }
                >>

            ::

                >>> for leaf in iterate(score[1][2]).by_timeline_from_component():
                ...     leaf
                ...
                Note("b'8")
                Note("c''8")
                Note("e'4")
                Note("f'4")

        ..  container:: example

            **Example 2.** Reverses direction of iteration:

            ::

                >>> score = Score([])
                >>> score.append(Staff("c'4 d'4 e'4 f'4"))
                >>> score.append(Staff("g'8 a'8 b'8 c''8"))
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                    \new Staff {
                        g'8
                        a'8
                        b'8
                        c''8
                    }
                >>

            ::

                >>> for leaf in iterate(score[1][2]).by_timeline_from_component(
                ...     reverse=True):
                ...     leaf
                ...
                Note("b'8")
                Note("c'4")
                Note("a'8")
                Note("g'8")

        Yields components sorted backward by score offset stop time
        when `reverse` is true.

        Iterates leaves when `prototype` is none.
        '''
        assert isinstance(self._client, scoretools.Component)
        if prototype is None:
            prototype = scoretools.Leaf
        root = self._client._get_parentage().root
        component_generator = iterate(root).by_timeline(
            prototype=prototype,
            reverse=reverse,
            )
        yielded_expr = False
        for component in component_generator:
            if yielded_expr:
                yield component
            elif component is self._client:
                yield component
                yielded_expr = True

    def by_topmost_logical_ties_and_components(self):
        r'''Iterates by topmost logical ties and components.

        ..  container:: example

            **Example 1.** Iterates topmost logical ties and components:

            ::

                >>> string = r"c'8 ~ c'32 d'8 ~ d'32 \times 2/3 { e'8 f'8 g'8 } "
                >>> string += "a'8 ~ a'32 b'8 ~ b'32"
                >>> staff = Staff(string)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 ~
                    c'32
                    d'8 ~
                    d'32
                    \times 2/3 {
                        e'8
                        f'8
                        g'8
                    }
                    a'8 ~
                    a'32
                    b'8 ~
                    b'32
                }

            ::

                >>> for item in iterate(staff).by_topmost_logical_ties_and_components():
                ...     item
                ...
                LogicalTie([Note("c'8"), Note("c'32")])
                LogicalTie([Note("d'8"), Note("d'32")])
                Tuplet(Multiplier(2, 3), "e'8 f'8 g'8")
                LogicalTie([Note("a'8"), Note("a'32")])
                LogicalTie([Note("b'8"), Note("b'32")])

        Returns generator.
        '''
        from abjad.tools import selectiontools
        prototype = (spannertools.Tie,)
        if isinstance(self._client, scoretools.Leaf):
            logical_tie = self._client._get_logical_tie()
            if len(logical_tie) == 1:
                yield logical_tie
            else:
                message = 'can not have only one leaf in logical tie.'
                raise ValueError(message)
        elif isinstance(
            self._client, (
                collections.Sequence,
                scoretools.Container,
                selectiontools.Selection,
                )):
            for component in self._client:
                if isinstance(component, scoretools.Leaf):
                    tie_spanners = component._get_spanners(prototype)
                    if not tie_spanners or \
                        tuple(tie_spanners)[0]._is_my_last_leaf(component):
                        yield component._get_logical_tie()
                elif isinstance(component, scoretools.Container):
                    yield component
        else:
            message = 'input must be iterable: {!r}.'
            message = message.format(self._client)
            raise ValueError(message)

    def by_vertical_moment(
        self,
        reverse=False,
        ):
        r'''Iterates by vertical moment.

        ..  container:: example

            **Example 1.** Iterates vertical moments:

            ::

                >>> score = Score([])
                >>> staff = Staff(r"\times 4/3 { d''8 c''8 b'8 }")
                >>> score.append(staff)
                >>> staff_group = StaffGroup([])
                >>> staff_group.context_name = 'PianoStaff'
                >>> staff_group.append(Staff("a'4 g'4"))
                >>> staff_group.append(Staff(r"""\clef "bass" f'8 e'8 d'8 c'8"""))
                >>> score.append(staff_group)
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3 {
                            d''8
                            c''8
                            b'8
                        }
                    }
                    \new PianoStaff <<
                        \new Staff {
                            a'4
                            g'4
                        }
                        \new Staff {
                            \clef "bass"
                            f'8
                            e'8
                            d'8
                            c'8
                        }
                    >>
                >>

            ::

                >>> for vertical_moment in iterate(score).by_vertical_moment():
                ...     vertical_moment.leaves
                ...
                (Note("d''8"), Note("a'4"), Note("f'8"))
                (Note("d''8"), Note("a'4"), Note("e'8"))
                (Note("c''8"), Note("a'4"), Note("e'8"))
                (Note("c''8"), Note("g'4"), Note("d'8"))
                (Note("b'8"), Note("g'4"), Note("d'8"))
                (Note("b'8"), Note("g'4"), Note("c'8"))

            ::

                >>> for vertical_moment in iterate(staff_group).by_vertical_moment():
                ...     vertical_moment.leaves
                ...
                (Note("a'4"), Note("f'8"))
                (Note("a'4"), Note("e'8"))
                (Note("g'4"), Note("d'8"))
                (Note("g'4"), Note("c'8"))

        ..  container:: example

            **Example 2.** Reverses direction of iteration:

            ::

                >>> score = Score([])
                >>> staff = Staff(r"\times 4/3 { d''8 c''8 b'8 }")
                >>> score.append(staff)
                >>> staff_group = StaffGroup([])
                >>> staff_group.context_name = 'PianoStaff'
                >>> staff_group.append(Staff("a'4 g'4"))
                >>> staff_group.append(Staff(r"""\clef "bass" f'8 e'8 d'8 c'8"""))
                >>> score.append(staff_group)
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3 {
                            d''8
                            c''8
                            b'8
                        }
                    }
                    \new PianoStaff <<
                        \new Staff {
                            a'4
                            g'4
                        }
                        \new Staff {
                            \clef "bass"
                            f'8
                            e'8
                            d'8
                            c'8
                        }
                    >>
                >>

            ::

                >>> for vertical_moment in iterate(score).by_vertical_moment(reverse=True):
                ...     vertical_moment.leaves
                ...
                (Note("b'8"), Note("g'4"), Note("c'8"))
                (Note("b'8"), Note("g'4"), Note("d'8"))
                (Note("c''8"), Note("g'4"), Note("d'8"))
                (Note("c''8"), Note("a'4"), Note("e'8"))
                (Note("d''8"), Note("a'4"), Note("e'8"))
                (Note("d''8"), Note("a'4"), Note("f'8"))

            ::

                >>> for vertical_moment in iterate(staff_group).by_vertical_moment(reverse=True):
                ...     vertical_moment.leaves
                ...
                (Note("g'4"), Note("c'8"))
                (Note("g'4"), Note("d'8"))
                (Note("a'4"), Note("e'8"))
                (Note("a'4"), Note("f'8"))

        Returns generator.
        '''
        from abjad.tools import selectiontools

        def _buffer_components_starting_with(component, buffer, stop_offsets):
            #if not isinstance(component, scoretools.Component):
            #    raise TypeError
            buffer.append(component)
            stop_offsets.append(component._get_timespan().stop_offset)
            if isinstance(component, scoretools.Container):
                if component.is_simultaneous:
                    for x in component:
                        _buffer_components_starting_with(
                            x, buffer, stop_offsets)
                else:
                    if component:
                        _buffer_components_starting_with(
                            component[0], buffer, stop_offsets)

        def _iterate_vertical_moments_forward_in_expr(expr):
            #if not isinstance(expr, scoretools.Component):
            #    raise TypeError
            governors = (expr,)
            current_offset, stop_offsets, buffer = \
                durationtools.Offset(0), [], []
            _buffer_components_starting_with(expr, buffer, stop_offsets)
            while buffer:
                vertical_moment = selectiontools.VerticalMoment()
                offset = durationtools.Offset(current_offset)
                components = list(buffer)
                components.sort(key=lambda x: x._get_parentage().score_index)
                vertical_moment._offset = offset
                vertical_moment._governors = governors
                vertical_moment._components = components
                yield vertical_moment
                current_offset, stop_offsets = min(stop_offsets), []
                _update_buffer(current_offset, buffer, stop_offsets)

        def _next_in_parent(component):
            from abjad.tools import selectiontools
            if not isinstance(component, scoretools.Component):
                raise TypeError
            selection = selectiontools.Selection(component)
            parent, start, stop = \
                selection._get_parent_and_start_stop_indices()
            assert start == stop
            if parent is None:
                raise StopIteration
            # can not advance within simultaneous parent
            if parent.is_simultaneous:
                raise StopIteration
            try:
                return parent[start + 1]
            except IndexError:
                raise StopIteration

        def _update_buffer(current_offset, buffer, stop_offsets):
            #print 'At %s with %s ...' % (current_offset, buffer)
            for component in buffer[:]:
                if component._get_timespan().stop_offset <= current_offset:
                    buffer.remove(component)
                    try:
                        next_component = _next_in_parent(component)
                        _buffer_components_starting_with(
                            next_component, buffer, stop_offsets)
                    except StopIteration:
                        pass
                else:
                    stop_offsets.append(component._get_timespan().stop_offset)

        if not reverse:
            for x in _iterate_vertical_moments_forward_in_expr(self._client):
                yield x
        else:
            moments_in_governor = []
            for component in self.by_class():
                offset = component._get_timespan().start_offset
                if offset not in moments_in_governor:
                    moments_in_governor.append(offset)
            moments_in_governor.sort()
            for moment_in_governor in reversed(moments_in_governor):
                yield self._client._get_vertical_moment_at(moment_in_governor)

    def depth_first(
        self,
        capped=True,
        direction=Left,
        forbid=None,
        unique=True,
        ):
        r'''Iterates depth first.

        ..  container:: example

            **Example 1.** Iterates depth first:

            ::

                >>> score = Score([])
                >>> score.append(Staff("c''4 ~ c''8 d''8 r4 ef''4"))
                >>> score.append(Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8"))
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        c''4 ~
                        c''8
                        d''8
                        r4
                        ef''4
                    }
                    \new Staff {
                        r8
                        g'4. ~
                        g'8
                        r16
                        f'8. ~
                        f'8
                    }
                >>

            ::

                >>> for component in iterate(score).depth_first():
                ...     component
                ...
                <Score<<2>>>
                Staff("c''4 ~ c''8 d''8 r4 ef''4")
                Note("c''4")
                Note("c''8")
                Note("d''8")
                Rest('r4')
                Note("ef''4")
                Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8")
                Rest('r8')
                Note("g'4.")
                Note("g'8")
                Rest('r16')
                Note("f'8.")
                Note("f'8")

        ..  container:: example

            **Example 2.** Reverses direction of iteration:

            ::

                >>> score = Score([])
                >>> score.append(Staff("c''4 ~ c''8 d''8 r4 ef''4"))
                >>> score.append(Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8"))
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        c''4 ~
                        c''8
                        d''8
                        r4
                        ef''4
                    }
                    \new Staff {
                        r8
                        g'4. ~
                        g'8
                        r16
                        f'8. ~
                        f'8
                    }
                >>

            ::

                >>> for component in iterate(score).depth_first(direction=Right):
                ...     component
                ...
                <Score<<2>>>
                Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8")
                Note("f'8")
                Note("f'8.")
                Rest('r16')
                Note("g'8")
                Note("g'4.")
                Rest('r8')
                Staff("c''4 ~ c''8 d''8 r4 ef''4")
                Note("ef''4")
                Rest('r4')
                Note("d''8")
                Note("c''8")
                Note("c''4")

        ..  container:: example

            **Example 3.** Iterates with grace notes:

            ::

                >>> voice = Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> grace_notes = [Note("cf''16"), Note("bf'16")]
                >>> grace = scoretools.GraceContainer(
                ...     grace_notes,
                ...     kind='grace',
                ...     )
                >>> attach(grace, voice[1])
                >>> after_grace_notes = [Note("af'16"), Note("gf'16")]
                >>> after_grace = scoretools.GraceContainer(
                ...     after_grace_notes,
                ...     kind='after')
                >>> attach(after_grace, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'8 [
                    \grace {
                        cf''16
                        bf'16
                    }
                    \afterGrace
                    d'8
                    {
                        af'16
                        gf'16
                    }
                    e'8
                    f'8 ]
                }

            ::

                >>> for component in iterate(voice).depth_first():
                ...     component
                ...
                Voice("c'8 d'8 e'8 f'8")
                Note("c'8")
                Note("d'8")
                GraceContainer("cf''16 bf'16")
                Note("cf''16")
                Note("bf'16")
                GraceContainer("af'16 gf'16")
                Note("af'16")
                Note("gf'16")
                Note("e'8")
                Note("f'8")

        ..  note:: Reverse-iteration does not yet support grace notes.
            (Relatively straightforward to implement when the need arises.)

        Returns generator.
        '''
        def _next_node_depth_first(component, total):
            r'''If client has unvisited music, return next unvisited node in
            client's music.

            If client has no univisited music and has a parent, return client's
            parent.

            If client has no univisited music and no parent, return none.
            '''
            # if component is a container with not-yet-returned children
            if (
                hasattr(component, '_music') and
                0 < len(component) and
                total < len(component)
                ):
                # return next not-yet-returned child
                return component[total], 0
            # if component is a leaf with grace container attached
            elif getattr(component, '_grace', None) is not None:
                # return grace container
                return component._grace, 0
            # if component is a leaf with after grace container attached
            elif getattr(component, '_after_grace', None) is not None:
                # return after grace container
                return component._after_grace, 0
            # if component is grace container with all children returned
            elif hasattr(component, '_carrier'):
                carrier = component._carrier
                # if grace container has no carrier
                if carrier is None:
                    return None, None
                # if there's also an after grace container
                if (
                    not component.kind == 'after' and
                    carrier._after_grace is not None
                    ):
                    return carrier._after_grace, 0
                carrier_parent = carrier._parent
                # if carrier has no parent
                if carrier_parent is None:
                    return None, None
                # advance to next node in carrier parent
                return carrier_parent, carrier_parent.index(carrier) + 1
            else:
                parent = component._parent
                if parent is None:
                    return None, None
                return parent, parent.index(component) + 1

        def _previous_node_depth_first(component, total=0):
            r'''If client has unvisited music, return previous unvisited node
            in client's music.

            If client has no univisited music and has a parent, return client's
            parent.

            If client has no univisited music and no parent, return none.
            '''
            if (
                hasattr(component, '_music') and
                0 < len(component) and
                total < len(component)
                ):
                return component[len(component) - 1 - total], 0
            else:
                parent = component._parent
                if parent is not None:
                    return parent, len(parent) - parent.index(component)
                else:
                    return None, None

        def _handle_forbidden_node(node, queue):
            node_parent = node._parent
            if node_parent is not None:
                rank = node_parent.index(node) + 1
                node = node_parent
            else:
                node, rank = None, None
            queue.pop()
            return node, rank

        def _advance_node_depth_first(node, rank, direction):
            if direction is Left:
                node, rank = _next_node_depth_first(node, rank)
            else:
                node, rank = _previous_node_depth_first(node, rank)
            return node, rank

        def _is_node_forbidden(node, forbid):
            if forbid is None:
                return False
            elif forbid == 'simultaneous':
                return getattr(node, 'is_simultaneous', False)
            else:
                return isinstance(node, forbid)

        def _find_yield(node, rank, queue, unique):
            if hasattr(node, '_music'):
                try:
                    visited = node is queue[-1]
                except IndexError:
                    visited = False
                if not visited or unique is not True:
                    queue.append(node)
                    return node
                elif rank == len(node):
                    queue.pop()
                    return None
            else:
                return node
        assert isinstance(self._client, scoretools.Component)
        component = self._client
        client_parent, node, rank = component._parent, component, 0
        queue = collections.deque([])
        while node is not None and not (capped and node is client_parent):
            result = _find_yield(node, rank, queue, unique)
            if result is not None:
                yield result
            if _is_node_forbidden(node, forbid):
                node, rank = _handle_forbidden_node(node, queue)
            else:
                node, rank = _advance_node_depth_first(node, rank, direction)
        queue.clear()

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''Gets client of iteration agent.

        ..  container:: example

            **Example 1.** Gets component client:

            ::

                >>> staff = Staff("c'4 d' e' f'")
                >>> agent = iterate(staff)

            ::

                >>> agent.client
                Staff("c'4 d'4 e'4 f'4")

        ..  container:: example

            **Example 2.** Gets selection client:

            ::

                >>> staff = Staff("c'4 d' e' f'")
                >>> agent = iterate(staff[:2])

            ::

                >>> agent.client
                Selection([Note("c'4"), Note("d'4")])

        Returns component or selection.
        '''
        return self._client
