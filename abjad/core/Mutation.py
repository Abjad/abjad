from abjad import enums
from abjad.indicators.TimeSignature import TimeSignature
from abjad.meter import Meter
from abjad.pitch.NamedInterval import NamedInterval
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.top.inspect import inspect
from abjad.top.iterate import iterate
from abjad.top.select import select
from abjad.top.sequence import sequence
from abjad.utilities.Duration import Duration

from .Chord import Chord
from .Component import Component
from .Container import Container
from .Leaf import Leaf
from .Note import Note
from .Selection import Selection


class Mutation(object):
    """
    Mutation.

    ..  container:: example

        Creates mutation for last two notes in staff:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.mutate(staff[2:])
        Mutation(client=Selection([Note("d'4"), Note("f'4")]))

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Collaborators"

    __slots__ = ("_client",)

    ### INITIALIZER ###

    def __init__(self, client=None):
        self._client = client

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        """
        Gets client.

        Returns selection or component.
        """
        return self._client

    ### PUBLIC METHODS ###

    def copy(self):
        r"""
        Copies client.

        ..  container:: example

            Copies explicit clefs:

            >>> staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
            >>> clef = abjad.Clef('treble')
            >>> abjad.attach(clef, staff[0])
            >>> clef = abjad.Clef('bass')
            >>> abjad.attach(clef, staff[4])
            >>> copied_notes = abjad.mutate(staff[:2]).copy()
            >>> staff.extend(copied_notes)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "treble"
                    c'8
                    cs'8
                    d'8
                    ef'8
                    \clef "bass"
                    e'8
                    f'8
                    fs'8
                    g'8
                    \clef "treble"
                    c'8
                    cs'8
                }

        ..  container:: example

            Does not copy implicit clefs:

            >>> staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
            >>> clef = abjad.Clef('treble')
            >>> abjad.attach(clef, staff[0])
            >>> clef = abjad.Clef('bass')
            >>> abjad.attach(clef, staff[4])
            >>> copied_notes = abjad.mutate(staff[2:4]).copy()
            >>> staff.extend(copied_notes)

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "treble"
                    c'8
                    cs'8
                    d'8
                    ef'8
                    \clef "bass"
                    e'8
                    f'8
                    fs'8
                    g'8
                    d'8
                    ef'8
                }

        ..  container:: example

            Copy components one time:

            >>> staff = abjad.Staff(r"c'8 d'8 e'8 f'8")
            >>> staff.extend(r"g'8 a'8 b'8 c''8")
            >>> time_signature = abjad.TimeSignature((2, 4))
            >>> abjad.attach(time_signature, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 2/4
                    c'8
                    d'8
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8
                    c''8
                }

            >>> selection = staff[2:4]
            >>> result = selection._copy()
            >>> new_staff = abjad.Staff(result)
            >>> abjad.show(new_staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(new_staff)
                \new Staff
                {
                    e'8
                    f'8
                }

            >>> staff[2] is new_staff[0]
            False

        Returns selection of new components.
        """
        if isinstance(self.client, Component):
            selection = select(self.client)
        else:
            selection = self.client
        result = selection._copy()
        if isinstance(self.client, Component):
            if len(result) == 1:
                result = result[0]
        return result

    def eject_contents(self):
        r"""
        Ejects contents from outside-of-score container.

        ..  container:: example

            Ejects leaves from container:

            >>> container = abjad.Container("c'4 ~ c'4 d'4 ~ d'4")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'4
                    ~
                    c'4
                    d'4
                    ~
                    d'4
                }

            Returns container contents as a selection with spanners preserved:

            >>> contents = abjad.mutate(container).eject_contents()
            >>> contents
            Selection([Note("c'4"), Note("c'4"), Note("d'4"), Note("d'4")])

            Container contents can be safely added to a new container:

            >>> staff = abjad.Staff(contents, lilypond_type='RhythmicStaff')
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new RhythmicStaff
                {
                    c'4
                    ~
                    c'4
                    d'4
                    ~
                    d'4
                }

            New container is well formed:

            >>> abjad.inspect(staff).wellformed()
            True

            Old container is empty:

            >>> container
            Container()

        Returns container contents as selection.
        """
        return self.client._eject_contents()

    def extract(self, scale_contents=False):
        r"""
        Extracts mutation client from score.

        Leaves children of mutation client in score.

        ..  container:: example

            Extract tuplets:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Tuplet((3, 2), "c'4 e'4"))
            >>> staff.append(abjad.Tuplet((3, 2), "d'4 f'4"))
            >>> leaves = abjad.select(staff).leaves()
            >>> time_signature = abjad.TimeSignature((3, 4))
            >>> abjad.attach(time_signature, leaves[0])
            >>> abjad.hairpin('p < f', leaves)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/2 {
                        \time 3/4
                        c'4
                        \p
                        \<
                        e'4
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/2 {
                        d'4
                        f'4
                        \f
                    }
                }

            >>> empty_tuplet = abjad.mutate(staff[-1]).extract()
            >>> empty_tuplet = abjad.mutate(staff[0]).extract()
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 3/4
                    c'4
                    \p
                    \<
                    e'4
                    d'4
                    f'4
                    \f
                }

        ..  container:: example

            Scales tuplet contents and then extracts tuplet:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Tuplet((3, 2), "c'4 e'4"))
            >>> staff.append(abjad.Tuplet((3, 2), "d'4 f'4"))
            >>> leaves = abjad.select(staff).leaves()
            >>> abjad.hairpin('p < f', leaves)
            >>> time_signature = abjad.TimeSignature((3, 4))
            >>> abjad.attach(time_signature, leaves[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/2 {
                        \time 3/4
                        c'4
                        \p
                        \<
                        e'4
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/2 {
                        d'4
                        f'4
                        \f
                    }
                }

            >>> empty_tuplet = abjad.mutate(staff[-1]).extract(
            ...     scale_contents=True)
            >>> empty_tuplet = abjad.mutate(staff[0]).extract(
            ...     scale_contents=True)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 3/4
                    c'4.
                    \p
                    \<
                    e'4.
                    d'4.
                    f'4.
                    \f
                }

        ..  container:: example

            Extracting out-of-score component does nothing and returns
            component:

            >>> tuplet = abjad.Tuplet((3, 2), "c'4 e'4")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    c'4
                    e'4
                }

            >>> abjad.mutate(tuplet).extract()
            Tuplet(Multiplier(3, 2), "c'4 e'4")

            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    c'4
                    e'4
                }

        Returns mutation client.
        """
        return self.client._extract(scale_contents=scale_contents)

    def fuse(self):
        r"""
        Fuses mutation client.

        ..  container:: example

            Fuses in-score leaves:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.mutate(staff[1:]).fuse()
            Selection([Note("d'4.")])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    d'4.
                }

        ..  container:: example

            Fuses parent-contiguous tuplets in selection:

            >>> tuplet_1 = abjad.Tuplet((2, 3), "c'8 d' e'")
            >>> abjad.beam(tuplet_1[:])
            >>> tuplet_2 = abjad.Tuplet((2, 3), "c'16 d' e'")
            >>> abjad.slur(tuplet_2[:])
            >>> staff = abjad.Staff([tuplet_1, tuplet_2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 2/3 {
                        c'8
                        [
                        d'8
                        e'8
                        ]
                    }
                    \times 2/3 {
                        c'16
                        (
                        d'16
                        e'16
                        )
                    }
                }

            >>> tuplets = staff[:]
            >>> abjad.mutate(tuplets).fuse()
            Tuplet(Multiplier(2, 3), "c'8 d'8 e'8 c'16 d'16 e'16")
            >>> abjad.show(staff) #doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 2/3 {
                        c'8
                        [
                        d'8
                        e'8
                        ]
                        c'16
                        (
                        d'16
                        e'16
                        )
                    }
                }

            Returns new tuplet in selection.

            Fuses zero or more parent-contiguous ``tuplets``.

            Allows in-score ``tuplets``.

            Allows outside-of-score ``tuplets``.

            All ``tuplets`` must carry the same multiplier.

            All ``tuplets`` must be of the same type.

        ..  container:: example

            REGRESSION. Trims tie from fused note:

            >>> staff = abjad.Staff("d'8 ~ d'32 ~ d'16 d'32")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    d'8
                    ~
                    d'32
                    ~
                    d'16
                    d'32
                }

            >>> logical_tie = abjad.select(staff[0]).logical_tie()
            >>> abjad.mutate(logical_tie).fuse()
            Selection([Note("d'8..")])

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    d'8..
                    d'32
                }

            >>> abjad.inspect(staff[0]).has_indicator(abjad.Tie)
            False

        Returns selection.
        """
        if isinstance(self.client, Component):
            selection = select(self.client)
            return selection._fuse()
        elif (
            isinstance(self.client, Selection)
            and self.client.are_contiguous_logical_voice()
        ):
            selection = select(self.client)
            return selection._fuse()

    def replace(self, recipients, wrappers=False):
        r"""
        Replaces mutation client (and contents of mutation client) with
        ``recipients``.

        ..  container:: example

            Replaces in-score tuplet (and children of tuplet) with notes.
            Functions exactly the same as container setitem:

            >>> tuplet_1 = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
            >>> tuplet_2 = abjad.Tuplet((2, 3), "d'4 e'4 f'4")
            >>> staff = abjad.Staff([tuplet_1, tuplet_2])
            >>> leaves = abjad.select(staff).leaves()
            >>> abjad.hairpin('p < f', leaves)
            >>> abjad.slur(leaves)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 2/3 {
                        c'4
                        \p
                        \<
                        (
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        d'4
                        e'4
                        f'4
                        \f
                        )
                    }
                }

            >>> maker = abjad.NoteMaker()
            >>> notes = maker("c' d' e' f' c' d' e' f'", (1, 16))
            >>> abjad.mutate([tuplet_1]).replace(notes)
            >>> abjad.attach(abjad.Dynamic('p'), staff[0])
            >>> abjad.attach(abjad.StartHairpin('<'), staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'16
                    \p
                    \<
                    d'16
                    e'16
                    f'16
                    c'16
                    d'16
                    e'16
                    f'16
                    \times 2/3 {
                        d'4
                        e'4
                        f'4
                        \f
                        )
                    }
                }

            Preserves both hairpin and slur.

        ..  container:: example

            Copies no wrappers when ``wrappers`` is false:

            >>> staff = abjad.Staff("c'2 f'4 g'")
            >>> abjad.attach(abjad.Clef('alto'), staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    c'2
                    f'4
                    g'4
                }

            >>> for leaf in staff:
            ...     leaf, abjad.inspect(leaf).effective(abjad.Clef)
            ...
            (Note("c'2"), Clef('alto'))
            (Note("f'4"), Clef('alto'))
            (Note("g'4"), Clef('alto'))

            >>> chord = abjad.Chord("<d' e'>2")
            >>> abjad.mutate(staff[0]).replace(chord)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    <d' e'>2
                    f'4
                    g'4
                }

            >>> for leaf in staff:
            ...     leaf, abjad.inspect(leaf).effective(abjad.Clef)
            ...
            (Chord("<d' e'>2"), None)
            (Note("f'4"), None)
            (Note("g'4"), None)

            >>> abjad.inspect(staff).wellformed()
            True

        ..  container:: example

            Set ``wrappers`` to true to copy all wrappers from one leaf to
            another leaf (and avoid full-score update). Only works from one
            leaf to another leaf:

            >>> staff = abjad.Staff("c'2 f'4 g'")
            >>> abjad.attach(abjad.Clef('alto'), staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    c'2
                    f'4
                    g'4
                }

            >>> for leaf in staff:
            ...     leaf, abjad.inspect(leaf).effective(abjad.Clef)
            ...
            (Note("c'2"), Clef('alto'))
            (Note("f'4"), Clef('alto'))
            (Note("g'4"), Clef('alto'))

            >>> chord = abjad.Chord("<d' e'>2")
            >>> abjad.mutate(staff[0]).replace(chord, wrappers=True)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    <d' e'>2
                    f'4
                    g'4
                }

            >>> for leaf in staff:
            ...     leaf, abjad.inspect(leaf).effective(abjad.Clef)
            ...
            (Chord("<d' e'>2"), Clef('alto'))
            (Note("f'4"), Clef('alto'))
            (Note("g'4"), Clef('alto'))

            >>> abjad.inspect(staff).wellformed()
            True

        ..  container:: example

            ..  todo:: Fix.

            Introduces duplicate ties:

            >>> staff = abjad.Staff("c'2 ~ c'2")
            >>> maker = abjad.NoteMaker()
            >>> tied_notes = maker(0, abjad.Duration(5, 8))
            >>> abjad.mutate(staff[:1]).replace(tied_notes)

            >>> abjad.f(staff)
            \new Staff
            {
                c'2
                ~
                c'8
                c'2
            }

        Returns none.
        """
        if isinstance(self.client, Selection):
            donors = self.client
        else:
            donors = select(self.client)
        assert donors.are_contiguous_same_parent()
        if not isinstance(recipients, Selection):
            recipients = select(recipients)
        assert recipients.are_contiguous_same_parent()
        if not donors:
            return
        if wrappers is True:
            if 1 < len(donors) or not isinstance(donors[0], Leaf):
                message = f"set wrappers only with single leaf: {donors!r}."
                raise Exception(message)
            if 1 < len(recipients) or not isinstance(recipients[0], Leaf):
                message = f"set wrappers only with single leaf: {recipients!r}."
                raise Exception(message)
            donor = donors[0]
            wrappers = inspect(donor).wrappers()
            recipient = recipients[0]
        parent, start, stop = donors._get_parent_and_start_stop_indices()
        assert parent is not None, repr(donors)
        parent.__setitem__(slice(start, stop + 1), recipients)
        if not wrappers:
            return
        for wrapper in wrappers:
            # bypass Wrapper._bind_component()
            # to avoid full-score update / traversal;
            # this works because one-to-one leaf replacement
            # including all (persistent) indicators
            # doesn't change score structure:
            donor._wrappers.remove(wrapper)
            wrapper._component = recipient
            recipient._wrappers.append(wrapper)
            context = wrapper._find_correct_effective_context()
            if context is not None:
                context._dependent_wrappers.append(wrapper)

    def rewrite_meter(
        self,
        meter,
        boundary_depth=None,
        initial_offset=None,
        maximum_dot_count=None,
        rewrite_tuplets=True,
    ):
        r"""
        Rewrites the contents of logical ties in an expression to match
        ``meter``.

        ..  container:: example

            Rewrites the contents of a measure in a staff using the default
            meter for that measure's time signature:

            >>> string = "abj: | 2/4 c'2 ~ |"
            >>> string += "| 4/4 c'32 d'2.. ~ d'16 e'32 ~ |"
            >>> string += "| 2/4 e'2 |"
            >>> staff = abjad.Staff(string)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 2/4
                        c'2
                        ~
                    }
                    {
                        \time 4/4
                        c'32
                        d'2..
                        ~
                        d'16
                        e'32
                        ~
                    }
                    {
                        \time 2/4
                        e'2
                    }
                }

            >>> meter = abjad.Meter((4, 4))
            >>> print(meter.pretty_rtm_format)
            (4/4 (
                1/4
                1/4
                1/4
                1/4))

            >>> abjad.mutate(staff[1][:]).rewrite_meter(meter)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 2/4
                        c'2
                        ~
                    }
                    {
                        \time 4/4
                        c'32
                        d'8..
                        ~
                        d'2
                        ~
                        d'8..
                        e'32
                        ~
                    }
                    {
                        \time 2/4
                        e'2
                    }
                }

        ..  container:: example

            Rewrites the contents of a measure in a staff using a custom meter:

            >>> staff = abjad.Staff(string)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 2/4
                        c'2
                        ~
                    }
                    {
                        \time 4/4
                        c'32
                        d'2..
                        ~
                        d'16
                        e'32
                        ~
                    }
                    {
                        \time 2/4
                        e'2
                    }
                }

            >>> rtm = '(4/4 ((2/4 (1/4 1/4)) (2/4 (1/4 1/4))))'
            >>> meter = abjad.Meter(rtm)
            >>> print(meter.pretty_rtm_format) # doctest: +SKIP
            (4/4 (
                (2/4 (
                    1/4
                    1/4))
                (2/4 (
                    1/4
                    1/4))))

            >>> abjad.mutate(staff[1][:]).rewrite_meter(meter)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 2/4
                        c'2
                        ~
                    }
                    {
                        \time 4/4
                        c'32
                        d'4...
                        ~
                        d'4...
                        e'32
                        ~
                    }
                    {
                        \time 2/4
                        e'2
                    }
                }

        ..  container:: example

            Limit the maximum number of dots per leaf using
            ``maximum_dot_count``:

            >>> string = "abj: | 3/4 c'32 d'8 e'8 fs'4... |"
            >>> staff = abjad.Staff(string)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 3/4
                        c'32
                        d'8
                        e'8
                        fs'4...
                    }
                }

            Without constraining the ``maximum_dot_count``:

            >>> measure = staff[0]
            >>> time_signature = abjad.inspect(measure[0]).indicator(
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.mutate(measure[:]).rewrite_meter(time_signature)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 3/4
                        c'32
                        d'16.
                        ~
                        d'32
                        e'16.
                        ~
                        e'32
                        fs'4...
                    }
                }

            Constraining the ``maximum_dot_count`` to ``2``:

            >>> staff = abjad.Staff(string)
            >>> measure = staff[0]
            >>> time_signature = abjad.inspect(measure[0]).indicator(
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.mutate(measure[:]).rewrite_meter(
            ...     time_signature,
            ...     maximum_dot_count=2,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 3/4
                        c'32
                        d'16.
                        ~
                        d'32
                        e'16.
                        ~
                        e'32
                        fs'8..
                        ~
                        fs'4
                    }
                }

            Constraining the ``maximum_dot_count`` to ``1``:

            >>> staff = abjad.Staff(string)
            >>> measure = staff[0]
            >>> time_signature = abjad.inspect(measure[0]).indicator(
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.mutate(measure[:]).rewrite_meter(
            ...     time_signature,
            ...     maximum_dot_count=1,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 3/4
                        c'32
                        d'16.
                        ~
                        d'32
                        e'16.
                        ~
                        e'32
                        fs'16.
                        ~
                        fs'8
                        ~
                        fs'4
                    }
                }

            Constraining the ``maximum_dot_count`` to ``0``:

            >>> staff = abjad.Staff(string)
            >>> measure = staff[0]
            >>> time_signature = abjad.inspect(measure[0]).indicator(
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.mutate(measure[:]).rewrite_meter(
            ...     time_signature,
            ...     maximum_dot_count=0,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 3/4
                        c'32
                        d'16
                        ~
                        d'32
                        ~
                        d'32
                        e'16
                        ~
                        e'32
                        ~
                        e'32
                        fs'16
                        ~
                        fs'32
                        ~
                        fs'8
                        ~
                        fs'4
                    }
                }

        ..  container:: example

            Split logical ties at different depths of the ``Meter``, if those
            logical ties cross any offsets at that depth, but do not also both
            begin and end at any of those offsets.

            Consider the default meter for ``9/8``:

            >>> meter = abjad.Meter((9, 8))
            >>> print(meter.pretty_rtm_format)
            (9/8 (
                (3/8 (
                    1/8
                    1/8
                    1/8))
                (3/8 (
                    1/8
                    1/8
                    1/8))
                (3/8 (
                    1/8
                    1/8
                    1/8))))

            We can establish that meter without specifying
            a ``boundary_depth``:

            >>> string = "abj: | 9/8 c'2 d'2 e'8 |"
            >>> staff = abjad.Staff(string)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 9/8
                        c'2
                        d'2
                        e'8
                    }
                }

            >>> measure = staff[0]
            >>> time_signature = abjad.inspect(measure[0]).indicator(
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.mutate(measure[:]).rewrite_meter(time_signature)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 9/8
                        c'2
                        d'4
                        ~
                        d'4
                        e'8
                    }
                }

            With a ``boundary_depth`` of `1`, logical ties which cross any
            offsets created by nodes with a depth of `1` in this Meter's rhythm
            tree - i.e.  `0/8`, `3/8`, `6/8` and `9/8` - which do not also
            begin and end at any of those offsets, will be split:

            >>> staff = abjad.Staff(string)
            >>> measure = staff[0]
            >>> time_signature = abjad.inspect(measure[0]).indicator(
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.mutate(measure[:]).rewrite_meter(
            ...     time_signature,
            ...     boundary_depth=1,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 9/8
                        c'4.
                        ~
                        c'8
                        d'4
                        ~
                        d'4
                        e'8
                    }
                }

            For this `9/8` meter, and this input notation, A ``boundary_depth``
            of `2` causes no change, as all logical ties already align to
            multiples of `1/8`:

            >>> staff = abjad.Staff(string)
            >>> measure = staff[0]
            >>> time_signature = abjad.inspect(measure[0]).indicator(
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.mutate(measure[:]).rewrite_meter(
            ...     time_signature,
            ...     boundary_depth=2,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 9/8
                        c'2
                        d'4
                        ~
                        d'4
                        e'8
                    }
                }

        ..  container:: example

            Comparison of `3/4` and `6/8`, at ``boundary_depths`` of 0 and 1:

            >>> triple = "abj: | 3/4 2 4 || 3/4 4 2 || 3/4 4. 4. |"
            >>> triple += "| 3/4 2 ~ 8 8 || 3/4 8 8 ~ 2 |"
            >>> duples = "abj: | 6/8 2 4 || 6/8 4 2 || 6/8 4. 4. |"
            >>> duples += "| 6/8 2 ~ 8 8 || 6/8 8 8 ~ 2 |"
            >>> score = abjad.Score([
            ...     abjad.Staff(triple),
            ...     abjad.Staff(duples),
            ...     ])

            In order to see the different time signatures on each staff,
            we need to move some engravers from the Score context to the
            Staff context:

            >>> engravers = [
            ...     'Timing_translator',
            ...     'Time_signature_engraver',
            ...     'Default_bar_line_engraver',
            ...     ]
            >>> score.remove_commands.extend(engravers)
            >>> score[0].consists_commands.extend(engravers)
            >>> score[1].consists_commands.extend(engravers)
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                \with
                {
                    \remove Timing_translator
                    \remove Time_signature_engraver
                    \remove Default_bar_line_engraver
                }
                <<
                    \new Staff
                    \with
                    {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    }
                    {
                        {
                            \time 3/4
                            c'2
                            c'4
                        }
                        {
                            \time 3/4
                            c'4
                            c'2
                        }
                        {
                            \time 3/4
                            c'4.
                            c'4.
                        }
                        {
                            \time 3/4
                            c'2
                            ~
                            c'8
                            c'8
                        }
                        {
                            \time 3/4
                            c'8
                            c'8
                            ~
                            c'2
                        }
                    }
                    \new Staff
                    \with
                    {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    }
                    {
                        {
                            \time 6/8
                            c'2
                            c'4
                        }
                        {
                            \time 6/8
                            c'4
                            c'2
                        }
                        {
                            \time 6/8
                            c'4.
                            c'4.
                        }
                        {
                            \time 6/8
                            c'2
                            ~
                            c'8
                            c'8
                        }
                        {
                            \time 6/8
                            c'8
                            c'8
                            ~
                            c'2
                        }
                    }
                >>

            Here we establish a meter without specifying any boundary depth:

            >>> for staff in score:
            ...     for container in staff:
            ...         leaf = abjad.inspect(container).leaf(0)
            ...         time_signature = abjad.inspect(leaf).indicator(
            ...             abjad.TimeSignature
            ...             )
            ...         abjad.mutate(container[:]).rewrite_meter(time_signature)
            ...
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                \with
                {
                    \remove Timing_translator
                    \remove Time_signature_engraver
                    \remove Default_bar_line_engraver
                }
                <<
                    \new Staff
                    \with
                    {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    }
                    {
                        {
                            \time 3/4
                            c'2
                            c'4
                        }
                        {
                            \time 3/4
                            c'4
                            c'2
                        }
                        {
                            \time 3/4
                            c'4.
                            c'4.
                        }
                        {
                            \time 3/4
                            c'2
                            ~
                            c'8
                            c'8
                        }
                        {
                            \time 3/4
                            c'8
                            c'8
                            ~
                            c'2
                        }
                    }
                    \new Staff
                    \with
                    {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    }
                    {
                        {
                            \time 6/8
                            c'2
                            c'4
                        }
                        {
                            \time 6/8
                            c'4
                            c'2
                        }
                        {
                            \time 6/8
                            c'4.
                            c'4.
                        }
                        {
                            \time 6/8
                            c'4.
                            ~
                            c'4
                            c'8
                        }
                        {
                            \time 6/8
                            c'8
                            c'4
                            ~
                            c'4.
                        }
                    }
                >>

            Here we reestablish meter at a boundary depth of `1`:

            >>> for staff in score:
            ...     for container in staff:
            ...         leaf = abjad.inspect(container).leaf(0)
            ...         time_signature = abjad.inspect(leaf).indicator(
            ...             abjad.TimeSignature
            ...             )
            ...         abjad.mutate(container[:]).rewrite_meter(
            ...             time_signature,
            ...             boundary_depth=1,
            ...             )
            ...
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                \with
                {
                    \remove Timing_translator
                    \remove Time_signature_engraver
                    \remove Default_bar_line_engraver
                }
                <<
                    \new Staff
                    \with
                    {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    }
                    {
                        {
                            \time 3/4
                            c'2
                            c'4
                        }
                        {
                            \time 3/4
                            c'4
                            c'2
                        }
                        {
                            \time 3/4
                            c'4
                            ~
                            c'8
                            c'8
                            ~
                            c'4
                        }
                        {
                            \time 3/4
                            c'2
                            ~
                            c'8
                            c'8
                        }
                        {
                            \time 3/4
                            c'8
                            c'8
                            ~
                            c'2
                        }
                    }
                    \new Staff
                    \with
                    {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    }
                    {
                        {
                            \time 6/8
                            c'4.
                            ~
                            c'8
                            c'4
                        }
                        {
                            \time 6/8
                            c'4
                            c'8
                            ~
                            c'4.
                        }
                        {
                            \time 6/8
                            c'4.
                            c'4.
                        }
                        {
                            \time 6/8
                            c'4.
                            ~
                            c'4
                            c'8
                        }
                        {
                            \time 6/8
                            c'8
                            c'4
                            ~
                            c'4.
                        }
                    }
                >>

            Note that the two time signatures are much more clearly
            disambiguated above.

        ..  container:: example

            Establishing meter recursively in measures with nested tuplets:

            >>> string = "abj: | 4/4 c'16 ~ c'4 d'8. ~ "
            >>> string += "2/3 { d'8. ~ 3/5 { d'16 e'8. f'16 ~ } } "
            >>> string += "f'4 |"
            >>> staff = abjad.Staff(string)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 4/4
                        c'16
                        ~
                        c'4
                        d'8.
                        ~
                        \times 2/3 {
                            d'8.
                            ~
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 3/5 {
                                d'16
                                e'8.
                                f'16
                                ~
                            }
                        }
                        f'4
                    }
                }

            When establishing a meter on a selection of components which
            contain containers, like tuplets or containers, ``rewrite_meter()``
            will recurse into those containers, treating them as measures whose
            time signature is derived from the preprolated preprolated_duration
            of the container's contents:

            >>> measure = staff[0]
            >>> time_signature = abjad.inspect(measure[0]).indicator(
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.mutate(measure[:]).rewrite_meter(
            ...     time_signature,
            ...     boundary_depth=1,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 4/4
                        c'4
                        ~
                        c'16
                        d'8.
                        ~
                        \times 2/3 {
                            d'8
                            ~
                            d'16
                            ~
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 3/5 {
                                d'16
                                e'8
                                ~
                                e'16
                                f'16
                                ~
                            }
                        }
                        f'4
                    }
                }

        ..  container:: example

            Default rewrite behavior doesn't subdivide the first note in this
            measure because the first note in the measure starts at the
            beginning of a level-0 beat in meter:

            >>> staff = abjad.Staff("c'4.. c'16 ~ c'4")
            >>> abjad.attach(abjad.TimeSignature((6, 8)), staff[0])
            >>> meter = abjad.Meter((6, 8))
            >>> abjad.mutate(staff[:]).rewrite_meter(meter)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 6/8
                    c'4..
                    c'16
                    ~
                    c'4
                }

            Setting boundary depth to 1 subdivides the first note in this
            measure:

            >>> staff = abjad.Staff("c'4.. c'16 ~ c'4")
            >>> abjad.attach(abjad.TimeSignature((6, 8)), staff[0])
            >>> meter = abjad.Meter((6, 8))
            >>> abjad.mutate(staff[:]).rewrite_meter(meter, boundary_depth=1)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 6/8
                    c'4.
                    ~
                    c'16
                    c'16
                    ~
                    c'4
                }

            Another way of doing this is by setting preferred boundary depth on
            the meter itself:

            >>> staff = abjad.Staff("c'4.. c'16 ~ c'4")
            >>> abjad.attach(abjad.TimeSignature((6, 8)), staff[0])
            >>> meter = abjad.Meter(
            ...     (6, 8),
            ...     preferred_boundary_depth=1,
            ...     )
            >>> abjad.mutate(staff[:]).rewrite_meter(meter)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 6/8
                    c'4.
                    ~
                    c'16
                    c'16
                    ~
                    c'4
                }

            This makes it possible to divide different meters in different
            ways.

        ..  container:: example

            Rewrites notes and tuplets:

            >>> string = r"c'8 ~ c'8 ~ c'8 \times 6/7 { c'4. r16 }"
            >>> string += r" \times 6/7 { r16 c'4. } c'8 ~ c'8 ~ c'8"
            >>> staff = abjad.Staff(string)
            >>> abjad.attach(abjad.TimeSignature((6, 4)), staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 6/4
                    c'8
                    ~
                    c'8
                    ~
                    c'8
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        c'4.
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        r16
                        c'4.
                    }
                    c'8
                    ~
                    c'8
                    ~
                    c'8
                }

            >>> meter = abjad.Meter((6, 4))
            >>> abjad.mutate(staff[:]).rewrite_meter(
            ...     meter,
            ...     boundary_depth=1,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 6/4
                    c'4.
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        c'8.
                        ~
                        c'8
                        ~
                        c'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        r16
                        c'8
                        ~
                        c'4
                    }
                    c'4.
                }

            The tied note rewriting is good while the tuplet rewriting
            could use some adjustment.

            Rewrites notes but not tuplets:

            >>> string = r"c'8 ~ c'8 ~ c'8 \times 6/7 { c'4. r16 }"
            >>> string += r" \times 6/7 { r16 c'4. } c'8 ~ c'8 ~ c'8"
            >>> staff = abjad.Staff(string)
            >>> abjad.attach(abjad.TimeSignature((6, 4)), staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 6/4
                    c'8
                    ~
                    c'8
                    ~
                    c'8
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        c'4.
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        r16
                        c'4.
                    }
                    c'8
                    ~
                    c'8
                    ~
                    c'8
                }

            >>> meter = abjad.Meter((6, 4))
            >>> abjad.mutate(staff[:]).rewrite_meter(
            ...     meter,
            ...     boundary_depth=1,
            ...     rewrite_tuplets=False,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 6/4
                    c'4.
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        c'4.
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        r16
                        c'4.
                    }
                    c'4.
                }

        Operates in place and returns none.
        """
        selection = self.client
        if isinstance(selection, Container):
            selection = selection[:]
        assert isinstance(selection, Selection)
        if isinstance(meter, TimeSignature):
            meter = Meter(meter)
        if not isinstance(meter, Meter):
            raise Exception(f"must be meter or time signature (not {meter}).")
        result = Meter._rewrite_meter(
            selection,
            meter,
            boundary_depth=boundary_depth,
            initial_offset=initial_offset,
            maximum_dot_count=maximum_dot_count,
            rewrite_tuplets=rewrite_tuplets,
        )
        return result

    def scale(self, multiplier):
        r"""
        Scales mutation client by ``multiplier``.

        ..  container:: example

            Scales note duration by dot-generating multiplier:

            >>> staff = abjad.Staff("c'8 ( d'8 e'8 f'8 )")
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.mutate(staff[1]).scale(abjad.Multiplier(3, 2))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    (
                    d'8.
                    e'8
                    f'8
                    )
                }

        ..  container:: example

            Scales nontrivial logical tie by dot-generating ``multiplier``:

            >>> staff = abjad.Staff(r"c'8 \accent ~ c'8 d'8")
            >>> time_signature = abjad.TimeSignature((3, 8))
            >>> abjad.attach(time_signature, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 3/8
                    c'8
                    - \accent
                    ~
                    c'8
                    d'8
                }

            >>> logical_tie = abjad.select(staff[0]).logical_tie()
            >>> agent = abjad.mutate(logical_tie)
            >>> logical_tie = agent.scale(abjad.Multiplier(3, 2))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 3/8
                    c'4.
                    - \accent
                    d'8
                }

        ..  container:: example

            Scales container by dot-generating multiplier:

            >>> container = abjad.Container(r"c'8 ( d'8 e'8 f'8 )")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'8
                    (
                    d'8
                    e'8
                    f'8
                    )
                }

            >>> abjad.mutate(container).scale(abjad.Multiplier(3, 2))
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'8.
                    (
                    d'8.
                    e'8.
                    f'8.
                    )
                }

        ..  container:: example

            Scales note by tie-generating multiplier:

            >>> staff = abjad.Staff("c'8 ( d'8 e'8 f'8 )")
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.mutate(staff[1]).scale(abjad.Multiplier(5, 4))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    (
                    d'8
                    ~
                    d'32
                    e'8
                    f'8
                    )
                }

        ..  container:: example

            Scales nontrivial logical tie by tie-generating ``multiplier``:

            >>> staff = abjad.Staff(r"c'8 \accent ~ c'8 d'16")
            >>> time_signature = abjad.TimeSignature((5, 16))
            >>> abjad.attach(time_signature, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 5/16
                    c'8
                    - \accent
                    ~
                    c'8
                    d'16
                }

            >>> logical_tie = abjad.select(staff[0]).logical_tie()
            >>> agent = abjad.mutate(logical_tie)
            >>> logical_tie = agent.scale(abjad.Multiplier(5, 4))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 5/16
                    c'4
                    - \accent
                    ~
                    c'16
                    d'16
                }

        ..  container:: example

            Scales container by tie-generating multiplier:

            >>> container = abjad.Container(r"c'8 d'8 e'8 f'8")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }

            >>> abjad.mutate(container).scale(abjad.Multiplier(5, 4))
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'8
                    ~
                    c'32
                    d'8
                    ~
                    d'32
                    e'8
                    ~
                    e'32
                    f'8
                    ~
                    f'32
                }

        ..  container:: example

            Scales note by tuplet-generating multiplier:

            >>> staff = abjad.Staff("c'8 ( d'8 e'8 f'8 )")
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.mutate(staff[1]).scale(abjad.Multiplier(2, 3))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    (
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        d'8
                    }
                    e'8
                    f'8
                    )
                }

        ..  container:: example

            Scales trivial logical tie by tuplet-generating multiplier:

            >>> staff = abjad.Staff(r"c'8 \accent")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    - \accent
                }

            >>> logical_tie = abjad.select(staff[0]).logical_tie()
            >>> agent = abjad.mutate(logical_tie)
            >>> logical_tie = agent.scale(abjad.Multiplier(4, 3))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        c'4
                        - \accent
                    }
                }

        ..  container:: example

            Scales container by tuplet-generating multiplier:

            >>> container = abjad.Container(r"c'8 ( d'8 e'8 f'8 )")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    c'8
                    (
                    d'8
                    e'8
                    f'8
                    )
                }

            >>> abjad.mutate(container).scale(abjad.Multiplier(4, 3))
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        c'4
                        (
                    }
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        d'4
                    }
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        e'4
                    }
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        f'4
                        )
                    }
                }

        ..  container:: example

            Scales note by tie- and tuplet-generating multiplier:

            >>> staff = abjad.Staff("c'8 ( d'8 e'8 f'8 )")
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.mutate(staff[1]).scale(abjad.Multiplier(5, 6))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    (
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        d'8
                        ~
                        d'32
                    }
                    e'8
                    f'8
                    )
                }

        ..  container:: example

            Scales note carrying LilyPond multiplier:

            >>> note = abjad.Note("c'8", multiplier=(1, 2))
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c'8 * 1/2

            >>> abjad.mutate(note).scale(abjad.Multiplier(5, 3))
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c'8 * 5/6

        ..  container:: example

            Scales tuplet:

            >>> staff = abjad.Staff()
            >>> tuplet = abjad.Tuplet((4, 5), [])
            >>> tuplet.extend("c'8 d'8 e'8 f'8 g'8")
            >>> staff.append(tuplet)
            >>> time_signature = abjad.TimeSignature((4, 8))
            >>> leaves = abjad.select(staff).leaves()
            >>> abjad.attach(time_signature, leaves[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 4/5 {
                        \time 4/8
                        c'8
                        d'8
                        e'8
                        f'8
                        g'8
                    }
                }

            >>> abjad.mutate(tuplet).scale(abjad.Multiplier(2))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 4/5 {
                        \time 4/8
                        c'4
                        d'4
                        e'4
                        f'4
                        g'4
                    }
                }

        ..  container:: example

            Scales tuplet:

            >>> staff = abjad.Staff()
            >>> tuplet = abjad.Tuplet((4, 5), "c'8 d'8 e'8 f'8 g'8")
            >>> staff.append(tuplet)
            >>> time_signature = abjad.TimeSignature((4, 8))
            >>> leaf = abjad.inspect(staff).leaf(0)
            >>> abjad.attach(time_signature, leaf)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 4/5 {
                        \time 4/8
                        c'8
                        d'8
                        e'8
                        f'8
                        g'8
                    }
                }

            >>> abjad.mutate(tuplet).scale(abjad.Multiplier(2))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 4/5 {
                        \time 4/8
                        c'4
                        d'4
                        e'4
                        f'4
                        g'4
                    }
                }

        Returns none.
        """
        if hasattr(self.client, "_scale"):
            self.client._scale(multiplier)
        else:
            assert isinstance(self.client, Selection)
            for component in self.client:
                component._scale(multiplier)

    # TODO: add tests of tupletted notes and rests.
    # TODO: add examples that show indicator handling.
    # TODO: add example showing grace and after grace handling.
    def split(self, durations, cyclic=False):
        r"""
        Splits mutation client by ``durations``.

        ..  container:: example

            Splits leaves cyclically and ties split notes:

            >>> staff = abjad.Staff("c'1 d'1")
            >>> abjad.hairpin('p < f', staff[:])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 3
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #3
                }
                {
                    c'1
                    \p
                    \<
                    d'1
                    \f
                }

            >>> durations = [(3, 4)]
            >>> result = abjad.mutate(staff[:]).split(
            ...     durations,
            ...     cyclic=True,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #3
                }
                {
                    c'2.
                    \p
                    ~
                    c'4
                    \<
                    d'2
                    \f
                    ~
                    d'2
                }

        ..  container:: example

            Splits custom voice and preserves context name:

            >>> voice = abjad.Voice(
            ...     "c'4 d' e' f'",
            ...     lilypond_type='CustomVoice',
            ...     name='1',
            ...     )
            >>> staff = abjad.Staff([voice])
            >>> abjad.hairpin('p < f', voice[:])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 3
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #3
                }
                {
                    \context CustomVoice = "1"
                    {
                        c'4
                        \p
                        \<
                        d'4
                        e'4
                        f'4
                        \f
                    }
                }

            >>> durations = [(1, 8)]
            >>> result = abjad.mutate(staff[:]).split(
            ...     durations,
            ...     cyclic=True,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #3
                }
                {
                    \context CustomVoice = "1"
                    {
                        c'8
                        \p
                        ~
                    }
                    \context CustomVoice = "1"
                    {
                        c'8
                        \<
                    }
                    \context CustomVoice = "1"
                    {
                        d'8
                        ~
                    }
                    \context CustomVoice = "1"
                    {
                        d'8
                    }
                    \context CustomVoice = "1"
                    {
                        e'8
                        ~
                    }
                    \context CustomVoice = "1"
                    {
                        e'8
                    }
                    \context CustomVoice = "1"
                    {
                        f'8
                        \f
                        ~
                    }
                    \context CustomVoice = "1"
                    {
                        f'8
                    }
                }

            >>> for voice in staff:
            ...     voice
            ...
            Voice("c'8 ~", lilypond_type='CustomVoice', name='1')
            Voice("c'8", lilypond_type='CustomVoice', name='1')
            Voice("d'8 ~", lilypond_type='CustomVoice', name='1')
            Voice("d'8", lilypond_type='CustomVoice', name='1')
            Voice("e'8 ~", lilypond_type='CustomVoice', name='1')
            Voice("e'8", lilypond_type='CustomVoice', name='1')
            Voice("f'8 ~", lilypond_type='CustomVoice', name='1')
            Voice("f'8", lilypond_type='CustomVoice', name='1')

        ..  container:: example

            Splits parallel container:

            >>> voice_1 = abjad.Voice(
            ...     "e''4 ( es'' f'' fs'' )",
            ...     name='Voice_1',
            ...     )
            >>> voice_2 = abjad.Voice(
            ...     r"c'4 \p \< cs' d' ds' \f",
            ...     name='Voice_2',
            ...     )
            >>> abjad.override(voice_1).stem.direction = abjad.Up
            >>> abjad.override(voice_1).slur.direction = abjad.Up
            >>> container = abjad.Container(
            ...     [voice_1, voice_2],
            ...     simultaneous=True,
            ...     )
            >>> abjad.override(voice_2).stem.direction = abjad.Down
            >>> staff = abjad.Staff([container])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    <<
                        \context Voice = "Voice_1"
                        \with
                        {
                            \override Slur.direction = #up
                            \override Stem.direction = #up
                        }
                        {
                            e''4
                            (
                            es''4
                            f''4
                            fs''4
                            )
                        }
                        \context Voice = "Voice_2"
                        \with
                        {
                            \override Stem.direction = #down
                        }
                        {
                            c'4
                            \p
                            \<
                            cs'4
                            d'4
                            ds'4
                            \f
                        }
                    >>
                }

            >>> durations = [(3, 8)]
            >>> result = abjad.mutate(container).split(
            ...     durations,
            ...     cyclic=False,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff)
            \new Staff
            {
                <<
                    \context Voice = "Voice_1"
                    \with
                    {
                        \override Slur.direction = #up
                        \override Stem.direction = #up
                    }
                    {
                        e''4
                        (
                        es''8
                        ~
                    }
                    \context Voice = "Voice_2"
                    \with
                    {
                        \override Stem.direction = #down
                    }
                    {
                        c'4
                        \p
                        \<
                        cs'8
                        ~
                    }
                >>
                <<
                    \context Voice = "Voice_1"
                    \with
                    {
                        \override Slur.direction = #up
                        \override Stem.direction = #up
                    }
                    {
                        es''8
                        f''4
                        fs''4
                        )
                    }
                    \context Voice = "Voice_2"
                    \with
                    {
                        \override Stem.direction = #down
                    }
                    {
                        cs'8
                        d'4
                        ds'4
                        \f
                    }
                >>
            }

        ..  container:: example

            Splits leaves with articulations:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Articulation('^'), staff[0])
            >>> abjad.attach(abjad.LaissezVibrer(), staff[1])
            >>> abjad.attach(abjad.Articulation('^'), staff[2])
            >>> abjad.attach(abjad.LaissezVibrer(), staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \marcato
                    d'4
                    \laissezVibrer
                    e'4
                    - \marcato
                    f'4
                    \laissezVibrer
                }

            >>> durations = [(1, 8)]
            >>> result = abjad.mutate(staff[:]).split(
            ...     durations,
            ...     cyclic=True,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    - \marcato
                    ~
                    c'8
                    d'8
                    ~
                    d'8
                    \laissezVibrer
                    e'8
                    - \marcato
                    ~
                    e'8
                    f'8
                    ~
                    f'8
                    \laissezVibrer
                }

        ..  container:: example

            REGRESSION. Preserves tie:

            >>> staff = abjad.Staff("d'2 ~ d'")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    d'2
                    ~
                    d'2
                }

            >>> result = abjad.mutate(staff[0]).split([(1, 32)])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    d'32
                    ~
                    d'4...
                    ~
                    d'2
                }

        Returns list of selections.
        """
        components = self.client
        single_component_input = False
        if isinstance(components, Component):
            single_component_input = True
            components = select(components)
        assert all(isinstance(_, Component) for _ in components)
        if not isinstance(components, Selection):
            components = select(components)
        durations = [Duration(_) for _ in durations]
        if not durations:
            if single_component_input:
                return components
            else:
                return [], components
        total_component_duration = inspect(components).duration()
        total_split_duration = sum(durations)
        if cyclic:
            durations = sequence(durations)
            durations = durations.repeat_to_weight(total_component_duration)
            durations = list(durations)
        elif total_split_duration < total_component_duration:
            final_offset = total_component_duration - sum(durations)
            durations.append(final_offset)
        elif total_component_duration < total_split_duration:
            weight = total_component_duration
            durations = sequence(durations).truncate(weight=weight)
            durations = list(durations)
        # keep copy of durations to partition result components
        durations_copy = durations[:]
        total_split_duration = sum(durations)
        assert total_split_duration == total_component_duration
        result, shard = [], []
        offset_index = 0
        current_shard_duration = Duration(0)
        remaining_components = list(components[:])
        advance_to_next_offset = True
        # build shards:
        # grab next component and next duration each time through loop
        while True:
            # grab next split point
            if advance_to_next_offset:
                if durations:
                    next_split_point = durations.pop(0)
                else:
                    break
            advance_to_next_offset = True
            # grab next component from input stack of components
            if remaining_components:
                current_component = remaining_components.pop(0)
            else:
                break
            # find where current component endpoint will position us
            duration_ = inspect(current_component).duration()
            candidate_shard_duration = current_shard_duration + duration_
            # if current component would fill current shard exactly
            if candidate_shard_duration == next_split_point:
                shard.append(current_component)
                result.append(shard)
                shard = []
                current_shard_duration = Duration(0)
                offset_index += 1
            # if current component would exceed current shard
            elif next_split_point < candidate_shard_duration:
                local_split_duration = next_split_point
                local_split_duration -= current_shard_duration
                if isinstance(current_component, Leaf):
                    leaf_split_durations = [local_split_duration]
                    duration_ = inspect(current_component).duration()
                    current_duration = duration_
                    additional_required_duration = current_duration
                    additional_required_duration -= local_split_duration
                    split_durations = sequence(durations)
                    split_durations = split_durations.split(
                        [additional_required_duration], cyclic=False, overhang=True,
                    )
                    split_durations = [list(_) for _ in split_durations]
                    additional_durations = split_durations[0]
                    leaf_split_durations.extend(additional_durations)
                    durations = split_durations[-1]
                    leaf_shards = current_component._split_by_durations(
                        leaf_split_durations, cyclic=False
                    )
                    shard.extend(leaf_shards)
                    result.append(shard)
                    offset_index += len(additional_durations)
                else:
                    assert isinstance(current_component, Container)
                    pair = current_component._split_by_duration(local_split_duration)
                    left_list, right_list = pair
                    shard.extend(left_list)
                    result.append(shard)
                    remaining_components.__setitem__(slice(0, 0), right_list)
                shard = []
                offset_index += 1
                current_shard_duration = Duration(0)
            # if current component would not fill current shard
            elif candidate_shard_duration < next_split_point:
                shard.append(current_component)
                duration_ = inspect(current_component).duration()
                current_shard_duration += duration_
                advance_to_next_offset = False
            else:
                message = "can not process candidate duration: {!r}."
                message = message.format(candidate_shard_duration)
                raise ValueError(message)
        # append any stub shard
        if len(shard):
            result.append(shard)
        # append any unexamined components
        if len(remaining_components):
            result.append(remaining_components)
        # partition split components according to input durations
        result = sequence(result).flatten(depth=-1)
        result = select(result).partition_by_durations(durations_copy, fill=enums.Exact)
        # return list of shards
        assert all(isinstance(_, Selection) for _ in result)
        return result

    def swap(self, container):
        r"""
        Swaps mutation client for empty ``container``.

        ..  container:: example

            Swaps containers for tuplet:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Container("c'4 d'4 e'4"))
            >>> staff.append(abjad.Container("d'4 e'4 f'4"))
            >>> abjad.attach(abjad.TimeSignature((3, 4)), staff[0][0])
            >>> leaves = abjad.select(staff).leaves()
            >>> abjad.hairpin('p < f', leaves)
            >>> measures = staff[:]
            >>> abjad.slur(leaves)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 3/4
                        c'4
                        \p
                        \<
                        (
                        d'4
                        e'4
                    }
                    {
                        d'4
                        e'4
                        f'4
                        \f
                        )
                    }
                }

            >>> containers = staff[:]
            >>> tuplet = abjad.Tuplet((2, 3), [])
            >>> tuplet.denominator = 4
            >>> abjad.mutate(containers).swap(tuplet)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 4/6 {
                        \time 3/4
                        c'4
                        \p
                        \<
                        (
                        d'4
                        e'4
                        d'4
                        e'4
                        f'4
                        \f
                        )
                    }
                }

        Returns none.
        """
        if isinstance(self.client, Selection):
            donors = self.client
        else:
            donors = select(self.client)
        assert donors.are_contiguous_same_parent()
        assert isinstance(container, Container)
        assert not container, repr(container)
        donors._give_components_to_empty_container(container)
        # donors._give_dominant_spanners([container])
        donors._give_position_in_parent_to_container(container)

    def transpose(self, argument):
        r"""
        Transposes notes and chords in mutation client by ``argument``.

        ..  todo:: Move to abjad.pitch package.

        ..  container:: example

            Transposes notes and chords in staff:

            >>> staff = abjad.Staff()
            >>> staff.extend("c'4 d'4 e'4 r4")
            >>> abjad.attach(abjad.TimeSignature((4, 4)), staff[0])
            >>> staff.extend("d'4 e'4 <f' a' c''>4")
            >>> abjad.attach(abjad.TimeSignature((3, 4)), staff[4])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 4/4
                    c'4
                    d'4
                    e'4
                    r4
                    \time 3/4
                    d'4
                    e'4
                    <f' a' c''>4
                }

            >>> abjad.mutate(staff).transpose("+m3")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 4/4
                    ef'4
                    f'4
                    g'4
                    r4
                    \time 3/4
                    f'4
                    g'4
                    <af' c'' ef''>4
                }

        Returns none.
        """
        named_interval = NamedInterval(argument)
        for x in iterate(self.client).components((Note, Chord)):
            if isinstance(x, Note):
                old_written_pitch = x.note_head.written_pitch
                new_written_pitch = old_written_pitch.transpose(named_interval)
                x.note_head.written_pitch = new_written_pitch
            else:
                for note_head in x.note_heads:
                    old_written_pitch = note_head.written_pitch
                    new_written_pitch = old_written_pitch.transpose(named_interval)
                    note_head.written_pitch = new_written_pitch

    def wrap(self, container):
        r"""
        Wraps mutation client in empty ``container``.

        ..  container:: example

            Wraps in-score notes in tuplet:

            >>> staff = abjad.Staff("c'8 [ ( d' e' ] ) c' [ ( d' e' ] )")
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
                    )
                    ]
                    c'8
                    [
                    (
                    d'8
                    e'8
                    )
                    ]
                }

            >>> tuplet = abjad.Tuplet((2, 3), [])
            >>> abjad.mutate(staff[-3:]).wrap(tuplet)
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
                    )
                    ]
                    \times 2/3 {
                        c'8
                        [
                        (
                        d'8
                        e'8
                        )
                        ]
                    }
                }

        ..  container:: example

            Wraps outside-score notes in tuplet:

            >>> maker = abjad.NoteMaker()
            >>> notes = maker([0, 2, 4], [(1, 8)])
            >>> tuplet = abjad.Tuplet((2, 3), [])
            >>> abjad.mutate(notes).wrap(tuplet)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

            (This usage merely substitutes for the tuplet initializer.)

        ..  container:: example

            Wraps leaves in container:

            >>> notes = [abjad.Note(n, (1, 8)) for n in range(8)]
            >>> staff = abjad.Staff(notes)
            >>> abjad.attach(abjad.TimeSignature((4, 8)), staff[0])
            >>> container = abjad.Container()
            >>> abjad.mutate(staff[:4]).wrap(container)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 4/8
                        c'8
                        cs'8
                        d'8
                        ef'8
                    }
                    e'8
                    f'8
                    fs'8
                    g'8
                }

        ..  container:: example

            Wraps each leaf in tuplet:

            >>> notes = [abjad.Note(n, (1, 1)) for n in range(4)]
            >>> staff = abjad.Staff(notes)
            >>> for note in staff:
            ...     tuplet = abjad.Tuplet((2, 3))
            ...     abjad.mutate(note).wrap(tuplet)
            ...

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        c'1
                    }
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        cs'1
                    }
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        d'1
                    }
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        ef'1
                    }
                }

        ..  container:: example

            Raises exception on nonempty ``container``:

            >>> import pytest
            >>> staff = abjad.Staff("c'8 [ ( d' e' ] ) c' [ ( d' e' ] )")
            >>> tuplet = abjad.Tuplet((2, 3), "g'8 a' fs'")
            >>> abjad.mutate(staff[-3:]).wrap(tuplet)
            Traceback (most recent call last):
                ...
            Exception: must be empty container: Tuplet(Multiplier(2, 3), "g'8 a'8 fs'8").

        ..  container:: example

            REGRESSION. Contexted indicators (like time signature) survive
            wrap:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> leaves = abjad.select(staff).leaves()
            >>> abjad.attach(abjad.TimeSignature((3, 8)), leaves[0])
            >>> container = abjad.Container()
            >>> abjad.mutate(leaves).wrap(container)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    {
                        \time 3/8
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                }

            >>> prototype = abjad.TimeSignature
            >>> for component in abjad.iterate(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     time_signature = inspection.effective(prototype)
            ...     print(component, time_signature)
            ...
            <Staff{1}> 3/8
            Container("c'4 d'4 e'4 f'4") 3/8
            c'4 3/8
            d'4 3/8
            e'4 3/8
            f'4 3/8

        Returns none.
        """
        if not isinstance(container, Container) or 0 < len(container):
            message = f"must be empty container: {container!r}."
            raise Exception(message)
        if isinstance(self.client, Component):
            selection = select(self.client)
        else:
            selection = self.client
        assert isinstance(selection, Selection), repr(selection)
        parent, start, stop = selection._get_parent_and_start_stop_indices(
            ignore_before_after_grace=True
        )
        if not selection.are_contiguous_logical_voice(ignore_before_after_grace=True):
            message = "must be contiguous components in same logical voice:\n"
            message += f"   {selection!r}."
            raise Exception(message)
        container._components = list(selection)
        container[:]._set_parents(container)
        if parent is not None:
            parent._components.insert(start, container)
            container._set_parent(parent)
        for component in selection:
            for wrapper in component._wrappers:
                wrapper._effective_context = None
                wrapper._update_effective_context()
