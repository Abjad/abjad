import collections
import inspect
from abjad.tools import abctools


class Iteration(abctools.AbjadObject):
    r'''Iteration.

    ..  container:: example

        Iterates components:

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'4
                    e'4
                    d'4
                    f'4
                }

        ..  container:: example

            ::

                >>> for component in abjad.iterate(staff).by_class():
                ...     component
                Staff("c'4 e'4 d'4 f'4")
                Note("c'4")
                Note("e'4")
                Note("d'4")
                Note("f'4")

    ..  container:: example

        Iterates leaves:

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'4
                    e'4
                    d'4
                    f'4
                }

        ..  container:: example

            ::

                >>> for leaf in abjad.iterate(staff).by_leaf():
                ...     leaf
                Note("c'4")
                Note("e'4")
                Note("d'4")
                Note("f'4")

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Collaborators'

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client=None):
        assert not isinstance(client, str), repr(client)
        self._client = client

    ### PRIVATE METHODS ###

    @staticmethod
    def _iterate_components(
        argument,
        pitched=None,
        prototype=None,
        reverse=False,
        with_grace_notes=True,
        ):
        import abjad
        if isinstance(argument, str):
            raise Exception(repr(argument))
        if not reverse:
            if (with_grace_notes and
                getattr(argument, '_grace_container', None) is not None):
                for component in argument._grace_container:
                    for x in Iteration._iterate_components(
                        component,
                        pitched=pitched,
                        prototype=prototype,
                        reverse=reverse,
                        with_grace_notes=with_grace_notes,
                        ):
                        yield x
            if isinstance(argument, prototype):
                if Iteration._matches_pitched(argument, pitched=pitched):
                    yield argument
            if (with_grace_notes and
                getattr(argument, '_after_grace_container', None) is not None):
                for component in argument._after_grace_container:
                    for x in Iteration._iterate_components(
                        component,
                        pitched=pitched,
                        prototype=prototype,
                        reverse=reverse,
                        with_grace_notes=with_grace_notes,
                        ):
                        yield x
            if isinstance(argument, collections.Iterable):
                for component in argument:
                    for x in Iteration._iterate_components(
                        component,
                        pitched=pitched,
                        prototype=prototype,
                        reverse=reverse,
                        with_grace_notes=with_grace_notes,
                        ):
                        yield x
        else:
            if (with_grace_notes and
                getattr(argument, '_after_grace_container', None) is not None):
                for component in reversed(argument._after_grace_container):
                    for x in Iteration._iterate_components(
                        component,
                        pitched=pitched,
                        prototype=prototype,
                        reverse=reverse,
                        with_grace_notes=with_grace_notes,
                        ):
                        yield x
            if isinstance(argument, prototype):
                if Iteration._matches_pitched(argument, pitched=pitched):
                    yield argument
            if (with_grace_notes and
                getattr(argument, '_grace_container', None) is not None):
                for component in reversed(argument._grace_container):
                    for x in Iteration._iterate_components(
                        component,
                        pitched=pitched,
                        prototype=prototype,
                        reverse=reverse,
                        with_grace_notes=with_grace_notes,
                        ):
                        yield x
            if isinstance(argument, collections.Iterable):
                for component in reversed(argument):
                    for x in Iteration._iterate_components(
                        component,
                        pitched=pitched,
                        prototype=prototype,
                        reverse=reverse,
                        with_grace_notes=with_grace_notes,
                        ):
                        yield x

    @staticmethod
    def _iterate_subrange(iterator, start=0, stop=None):
        assert 0 <= start
        try:
            for i in range(start):
                next(iterator)
            if stop is None:
                for item in iterator:
                    yield item
            else:
                for i in range(stop - start):
                    yield next(iterator)
        except StopIteration:
            pass

    @staticmethod
    def _list_ordered_pitch_pairs(expr_1, expr_2):
        import abjad
        pitches_1 = sorted(abjad.iterate(expr_1).by_pitch())
        pitches_2 = sorted(abjad.iterate(expr_2).by_pitch())
        sequences = [pitches_1, pitches_2]
        enumerator = abjad.Enumerator(sequences)
        for pair in enumerator.yield_outer_product():
            yield pair

    @staticmethod
    def _list_unordered_pitch_pairs(argument):
        import abjad
        pitches = sorted(abjad.iterate(argument).by_pitch())
        enumerator = abjad.Enumerator(pitches)
        for pair in enumerator.yield_pairs():
            yield pair

    @staticmethod
    def _matches_pitched(component, pitched=None):
        import abjad
        prototype = (abjad.Chord, abjad.Note)
        if (pitched is None or
            (pitched is True and isinstance(component, prototype)) or
            (pitched is not True and not isinstance(component, prototype))):
            return True
        else:
            return False

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''Gets client of iteration.

        ..  container:: example

            Gets component client:

            ::

                >>> staff = abjad.Staff("c'4 d' e' f'")
                >>> agent = abjad.iterate(staff)

            ::

                >>> agent.client
                Staff("c'4 d'4 e'4 f'4")

        ..  container:: example

            Gets selection client:

            ::

                >>> staff = abjad.Staff("c'4 d' e' f'")
                >>> agent = abjad.iterate(staff[:2])

            ::

                >>> agent.client
                Selection([Note("c'4"), Note("d'4")])

        Returns component or selection.
        '''
        return self._client

    ### PUBLIC METHODS ###

    def by_class(
        self,
        prototype=None,
        pitched=None,
        reverse=False,
        start=0,
        stop=None,
        with_grace_notes=True,
        ):
        r'''Iterates by class.

        ..  container:: example

            Iterates notes:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff()
                    >>> staff.append(abjad.Measure((2, 8), "c'8 d'8"))
                    >>> staff.append(abjad.Measure((2, 8), "e'8 f'8"))
                    >>> staff.append(abjad.Measure((2, 8), "g'8 a'8"))
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> agent = abjad.iterate(staff)
                    >>> for note in agent.by_class(prototype=abjad.Note):
                    ...     note
                    ...
                    Note("c'8")
                    Note("d'8")
                    Note("e'8")
                    Note("f'8")
                    Note("g'8")
                    Note("a'8")

        ..  container:: example

            Iterates notes constrained by index:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff()
                    >>> staff.append(abjad.Measure((2, 8), "c'8 d'8"))
                    >>> staff.append(abjad.Measure((2, 8), "e'8 f'8"))
                    >>> staff.append(abjad.Measure((2, 8), "g'8 a'8"))
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for note in abjad.iterate(staff).by_class(
                    ...     prototype=abjad.Note,
                    ...     start=0,
                    ...     stop=3,
                    ...     ):
                    ...     note
                    ...
                    Note("c'8")
                    Note("d'8")
                    Note("e'8")

                ::

                    >>> for note in abjad.iterate(staff).by_class(
                    ...     prototype=abjad.Note,
                    ...     start=2,
                    ...     stop=4,
                    ...     ):
                    ...     note
                    ...
                    Note("e'8")
                    Note("f'8")

        ..  container:: example

            Iterates notes in reverse:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff()
                    >>> staff.append(abjad.Measure((2, 8), "c'8 d'8"))
                    >>> staff.append(abjad.Measure((2, 8), "e'8 f'8"))
                    >>> staff.append(abjad.Measure((2, 8), "g'8 a'8"))
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for note in abjad.iterate(staff).by_class(
                    ...     prototype=abjad.Note,
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

            Iterates notes together with grace notes:

            ..  container:: example

                ::

                    >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                    >>> container = abjad.GraceContainer("cf''16 bf'16")
                    >>> abjad.attach(container, voice[1])
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for component in abjad.iterate(voice).by_class():
                    ...     component
                    ...
                    Voice("c'8 d'8 e'8 f'8")
                    Note("c'8")
                    Note("cf''16")
                    Note("bf'16")
                    Note("d'8")
                    Note("e'8")
                    Note("f'8")

        ..  container:: example

            Iterates notes together with both grace notes and after grace
            notes:

            ..  container:: example

                ::

                    >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                    >>> container = abjad.GraceContainer("cf''16 bf'16")
                    >>> abjad.attach(container, voice[1])
                    >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                    >>> abjad.attach(container, voice[1])
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for leaf in abjad.iterate(voice).by_class():
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

            Iterates grace notes and after grace notes in reverse:

            ..  container:: example

                ::

                    >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                    >>> container = abjad.GraceContainer("cf''16 bf'16")
                    >>> abjad.attach(container, voice[1])
                    >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                    >>> abjad.attach(container, voice[1])
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for leaf in abjad.iterate(voice).by_class(
                    ...     reverse=True,
                    ...     ):
                    ...     leaf
                    ...
                    Voice("c'8 d'8 e'8 f'8")
                    Note("f'8")
                    Note("e'8")
                    Note("gf'16")
                    Note("af'16")
                    Note("d'8")
                    Note("bf'16")
                    Note("cf''16")
                    Note("c'8")

        ..  container:: example

            Iterates pitched components:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff()
                    >>> staff.append(abjad.Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                    >>> staff.append(abjad.Measure((2, 8), "af'8 r8"))
                    >>> staff.append(abjad.Measure((2, 8), "r8 gf'8"))
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for leaf in abjad.iterate(staff).by_class(pitched=True):
                    ...     leaf
                    ...
                    Chord("<c' bf'>8")
                    Chord("<g' a'>8")
                    Note("af'8")
                    Note("gf'8")

        ..  container:: example

            Iterates nonpitched components:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff()
                    >>> staff.append(abjad.Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                    >>> staff.append(abjad.Measure((2, 8), "af'8 r8"))
                    >>> staff.append(abjad.Measure((2, 8), "r8 gf'8"))
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for leaf in abjad.iterate(staff).by_class(pitched=False):
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
        import abjad
        prototype = prototype or abjad.Component
        iterator = self._iterate_components(
            self.client,
            pitched=pitched,
            prototype=prototype,
            reverse=reverse,
            with_grace_notes=with_grace_notes,
            )
        return self._iterate_subrange(iterator, start, stop)

    def by_leaf(
        self,
        prototype=None,
        pitched=None,
        reverse=False,
        start=0,
        stop=None,
        with_grace_notes=True,
        ):
        r'''Iterates by leaf.

        ..  container:: example

            Iterates leaves:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff()
                    >>> staff.append(abjad.Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                    >>> staff.append(abjad.Measure((2, 8), "af'8 r8"))
                    >>> staff.append(abjad.Measure((2, 8), "r8 gf'8"))
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for leaf in abjad.iterate(staff).by_leaf():
                    ...     leaf
                    ...
                    Chord("<c' bf'>8")
                    Chord("<g' a'>8")
                    Note("af'8")
                    Rest('r8')
                    Rest('r8')
                    Note("gf'8")

        ..  container:: example

            Iterates leaves constrained by index:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff()
                    >>> staff.append(abjad.Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                    >>> staff.append(abjad.Measure((2, 8), "af'8 r8"))
                    >>> staff.append(abjad.Measure((2, 8), "r8 gf'8"))
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for leaf in abjad.iterate(staff).by_leaf(start=0, stop=3):
                    ...     leaf
                    ...
                    Chord("<c' bf'>8")
                    Chord("<g' a'>8")
                    Note("af'8")

                ::

                    >>> for leaf in abjad.iterate(staff).by_leaf(start=2, stop=4):
                    ...     leaf
                    ...
                    Note("af'8")
                    Rest('r8')

        ..  container:: example

            Iterates leaves in reverse:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff()
                    >>> staff.append(abjad.Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                    >>> staff.append(abjad.Measure((2, 8), "af'8 r8"))
                    >>> staff.append(abjad.Measure((2, 8), "r8 gf'8"))
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for leaf in abjad.iterate(staff).by_leaf(reverse=True):
                    ...     leaf
                    ...
                    Note("gf'8")
                    Rest('r8')
                    Rest('r8')
                    Note("af'8")
                    Chord("<g' a'>8")
                    Chord("<c' bf'>8")

        ..  container:: example

            Iterates leaves together with grace notes:

            ..  container:: example

                ::

                    >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                    >>> container = abjad.GraceContainer("cf''16 bf'16")
                    >>> abjad.attach(container, voice[1])
                    >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                    >>> abjad.attach(container, voice[1])
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for leaf in abjad.iterate(voice).by_leaf():
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

            Iterates pitched leaves:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff()
                    >>> staff.append(abjad.Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                    >>> staff.append(abjad.Measure((2, 8), "af'8 r8"))
                    >>> staff.append(abjad.Measure((2, 8), "r8 gf'8"))
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for leaf in abjad.iterate(staff).by_leaf(pitched=True):
                    ...     leaf
                    ...
                    Chord("<c' bf'>8")
                    Chord("<g' a'>8")
                    Note("af'8")
                    Note("gf'8")

        ..  container:: example

            Iterates nonpitched leaves:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff()
                    >>> staff.append(abjad.Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                    >>> staff.append(abjad.Measure((2, 8), "af'8 r8"))
                    >>> staff.append(abjad.Measure((2, 8), "r8 gf'8"))
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for leaf in abjad.iterate(staff).by_leaf(pitched=False):
                    ...     leaf
                    ...
                    Rest('r8')
                    Rest('r8')

        Returns generator.
        '''
        import abjad
        prototype = prototype or abjad.Leaf
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

            Iterates leaf pairs:

            ..  container:: example

                ::

                    >>> score = abjad.Score()
                    >>> score.append(abjad.Staff("c'8 d'8 e'8 f'8 g'4"))
                    >>> score.append(abjad.Staff("c4 a,4 g,4"))
                    >>> abjad.attach(abjad.Clef('bass'), score[1][0])
                    >>> show(score) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for leaf_pair in abjad.iterate(score).by_leaf_pair():
                    ...     leaf_pair
                    ...
                    Selection([Note("c'8"), Note('c4')])
                    Selection([Note("c'8"), Note("d'8")])
                    Selection([Note('c4'), Note("d'8")])
                    Selection([Note("d'8"), Note("e'8")])
                    Selection([Note("d'8"), Note('a,4')])
                    Selection([Note('c4'), Note("e'8")])
                    Selection([Note('c4'), Note('a,4')])
                    Selection([Note("e'8"), Note('a,4')])
                    Selection([Note("e'8"), Note("f'8")])
                    Selection([Note('a,4'), Note("f'8")])
                    Selection([Note("f'8"), Note("g'4")])
                    Selection([Note("f'8"), Note('g,4')])
                    Selection([Note('a,4'), Note("g'4")])
                    Selection([Note('a,4'), Note('g,4')])
                    Selection([Note("g'4"), Note('g,4')])

        Iterates leaf pairs left-to-right and top-to-bottom.

        Returns generator.
        '''
        import abjad
        vertical_moments = self.by_vertical_moment()
        for moment_1, moment_2 in abjad.sequence(vertical_moments).nwise():
            enumerator = abjad.Enumerator(moment_1.start_leaves)
            for pair in enumerator.yield_pairs():
                yield abjad.select(pair)
            sequences = [moment_1.leaves, moment_2.start_leaves]
            enumerator = abjad.Enumerator(sequences)
            for pair in enumerator.yield_outer_product():
                yield abjad.select(pair)
        else:
            enumerator = abjad.Enumerator(moment_2.start_leaves)
            for pair in enumerator.yield_pairs():
                yield abjad.select(pair)

    def by_logical_tie(
        self,
        nontrivial=False,
        pitched=False,
        reverse=False,
        parentage_mask=None,
        with_grace_notes=True,
        ):
        r'''Iterates by logical tie.

        ..  container:: example

            Iterates logical ties:

            ..  container:: example

                ::

                    >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
                    >>> staff = abjad.Staff(string)
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for logical_tie in abjad.iterate(staff).by_logical_tie():
                    ...     logical_tie
                    ...
                    LogicalTie([Note("c'4"), Note("c'16")])
                    LogicalTie([Note("d'8")])
                    LogicalTie([Note("e'8")])
                    LogicalTie([Note("f'4"), Note("f'16")])

        ..  container:: example

            Iterates logical ties in reverse:

            ..  container:: example

                ::

                    >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
                    >>> staff = abjad.Staff(string)
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for logical_tie in abjad.iterate(staff).by_logical_tie(
                    ...     reverse=True,
                    ...     with_grace_notes=False,
                    ...     ):
                    ...     logical_tie
                    ...
                    LogicalTie([Note("f'4"), Note("f'16")])
                    LogicalTie([Note("e'8")])
                    LogicalTie([Note("d'8")])
                    LogicalTie([Note("c'4"), Note("c'16")])

        ..  container:: example

            Iterates pitched logical ties:

            ..  container:: example

                ::

                    >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
                    >>> staff = abjad.Staff(string)
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for logical_tie in abjad.iterate(staff).by_logical_tie(
                    ...     pitched=True,
                    ...     ):
                    ...     logical_tie
                    ...
                    LogicalTie([Note("c'4"), Note("c'16")])
                    LogicalTie([Note("d'8")])
                    LogicalTie([Note("e'8")])
                    LogicalTie([Note("f'4"), Note("f'16")])

        ..  container:: example

            Iterates nontrivial logical ties:

            ..  container:: example

                ::

                    >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
                    >>> staff = abjad.Staff(string)
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for logical_tie in abjad.iterate(staff).by_logical_tie(
                    ...     nontrivial=True,
                    ...     ):
                    ...     logical_tie
                    ...
                    LogicalTie([Note("c'4"), Note("c'16")])
                    LogicalTie([Note("f'4"), Note("f'16")])

        ..  container:: example

            Iterates logical ties masked by parentage:

            ..  note::

                When iterating logical ties in a container, the yielded logical
                ties may contain leaves outside that container's parentage. By
                specifying a parentage mask, composers can constrain the
                contents of the yielded logical ties to only those leaves
                actually within the parentage of the container under iteration.

            ..  container:: example

                ::

                    >>> staff = abjad.Staff("{ c'1 ~ } { c'2 d'2 ~ } { d'1 }")
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        {
                            c'1 ~
                        }
                        {
                            c'2
                            d'2 ~
                        }
                        {
                            d'1
                        }
                    }

            ..  container:: example

                ::

                    >>> for logical_tie in abjad.iterate(staff[1]).by_logical_tie():
                    ...     logical_tie
                    ...
                    LogicalTie([Note("d'2"), Note("d'1")])

                ::

                    >>> for logical_tie in abjad.iterate(staff[1]).by_logical_tie(
                    ...     parentage_mask=staff[1]):
                    ...     logical_tie
                    ...
                    LogicalTie([Note("d'2")])

        ..  container:: example

            Iterates logical ties together with grace notes:

            ..  container:: example

                ::

                    >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                    >>> container = abjad.GraceContainer("cf''16 bf'16")
                    >>> abjad.attach(container, voice[1])
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for item in abjad.iterate(voice).by_logical_tie():
                    ...     item
                    ...
                    LogicalTie([Note("c'8")])
                    LogicalTie([Note("cf''16")])
                    LogicalTie([Note("bf'16")])
                    LogicalTie([Note("d'8")])
                    LogicalTie([Note("e'8")])
                    LogicalTie([Note("f'8")])

        ..  container:: example

            Iterates logical ties together with after grace notes:

            ..  container:: example

                ::

                    >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                    >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                    >>> abjad.attach(container, voice[1])
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for item in abjad.iterate(voice).by_logical_tie():
                    ...     item
                    ...
                    LogicalTie([Note("c'8")])
                    LogicalTie([Note("d'8")])
                    LogicalTie([Note("af'16")])
                    LogicalTie([Note("gf'16")])
                    LogicalTie([Note("e'8")])
                    LogicalTie([Note("f'8")])

        ..  container:: example

            Iterates logical ties together with both grace notes and after
            grace notes:

            ..  container:: example

                ::

                    >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                    >>> container = abjad.GraceContainer("cf''16 bf'16")
                    >>> abjad.attach(container, voice[1])
                    >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                    >>> abjad.attach(container, voice[1])
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for item in abjad.iterate(voice).by_logical_tie():
                    ...     item
                    ...
                    LogicalTie([Note("c'8")])
                    LogicalTie([Note("cf''16")])
                    LogicalTie([Note("bf'16")])
                    LogicalTie([Note("d'8")])
                    LogicalTie([Note("af'16")])
                    LogicalTie([Note("gf'16")])
                    LogicalTie([Note("e'8")])
                    LogicalTie([Note("f'8")])

        ..  container:: example

            Regression: returns at least one logical tie even when note all
            leaves in logical tie are passed as input:

            ..  container:: example

                ::

                    >>> voice = abjad.Voice("c'8 [ ~ c' ~ c' d' ]")
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

                    >>> f(voice)
                    \new Voice {
                        c'8 ~ [
                        c'8 ~
                        c'8
                        d'8 ]
                    }

            ..  container:: example

                ::

                    >>> selection = voice[:2]
                    >>> for lt in abjad.iterate(selection).by_logical_tie():
                    ...     lt
                    ...
                    LogicalTie([Note("c'8"), Note("c'8"), Note("c'8")])

        Returns generator.
        '''
        import abjad
        if pitched:
            prototype = (abjad.Chord, abjad.Note)
        else:
            prototype = abjad.Leaf
        yielded_logical_ties = set()
        for leaf in self.by_class(
            prototype=prototype,
            reverse=reverse,
            with_grace_notes=with_grace_notes,
            ):
            logical_tie = abjad.inspect(leaf).get_logical_tie()
            if leaf is not logical_tie.head:
                continue
            if parentage_mask:
                leaves = []
                for leaf in logical_tie:
                    parentage = abjad.inspect(leaf).get_parentage()
                    if parentage_mask in parentage:
                        leaves.append(leaf)
                logical_tie = abjad.LogicalTie(leaves)
                if not logical_tie:
                    continue
            if not bool(nontrivial) or not logical_tie.is_trivial:
                if logical_tie not in yielded_logical_ties:
                    yielded_logical_ties.add(logical_tie)
                    yield logical_tie

    def by_logical_voice(
        self,
        prototype,
        logical_voice,
        reverse=False,
        ):
        r'''Iterates by logical voice.

        ..  container:: example

            Iterates notes in logical voice 1:

            ..  container:: example

                ::

                    >>> container_1 = abjad.Container([
                    ...     abjad.Voice("c'8 d'8"),
                    ...     abjad.Voice("e'8 f'8"),
                    ...     ])
                    >>> container_1.is_simultaneous = True
                    >>> container_1[0].name = 'Voice 1'
                    >>> abjad.override(container_1[0]).stem.direction = abjad.Down
                    >>> container_1[1].name = 'Voice 2'
                    >>> container_2 = abjad.Container([
                    ...     abjad.Voice("g'8 a'8"),
                    ...     abjad.Voice("b'8 c''8"),
                    ...     ])
                    >>> container_2.is_simultaneous = True
                    >>> container_2[0].name = 'Voice 1'
                    >>> abjad.override(container_2[0]).stem.direction = abjad.Down
                    >>> container_2[1].name = 'Voice 2'
                    >>> staff = abjad.Staff([container_1, container_2])
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        <<
                            \context Voice = "Voice 1" \with {
                                \override Stem.direction = #down
                            } {
                                c'8
                                d'8
                            }
                            \context Voice = "Voice 2" {
                                e'8
                                f'8
                            }
                        >>
                        <<
                            \context Voice = "Voice 1" \with {
                                \override Stem.direction = #down
                            } {
                                g'8
                                a'8
                            }
                            \context Voice = "Voice 2" {
                                b'8
                                c''8
                            }
                        >>
                    }

            ..  container:: example

                ::

                    >>> selector = abjad.select().by_leaf()
                    >>> leaves = selector(staff)
                    >>> leaf = leaves[0]
                    >>> agent = abjad.inspect(leaf)
                    >>> signature = agent.get_parentage().logical_voice
                    >>> for note in abjad.iterate(staff).by_logical_voice(
                    ...     prototype=abjad.Note,
                    ...     logical_voice=signature,
                    ...     ):
                    ...     note
                    ...
                    Note("c'8")
                    Note("d'8")
                    Note("g'8")
                    Note("a'8")

        Returns generator.
        '''
        import abjad
        if (isinstance(self.client, prototype) and
            self.client._get_parentage().logical_voice == logical_voice):
            yield self.client
        if not reverse:
            if isinstance(self.client, (list, tuple)):
                for component in self.client:
                    for x in abjad.iterate(component).by_logical_voice(
                        prototype,
                        logical_voice,
                        ):
                        yield x
            if hasattr(self.client, 'components'):
                for component in self.client.components:
                    for x in abjad.iterate(component).by_logical_voice(
                        prototype,
                        logical_voice,
                        ):
                        yield x
        else:
            if isinstance(self.client, (list, tuple)):
                for component in reversed(self.client):
                    for x in abjad.iterate(component).by_logical_voice(
                        prototype,
                        logical_voice,
                        reverse=True,
                        ):
                        yield x
            if hasattr(self.client, 'components'):
                for component in reversed(self.client.components):
                    for x in abjad.iterate(component).by_logical_voice(
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

            Iterates from first leaf in score:

            ..  container:: example

                ::

                    >>> container_1 = abjad.Container([
                    ...     abjad.Voice("c'8 d'8"),
                    ...     abjad.Voice("e'8 f'8"),
                    ...     ])
                    >>> container_1.is_simultaneous = True
                    >>> container_1[0].name = 'Voice 1'
                    >>> abjad.override(container_1[0]).stem.direction = abjad.Down
                    >>> container_1[1].name = 'Voice 2'
                    >>> container_2 = abjad.Container([
                    ...     abjad.Voice("g'8 a'8"),
                    ...     abjad.Voice("b'8 c''8"),
                    ...     ])
                    >>> container_2.is_simultaneous = True
                    >>> container_2[0].name = 'Voice 1'
                    >>> abjad.override(container_2[0]).stem.direction = abjad.Down
                    >>> container_2[1].name = 'Voice 2'
                    >>> staff = abjad.Staff([container_1, container_2])
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        <<
                            \context Voice = "Voice 1" \with {
                                \override Stem.direction = #down
                            } {
                                c'8
                                d'8
                            }
                            \context Voice = "Voice 2" {
                                e'8
                                f'8
                            }
                        >>
                        <<
                            \context Voice = "Voice 1" \with {
                                \override Stem.direction = #down
                            } {
                                g'8
                                a'8
                            }
                            \context Voice = "Voice 2" {
                                b'8
                                c''8
                            }
                        >>
                    }

            ..  container:: example

                ::

                    >>> selector = abjad.select().by_leaf()
                    >>> leaves = selector(staff)
                    >>> leaf = leaves[0]
                    >>> for note in abjad.iterate(leaf).by_logical_voice_from_component(
                    ...     prototype=abjad.Note,
                    ...     ):
                    ...     note
                    ...
                    Note("c'8")
                    Note("d'8")
                    Note("g'8")
                    Note("a'8")

        ..  container:: example

            Iterates from second leaf in score:

                ::

                    >>> container_1 = abjad.Container([
                    ...     abjad.Voice("c'8 d'8"),
                    ...     abjad.Voice("e'8 f'8"),
                    ...     ])
                    >>> container_1.is_simultaneous = True
                    >>> container_1[0].name = 'Voice 1'
                    >>> abjad.override(container_1[0]).stem.direction = abjad.Down
                    >>> container_1[1].name = 'Voice 2'
                    >>> container_2 = abjad.Container([
                    ...     abjad.Voice("g'8 a'8"),
                    ...     abjad.Voice("b'8 c''8"),
                    ...     ])
                    >>> container_2.is_simultaneous = True
                    >>> container_2[0].name = 'Voice 1'
                    >>> abjad.override(container_2[0]).stem.direction = abjad.Down
                    >>> container_2[1].name = 'Voice 2'
                    >>> staff = abjad.Staff([container_1, container_2])
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        <<
                            \context Voice = "Voice 1" \with {
                                \override Stem.direction = #down
                            } {
                                c'8
                                d'8
                            }
                            \context Voice = "Voice 2" {
                                e'8
                                f'8
                            }
                        >>
                        <<
                            \context Voice = "Voice 1" \with {
                                \override Stem.direction = #down
                            } {
                                g'8
                                a'8
                            }
                            \context Voice = "Voice 2" {
                                b'8
                                c''8
                            }
                        >>
                    }

            ..  container:: example

                ::

                    >>> leaf = leaves[1]
                    >>> agent = abjad.iterate(leaf)
                    >>> for note in agent.by_logical_voice_from_component(
                    ...     prototype=abjad.Note,
                    ...     ):
                    ...     note
                    ...
                    Note("d'8")
                    Note("g'8")
                    Note("a'8")

        ..  container:: example

            Iterates all components in logical voice:

            ..  container:: example

                ::

                    >>> container_1 = abjad.Container([
                    ...     abjad.Voice("c'8 d'8"),
                    ...     abjad.Voice("e'8 f'8"),
                    ...     ])
                    >>> container_1.is_simultaneous = True
                    >>> container_1[0].name = 'Voice 1'
                    >>> abjad.override(container_1[0]).stem.direction = abjad.Down
                    >>> container_1[1].name = 'Voice 2'
                    >>> container_2 = abjad.Container([
                    ...     abjad.Voice("g'8 a'8"),
                    ...     abjad.Voice("b'8 c''8"),
                    ...     ])
                    >>> container_2.is_simultaneous = True
                    >>> container_2[0].name = 'Voice 1'
                    >>> abjad.override(container_2[0]).stem.direction = abjad.Down
                    >>> container_2[1].name = 'Voice 2'
                    >>> staff = abjad.Staff([container_1, container_2])
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        <<
                            \context Voice = "Voice 1" \with {
                                \override Stem.direction = #down
                            } {
                                c'8
                                d'8
                            }
                            \context Voice = "Voice 2" {
                                e'8
                                f'8
                            }
                        >>
                        <<
                            \context Voice = "Voice 1" \with {
                                \override Stem.direction = #down
                            } {
                                g'8
                                a'8
                            }
                            \context Voice = "Voice 2" {
                                b'8
                                c''8
                            }
                        >>
                    }

            ..  container:: example

                ::

                    >>> leaf = leaves[0]
                    >>> for component in abjad.iterate(leaf).by_logical_voice_from_component():
                    ...     component
                    ...
                    Note("c'8")
                    Voice("c'8 d'8", name='Voice 1')
                    Note("d'8")
                    Voice("g'8 a'8", name='Voice 1')
                    Note("g'8")
                    Note("a'8")

        ..  container:: example

            Iterates all components in logical voice in reverse:

            ..  container:: example

                ::

                    >>> container_1 = abjad.Container([
                    ...     abjad.Voice("c'8 d'8"),
                    ...     abjad.Voice("e'8 f'8"),
                    ...     ])
                    >>> container_1.is_simultaneous = True
                    >>> container_1[0].name = 'Voice 1'
                    >>> abjad.override(container_1[0]).stem.direction = abjad.Down
                    >>> container_1[1].name = 'Voice 2'
                    >>> container_2 = abjad.Container([
                    ...     abjad.Voice("g'8 a'8"),
                    ...     abjad.Voice("b'8 c''8"),
                    ...     ])
                    >>> container_2.is_simultaneous = True
                    >>> container_2[0].name = 'Voice 1'
                    >>> abjad.override(container_2[0]).stem.direction = abjad.Down
                    >>> container_2[1].name = 'Voice 2'
                    >>> staff = abjad.Staff([container_1, container_2])
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        <<
                            \context Voice = "Voice 1" \with {
                                \override Stem.direction = #down
                            } {
                                c'8
                                d'8
                            }
                            \context Voice = "Voice 2" {
                                e'8
                                f'8
                            }
                        >>
                        <<
                            \context Voice = "Voice 1" \with {
                                \override Stem.direction = #down
                            } {
                                g'8
                                a'8
                            }
                            \context Voice = "Voice 2" {
                                b'8
                                c''8
                            }
                        >>
                    }

            ..  container:: example

                ::

                    >>> leaf = leaves[-1]
                    >>> for note in abjad.iterate(leaf).by_logical_voice_from_component(
                    ...     prototype=abjad.Note,
                    ...     reverse=True,
                    ...     ):
                    ...     note
                    ...
                    Note("c''8")
                    Note("b'8")
                    Note("f'8")
                    Note("e'8")

                ::

                    >>> leaf = leaves[-1]
                    >>> for component in abjad.iterate(leaf).by_logical_voice_from_component(
                    ...     reverse=True,
                    ...     ):
                    ...     component
                    ...
                    Note("c''8")
                    Voice("b'8 c''8", name='Voice 2')
                    Note("b'8")
                    Voice("e'8 f'8", name='Voice 2')
                    Note("f'8")
                    Note("e'8")

        Returns generator.
        '''
        import abjad
        if prototype is None:
            prototype = abjad.Component
        signature = self.client._get_parentage().logical_voice
        if not reverse:
            for x in abjad.iterate(self.client).depth_first(
                capped=False,
                direction=abjad.Left,
                ):
                if isinstance(x, prototype):
                    if x._get_parentage().logical_voice == signature:
                        yield x
        else:
            for x in abjad.iterate(self.client).depth_first(
                capped=False,
                direction=abjad.Right,
                ):
                if isinstance(x, prototype):
                    if x._get_parentage().logical_voice == signature:
                        yield x

    def by_pitch(self):
        r'''Iterates by pitch.

        ..  container:: example

            Iterates pitches in container:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                    >>> beam = abjad.Beam()
                    >>> abjad.attach(beam, staff[:])
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        c'8 [
                        d'8
                        e'8
                        f'8 ]
                    }

            ..  container:: example

                ::

                    >>> for pitch in abjad.iterate(staff).by_pitch():
                    ...     pitch
                    ...
                    NamedPitch("c'")
                    NamedPitch("d'")
                    NamedPitch("e'")
                    NamedPitch("f'")

        ..  container:: example

            Iterates pitches in spanner:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                    >>> beam = abjad.Beam()
                    >>> abjad.attach(beam, staff[:])
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        c'8 [
                        d'8
                        e'8
                        f'8 ]
                    }

            ..  container:: example

                ::

                    >>> for pitch in abjad.iterate(beam).by_pitch():
                    ...     pitch
                    ...
                    NamedPitch("c'")
                    NamedPitch("d'")
                    NamedPitch("e'")
                    NamedPitch("f'")

        ..  container:: example

            Iterates pitches in pitch set:

            ..  container:: example

                ::

                    >>> pitch_set = abjad.PitchSet([0, 2, 4, 5])

            ..  container:: example

                ::

                    >>> for pitch in abjad.iterate(pitch_set).by_pitch():
                    ...     pitch
                    ...
                    NumberedPitch(0)
                    NumberedPitch(2)
                    NumberedPitch(4)
                    NumberedPitch(5)

        ..  container:: example

            Iterates different types of object in tuple:

            ..  container:: example

                ::

                    >>> pitches = (
                    ...     abjad.NamedPitch("c'"),
                    ...     abjad.Note("d'4"),
                    ...     abjad.Chord("<e' fs' g>4"),
                    ...     )

            ..  container:: example

                ::

                    >>> for pitch in abjad.iterate(pitches).by_pitch():
                    ...     pitch
                    ...
                    NamedPitch("c'")
                    NamedPitch("d'")
                    NamedPitch('g')
                    NamedPitch("e'")
                    NamedPitch("fs'")

        Returns generator.
        '''
        import abjad
        if isinstance(self.client, abjad.Pitch):
            pitch = abjad.NamedPitch.from_pitch_carrier(self.client)
            yield pitch
        result = []
        try:
            result.extend(self.client.pitches)
        except AttributeError:
            pass
        if isinstance(self.client, abjad.Chord):
            result.extend(self.client.written_pitches)
        elif isinstance(self.client, abjad.Spanner):
            for leaf in self.client.leaves:
                try:
                    result.append(leaf.written_pitch)
                except AttributeError:
                    pass
                try:
                    result.extedn(leaf.written_pitches)
                except AttributeError:
                    pass
        elif isinstance(self.client, abjad.PitchSet):
            result.extend(sorted(list(self.client)))
        elif isinstance(self.client, (list, tuple, set)):
            for item in self.client:
                for pitch_ in abjad.iterate(item).by_pitch():
                    result.append(pitch_)
        else:
            for leaf in abjad.iterate(self.client).by_leaf():
                try:
                    result.append(leaf.written_pitch)
                except AttributeError:
                    pass
                try:
                    result.extedn(leaf.written_pitches)
                except AttributeError:
                    pass
        for pitch in result:
            yield pitch

    def by_pitch_pair(self):
        r'''Iterates by pitch pair.

        ..  container:: example

            Iterates notes by pitch pair:

            ..  container:: example

                ::

                    >>> score = abjad.Score()
                    >>> score.append(abjad.Staff("c'8 d' e' f' g'4"))
                    >>> score.append(abjad.Staff("c4 a, g,"))
                    >>> abjad.attach(abjad.Clef('bass'), score[1][0])
                    >>> show(score) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for pair in abjad.iterate(score).by_pitch_pair():
                    ...     pair
                    ...
                    PitchSegment("c' c")
                    PitchSegment("c' d'")
                    PitchSegment("c d'")
                    PitchSegment("d' e'")
                    PitchSegment("d' a,")
                    PitchSegment("c e'")
                    PitchSegment("c a,")
                    PitchSegment("e' a,")
                    PitchSegment("e' f'")
                    PitchSegment("a, f'")
                    PitchSegment("f' g'")
                    PitchSegment("f' g,")
                    PitchSegment("a, g'")
                    PitchSegment("a, g,")
                    PitchSegment("g' g,")

        ..  container:: example

            Iterates chords by pitch pair:

            ..  container:: example

                ::

                    >>> chord_1 = abjad.Chord([0, 2, 4], (1, 4))
                    >>> chord_2 = abjad.Chord([17, 19], (1, 4))
                    >>> staff = abjad.Staff([chord_1, chord_2])

                ..  docs::

                    >>> f(staff)
                    \new Staff {
                        <c' d' e'>4
                        <f'' g''>4
                    }

            ..  container:: example

                ::

                    >>> for pair in abjad.iterate(staff).by_pitch_pair():
                    ...     pair
                    ...
                    PitchSegment("c' d'")
                    PitchSegment("c' e'")
                    PitchSegment("d' e'")
                    PitchSegment("c' f''")
                    PitchSegment("c' g''")
                    PitchSegment("d' f''")
                    PitchSegment("d' g''")
                    PitchSegment("e' f''")
                    PitchSegment("e' g''")
                    PitchSegment("f'' g''")

        Returns generator.
        '''
        import abjad
        for leaf_pair in self.by_leaf_pair():
            leaf_pair_list = list(leaf_pair)
            for pair in self._list_unordered_pitch_pairs(
                leaf_pair_list[0]):
                yield abjad.PitchSegment(items=pair)
            if isinstance(leaf_pair, set):
                for pair in self._list_unordered_pitch_pairs(leaf_pair):
                    yield abjad.PitchSegment(items=pair)
            else:
                for pair in self._list_ordered_pitch_pairs(*leaf_pair):
                    yield abjad.PitchSegment(items=pair)
            for pair in self._list_unordered_pitch_pairs(
                leaf_pair_list[1]):
                yield abjad.PitchSegment(items=pair)

    def by_run(self, prototype=None):
        r'''Iterates by run.

        ..  container:: example

            Iterates runs of notes and chords at only the top level of score:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff(r"\times 2/3 { c'8 d'8 r8 }")
                    >>> staff.append(r"\times 2/3 { r8 <e' g'>8 <f' a'>8 }")
                    >>> staff.extend("g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> prototype = (abjad.Note, abjad.Chord)
                    >>> for run in abjad.iterate(staff[:]).by_run(
                    ...     prototype=prototype,
                    ...     ):
                    ...     run
                    ...
                    Selection([Note("g'8"), Note("a'8")])
                    Selection([Chord("<b' d''>8"), Chord("<c'' e''>8")])

        ..  container:: example

            Iterates runs of notes and chords at all levels of score:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff(r"\times 2/3 { c'8 d'8 r8 }")
                    >>> staff.append(r"\times 2/3 { r8 <e' g'>8 <f' a'>8 }")
                    >>> staff.extend("g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> leaves = abjad.iterate(staff).by_leaf()
                    >>> prototype = (abjad.Note, abjad.Chord)
                    >>> for run in abjad.iterate(leaves).by_run(
                    ...     prototype=prototype,
                    ...     ):
                    ...     run
                    ...
                    Selection([Note("c'8"), Note("d'8")])
                    Selection([Chord("<e' g'>8"), Chord("<f' a'>8"), Note("g'8"), Note("a'8")])
                    Selection([Chord("<b' d''>8"), Chord("<c'' e''>8")])

        ..  container:: example

            Interprets none prototype equal to leaves:

            ..  container:: example

                ::

                    >>> components = [
                    ...     abjad.Note("c'4"),
                    ...     abjad.Note("d'4"),
                    ...     abjad.Staff(),
                    ...     abjad.Note("e'4"),
                    ...     abjad.Note("f'4"),
                    ...     abjad.Staff(),
                    ...     abjad.Rest('r4'),
                    ...     ]

            ..  container:: example

                ::

                    >>> for run in abjad.iterate(components).by_run():
                    ...     run
                    ...
                    Selection([Note("c'4"), Note("d'4")])
                    Selection([Note("e'4"), Note("f'4")])
                    Selection([Rest('r4')])

        Returns generator.
        '''
        import abjad
        prototype = prototype or abjad.Leaf
        if not isinstance(prototype, collections.Sequence):
            prototype = (prototype,)
        selection = abjad.select(self.client)
        current_run = ()
        for run in selection.group(type):
            if isinstance(run[0], prototype):
                current_run = current_run + run
            elif current_run:
                yield abjad.select(current_run)
                current_run = ()
        if current_run:
            yield abjad.select(current_run)

    def by_spanner(
        self,
        prototype=None,
        reverse=False,
        ):
        r'''Iterates by spanner.

        ..  container:: example

            Iterates spanners:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 f'8 b'8 c''8")
                    >>> abjad.attach(abjad.Slur(), staff[:4])
                    >>> abjad.attach(abjad.Slur(), staff[4:])
                    >>> abjad.attach(abjad.Beam(), staff[:])
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for spanner in abjad.iterate(staff).by_spanner():
                    ...     spanner
                    ...
                    Beam("c'8, d'8, ... [5] ..., b'8, c''8")
                    Slur("c'8, d'8, e'8, f'8")
                    Slur("g'8, a'8, f'8, b'8, c''8")

        ..  container:: example

            Iterates spanners in reverse:

            ..  container:: example

                ::

                    >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 f'8 b'8 c''8")
                    >>> abjad.attach(abjad.Slur(), staff[:4])
                    >>> abjad.attach(abjad.Slur(), staff[4:])
                    >>> abjad.attach(abjad.Beam(), staff[:])
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for spanner in abjad.iterate(staff).by_spanner(reverse=True):
                    ...     spanner
                    ...
                    Beam("c'8, d'8, ... [5] ..., b'8, c''8")
                    Slur("g'8, a'8, f'8, b'8, c''8")
                    Slur("c'8, d'8, e'8, f'8")

        Returns generator.
        '''
        import abjad
        visited_spanners = set()
        for component in self.by_class(reverse=reverse):
            spanners = abjad.inspect(component).get_spanners(
                prototype=prototype,
                )
            spanners = sorted(spanners,
                key=lambda x: (
                    type(x).__name__,
                    abjad.inspect(x).get_timespan(),
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

            Timeline-iterates leaves:

            ..  container:: example

                ::

                    >>> score = abjad.Score()
                    >>> score.append(abjad.Staff("c'4 d'4 e'4 f'4"))
                    >>> score.append(abjad.Staff("g'8 a'8 b'8 c''8"))
                    >>> show(score) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for leaf in abjad.iterate(score).by_timeline():
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

            Timeline-iterates leaves in reverse:

            ..  container:: example

                ::

                    >>> score = abjad.Score()
                    >>> score.append(abjad.Staff("c'4 d'4 e'4 f'4"))
                    >>> score.append(abjad.Staff("g'8 a'8 b'8 c''8"))
                    >>> show(score) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for leaf in abjad.iterate(score).by_timeline(reverse=True):
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

            Timeline-iterates leaves together grace notes:

            ..  container:: example

                ::

                    >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                    >>> container = abjad.GraceContainer("cf''16 bf'16")
                    >>> abjad.attach(container, voice[1])
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for component in abjad.iterate(voice).by_timeline():
                    ...     component
                    ...
                    Note("c'8")
                    Note("d'8")
                    Note("e'8")
                    Note("f'8")

                ..  todo:: Incorrect because grace notes are not included.

        Iterates leaves when `prototype` is none.
        '''
        import abjad
        prototype = prototype or abjad.Leaf
        if isinstance(self.client, abjad.Component):
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
                    key=lambda x: x._get_parentage(
                        with_grace_notes=True).score_index,
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
                    if not isinstance(component, abjad.Container):
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
                    key=lambda x: x._get_parentage(
                        with_grace_notes=True).score_index,
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
                    if not isinstance(component, abjad.Container):
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

            Timeline-iterates logical ties:

            ..  container:: example

                ::

                    >>> score = abjad.Score()
                    >>> score.append(abjad.Staff("c''4 ~ c''8 d''8 r4 ef''4"))
                    >>> score.append(abjad.Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8"))
                    >>> show(score) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> agent = abjad.iterate(score)
                    >>> for logical_tie in agent.by_timeline_and_logical_tie():
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

            Timeline-iterates logical ties in reverse:

            ..  container:: example

                ::

                    >>> score = abjad.Score([])
                    >>> score.append(abjad.Staff("c''4 ~ c''8 d''8 r4 ef''4"))
                    >>> score.append(abjad.Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8"))
                    >>> show(score) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> agent = abjad.iterate(score)
                    >>> for logical_tie in agent.by_timeline_and_logical_tie(
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

            Timeline-iterates pitched logical ties:

            ..  container:: example

                ::

                    >>> agent = abjad.iterate(score)
                    >>> for logical_tie in agent.by_timeline_and_logical_tie(
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

            Timeline-iterates nontrivial logical ties:

            ..  container:: example

                ::

                    >>> agent = abjad.iterate(score)
                    >>> for logical_tie in agent.by_timeline_and_logical_tie(
                    ...     nontrivial=True,
                    ...     ):
                    ...     logical_tie
                    ...
                    LogicalTie([Note("c''4"), Note("c''8")])
                    LogicalTie([Note("g'4."), Note("g'8")])
                    LogicalTie([Note("f'8."), Note("f'8")])

        Returns generator.
        '''
        visited_logical_ties = set()
        iterator = self.by_timeline(reverse=reverse)
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

            Timeline-iterates from note:

            ..  container:: example

                ::

                    >>> score = abjad.Score()
                    >>> score.append(abjad.Staff("c'4 d'4 e'4 f'4"))
                    >>> score.append(abjad.Staff("g'8 a'8 b'8 c''8"))
                    >>> show(score) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> agent = abjad.iterate(score[1][2])
                    >>> for leaf in agent.by_timeline_from_component():
                    ...     leaf
                    ...
                    Note("b'8")
                    Note("c''8")
                    Note("e'4")
                    Note("f'4")

        ..  container:: example

            Timeline-iterates from note in reverse:

            ..  container:: example

                ::

                    >>> score = abjad.Score([])
                    >>> score.append(abjad.Staff("c'4 d'4 e'4 f'4"))
                    >>> score.append(abjad.Staff("g'8 a'8 b'8 c''8"))
                    >>> show(score) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> agent = abjad.iterate(score[1][2])
                    >>> for leaf in agent.by_timeline_from_component(
                    ...     reverse=True,
                    ...     ):
                    ...     leaf
                    ...
                    Note("b'8")
                    Note("c'4")
                    Note("a'8")
                    Note("g'8")

        Returns generator.
        '''
        import abjad
        assert isinstance(self.client, abjad.Component)
        prototype = prototype or abjad.Leaf
        root = self.client._get_parentage().root
        component_generator = abjad.iterate(root).by_timeline(
            prototype=prototype,
            reverse=reverse,
            )
        yielded_expr = False
        for component in component_generator:
            if yielded_expr:
                yield component
            elif component is self.client:
                yield component
                yielded_expr = True

    def by_topmost_logical_ties_and_components(self):
        r'''Iterates by topmost logical ties and components.

        ..  container:: example

            Iterates topmost logical ties and components:

            ..  container:: example

                ::

                    >>> string = r"c'8 ~ c'32 d'8 ~ d'32 \times 2/3 { e'8 f'8 g'8 } "
                    >>> string += "a'8 ~ a'32 b'8 ~ b'32"
                    >>> staff = abjad.Staff(string)
                    >>> show(staff) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> agent = abjad.iterate(staff)
                    >>> for item in agent.by_topmost_logical_ties_and_components():
                    ...     item
                    ...
                    LogicalTie([Note("c'8"), Note("c'32")])
                    LogicalTie([Note("d'8"), Note("d'32")])
                    Tuplet(Multiplier(2, 3), "e'8 f'8 g'8")
                    LogicalTie([Note("a'8"), Note("a'32")])
                    LogicalTie([Note("b'8"), Note("b'32")])

        Returns generator.
        '''
        import abjad
        if isinstance(self.client, abjad.Leaf):
            logical_tie = self.client._get_logical_tie()
            if len(logical_tie) == 1:
                yield logical_tie
            else:
                message = 'can not have only one leaf in logical tie.'
                raise ValueError(message)
        elif isinstance(self.client, collections.Iterable):
            for component in self.client:
                if isinstance(component, abjad.Leaf):
                    ties = component._get_spanners(abjad.Tie)
                    if (not ties or
                        tuple(ties)[0]._is_my_last_leaf(component)):
                        yield component._get_logical_tie()
                elif isinstance(component, abjad.Container):
                    yield component

    def by_vertical_moment(self, reverse=False):
        r'''Iterates by vertical moment.

        ..  container:: example

            Iterates vertical moments:

            ..  container:: example

                ::

                    >>> score = abjad.Score([])
                    >>> staff = abjad.Staff(r"\times 4/3 { d''8 c''8 b'8 }")
                    >>> score.append(staff)
                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff_group.context_name = 'PianoStaff'
                    >>> staff_group.append(abjad.Staff("a'4 g'4"))
                    >>> staff_group.append(abjad.Staff(r"""\clef "bass" f'8 e'8 d'8 c'8"""))
                    >>> score.append(staff_group)
                    >>> show(score) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for vertical_moment in abjad.iterate(score).by_vertical_moment():
                    ...     vertical_moment.leaves
                    ...
                    Selection([Note("d''8"), Note("a'4"), Note("f'8")])
                    Selection([Note("d''8"), Note("a'4"), Note("e'8")])
                    Selection([Note("c''8"), Note("a'4"), Note("e'8")])
                    Selection([Note("c''8"), Note("g'4"), Note("d'8")])
                    Selection([Note("b'8"), Note("g'4"), Note("d'8")])
                    Selection([Note("b'8"), Note("g'4"), Note("c'8")])

                ::

                    >>> for vertical_moment in abjad.iterate(staff_group).by_vertical_moment():
                    ...     vertical_moment.leaves
                    ...
                    Selection([Note("a'4"), Note("f'8")])
                    Selection([Note("a'4"), Note("e'8")])
                    Selection([Note("g'4"), Note("d'8")])
                    Selection([Note("g'4"), Note("c'8")])

        ..  container:: example

            Iterates vertical moments in reverse:

            ..  container:: example

                ::

                    >>> score = abjad.Score([])
                    >>> staff = abjad.Staff(r"\times 4/3 { d''8 c''8 b'8 }")
                    >>> score.append(staff)
                    >>> staff_group = abjad.StaffGroup([])
                    >>> staff_group.context_name = 'PianoStaff'
                    >>> staff_group.append(abjad.Staff("a'4 g'4"))
                    >>> staff_group.append(abjad.Staff(r"""\clef "bass" f'8 e'8 d'8 c'8"""))
                    >>> score.append(staff_group)
                    >>> show(score) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> agent = abjad.iterate(score)
                    >>> for vertical_moment in agent.by_vertical_moment(
                    ...     reverse=True,
                    ...     ):
                    ...     vertical_moment.leaves
                    ...
                    Selection([Note("b'8"), Note("g'4"), Note("c'8")])
                    Selection([Note("b'8"), Note("g'4"), Note("d'8")])
                    Selection([Note("c''8"), Note("g'4"), Note("d'8")])
                    Selection([Note("c''8"), Note("a'4"), Note("e'8")])
                    Selection([Note("d''8"), Note("a'4"), Note("e'8")])
                    Selection([Note("d''8"), Note("a'4"), Note("f'8")])

                ::

                    >>> agent = abjad.iterate(staff_group)
                    >>> for vertical_moment in agent.by_vertical_moment(
                    ...     reverse=True,
                    ...     ):
                    ...     vertical_moment.leaves
                    ...
                    Selection([Note("g'4"), Note("c'8")])
                    Selection([Note("g'4"), Note("d'8")])
                    Selection([Note("a'4"), Note("e'8")])
                    Selection([Note("a'4"), Note("f'8")])

        Returns generator.
        '''
        import abjad
        def _buffer_components_starting_with(component, buffer, stop_offsets):
            buffer.append(component)
            stop_offsets.append(component._get_timespan().stop_offset)
            if isinstance(component, abjad.Container):
                if component.is_simultaneous:
                    for x in component:
                        _buffer_components_starting_with(
                            x, buffer, stop_offsets)
                else:
                    if component:
                        _buffer_components_starting_with(
                            component[0], buffer, stop_offsets)

        def _iterate_vertical_moments(argument):
            governors = (argument,)
            current_offset, stop_offsets, buffer = abjad.Offset(0), [], []
            _buffer_components_starting_with(argument, buffer, stop_offsets)
            while buffer:
                vertical_moment = abjad.VerticalMoment()
                offset = abjad.Offset(current_offset)
                components = list(buffer)
                components.sort(key=lambda x: x._get_parentage().score_index)
                vertical_moment._offset = offset
                vertical_moment._governors = governors
                vertical_moment._items = components
                yield vertical_moment
                current_offset, stop_offsets = min(stop_offsets), []
                _update_buffer(current_offset, buffer, stop_offsets)
        def _next_in_parent(component):
            assert isinstance(component, abjad.Component), repr(component)
            selection = abjad.select(component)
            result = selection._get_parent_and_start_stop_indices()
            parent, start, stop = result
            assert start == stop
            if parent is None:
                raise StopIteration
            if parent.is_simultaneous:
                raise StopIteration
            try:
                return parent[start + 1]
            except IndexError:
                raise StopIteration
        def _update_buffer(current_offset, buffer, stop_offsets):
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
            for x in _iterate_vertical_moments(self.client):
                yield x
        else:
            moments_in_governor = []
            for component in self.by_class():
                offset = component._get_timespan().start_offset
                if offset not in moments_in_governor:
                    moments_in_governor.append(offset)
            moments_in_governor.sort()
            for moment_in_governor in reversed(moments_in_governor):
                yield self.client._get_vertical_moment_at(
                    moment_in_governor)

    def depth_first(
        self,
        capped=True,
        direction=None,
        forbid=None,
        unique=True,
        ):
        r'''Iterates depth first.

        ..  container:: example

            Iterates depth first:

            ..  container:: example

                ::

                    >>> score = abjad.Score([])
                    >>> score.append(abjad.Staff("c''4 ~ c''8 d''8 r4 ef''4"))
                    >>> score.append(abjad.Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8"))
                    >>> show(score) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for component in abjad.iterate(score).depth_first():
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

            Iterates depth first in reverse:

            ..  container:: example

                ::

                    >>> score = abjad.Score([])
                    >>> score.append(abjad.Staff("c''4 ~ c''8 d''8 r4 ef''4"))
                    >>> score.append(abjad.Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8"))
                    >>> show(score) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> agent = abjad.iterate(score)
                    >>> for component in agent.depth_first(direction=abjad.Right):
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

            Iterates depth first with grace notes:

            ..  container:: example

                ::

                    >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                    >>> container = abjad.GraceContainer("cf''16 bf'16")
                    >>> abjad.attach(container, voice[1])
                    >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                    >>> abjad.attach(container, voice[1])
                    >>> show(voice) # doctest: +SKIP

                ..  docs::

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

            ..  container:: example

                ::

                    >>> for component in abjad.iterate(voice).depth_first():
                    ...     component
                    ...
                    Voice("c'8 d'8 e'8 f'8")
                    Note("c'8")
                    Note("d'8")
                    GraceContainer("cf''16 bf'16")
                    Note("cf''16")
                    Note("bf'16")
                    AfterGraceContainer("af'16 gf'16")
                    Note("af'16")
                    Note("gf'16")
                    Note("e'8")
                    Note("f'8")

        Returns generator.
        '''
        import abjad
        direction = direction or abjad.Left
        def _next_node_depth_first(component, total):
            r'''If client has unvisited components, return next unvisited
            component in client.

            If client has no univisited components, return client's parent.
            '''
            # if component is a container with not-yet-returned children
            if (hasattr(component, 'components') and
                0 < len(component) and
                total < len(component)):
                # return next not-yet-returned child
                return component[total], 0
            # if component is a leaf with grace container attached
            elif getattr(component, '_grace_container', None) is not None:
                # return grace container
                return component._grace_container, 0
            # if component is a leaf with after grace container attached
            elif (getattr(component, '_after_grace_container', None)
                is not None):
                # return after grace container
                return component._after_grace_container, 0
            # if component is grace container with all children returned
            elif hasattr(component, '_carrier'):
                carrier = component._carrier
                # if grace container has no carrier
                if carrier is None:
                    return None, None
                # if there's also an after grace container
                if (not isinstance(component, abjad.AfterGraceContainer) and
                    carrier._after_grace_container is not None):
                    return carrier._after_grace_container, 0
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
            r'''If client has unvisited components, return previous unvisited
            component in client.

            If client has no univisited components, return client's parent.
            '''
            if (hasattr(component, 'components') and
                0 < len(component) and
                total < len(component)):
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
            if direction == abjad.Left:
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
            if hasattr(node, 'components'):
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
        assert isinstance(self.client, abjad.Component)
        component = self.client
        client_parent, node, rank = component._parent, component, 0
        queue = collections.deque([])
        while node is not None and not (capped and node is client_parent):
            result = _find_yield(node, rank, queue, unique)
            if result is not None:
                yield result
            if _is_node_forbidden(node, forbid):
                node, rank = _handle_forbidden_node(node, queue)
            else:
                node, rank = _advance_node_depth_first(
                    node, rank, direction)
        queue.clear()

    def out_of_range(self):
        r'''Iterates notes and chords outside traditional instrument ranges.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'8 r8 <d fs>8 r8")
                >>> violin = abjad.instrumenttools.Violin()
                >>> abjad.attach(violin, staff[0])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { Violin }
                    \set Staff.shortInstrumentName = \markup { Vn. }
                    c'8
                    r8
                    <d fs>8
                    r8
                }

            ::

                >>> for leaf in abjad.iterate(staff).out_of_range():
                ...     leaf
                ...
                Chord('<d fs>8')

        Returns generator.
        '''
        import abjad
        for leaf in abjad.iterate(self.client).by_leaf(pitched=True):
            instrument = leaf._get_effective(abjad.Instrument)
            if instrument is None:
                message = 'no instrument found.'
                raise ValueError(message)
            if leaf not in instrument.pitch_range:
                yield leaf
