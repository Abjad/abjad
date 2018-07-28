import collections
import typing
from abjad import exceptions
from abjad.indicators.TimeSignature import TimeSignature
from abjad.markups import Markup
from abjad.pitch.NamedPitch import NamedPitch
from abjad.pitch.PitchSet import PitchSet
from abjad.spanners.Spanner import Spanner
from abjad.system.AbjadObject import AbjadObject
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.system.WellformednessManager import WellformednessManager
from abjad.system.Wrapper import Wrapper
from abjad.timespans.Timespan import Timespan
from abjad.top.inspect import inspect
from abjad.top.iterate import iterate
from abjad.utilities.Duration import Duration
from .AfterGraceContainer import AfterGraceContainer
from .Chord import Chord
from .Component import Component
from .Container import Container
from .GraceContainer import GraceContainer
from .Leaf import Leaf
from .Lineage import Lineage
from .LogicalTie import LogicalTie
from .Note import Note
from .Parentage import Parentage
from .Selection import Selection
from .Staff import Staff
from .Tuplet import Tuplet
from .VerticalMoment import VerticalMoment


class Inspection(AbjadObject):
    """
    Inspection.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.inspect(staff)
        Inspection(client=Staff("c'4 e'4 d'4 f'4"))

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Collaborators'

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        client: typing.Union[Component, typing.Iterable[Component]] = None,
        ) -> None:
        assert not isinstance(client, str), repr(client)
        prototype = (Component, collections.Iterable, type(None))
        if not isinstance(client, prototype):
            message = 'must be component, nonstring iterable or none:'
            message += f' (not {client!r}).'
            raise TypeError(message)
        self._client = client

    ### PUBLIC PROPERTIES ###

    @property
    def client(self) -> typing.Union[
        Component, typing.Iterable[Component], None
        ]:
        r"""
        Gets client of inspection.

        ..  container:: example

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Voice("c'8 d'8 e'8 f'8"))
            >>> staff.append(abjad.Voice("g'8 a'8 b'8 c''8"))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                    \new Voice
                    {
                        g'8
                        a'8
                        b'8
                        c''8
                    }
                }

            >>> abjad.inspect(staff).client
            <Staff{2}>

        """
        return self._client

    ### PUBLIC METHODS ###

    def after_grace_container(self) -> typing.Optional[
        AfterGraceContainer]:
        r"""
        Gets after grace containers attached to leaf.

        ..  container:: example

            Get after grace container attached to note:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> note = abjad.Note("ds'16")
            >>> container = abjad.AfterGraceContainer([note])
            >>> abjad.attach(container, staff[1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    \afterGrace
                    d'8
                    {
                        ds'16
                    }
                    e'8
                    f'8
                }

            >>> abjad.inspect(staff[1]).after_grace_container()
            AfterGraceContainer("ds'16")

        """
        return getattr(self.client, '_after_grace_container', None)

    def annotation(
        self,
        annotation,
        default=None,
        unwrap=True,
        ) -> typing.Any:
        r"""
        Gets annotation.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 e' e' f'")
            >>> abjad.annotate(staff[0], 'default_instrument', abjad.Cello())
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    e'4
                    e'4
                    f'4
                }

            >>> string = 'default_instrument'
            >>> abjad.inspect(staff[0]).annotation(string)
            Cello()

            >>> abjad.inspect(staff[1]).annotation(string) is None
            True

            >>> abjad.inspect(staff[2]).annotation(string) is None
            True

            >>> abjad.inspect(staff[3]).annotation(string) is None
            True

            Returns default when no annotation is found:

            >>> abjad.inspect(staff[3]).annotation(string, abjad.Violin())
            Violin()

        ..  container:: example

            REGRESSION: annotation is not picked up as effective indicator:

            >>> prototype = abjad.Instrument
            >>> abjad.inspect(staff[0]).effective(prototype) is None
            True

            >>> abjad.inspect(staff[1]).effective(prototype) is None
            True

            >>> abjad.inspect(staff[2]).effective(prototype) is None
            True

            >>> abjad.inspect(staff[3]).effective(prototype) is None
            True

        """
        assert isinstance(annotation, str), repr(annotation)
        for wrapper in self.annotation_wrappers():
            if wrapper.annotation == annotation:
                if unwrap is True:
                    return wrapper.indicator
                else:
                    return wrapper
        return default

    def annotation_wrappers(self) -> typing.List[Wrapper]:
        r"""
        Gets annotation wrappers.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 e' e' f'")
            >>> abjad.annotate(staff[0], 'default_instrument', abjad.Cello())
            >>> abjad.annotate(staff[0], 'default_clef', abjad.Clef('tenor'))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    e'4
                    e'4
                    f'4
                }

            >>> for wrapper in abjad.inspect(staff[0]).annotation_wrappers():
            ...     abjad.f(wrapper)
            ...
            abjad.Wrapper(
                annotation='default_instrument',
                indicator=abjad.Cello(
                    name='cello',
                    short_name='vc.',
                    markup=abjad.Markup(
                        contents=['Cello'],
                        ),
                    short_markup=abjad.Markup(
                        contents=['Vc.'],
                        ),
                    allowable_clefs=('bass', 'tenor', 'treble'),
                    context='Staff',
                    default_tuning=abjad.Tuning(
                        pitches=abjad.PitchSegment(
                            (
                                abjad.NamedPitch('c,'),
                                abjad.NamedPitch('g,'),
                                abjad.NamedPitch('d'),
                                abjad.NamedPitch('a'),
                                ),
                            item_class=abjad.NamedPitch,
                            ),
                        ),
                    middle_c_sounding_pitch=abjad.NamedPitch("c'"),
                    pitch_range=abjad.PitchRange('[C2, G5]'),
                    primary=True,
                    ),
                tag=abjad.Tag(),
                )
            abjad.Wrapper(
                annotation='default_clef',
                indicator=abjad.Clef('tenor'),
                tag=abjad.Tag(),
                )

        """
        result = []
        for wrapper in getattr(self.client, '_wrappers', []):
            if wrapper.annotation:
                result.append(wrapper)
        return result

    def badly_formed_components(self) -> typing.List[Component]:
        r"""
        Gets badly formed components.
        """
        manager = WellformednessManager()
        violators: typing.List[Component] = []
        for violators_, total, check_name in manager(self.client):
            violators.extend(violators_)
        return violators

    def contents(self, include_self=True) -> typing.Optional[Selection]:
        r"""
        Gets contents.

        ..  container:: example

            >>> staff = abjad.Staff(r"\times 2/3 { c'8 d'8 e'8 } f'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 2/3 {
                        c'8
                        d'8
                        e'8
                    }
                    f'4
                }

            >>> for component in abjad.inspect(staff).contents():
            ...     component
            ...
            <Staff{2}>
            Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")
            Note("f'4")

            >>> for component in abjad.inspect(staff).contents(
            ...     include_self=False,
            ...     ):
            ...     component
            ...
            Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")
            Note("f'4")

        """
        if not isinstance(self.client, Component):
            raise Exception('can only get contents of component.')
        return self.client._get_contents(include_self=include_self)

    def descendants(self, include_self=True) -> Selection:
        r"""
        Gets descendants.

        ..  container:: example

            >>> staff = abjad.Staff(r"\times 2/3 { c'8 d'8 e'8 } f'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 2/3 {
                        c'8
                        d'8
                        e'8
                    }
                    f'4
                }

            >>> for component in abjad.inspect(staff).descendants():
            ...     component
            ...
            <Staff{2}>
            Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")
            Note("c'8")
            Note("d'8")
            Note("e'8")
            Note("f'4")

            >>> for component in abjad.inspect(staff).descendants(
            ...     include_self=False,
            ...     ):
            ...     component
            ...
            Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")
            Note("c'8")
            Note("d'8")
            Note("e'8")
            Note("f'4")

            >>> for component in abjad.inspect(staff[:1]).descendants(
            ...     include_self=False,
            ...     ):
            ...     component
            ...
            Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")
            Note("c'8")
            Note("d'8")
            Note("e'8")

        """
        if isinstance(self.client, Component):
            return self.client._get_descendants(include_self=include_self)
        descendants: typing.List[Component] = []
        assert isinstance(self.client, Selection)
        for argument in self.client:
            descendants_ = Inspection(argument).descendants()
            for descendant_ in descendants_:
                if descendant_ not in descendants:
                    descendants.append(descendant_)
        result = Selection(descendants)
        return result

    def duration(self, in_seconds=False) -> Duration:
        r"""
        Gets duration.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> selection = staff[:3]
            >>> abjad.inspect(selection).duration()
            Duration(3, 4)

        """
        if isinstance(self.client, Component):
            return self.client._get_duration(in_seconds=in_seconds)
        assert isinstance(self.client, collections.Iterable), repr(self.client)
        durations = [
            Inspection(_).duration(in_seconds=in_seconds)
            for _ in self.client
            ]
        return Duration(sum(durations))

    def effective(
        self,
        prototype=None,
        unwrap=True,
        n=0,
        default=None,
        ) -> typing.Any:
        r"""
        Gets effective indicator.

        ..  container:: example

            Gets effective clef:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef('alto'), staff[0])
            >>> abjad.attach(abjad.AcciaccaturaContainer("fs'16"), staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    c'4
                    d'4
                    e'4
                    \acciaccatura {
                        fs'16
                    }
                    f'4
                }

            >>> for component in abjad.iterate(staff).components():
            ...     clef = abjad.inspect(component).effective(abjad.Clef)
            ...     print(component, clef)
            ...
            Staff("c'4 d'4 e'4 f'4") Clef('alto')
            c'4 Clef('alto')
            d'4 Clef('alto')
            e'4 Clef('alto')
            fs'16 Clef('alto')
            f'4 Clef('alto')

        ..  container:: example

            Arbitrary objects (like strings) can be contexted:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> abjad.attach('color', staff[1], context='Staff')
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }

            >>> for component in abjad.iterate(staff).components():
            ...     string = abjad.inspect(component).effective(str)
            ...     print(component, repr(string))
            ...
            Staff("c'8 d'8 e'8 f'8") None
            c'8 None
            d'8 'color'
            e'8 'color'
            f'8 'color'

        ..  container:: example

            Scans forwards or backwards when ``n`` is set: 

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8")
            >>> abjad.attach('red', staff[0], context='Staff')
            >>> abjad.attach('blue', staff[2], context='Staff')
            >>> abjad.attach('yellow', staff[4], context='Staff')
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                    g'8
                }
                
            >>> for n in (-1, 0, 1):
            ...     color = abjad.inspect(staff[0]).effective(str, n=n)
            ...     print(n, repr(color))
            ...
            -1 None
            0 'red'
            1 'blue'

            >>> for n in (-1, 0, 1):
            ...     color = abjad.inspect(staff[1]).effective(str, n=n)
            ...     print(n, repr(color))
            ...
            -1 None
            0 'red'
            1 'blue'

            >>> for n in (-1, 0, 1):
            ...     color = abjad.inspect(staff[2]).effective(str, n=n)
            ...     print(n, repr(color))
            ...
            -1 'red'
            0 'blue'
            1 'yellow'

            >>> for n in (-1, 0, 1):
            ...     color = abjad.inspect(staff[3]).effective(str, n=n)
            ...     print(n, repr(color))
            ...
            -1 'red'
            0 'blue'
            1 'yellow'

            >>> for n in (-1, 0, 1):
            ...     color = abjad.inspect(staff[4]).effective(str, n=n)
            ...     print(n, repr(color))
            ...
            -1 'blue'
            0 'yellow'
            1 None

        ..  container:: example

            Synthetic offsets works this way:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> abjad.attach(
            ...     'red',
            ...     staff[-1],
            ...     context='Staff',
            ...     synthetic_offset=-1,
            ...     )
            >>> abjad.attach('blue', staff[0], context='Staff')
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }

            Entire staff is effectively blue:

            >>> abjad.inspect(staff).effective(str)
            'blue'

            The (synthetic) offset just prior to (start of) staff is red:

            >>> abjad.inspect(staff).effective(str, n=-1)
            'red'

        ..  container:: example

            Gets effective time signature:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> leaves = abjad.select(staff).leaves()
            >>> abjad.attach(abjad.TimeSignature((3, 8)), leaves[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 3/8
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> prototype = abjad.TimeSignature
            >>> for component in abjad.iterate(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     time_signature = inspection.effective(prototype)
            ...     print(component, time_signature)
            ...
            Staff("c'4 d'4 e'4 f'4") 3/8
            c'4 3/8
            d'4 3/8
            e'4 3/8
            f'4 3/8

        """
        if not isinstance(self.client, Component):
            raise Exception('can only get effective on components.')
        result = self.client._get_effective(
            prototype=prototype,
            unwrap=unwrap,
            n=n,
            )
        if result is None:
            result = default
        return result

    def effective_staff(self) -> typing.Optional[Staff]:
        """
        Gets effective staff.
        """
        if not isinstance(self.client, Component):
            raise Exception('can only get effective staff on components.')
        return self.client._get_effective_staff()

    def effective_wrapper(
        self,
        prototype=None,
        n=0,
        ) -> typing.Optional[Wrapper]:
        r"""
        Gets effective wrapper.

        ..  container:: example

            Gets effective clef wrapper:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef('alto'), staff[0])
            >>> abjad.attach(abjad.AcciaccaturaContainer("fs'16"), staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    c'4
                    d'4
                    e'4
                    \acciaccatura {
                        fs'16
                    }
                    f'4
                }

            >>> for component in abjad.iterate(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     wrapper = inspection.effective_wrapper(abjad.Clef)
            ...     print(component, wrapper)
            ...
            Staff("c'4 d'4 e'4 f'4") Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            c'4 Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            d'4 Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            e'4 Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            fs'16 Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            f'4 Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())

        """
        return self.effective(prototype=prototype, n=n, unwrap=False)

    def grace_container(self) -> typing.Optional[GraceContainer]:
        r"""
        Gets grace container attached to leaf.

        ..  container:: example

            Get acciaccatura container attached to note:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> note = abjad.Note("cs'16")
            >>> container = abjad.AcciaccaturaContainer([note])
            >>> abjad.attach(container, staff[1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    \acciaccatura {
                        cs'16
                    }
                    d'8
                    e'8
                    f'8
                }

            >>> abjad.inspect(staff[1]).grace_container()
            AcciaccaturaContainer("cs'16")

        """
        if not isinstance(self.client, Leaf):
            raise Exception('can only get grace container on leaf.')
        return self.client._grace_container

    def has_effective_indicator(self, prototype=None) -> bool:
        """
        Is true when client has effective indicator.
        """
        if not isinstance(self.client, Component):
            raise Exception('can only get effective indicator on component.')
        return self.client._has_effective_indicator(prototype=prototype)

    def has_indicator(self, prototype=None) -> bool:
        """
        Is true when client has one or more indicators.
        """
        if not isinstance(self.client, Component):
            raise Exception('can only get indicator on component.')
        return self.client._has_indicator(prototype=prototype)

    def has_spanner(self, prototype=None) -> bool:
        """
        Is true when client has one or more spanners.
        """
        if not isinstance(self.client, Leaf):
            raise Exception('can only get spanner on leaf.')
        return self.client._has_spanner(prototype=prototype)

    def indicator(
        self,
        prototype=None,
        default=None,
        unwrap=True,
        ) -> typing.Any:
        """
        Gets indicator.

        Raises exception when more than one indicator of ``prototype`` attach
        to client.

        Returns default when no indicator of ``prototype`` attaches to client.
        """
        if not isinstance(self.client, Component):
            raise Exception('can only get indicator on component.')
        indicators = self.client._get_indicators(
            prototype=prototype,
            unwrap=unwrap,
            )
        if not indicators:
            return default
        elif len(indicators) == 1:
            return list(indicators)[0]
        else:
            raise Exception('multiple indicators attached to client.')

    def indicators(self, prototype=None, unwrap=True) -> typing.List:
        r"""
        Get indicators.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Articulation('^'), staff[0])
            >>> abjad.attach(abjad.Articulation('^'), staff[1])
            >>> abjad.attach(abjad.Articulation('^'), staff[2])
            >>> abjad.attach(abjad.Articulation('^'), staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    -\marcato
                    d'4
                    -\marcato
                    e'4
                    -\marcato
                    f'4
                    -\marcato
                }

            >>> abjad.inspect(staff).indicators(abjad.Articulation)
            []

            >>> abjad.inspect(staff[0]).indicators(abjad.Articulation)
            [Articulation('^')]

        """
        # TODO: extend to any non-none client
        if not isinstance(self.client, Component):
            raise Exception('can only get indicators on component.')
        result = self.client._get_indicators(
            prototype=prototype,
            unwrap=unwrap,
            )
        return list(result)

    def is_bar_line_crossing(self) -> bool:
        r"""
        Is true when client crosses bar line.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4")
            >>> time_signature = abjad.TimeSignature((3, 8))
            >>> abjad.attach(time_signature, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 3/8
                    c'4
                    d'4
                    e'4
                }

            >>> for note in staff:
            ...     result = abjad.inspect(note).is_bar_line_crossing()
            ...     print(note, result)
            ...
            c'4 False
            d'4 True
            e'4 False

        """
        if not isinstance(self.client, Component):
            raise Exception('can only get indicator on component.')
        time_signature = self.client._get_effective(TimeSignature)
        if time_signature is None:
            time_signature_duration = Duration(4, 4)
        else:
            time_signature_duration = time_signature.duration
        partial = getattr(time_signature, 'partial', 0)
        partial = partial or 0
        start_offset = Inspection(self.client).timespan().start_offset
        shifted_start = start_offset - partial
        shifted_start %= time_signature_duration
        stop_offset = self.client._get_duration() + shifted_start
        if time_signature_duration < stop_offset:
            return True
        return False

    def is_grace_note(self) -> bool:
        """
        Is true when client is grace note.
        """
        if not isinstance(self.client, Leaf):
            return False
        prototype = (AfterGraceContainer, GraceContainer)
        for component in Inspection(self.client).parentage():
            if isinstance(component, prototype):
                return True
        return False

    def is_well_formed(
        self,
        check_beamed_long_notes=True,
        check_discontiguous_spanners=True,
        check_duplicate_ids=True,
        check_empty_containers=True,
        check_misdurated_measures=True,
        check_misfilled_measures=True,
        check_mismatched_enchained_hairpins=True,
        check_mispitched_ties=True,
        check_misrepresented_flags=True,
        check_missing_parents=True,
        check_nested_measures=True,
        check_notes_on_wrong_clef=True,
        check_out_of_range_notes=True,
        check_overlapping_beams=True,
        check_overlapping_glissandi=True,
        check_overlapping_hairpins=True,
        check_overlapping_octavation_spanners=True,
        check_overlapping_ties=True,
        check_overlapping_trill_spanners=True,
        check_tied_rests=True,
        ) -> bool:
        """
        Is true when client is well-formed.
        """
        manager = WellformednessManager()
        for violators, total, check_name in manager(self.client):
            if eval(check_name) is not True:
                continue
            if violators:
                return False
        return True

    def leaf(self, n=0) -> typing.Optional[Leaf]:
        r"""
        Gets leaf ``n``.

        ..  container:: example

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Voice("c'8 d'8 e'8 f'8"))
            >>> staff.append(abjad.Voice("g'8 a'8 b'8 c''8"))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                    \new Voice
                    {
                        g'8
                        a'8
                        b'8
                        c''8
                    }
                }

        ..  container:: example

            Gets leaf ``n`` **from** client when client is a leaf.

            With positive indices:

            >>> first_leaf = staff[0][0]
            >>> first_leaf
            Note("c'8")

            >>> for n in range(8):
            ...     leaf = abjad.inspect(first_leaf).leaf(n)
            ...     print(n, leaf)
            ...
            0 c'8
            1 d'8
            2 e'8
            3 f'8
            4 None
            5 None
            6 None
            7 None

            With negative indices:

            >>> last_leaf = staff[0][-1]
            >>> last_leaf
            Note("f'8")

            >>> for n in range(0, -8, -1):
            ...     leaf = abjad.inspect(last_leaf).leaf(n)
            ...     print(n, leaf)
            ...
            0 f'8
            -1 e'8
            -2 d'8
            -3 c'8
            -4 None
            -5 None
            -6 None
            -7 None

        ..  container:: example

            Gets leaf ``n`` **in** client when client is a container.

            With positive indices:

            >>> first_voice = staff[0]
            >>> first_voice
            Voice("c'8 d'8 e'8 f'8")

            >>> for n in range(8):
            ...     leaf = abjad.inspect(first_voice).leaf(n)
            ...     print(n, leaf)
            ...
            0 c'8
            1 d'8
            2 e'8
            3 f'8
            4 None
            5 None
            6 None
            7 None

            With negative indices:

            >>> first_voice = staff[0]
            >>> first_voice
            Voice("c'8 d'8 e'8 f'8")

            >>> for n in range(-1, -9, -1):
            ...     leaf = abjad.inspect(first_voice).leaf(n)
            ...     print(n, leaf)
            ...
            -1 f'8
            -2 e'8
            -3 d'8
            -4 c'8
            -5 None
            -6 None
            -7 None
            -8 None

        """
        if isinstance(self.client, Leaf):
            return self.client._get_leaf(n)
        if 0 <= n:
            reverse = False
        else:
            reverse = True
            n = abs(n) - 1
        leaves = iterate(self.client).leaves(reverse=reverse)
        for i, leaf in enumerate(leaves):
            if i == n:
                return leaf
        return None

    def lineage(self) -> Lineage:
        """
        Gets lineage.
        """
        if not isinstance(self.client, Component):
            raise Exception('can only get lineage on component.')
        return self.client._get_lineage()

    def logical_tie(self) -> LogicalTie:
        """
        Gets logical tie.
        """
        if not isinstance(self.client, Leaf):
            raise Exception('can only get logical tie on leaf.')
        return self.client._get_logical_tie()

    def markup(self, direction=None) -> typing.List[Markup]:
        """
        Gets markup.
        """
        # TODO: extend to any non-none client
        if not isinstance(self.client, Component):
            raise Exception('can only get markup on component.')
        result = self.client._get_markup(direction=direction)
        return list(result)

    def parentage(
        self,
        include_self=True,
        grace_notes=False,
        ) -> Parentage:
        r"""
        Gets parentage.

        .. container:: example

            Gets parentage without grace notes:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> container = abjad.GraceContainer("c'16 d'16")
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \grace {
                        c'16
                        d'16
                    }
                    d'4
                    e'4
                    f'4
                }

            >>> abjad.inspect(container[0]).parentage()
            Parentage(component=Note("c'16"))

        .. container:: example

            Gets parentage with grace notes:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> container = abjad.GraceContainer("c'16 d'16")
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \grace {
                        c'16
                        d'16
                    }
                    d'4
                    e'4
                    f'4
                }

            >>> agent = abjad.inspect(container[0])
            >>> parentage = agent.parentage(grace_notes=True)
            >>> for component in parentage:
            ...     component
            ...
            Note("c'16")
            GraceContainer("c'16 d'16")
            Note("d'4")
            Voice("c'4 d'4 e'4 f'4")

        """
        if not isinstance(self.client, Component):
            raise Exception('can only get parentage on component.')
        return self.client._get_parentage(
            include_self=include_self,
            grace_notes=grace_notes,
            )

    def pitches(self) -> typing.Optional[PitchSet]:
        """
        Gets pitches.
        """
        if not self.client:
            return None
        selection = Selection(self.client)
        return PitchSet.from_selection(selection)

    def report_modifications(self) -> str:
        r"""
        Reports modifications.

        ..  container:: example

            Reports container modifications:

            >>> container = abjad.Container("c'8 d'8 e'8 f'8")
            >>> abjad.override(container).note_head.color = 'red'
            >>> abjad.override(container).note_head.style = 'harmonic'
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    \override NoteHead.color = #red
                    \override NoteHead.style = #'harmonic
                    c'8
                    d'8
                    e'8
                    f'8
                    \revert NoteHead.color
                    \revert NoteHead.style
                }

            >>> report = abjad.inspect(container).report_modifications()
            >>> print(report)
            {
                \override NoteHead.color = #red
                \override NoteHead.style = #'harmonic
                %%% 4 components omitted %%%
                \revert NoteHead.color
                \revert NoteHead.style
            }

        ..  container:: example

            Reports leaf modifications:

            >>> container = abjad.Container("c'8 d'8 e'8 f'8")
            >>> abjad.attach(abjad.Clef('alto'), container[0])
            >>> abjad.override(container[0]).note_head.color = 'red'
            >>> abjad.override(container[0]).stem.color = 'red'
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    \clef "alto"
                    c'8
                    d'8
                    e'8
                    f'8
                }

            >>> report = abjad.inspect(container[0]).report_modifications()
            >>> print(report)
            slot absolute before:
            slot 1:
                grob overrides:
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
            slot 3:
                commands:
                    \clef "alto"
            slot 4:
                leaf body:
                    c'8
            slot 5:
            slot 7:
            slot absolute after:

        """
        if isinstance(self.client, Container):
            bundle = LilyPondFormatManager.bundle_format_contributions(
                self.client
                )
            result: typing.List[str] = []
            for slot in ('before', 'open brackets', 'opening'):
                lines = self.client._get_format_contributions_for_slot(
                    slot,
                    bundle,
                    )
                result.extend(lines)
            line = f'    %%% {len(self.client)} components omitted %%%'
            result.append(line)
            for slot in ('closing', 'close brackets', 'after'):
                lines = self.client._get_format_contributions_for_slot(
                    slot,
                    bundle,
                    )
                result.extend(lines)
            return '\n'.join(result)
        elif isinstance(self.client, Leaf):
            return self.client._report_format_contributions()
        else:
            return f'only defined for components: {self.client}.'

    def sounding_pitch(self) -> NamedPitch:
        r"""
        Gets sounding pitch.

        ..  container:: example

            >>> staff = abjad.Staff("d''8 e''8 f''8 g''8")
            >>> piccolo = abjad.Piccolo()
            >>> abjad.attach(piccolo, staff[0])
            >>> abjad.Instrument.transpose_from_sounding_pitch(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    d'8
                    e'8
                    f'8
                    g'8
                }

        """
        if not isinstance(self.client, Note):
            raise Exception('can only get sounding pitch of note.')
        return self.client._get_sounding_pitch()

    # TODO: return PitchSet instead of list
    def sounding_pitches(self) -> typing.List[NamedPitch]:
        r"""
        Gets sounding pitches.

        ..  container:: example

            >>> staff = abjad.Staff("<c''' e'''>4 <d''' fs'''>4")
            >>> glockenspiel = abjad.Glockenspiel()
            >>> abjad.attach(glockenspiel, staff[0])
            >>> abjad.Instrument.transpose_from_sounding_pitch(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    <c' e'>4
                    <d' fs'>4
                }

            >>> abjad.inspect(staff[0]).sounding_pitches()
            [NamedPitch("c'''"), NamedPitch("e'''")]

        Returns tuple.
        """
        # TODO: extend to any non-none client
        if not isinstance(self.client, Chord):
            raise Exception('can only get sounding pitches of chord.')
        result = self.client._get_sounding_pitches()
        return list(result)

    def spanner(
        self,
        prototype=None,
        default=None,
        ) -> typing.Any:
        """
        Gets spanner.

        Raises exception when more than one spanner of ``prototype`` attaches
        to client.

        Returns ``default`` when no spanner of ``prototype`` attaches to
        client.
        """
        # TODO: extend to any non-none client
        if not isinstance(self.client, (Leaf, Selection)):
            raise Exception('can only get spanner on leaf or selection.')
        spanners = self.client._get_spanners(prototype=prototype)
        assert isinstance(spanners, list), repr(spanners)
        if not spanners:
            return default
        elif len(spanners) == 1:
            return spanners[0]
        else:
            raise exceptions.ExtraSpannerError

    def spanners(self, prototype=None) -> typing.List[Spanner]:
        r"""
        Gets spanners.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d' e' f'")
            >>> abjad.attach(abjad.Beam(), staff[:2])
            >>> abjad.attach(abjad.Beam(), staff[2:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    [
                    d'8
                    ]
                    e'8
                    [
                    f'8
                    ]
                }

            >>> abjad.inspect(staff).spanners()
            []

            >>> abjad.inspect(staff[0]).spanners()
            [Beam("c'8, d'8", durations=(), span_beam_count=1)]

            >>> beams = abjad.inspect(staff[:]).spanners()
            >>> beams = list(beams)
            >>> beams.sort()
            >>> beams
            [Beam("c'8, d'8", durations=(), span_beam_count=1), Beam("e'8, f'8", durations=(), span_beam_count=1)]

        """
        if isinstance(self.client, Container):
            return []
        if isinstance(self.client, (Leaf, Selection)):
            return self.client._get_spanners(prototype=prototype)
        assert isinstance(self.client, collections.Iterable), repr(self.client)
        known_ids: typing.List[int] = []
        result = []
        for item in self.client:
            for spanner in inspect(item).spanners(prototype=prototype):
                id_ = id(spanner)
                if id_ not in known_ids:
                    known_ids.append(id_)
                    result.append(spanner)
        return result

    def tabulate_wellformedness(
        self,
        allow_percussion_clef=None,
        check_beamed_long_notes=True,
        check_discontiguous_spanners=True,
        check_duplicate_ids=True,
        check_empty_containers=True,
        check_misdurated_measures=True,
        check_misfilled_measures=True,
        check_mismatched_enchained_hairpins=True,
        check_mispitched_ties=True,
        check_misrepresented_flags=True,
        check_missing_parents=True,
        check_nested_measures=True,
        check_notes_on_wrong_clef=True,
        check_out_of_range_notes=True,
        check_overlapping_beams=True,
        check_overlapping_glissandi=True,
        check_overlapping_hairpins=True,
        check_overlapping_octavation_spanners=True,
        check_overlapping_ties=True,
        check_overlapping_trill_spanners=True,
        check_tied_rests=True,
        ) -> str:
        r"""
        Tabulates well-formedness.
        """
        manager = WellformednessManager(
            allow_percussion_clef=allow_percussion_clef,
            )
        triples = manager(self.client)
        strings = []
        for violators, total, check_name in triples:
            if eval(check_name) is not True:
                continue
            violator_count = len(violators)
            check_name = check_name.replace('check_', '')
            check_name = check_name.replace('_', ' ')
            string = f'{violator_count} /\t{total} {check_name}'
            strings.append(string)
        return '\n'.join(strings)

    def timespan(self, in_seconds=False) -> Timespan:
        r"""
        Gets timespan.

        ..  container:: example

            Gets timespan of grace notes:

            >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
            >>> grace_notes = [abjad.Note("c'16"), abjad.Note("d'16")]
            >>> container = abjad.GraceContainer(grace_notes)
            >>> abjad.attach(container, voice[1])
            >>> container = abjad.AfterGraceContainer("e'16 f'16")
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'8
                    [
                    \grace {
                        c'16
                        d'16
                    }
                    \afterGrace
                    d'8
                    {
                        e'16
                        f'16
                    }
                    e'8
                    f'8
                    ]
                }

            >>> for leaf in abjad.iterate(voice).leaves():
            ...     timespan = abjad.inspect(leaf).timespan()
            ...     print(str(leaf) + ':')
            ...     abjad.f(timespan)
            ...
            c'8:
            abjad.Timespan(
                start_offset=abjad.Offset(0, 1),
                stop_offset=abjad.Offset(1, 8),
                )
            c'16:
            abjad.Timespan(
                start_offset=abjad.Offset(
                    (1, 8),
                    grace_displacement=abjad.Duration(-1, 8),
                    ),
                stop_offset=abjad.Offset(
                    (1, 8),
                    grace_displacement=abjad.Duration(-1, 16),
                    ),
                )
            d'16:
            abjad.Timespan(
                start_offset=abjad.Offset(
                    (1, 8),
                    grace_displacement=abjad.Duration(-1, 16),
                    ),
                stop_offset=abjad.Offset(1, 8),
                )
            d'8:
            abjad.Timespan(
                start_offset=abjad.Offset(1, 8),
                stop_offset=abjad.Offset(1, 4),
                )
            e'16:
            abjad.Timespan(
                start_offset=abjad.Offset(
                    (1, 4),
                    grace_displacement=abjad.Duration(-1, 8),
                    ),
                stop_offset=abjad.Offset(
                    (1, 4),
                    grace_displacement=abjad.Duration(-1, 16),
                    ),
                )
            f'16:
            abjad.Timespan(
                start_offset=abjad.Offset(
                    (1, 4),
                    grace_displacement=abjad.Duration(-1, 16),
                    ),
                stop_offset=abjad.Offset(1, 4),
                )
            e'8:
            abjad.Timespan(
                start_offset=abjad.Offset(1, 4),
                stop_offset=abjad.Offset(3, 8),
                )
            f'8:
            abjad.Timespan(
                start_offset=abjad.Offset(3, 8),
                stop_offset=abjad.Offset(1, 2),
                )

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d' e' f'")
            >>> abjad.attach(abjad.Beam(), staff[:2])
            >>> abjad.attach(abjad.Beam(), staff[2:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    [
                    d'8
                    ]
                    e'8
                    [
                    f'8
                    ]
                }

            >>> abjad.inspect(staff).timespan()
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(1, 2))

            >>> abjad.inspect(staff[0]).timespan()
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(1, 8))

            >>> abjad.inspect(staff[:3]).timespan()
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(3, 8))

        """
        if isinstance(self.client, Component):
            return self.client._get_timespan(in_seconds=in_seconds)
        assert isinstance(self.client, collections.Iterable), repr(self.client)
        remaining_items = []
        for i, item in enumerate(self.client):
            if i == 0:
                first_item = item
            else:
                remaining_items.append(item)
        timespan = Inspection(first_item).timespan(in_seconds=in_seconds)
        start_offset = timespan.start_offset
        stop_offset = timespan.stop_offset
        for item in remaining_items:
            timespan = Inspection(item).timespan(in_seconds=in_seconds)
            if timespan.start_offset < start_offset:
                start_offset = timespan.start_offset
            if stop_offset < timespan.stop_offset:
                stop_offset = timespan.stop_offset
        return Timespan(start_offset, stop_offset)

    def tuplet(self, n=0) -> typing.Optional[Tuplet]:
        r"""
        Gets tuplet ``n``.

        ..  container:: example

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Tuplet((2, 3), "c'8 d' e'"))
            >>> staff.append(abjad.Tuplet((2, 3), "d'8 e' f'"))
            >>> staff.append(abjad.Tuplet((2, 3), "e'8 f' g'"))
            >>> staff.append(abjad.Tuplet((2, 3), "f'8 g' a'"))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 2/3 {
                        c'8
                        d'8
                        e'8
                    }
                    \times 2/3 {
                        d'8
                        e'8
                        f'8
                    }
                    \times 2/3 {
                        e'8
                        f'8
                        g'8
                    }
                    \times 2/3 {
                        f'8
                        g'8
                        a'8
                    }
                }

        ..  container:: example

            >>> for n in range(4):
            ...     tuplet = abjad.inspect(staff).tuplet(n)
            ...     print(n, tuplet)
            ...
            0 Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")
            1 Tuplet(Multiplier(2, 3), "d'8 e'8 f'8")
            2 Tuplet(Multiplier(2, 3), "e'8 f'8 g'8")
            3 Tuplet(Multiplier(2, 3), "f'8 g'8 a'8")

            >>> for n in range(-1, -5, -1):
            ...     tuplet = abjad.inspect(staff).tuplet(n)
            ...     print(n, tuplet)
            ...
            -1 Tuplet(Multiplier(2, 3), "f'8 g'8 a'8")
            -2 Tuplet(Multiplier(2, 3), "e'8 f'8 g'8")
            -3 Tuplet(Multiplier(2, 3), "d'8 e'8 f'8")
            -4 Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")

        """
        if 0 <= n:
            reverse = False
        else:
            reverse = True
            n = abs(n) - 1
        tuplets = iterate(self.client).components(Tuplet, reverse=reverse)
        for i, tuplet in enumerate(tuplets):
            if i == n:
                return tuplet
        return None

    def vertical_moment(self, governor=None) -> VerticalMoment:
        r"""
        Gets vertical moment.

        ..  container:: example

            >>> score = abjad.Score()
            >>> tuplet = abjad.Tuplet((4, 3), "d''8 c''8 b'8")
            >>> score.append(abjad.Staff([tuplet]))
            >>> staff_group = abjad.StaffGroup(lilypond_type='PianoStaff')
            >>> staff_group.append(abjad.Staff("a'4 g'4"))
            >>> staff_group.append(abjad.Staff("f'8 e'8 d'8 c'8"))
            >>> clef = abjad.Clef('bass')
            >>> abjad.attach(clef, staff_group[1][0])
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

            >>> agent = abjad.inspect(staff_group[1][0])
            >>> moment = agent.vertical_moment(governor=staff_group)
            >>> moment.leaves
            Selection([Note("a'4"), Note("f'8")])

            >>> agent = abjad.inspect(staff_group[1][1])
            >>> moment = agent.vertical_moment(governor=staff_group)
            >>> moment.leaves
            Selection([Note("a'4"), Note("e'8")])

            >>> agent = abjad.inspect(staff_group[1][2])
            >>> moment = agent.vertical_moment(governor=staff_group)
            >>> moment.leaves
            Selection([Note("g'4"), Note("d'8")])

            >>> agent = abjad.inspect(staff_group[1][3])
            >>> moment = agent.vertical_moment(governor=staff_group)
            >>> moment.leaves
            Selection([Note("g'4"), Note("c'8")])

        """
        if not isinstance(self.client, Component):
            raise Exception('can only get vertical moment on component.')
        return self.client._get_vertical_moment(governor=governor)

    def vertical_moment_at(self, offset) -> VerticalMoment:
        """
        Gets vertical moment at ``offset``.
        """
        if not isinstance(self.client, Component):
            raise Exception('can only get vertical moment on component.')
        return self.client._get_vertical_moment_at(offset)

    def wrapper(self, prototype=None) -> typing.Optional[Wrapper]:
        r"""
        Gets wrapper.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Articulation('^'), staff[0])
            >>> abjad.attach(abjad.Articulation('^'), staff[1])
            >>> abjad.attach(abjad.Articulation('^'), staff[2])
            >>> abjad.attach(abjad.Articulation('^'), staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    -\marcato
                    d'4
                    -\marcato
                    e'4
                    -\marcato
                    f'4
                    -\marcato
                }

            >>> abjad.inspect(staff).wrapper(abjad.Articulation) is None
            True

            >>> abjad.inspect(staff[0]).wrapper(abjad.Articulation)
            Wrapper(indicator=Articulation('^'), tag=Tag())

        Raises exception when more than one indicator of ``prototype`` attach
        to client.
        """
        return self.indicator(prototype=prototype, unwrap=False)

    def wrappers(self, prototype=None) -> typing.Optional[
        typing.List[Wrapper]
        ]:
        r"""
        Gets wrappers.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Articulation('^'), staff[0])
            >>> abjad.attach(abjad.Articulation('^'), staff[1])
            >>> abjad.attach(abjad.Articulation('^'), staff[2])
            >>> abjad.attach(abjad.Articulation('^'), staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    -\marcato
                    d'4
                    -\marcato
                    e'4
                    -\marcato
                    f'4
                    -\marcato
                }

            >>> abjad.inspect(staff).wrappers(abjad.Articulation)
            []

            >>> abjad.inspect(staff[0]).wrappers(abjad.Articulation)
            [Wrapper(indicator=Articulation('^'), tag=Tag())]

        """
        return self.indicators(prototype=prototype, unwrap=False)
