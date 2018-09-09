import collections
from abjad import enums
from abjad.instruments import Instrument
from abjad.pitch import NamedPitch
from abjad.pitch import Pitch
from abjad.pitch import PitchSegment
from abjad.pitch import PitchSet
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.utilities.Enumerator import Enumerator
from abjad.utilities.Offset import Offset
from abjad.utilities.OrderedDict import OrderedDict
from abjad.utilities.Sequence import Sequence
from abjad.top.inspect import inspect


class Iteration(object):
    r"""
    Iteration.

    ..  container:: example

        Iterates leaves:

        ..  container:: example

            >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    e'4
                    d'4
                    f'4
                }

        ..  container:: example

            >>> for leaf in abjad.iterate(staff).leaves():
            ...     leaf
            Note("c'4")
            Note("e'4")
            Note("d'4")
            Note("f'4")

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Collaborators'

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client=None):
        assert not isinstance(client, str), repr(client)
        self._client = client

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
    def _coerce_exclude(exclude):
        if exclude is None:
            exclude = ()
        elif isinstance(exclude, str):
            exclude = (exclude,)
        else:
            exclude = tuple(exclude)
        assert isinstance(exclude, tuple), repr(exclude)
        return exclude

    @staticmethod
    def _should_exclude(argument, exclude):
        assert isinstance(exclude, tuple)
        for string in exclude:
            if inspect(argument).annotation(string) is True:
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        """
        Gets client.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.iterate(staff[:2]).client
            Selection([Note("c'4"), Note("d'4")])

        Returns component or selection.
        """
        return self._client

    ### PUBLIC METHODS ###

    def components(
        self,
        prototype=None,
        *,
        exclude=None,
        do_not_iterate_grace_containers=None,
        grace_notes=None,
        reverse=None,
        ):
        r"""
        Iterates components.

        ..  container:: example

            Iterates notes:

            ..  container:: example

                >>> staff = abjad.Staff()
                >>> staff.extend("c'8 d'8")
                >>> staff.extend("e'8 f'8")
                >>> staff.extend("g'8 a'8")
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        \time 2/8
                        c'8
                        d'8
                        e'8
                        f'8
                        g'8
                        a'8
                    }

            ..  container:: example

                >>> agent = abjad.iterate(staff)
                >>> for note in agent.components(prototype=abjad.Note):
                ...     note
                ...
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Note("g'8")
                Note("a'8")

        ..  container:: example

            Iterates grace notes and nongrace notes:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> container = abjad.GraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, voice[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        [
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
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for component in abjad.iterate(voice).components():
                ...     component
                ...
                Voice("c'8 d'8 e'8 f'8")
                Note("c'8")
                GraceContainer("cf''16 bf'16")
                Note("cf''16")
                Note("bf'16")
                Note("d'8")
                AfterGraceContainer("af'16 gf'16")
                Note("af'16")
                Note("gf'16")
                Note("e'8")
                Note("f'8")

        ..  container:: example

            Iterates components in reverse:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> container = abjad.GraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, voice[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        [
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
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for component in abjad.iterate(voice).components(
                ...     reverse=True,
                ...     ):
                ...     component
                ...
                Voice("c'8 d'8 e'8 f'8")
                Note("f'8")
                Note("e'8")
                AfterGraceContainer("af'16 gf'16")
                Note("gf'16")
                Note("af'16")
                Note("d'8")
                GraceContainer("cf''16 bf'16")
                Note("bf'16")
                Note("cf''16")
                Note("c'8")

        Returns generator.
        """
        from .Component import Component
        from .Leaf import Leaf
        argument = self.client
        prototype = prototype or Component
        grace_container, after_grace_container = None, None
        exclude = self._coerce_exclude(exclude)
        assert isinstance(exclude, tuple), repr(exclude)
        if grace_notes is not False and isinstance(argument, Leaf):
            inspection = inspect(argument)
            grace_container = inspection.grace_container()
            after_grace_container = inspection.after_grace_container()
        if not reverse:
            if (not do_not_iterate_grace_containers and
                grace_notes is not False and
                grace_container):
                for component_ in Iteration(grace_container).components(
                    prototype,
                    do_not_iterate_grace_containers=do_not_iterate_grace_containers,
                    grace_notes=grace_notes,
                    reverse=reverse,
                    ):
                    yield component_
            if isinstance(argument, prototype):
                if (grace_notes is None or
                    (grace_notes is True and
                    inspect(argument).grace_note()) or
                    (grace_notes is False and
                    not inspect(argument).grace_note())):
                    if not self._should_exclude(argument, exclude):
                        yield argument
            if (not do_not_iterate_grace_containers and
                grace_notes is not False and
                after_grace_container):
                for component_ in Iteration(after_grace_container).components(
                    prototype,
                    exclude=exclude,
                    do_not_iterate_grace_containers=do_not_iterate_grace_containers,
                    grace_notes=grace_notes,
                    reverse=reverse,
                    ):
                    yield component_
            if isinstance(argument, collections.Iterable):
                for item in argument:
                    for component in Iteration(item).components(
                        prototype,
                        exclude=exclude,
                        do_not_iterate_grace_containers=do_not_iterate_grace_containers,
                        grace_notes=grace_notes,
                        reverse=reverse,
                        ):
                        yield component
        else:
            if (not do_not_iterate_grace_containers and
                grace_notes is not False and
                after_grace_container):
                for component_ in Iteration(after_grace_container).components(
                    prototype,
                    exclude=exclude,
                    do_not_iterate_grace_containers=do_not_iterate_grace_containers,
                    grace_notes=grace_notes,
                    reverse=reverse,
                    ):
                    yield component_
            if isinstance(argument, prototype):
                if (grace_notes is None or
                    (grace_notes is True and
                    inspect(argument).grace_note()) or
                    (grace_notes is False and
                    not inspect(argument).grace_note())):
                    if not self._should_exclude(argument, exclude):
                        yield argument
            if (not do_not_iterate_grace_containers and
                grace_notes is not False and
                grace_container):
                for component_ in Iteration(grace_container).components(
                    prototype,
                    exclude=exclude,
                    do_not_iterate_grace_containers=do_not_iterate_grace_containers,
                    grace_notes=grace_notes,
                    reverse=reverse,
                    ):
                    yield component_
            if isinstance(argument, collections.Iterable):
                for item in reversed(argument):
                    for component in Iteration(item).components(
                        prototype,
                        exclude=exclude,
                        do_not_iterate_grace_containers=do_not_iterate_grace_containers,
                        grace_notes=grace_notes,
                        reverse=reverse,
                        ):
                        yield component

    def leaf_pairs(self):
        r"""
        Iterates leaf pairs.

        ..  container:: example

            Iterates leaf pairs:

            ..  container:: example

                >>> score = abjad.Score()
                >>> score.append(abjad.Staff("c'8 d'8 e'8 f'8 g'4"))
                >>> score.append(abjad.Staff("c4 a,4 g,4"))
                >>> abjad.attach(abjad.Clef('bass'), score[1][0])
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        {
                            c'8
                            d'8
                            e'8
                            f'8
                            g'4
                        }
                        \new Staff
                        {
                            \clef "bass"
                            c4
                            a,4
                            g,4
                        }
                    >>

            ..  container:: example

                >>> for leaf_pair in abjad.iterate(score).leaf_pairs():
                ...     leaf_pair
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
        """
        from .Selection import Selection
        vertical_moments = self.vertical_moments()
        for moment_1, moment_2 in Sequence(vertical_moments).nwise():
            enumerator = Enumerator(moment_1.start_leaves)
            for pair in enumerator.yield_pairs():
                yield Selection(pair)
            sequences = [moment_1.leaves, moment_2.start_leaves]
            enumerator = Enumerator(sequences)
            for pair in enumerator.yield_outer_product():
                yield Selection(pair)
        else:
            enumerator = Enumerator(moment_2.start_leaves)
            for pair in enumerator.yield_pairs():
                yield Selection(pair)

    def leaves(
        self,
        prototype=None,
        *,
        exclude=None,
        do_not_iterate_grace_containers=None,
        grace_notes=None,
        pitched=None,
        reverse=False,
        ):
        r"""
        Iterates leaves.

        ..  container:: example

            Iterates leaves:

            ..  container:: example

                >>> staff = abjad.Staff()
                >>> staff.extend("<c' bf'>8 <g' a'>8")
                >>> staff.extend("af'8 r8")
                >>> staff.extend("r8 gf'8")
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        \time 2/8
                        <c' bf'>8
                        <g' a'>8
                        af'8
                        r8
                        r8
                        gf'8
                    }

            ..  container:: example

                >>> for leaf in abjad.iterate(staff).leaves():
                ...     leaf
                ...
                Chord("<c' bf'>8")
                Chord("<g' a'>8")
                Note("af'8")
                Rest('r8')
                Rest('r8')
                Note("gf'8")

        ..  container:: example

            Iterates grace notes and nongrace notes:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> container = abjad.GraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, voice[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        [
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
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for leaf in abjad.iterate(voice).leaves():
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

            Iterates grace notes only:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> container = abjad.GraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, voice[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        [
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
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for leaf in abjad.iterate(voice).leaves(grace_notes=True):
                ...     leaf
                ...
                Note("cf''16")
                Note("bf'16")
                Note("af'16")
                Note("gf'16")

        ..  container:: example

            Iterates nongrace notes only:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> container = abjad.GraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, voice[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        [
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
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for leaf in abjad.iterate(voice).leaves(grace_notes=False):
                ...     leaf
                ...
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Note("f'8")

        ..  container:: example

            Iterates pitched leaves only:

            ..  container:: example

                >>> staff = abjad.Staff()
                >>> staff.extend("<c' bf'>8 <g' a'>8")
                >>> staff.extend("af'8 r8")
                >>> staff.extend("r8 gf'8")
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        \time 2/8
                        <c' bf'>8
                        <g' a'>8
                        af'8
                        r8
                        r8
                        gf'8
                    }

            ..  container:: example

                >>> for leaf in abjad.iterate(staff).leaves(pitched=True):
                ...     leaf
                ...
                Chord("<c' bf'>8")
                Chord("<g' a'>8")
                Note("af'8")
                Note("gf'8")

        ..  container:: example

            Iterates nonpitched leaves only:

            ..  container:: example

                >>> staff = abjad.Staff()
                >>> staff.extend("<c' bf'>8 <g' a'>8")
                >>> staff.extend("af'8 r8")
                >>> staff.extend("r8 gf'8")
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        \time 2/8
                        <c' bf'>8
                        <g' a'>8
                        af'8
                        r8
                        r8
                        gf'8
                    }

            ..  container:: example

                >>> for leaf in abjad.iterate(staff).leaves(pitched=False):
                ...     leaf
                ...
                Rest('r8')
                Rest('r8')

        ..  container:: example

            Iterates leaves in reverse:

            ..  container:: example

                >>> staff = abjad.Staff()
                >>> staff.extend("<c' bf'>8 <g' a'>8")
                >>> staff.extend("af'8 r8")
                >>> staff.extend("r8 gf'8")
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        \time 2/8
                        <c' bf'>8
                        <g' a'>8
                        af'8
                        r8
                        r8
                        gf'8
                    }

            ..  container:: example

                >>> for leaf in abjad.iterate(staff).leaves(reverse=True):
                ...     leaf
                ...
                Note("gf'8")
                Rest('r8')
                Rest('r8')
                Note("af'8")
                Chord("<g' a'>8")
                Chord("<c' bf'>8")

        ..  container:: example

            Excludes leaves with ``'RED'`` or ``'BLUE'`` annotations:

            ..  container:: example

                >>> staff = abjad.Staff()
                >>> staff.extend("<c' bf'>8 <g' a'>8")
                >>> staff.extend("af'8 r8")
                >>> staff.extend("r8 gf'8")
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.annotate(staff[0], 'RED', True)
                >>> abjad.annotate(staff[1], 'BLUE', True)
                >>> abjad.annotate(staff[2], 'GREEN', True)
                >>> abjad.annotate(staff[3], 'RED', True)
                >>> abjad.annotate(staff[4], 'BLUE', True)
                >>> abjad.annotate(staff[5], 'GREEN', True)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        \time 2/8
                        <c' bf'>8
                        <g' a'>8
                        af'8
                        r8
                        r8
                        gf'8
                    }

            ..  container:: example

                >>> for leaf in abjad.iterate(staff).leaves(
                ...     exclude=['RED', 'BLUE'],
                ...     ):
                ...     leaf
                ...
                Note("af'8")
                Note("gf'8")

        Returns generator.
        """
        from .Chord import Chord
        from .Leaf import Leaf
        from .MultimeasureRest import MultimeasureRest
        from .Note import Note
        from .Rest import Rest
        from .Skip import Skip
        prototype = prototype or Leaf
        if pitched is True:
            prototype = (Chord, Note)
        elif pitched is False:
            prototype = (MultimeasureRest, Rest, Skip)
        return self.components(
            prototype=prototype,
            exclude=exclude,
            do_not_iterate_grace_containers=do_not_iterate_grace_containers,
            grace_notes=grace_notes,
            reverse=reverse,
            )

    def logical_ties(
        self,
        *,
        exclude=None,
        grace_notes=None,
        nontrivial=None,
        pitched=None,
        reverse=False,
        ):
        r"""
        Iterates logical ties.

        ..  container:: example

            Iterates logical ties:

            ..  container:: example

                >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
                >>> staff = abjad.Staff(string)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'4
                        ~
                        \times 2/3 {
                            c'16
                            d'8
                        }
                        e'8
                        f'4
                        ~
                        f'16
                    }

            ..  container:: example

                >>> for logical_tie in abjad.iterate(staff).logical_ties():
                ...     logical_tie
                ...
                LogicalTie([Note("c'4"), Note("c'16")])
                LogicalTie([Note("d'8")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("f'4"), Note("f'16")])

        ..  container:: example

            Iterates pitched logical ties:

            ..  container:: example

                >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
                >>> staff = abjad.Staff(string)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'4
                        ~
                        \times 2/3 {
                            c'16
                            d'8
                        }
                        e'8
                        f'4
                        ~
                        f'16
                    }

            ..  container:: example

                >>> for logical_tie in abjad.iterate(staff).logical_ties(
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

                >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
                >>> staff = abjad.Staff(string)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'4
                        ~
                        \times 2/3 {
                            c'16
                            d'8
                        }
                        e'8
                        f'4
                        ~
                        f'16
                    }

            ..  container:: example

                >>> for logical_tie in abjad.iterate(staff).logical_ties(
                ...     nontrivial=True,
                ...     ):
                ...     logical_tie
                ...
                LogicalTie([Note("c'4"), Note("c'16")])
                LogicalTie([Note("f'4"), Note("f'16")])

        ..  container:: example

            Iterates trivial logical ties:

            ..  container:: example

                >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
                >>> staff = abjad.Staff(string)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'4
                        ~
                        \times 2/3 {
                            c'16
                            d'8
                        }
                        e'8
                        f'4
                        ~
                        f'16
                    }

            ..  container:: example

                >>> for logical_tie in abjad.iterate(staff).logical_ties(
                ...     nontrivial=False,
                ...     ):
                ...     logical_tie
                ...
                LogicalTie([Note("d'8")])
                LogicalTie([Note("e'8")])

        ..  container:: example

            Iterates logical ties together with grace notes and after grace
            notes:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> container = abjad.GraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, voice[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        [
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
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for item in abjad.iterate(voice).logical_ties():
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

            Iterates logical ties in reverse:

            ..  container:: example

                >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
                >>> staff = abjad.Staff(string)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'4
                        ~
                        \times 2/3 {
                            c'16
                            d'8
                        }
                        e'8
                        f'4
                        ~
                        f'16
                    }

            ..  container:: example

                >>> for logical_tie in abjad.iterate(staff).logical_ties(
                ...     reverse=True,
                ...     ):
                ...     logical_tie
                ...
                LogicalTie([Note("f'4"), Note("f'16")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("d'8")])
                LogicalTie([Note("c'4"), Note("c'16")])

        ..  container:: example

            REGRESSION: yields logical tie even when leaves are missing in
            input:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ ~ c' ~ c' d' ]")
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        ~
                        [
                        c'8
                        ~
                        c'8
                        d'8
                        ]
                    }

            ..  container:: example

                >>> selection = voice[:2]
                >>> for logical_tie in abjad.iterate(selection).logical_ties():
                ...     logical_tie
                ...
                LogicalTie([Note("c'8"), Note("c'8"), Note("c'8")])

        Returns generator.
        """
        yielded_logical_ties = set()
        for leaf in self.leaves(
            exclude=exclude,
            grace_notes=grace_notes,
            pitched=pitched,
            reverse=reverse,
            ):
            logical_tie = inspect(leaf).logical_tie()
            if leaf is not logical_tie.head:
                continue
            if (nontrivial is None or
                (nontrivial is True and not logical_tie.is_trivial) or
                (nontrivial is False and logical_tie.is_trivial)):
                if logical_tie not in yielded_logical_ties:
                    yielded_logical_ties.add(logical_tie)
                    yield logical_tie

    def out_of_range(self):
        r"""
        Iterates out-of-range notes and chords.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 r8 <d fs>8 r8")
            >>> violin = abjad.Violin()
            >>> abjad.attach(violin, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    r8
                    <d fs>8
                    r8
                }

            >>> for leaf in abjad.iterate(staff).out_of_range():
            ...     leaf
            ...
            Chord('<d fs>8')

        Returns generator.
        """
        for leaf in self.leaves(pitched=True):
            instrument = inspect(leaf).effective(Instrument)
            if instrument is None:
                raise ValueError('no instrument found.')
            if leaf not in instrument.pitch_range:
                yield leaf

    def pitch_pairs(self):
        r"""
        Iterates pitch pairs.

        ..  container:: example

            Iterates note pitch pairs:

            ..  container:: example

                >>> score = abjad.Score()
                >>> score.append(abjad.Staff("c'8 d' e' f' g'4"))
                >>> score.append(abjad.Staff("c4 a, g,"))
                >>> abjad.attach(abjad.Clef('bass'), score[1][0])
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        {
                            c'8
                            d'8
                            e'8
                            f'8
                            g'4
                        }
                        \new Staff
                        {
                            \clef "bass"
                            c4
                            a,4
                            g,4
                        }
                    >>

            ..  container:: example

                >>> for pair in abjad.iterate(score).pitch_pairs():
                ...     pair
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

            Iterates chord pitch pairs:

            ..  container:: example

                >>> staff = abjad.Staff("<c' d' e'>4 <f'' g''>4")

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        <c' d' e'>4
                        <f'' g''>4
                    }

            ..  container:: example

                >>> for pair in abjad.iterate(staff).pitch_pairs():
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
        """
        for leaf_pair in self.leaf_pairs():
            pitches = sorted(Iteration(leaf_pair[0]).pitches())
            enumerator = Enumerator(pitches)
            for pair in enumerator.yield_pairs():
                yield PitchSegment(pair)
            if isinstance(leaf_pair, set):
                pitches = sorted(Iteration(leaf_pair).pitches())
                enumerator = Enumerator(pitches)
                for pair in enumerator.yield_pairs():
                    yield PitchSegment(pair)
            else:
                pitches_1 = sorted(Iteration(leaf_pair[0]).pitches())
                pitches_2 = sorted(Iteration(leaf_pair[1]).pitches())
                sequences = [pitches_1, pitches_2]
                enumerator = Enumerator(sequences)
                for pair in enumerator.yield_outer_product():
                    yield PitchSegment(pair)
            pitches = sorted(Iteration(leaf_pair[1]).pitches())
            enumerator = Enumerator(pitches)
            for pair in enumerator.yield_pairs():
                yield PitchSegment(pair)

    def pitches(self):
        r"""
        Iterates pitches.

        ..  container:: example

            Iterates pitches in container:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> beam = abjad.Beam()
                >>> abjad.attach(beam, staff[:])
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'8
                        [
                        d'8
                        e'8
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for pitch in abjad.iterate(staff).pitches():
                ...     pitch
                ...
                NamedPitch("c'")
                NamedPitch("d'")
                NamedPitch("e'")
                NamedPitch("f'")

        ..  container:: example

            Iterates pitches in spanner:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> beam = abjad.Beam()
                >>> abjad.attach(beam, staff[:])
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'8
                        [
                        d'8
                        e'8
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for pitch in abjad.iterate(beam).pitches():
                ...     pitch
                ...
                NamedPitch("c'")
                NamedPitch("d'")
                NamedPitch("e'")
                NamedPitch("f'")

        ..  container:: example

            Iterates pitches in pitch set:

            ..  container:: example

                >>> pitch_set = abjad.PitchSet([0, 2, 4, 5])

            ..  container:: example

                >>> for pitch in abjad.iterate(pitch_set).pitches():
                ...     pitch
                ...
                NumberedPitch(0)
                NumberedPitch(2)
                NumberedPitch(4)
                NumberedPitch(5)

        ..  container:: example

            Iterates different types of object in tuple:

            ..  container:: example

                >>> pitches = (
                ...     abjad.NamedPitch("c'"),
                ...     abjad.Note("d'4"),
                ...     abjad.Chord("<e' fs' g>4"),
                ...     )

            ..  container:: example

                >>> for pitch in abjad.iterate(pitches).pitches():
                ...     pitch
                ...
                NamedPitch("c'")
                NamedPitch("d'")
                NamedPitch('g')
                NamedPitch("e'")
                NamedPitch("fs'")

        Returns generator.
        """
        from abjad.spanners.Spanner import Spanner
        from .Chord import Chord
        if isinstance(self.client, Pitch):
            pitch = NamedPitch(self.client)
            yield pitch
        result = []
        try:
            result.extend(self.client.pitches)
        except AttributeError:
            pass
        if isinstance(self.client, Chord):
            result.extend(self.client.written_pitches)
        elif isinstance(self.client, Spanner):
            for leaf in self.client.leaves:
                try:
                    result.append(leaf.written_pitch)
                except AttributeError:
                    pass
                try:
                    result.extedn(leaf.written_pitches)
                except AttributeError:
                    pass
        elif isinstance(self.client, PitchSet):
            result.extend(sorted(list(self.client)))
        elif isinstance(self.client, (list, tuple, set)):
            for item in self.client:
                for pitch_ in Iteration(item).pitches():
                    result.append(pitch_)
        else:
            for leaf in Iteration(self.client).leaves():
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

    def spanners(self, prototype=None, reverse=False):
        r"""
        Iterates spanners.

        ..  container:: example

            Iterates spanners:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 f'8 b'8 c''8")
                >>> abjad.attach(abjad.Slur(), staff[:4])
                >>> abjad.attach(abjad.Slur(), staff[4:])
                >>> abjad.attach(abjad.Beam(), staff[:])
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'8
                        [
                        (
                        d'8
                        e'8
                        f'8
                        )
                        g'8
                        (
                        a'8
                        f'8
                        b'8
                        c''8
                        ]
                        )
                    }

            ..  container:: example

                >>> for spanner in abjad.iterate(staff).spanners():
                ...     spanner
                ...
                Beam("c'8, d'8, ... [5] ..., b'8, c''8", durations=(), span_beam_count=1)
                Slur("c'8, d'8, e'8, f'8")
                Slur("g'8, a'8, f'8, b'8, c''8")

        ..  container:: example

            Iterates spanners in reverse:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 f'8 b'8 c''8")
                >>> abjad.attach(abjad.Slur(), staff[:4])
                >>> abjad.attach(abjad.Slur(), staff[4:])
                >>> abjad.attach(abjad.Beam(), staff[:])
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'8
                        [
                        (
                        d'8
                        e'8
                        f'8
                        )
                        g'8
                        (
                        a'8
                        f'8
                        b'8
                        c''8
                        ]
                        )
                    }

            ..  container:: example

                >>> for spanner in abjad.iterate(staff).spanners(reverse=True):
                ...     spanner
                ...
                Beam("c'8, d'8, ... [5] ..., b'8, c''8", durations=(), span_beam_count=1)
                Slur("g'8, a'8, f'8, b'8, c''8")
                Slur("c'8, d'8, e'8, f'8")

        Returns generator.
        """
        visited_spanners = set()
        for component in self.components(reverse=reverse):
            spanners = inspect(component).spanners(
                prototype=prototype,
                )
            spanners = sorted(spanners,
                key=lambda x: (
                    type(x).__name__,
                    inspect(x).timespan(),
                    ),
                )
            for spanner in spanners:
                if spanner in visited_spanners:
                    continue
                visited_spanners.add(spanner)
                yield spanner

    def timeline(
        self,
        prototype=None,
        *,
        exclude=None,
        reverse=False,
        ):
        r"""
        Iterates timeline.

        ..  container:: example

            Timeline-iterates leaves:

            ..  container:: example

                >>> score = abjad.Score()
                >>> score.append(abjad.Staff("c'4 d'4 e'4 f'4"))
                >>> score.append(abjad.Staff("g'8 a'8 b'8 c''8"))
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        {
                            c'4
                            d'4
                            e'4
                            f'4
                        }
                        \new Staff
                        {
                            g'8
                            a'8
                            b'8
                            c''8
                        }
                    >>

            ..  container:: example

                >>> for leaf in abjad.iterate(score).timeline():
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

                >>> score = abjad.Score()
                >>> score.append(abjad.Staff("c'4 d'4 e'4 f'4"))
                >>> score.append(abjad.Staff("g'8 a'8 b'8 c''8"))
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        {
                            c'4
                            d'4
                            e'4
                            f'4
                        }
                        \new Staff
                        {
                            g'8
                            a'8
                            b'8
                            c''8
                        }
                    >>

        ..  container:: example

            Timeline-iterates leaves together grace notes:

            ..  container:: example

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> container = abjad.GraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'8
                        [
                        \grace {
                            cf''16
                            bf'16
                        }
                        d'8
                        e'8
                        f'8
                        ]
                    }

            ..  container:: example

                >>> for component in abjad.iterate(voice).timeline():
                ...     component
                ...
                Note("c'8")
                Note("cf''16")
                Note("bf'16")
                Note("d'8")
                Note("e'8")
                Note("f'8")

        Iterates leaves when ``prototype`` is none.
        """
        components = self.leaves(
            prototype=prototype,
            exclude=exclude,
            )
        components = list(components)
        components.sort(key=lambda _: inspect(_).timespan().start_offset)
        offset_to_components = OrderedDict()
        for component in components:
            start_offset = inspect(component).timespan().start_offset
            if start_offset not in offset_to_components:
                offset_to_components[start_offset] = []
        for component in components:
            start_offset = inspect(component).timespan().start_offset
            offset_to_components[start_offset].append(component)
        components = []
        for start_offset, list_ in offset_to_components.items():
            components.extend(list_)
        if reverse:
            components.reverse()
        return tuple(components)

    def vertical_moments(self, reverse=False):
        r'''
        Iterates vertical moments.

        ..  container:: example

            Iterates vertical moments:

            ..  container:: example

                >>> score = abjad.Score([])
                >>> staff = abjad.Staff(r"\times 4/3 { d''8 c''8 b'8 }")
                >>> score.append(staff)
                >>> staff_group = abjad.StaffGroup([])
                >>> staff_group.lilypond_type = 'PianoStaff'
                >>> staff_group.append(abjad.Staff("a'4 g'4"))
                >>> staff_group.append(abjad.Staff(r"""\clef "bass" f'8 e'8 d'8 c'8"""))
                >>> score.append(staff_group)
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 4/3 {
                                d''8
                                c''8
                                b'8
                            }
                        }
                        \new PianoStaff
                        <<
                            \new Staff
                            {
                                a'4
                                g'4
                            }
                            \new Staff
                            {
                                \clef "bass"
                                f'8
                                e'8
                                d'8
                                c'8
                            }
                        >>
                    >>

            ..  container:: example

                >>> for vertical_moment in abjad.iterate(score).vertical_moments():
                ...     vertical_moment.leaves
                ...
                Selection([Note("d''8"), Note("a'4"), Note("f'8")])
                Selection([Note("d''8"), Note("a'4"), Note("e'8")])
                Selection([Note("c''8"), Note("a'4"), Note("e'8")])
                Selection([Note("c''8"), Note("g'4"), Note("d'8")])
                Selection([Note("b'8"), Note("g'4"), Note("d'8")])
                Selection([Note("b'8"), Note("g'4"), Note("c'8")])

                >>> for vertical_moment in abjad.iterate(staff_group).vertical_moments():
                ...     vertical_moment.leaves
                ...
                Selection([Note("a'4"), Note("f'8")])
                Selection([Note("a'4"), Note("e'8")])
                Selection([Note("g'4"), Note("d'8")])
                Selection([Note("g'4"), Note("c'8")])

        ..  container:: example

            Iterates vertical moments in reverse:

            ..  container:: example

                >>> score = abjad.Score([])
                >>> staff = abjad.Staff(r"\times 4/3 { d''8 c''8 b'8 }")
                >>> score.append(staff)
                >>> staff_group = abjad.StaffGroup([])
                >>> staff_group.lilypond_type = 'PianoStaff'
                >>> staff_group.append(abjad.Staff("a'4 g'4"))
                >>> staff_group.append(abjad.Staff(r"""\clef "bass" f'8 e'8 d'8 c'8"""))
                >>> score.append(staff_group)
                >>> abjad.show(score) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(score)
                    \new Score
                    <<
                        \new Staff
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 4/3 {
                                d''8
                                c''8
                                b'8
                            }
                        }
                        \new PianoStaff
                        <<
                            \new Staff
                            {
                                a'4
                                g'4
                            }
                            \new Staff
                            {
                                \clef "bass"
                                f'8
                                e'8
                                d'8
                                c'8
                            }
                        >>
                    >>

            ..  container:: example

                >>> agent = abjad.iterate(score)
                >>> for vertical_moment in agent.vertical_moments(
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

                >>> agent = abjad.iterate(staff_group)
                >>> for vertical_moment in agent.vertical_moments(
                ...     reverse=True,
                ...     ):
                ...     vertical_moment.leaves
                ...
                Selection([Note("g'4"), Note("c'8")])
                Selection([Note("g'4"), Note("d'8")])
                Selection([Note("a'4"), Note("e'8")])
                Selection([Note("a'4"), Note("f'8")])

        Returns tuple.
        '''
        from .Selection import Selection
        from .VerticalMoment import VerticalMoment
        moments = []
        components = list(self.components())
        components.sort(key=lambda _: inspect(_).timespan().start_offset)
        offset_to_components = OrderedDict()
        for component in components:
            start_offset = inspect(component).timespan().start_offset
            if start_offset not in offset_to_components:
                offset_to_components[start_offset] = []
        # TODO: optimize with bisect
        for component in components:
            inserted = False
            timespan = inspect(component).timespan()
            for offset, list_ in offset_to_components.items():
                if (timespan.start_offset <= offset < timespan.stop_offset and
                    component not in list_):
                    list_.append(component)
                    inserted = True
                elif inserted is True:
                    break
        moments = []
        for offset, list_ in offset_to_components.items():
            list_.sort(key=lambda _: inspect(_).parentage().score_index())
            moment = VerticalMoment(
                components=list_,
                offset=offset,
                )
            moments.append(moment)
        if reverse is True:
            moments.reverse()
        return tuple(moments)
