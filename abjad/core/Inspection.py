import collections
import typing
from abjad import enums
from abjad import exceptions
from abjad import typings
from abjad.indicators.TimeSignature import TimeSignature
from abjad.markups import Markup
from abjad.pitch.NamedPitch import NamedPitch
from abjad.pitch.PitchSet import PitchSet
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.system.Wrapper import Wrapper
from abjad.timespans import Timespan
from abjad.top.inspect import inspect
from abjad.top.iterate import iterate
from abjad.utilities.Duration import Duration
from abjad.utilities.Offset import Offset
from .AfterGraceContainer import AfterGraceContainer
from .Chord import Chord
from .Component import Component
from .Container import Container
from .Descendants import Descendants
from .GraceContainer import GraceContainer
from .Leaf import Leaf
from .Lineage import Lineage
from .LogicalTie import LogicalTie
from .Note import Note
from .OnBeatGraceContainer import OnBeatGraceContainer
from .Parentage import Parentage
from .Selection import Selection
from .Staff import Staff
from .Tuplet import Tuplet
from .VerticalMoment import VerticalMoment
from .Wellformedness import Wellformedness


class Inspection(object):
    """
    Inspection.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.inspect(staff)
        Inspection(client=Staff("c'4 e'4 d'4 f'4"))

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Collaborators"

    __slots__ = ("_client",)

    ### INITIALIZER ###

    def __init__(
        self,
        client: typing.Union[Component, typing.Iterable[Component]] = None,
    ) -> None:
        assert not isinstance(client, str), repr(client)
        prototype = (Component, collections.abc.Iterable, type(None))
        if not isinstance(client, prototype):
            message = "must be component, nonstring iterable or none:"
            message += f" (not {client!r})."
            raise TypeError(message)
        self._client = client

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Delegates to storage format manager.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def client(
        self
    ) -> typing.Union[Component, typing.Iterable[Component], None]:
        r"""
        Gets client.

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

            >>> abjad.inspect(staff).client
            Staff("c'4 d'4 e'4 f'4")

        """
        return self._client

    ### PUBLIC METHODS ###

    def after_grace_container(self) -> typing.Optional[AfterGraceContainer]:
        r"""
        Gets after grace containers attached to component.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, voice[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, voice[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(voice).components():
            ...     container = abjad.inspect(component).after_grace_container()
            ...     print(f"{repr(component):30} {repr(container)}")
            Voice("c'4 d'4 e'4 f'4")       None
            Note("c'4")                    None
            GraceContainer("cs'16")        None
            Note("cs'16")                  None
            Note("d'4")                    None
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") None
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") None
            Note("gs'16 * 1")              None
            Note("a'16 * 1")               None
            Note("as'16 * 1")              None
            Note("e'4")                    None
            Note("f'4")                    AfterGraceContainer("fs'16")
            AfterGraceContainer("fs'16")   None
            Note("fs'16")                  None

        """
        return getattr(self.client, "_after_grace_container", None)

    def annotation(
        self,
        annotation: typing.Any,
        default: typing.Any = None,
        unwrap: bool = True,
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
        for wrapper in getattr(self.client, "_wrappers", []):
            if wrapper.annotation:
                result.append(wrapper)
        return result

    def badly_formed_components(self) -> typing.List[Component]:
        r"""
        Gets badly formed components.
        """
        manager = Wellformedness()
        violators: typing.List[Component] = []
        for violators_, total, check_name in manager(self.client):
            violators.extend(violators_)
        return violators

    def bar_line_crossing(self) -> bool:
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
            ...     result = abjad.inspect(note).bar_line_crossing()
            ...     print(note, result)
            ...
            c'4 False
            d'4 True
            e'4 False

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get indicator on component.")
        time_signature = self.client._get_effective(TimeSignature)
        if time_signature is None:
            time_signature_duration = Duration(4, 4)
        else:
            time_signature_duration = time_signature.duration
        partial = getattr(time_signature, "partial", 0)
        partial = partial or 0
        start_offset = Inspection(self.client).timespan().start_offset
        shifted_start = start_offset - partial
        shifted_start %= time_signature_duration
        stop_offset = self.client._get_duration() + shifted_start
        if time_signature_duration < stop_offset:
            return True
        return False

    def contents(self,) -> typing.Optional[Selection]:
        r"""
        Gets contents.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, voice[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, voice[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(voice).components():
            ...     contents = abjad.inspect(component).contents()
            ...     print(f"{repr(component)}:")
            ...     for component_ in contents:
            ...         print(f"    {repr(component_)}")
            Voice("c'4 d'4 e'4 f'4"):
                Voice("c'4 d'4 e'4 f'4")
                Note("c'4")
                Note("d'4")
                Note("e'4")
                Note("f'4")
            Note("c'4"):
                Note("c'4")
            GraceContainer("cs'16"):
                GraceContainer("cs'16")
                Note("cs'16")
            Note("cs'16"):
                Note("cs'16")
            Note("d'4"):
                Note("d'4")
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1"):
                OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1")
                Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1")
                Note("gs'16 * 1")
                Note("a'16 * 1")
                Note("as'16 * 1")
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1"):
                Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1")
            Note("gs'16 * 1"):
                Note("gs'16 * 1")
            Note("a'16 * 1"):
                Note("a'16 * 1")
            Note("as'16 * 1"):
                Note("as'16 * 1")
            Note("e'4"):
                Note("e'4")
            Note("f'4"):
                Note("f'4")
            AfterGraceContainer("fs'16"):
                AfterGraceContainer("fs'16")
                Note("fs'16")
            Note("fs'16"):
                Note("fs'16")

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get contents of component.")
        return self.client._get_contents()

    def descendants(self,) -> typing.Union[Descendants, Selection]:
        r"""
        Gets descendants.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, voice[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, voice[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(voice).components():
            ...     descendants = abjad.inspect(component).descendants()
            ...     print(f"{repr(component)}:")
            ...     for component_ in descendants:
            ...         print(f"    {repr(component_)}")
            Voice("c'4 d'4 e'4 f'4"):
                Voice("c'4 d'4 e'4 f'4")
                Note("c'4")
                GraceContainer("cs'16")
                Note("cs'16")
                Note("d'4")
                OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1")
                Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1")
                Note("gs'16 * 1")
                Note("a'16 * 1")
                Note("as'16 * 1")
                Note("e'4")
                Note("f'4")
                AfterGraceContainer("fs'16")
                Note("fs'16")
            Note("c'4"):
                Note("c'4")
            GraceContainer("cs'16"):
                GraceContainer("cs'16")
                Note("cs'16")
            Note("cs'16"):
                Note("cs'16")
            Note("d'4"):
                Note("d'4")
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1"):
                OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1")
                Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1")
                Note("gs'16 * 1")
                Note("a'16 * 1")
                Note("as'16 * 1")
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1"):
                Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1")
            Note("gs'16 * 1"):
                Note("gs'16 * 1")
            Note("a'16 * 1"):
                Note("a'16 * 1")
            Note("as'16 * 1"):
                Note("as'16 * 1")
            Note("e'4"):
                Note("e'4")
            Note("f'4"):
                Note("f'4")
            AfterGraceContainer("fs'16"):
                AfterGraceContainer("fs'16")
                Note("fs'16")
            Note("fs'16"):
                Note("fs'16")

        """
        if isinstance(self.client, Component):
            return Descendants(self.client)
        descendants: typing.List[Component] = []
        assert isinstance(self.client, Selection)
        for argument in self.client:
            descendants_ = Inspection(argument).descendants()
            for descendant_ in descendants_:
                if descendant_ not in descendants:
                    descendants.append(descendant_)
        result = Selection(descendants)
        return result

    def duration(self, in_seconds: bool = False) -> Duration:
        r"""
        Gets duration.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, voice[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, voice[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(voice).components():
            ...     duration = abjad.inspect(component).duration()
            ...     print(f"{repr(component):30} {repr(duration)}")
            Voice("c'4 d'4 e'4 f'4")       Duration(1, 1)
            Note("c'4")                    Duration(1, 4)
            GraceContainer("cs'16")        Duration(1, 16)
            Note("cs'16")                  Duration(1, 16)
            Note("d'4")                    Duration(1, 4)
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") Duration(1, 4)
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") Duration(1, 16)
            Note("gs'16 * 1")              Duration(1, 16)
            Note("a'16 * 1")               Duration(1, 16)
            Note("as'16 * 1")              Duration(1, 16)
            Note("e'4")                    Duration(1, 4)
            Note("f'4")                    Duration(1, 4)
            AfterGraceContainer("fs'16")   Duration(1, 16)
            Note("fs'16")                  Duration(1, 16)

        ..  container:: example

            REGRESSION. Works with selections:

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
        assert isinstance(self.client, collections.abc.Iterable), repr(
            self.client
        )
        durations = [
            Inspection(_).duration(in_seconds=in_seconds) for _ in self.client
        ]
        return Duration(sum(durations))

    def effective(
        self,
        prototype: typings.Prototype,
        *,
        attributes: typing.Dict = None,
        default: bool = None,
        n: int = 0,
        unwrap: bool = True,
    ) -> typing.Any:
        r"""
        Gets effective indicator.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef("alto"), staff[0])
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, staff[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     clef = abjad.inspect(component).effective(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(clef)}")
            Staff("c'4 d'4 e'4 f'4")       Clef('alto')
            Note("c'4")                    Clef('alto')
            GraceContainer("cs'16")        Clef('alto')
            Note("cs'16")                  Clef('alto')
            Note("d'4")                    Clef('alto')
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") None
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") None
            Note("gs'16 * 1")              None
            Note("a'16 * 1")               None
            Note("as'16 * 1")              None
            Note("e'4")                    Clef('alto')
            Note("f'4")                    Clef('alto')
            AfterGraceContainer("fs'16")   Clef('alto')
            Note("fs'16")                  Clef('alto')

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

        ..  container:: example

            Test attributes like this:

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> start_text_span = abjad.StartTextSpan()
            >>> abjad.attach(start_text_span, voice[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, voice[2])
            >>> abjad.show(voice) # doctest: +SKIP 

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \startTextSpan
                    d'4
                    e'4
                    \stopTextSpan
                    f'4
                }

            >>> for note in voice:
            ...     note, abjad.inspect(note).effective(abjad.StartTextSpan)
            ...
            (Note("c'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))
            (Note("d'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))
            (Note("e'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))
            (Note("f'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))

            >>> for note in voice:
            ...     note, abjad.inspect(note).effective(abjad.StopTextSpan)
            ...
            (Note("c'4"), None)
            (Note("d'4"), None)
            (Note("e'4"), StopTextSpan(command='\\stopTextSpan'))
            (Note("f'4"), StopTextSpan(command='\\stopTextSpan'))

            >>> attributes = {'parameter': 'TEXT_SPANNER'}
            >>> for note in voice:
            ...     indicator = abjad.inspect(note).effective(
            ...         object,
            ...         attributes=attributes,
            ...         )
            ...     note, indicator
            ...
            (Note("c'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))
            (Note("d'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))
            (Note("e'4"), StopTextSpan(command='\\stopTextSpan'))
            (Note("f'4"), StopTextSpan(command='\\stopTextSpan'))

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get effective on components.")
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        result = self.client._get_effective(
            prototype, attributes=attributes, n=n, unwrap=unwrap
        )
        if result is None:
            result = default
        return result

    def effective_staff(self) -> typing.Optional[Staff]:
        r"""
        Gets effective staff.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> staff = abjad.Staff("c'4 d' e' f'", name="Music_Staff")
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, staff[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \context Staff = "Music_Staff"
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     staff = abjad.inspect(component).effective_staff()
            ...     print(f"{repr(component):30} {repr(staff)}")
            Staff("c'4 d'4 e'4 f'4", name='Music_Staff') Staff("c'4 d'4 e'4 f'4", name='Music_Staff')
            Note("c'4")                    Staff("c'4 d'4 e'4 f'4", name='Music_Staff')
            GraceContainer("cs'16")        Staff("c'4 d'4 e'4 f'4", name='Music_Staff')
            Note("cs'16")                  Staff("c'4 d'4 e'4 f'4", name='Music_Staff')
            Note("d'4")                    Staff("c'4 d'4 e'4 f'4", name='Music_Staff')
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") None
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") None
            Note("gs'16 * 1")              None
            Note("a'16 * 1")               None
            Note("as'16 * 1")              None
            Note("e'4")                    Staff("c'4 d'4 e'4 f'4", name='Music_Staff')
            Note("f'4")                    Staff("c'4 d'4 e'4 f'4", name='Music_Staff')
            AfterGraceContainer("fs'16")   Staff("c'4 d'4 e'4 f'4", name='Music_Staff')
            Note("fs'16")                  Staff("c'4 d'4 e'4 f'4", name='Music_Staff')

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get effective staff on components.")
        return self.client._get_effective_staff()

    def effective_wrapper(
        self,
        prototype: typings.Prototype,
        *,
        attributes: typing.Dict = None,
        n: int = 0,
    ) -> typing.Optional[Wrapper]:
        r"""
        Gets effective wrapper.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef("alto"), staff[0])
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, staff[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     wrapper = inspection.effective_wrapper(abjad.Clef)
            ...     print(f"{repr(component):}")
            ...     print(f"    {repr(wrapper)}")
            Staff("c'4 d'4 e'4 f'4")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Note("c'4")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            GraceContainer("cs'16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Note("cs'16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Note("d'4")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1")
                None
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1")
                None
            Note("gs'16 * 1")
                None
            Note("a'16 * 1")
                None
            Note("as'16 * 1")
                None
            Note("e'4")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Note("f'4")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            AfterGraceContainer("fs'16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Note("fs'16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())

        """
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        return self.effective(
            prototype, attributes=attributes, n=n, unwrap=False
        )

    def grace(self) -> bool:
        r"""
        Is true when client is grace music.

        Grace music defined equal to grace container, after-grace container and
        contents of those containers.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef("alto"), staff[0])
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, staff[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).grace()
            ...     print(f"{repr(component):30} {repr(result)}")
            Staff("c'4 d'4 e'4 f'4")       False
            Note("c'4")                    False
            GraceContainer("cs'16")        True
            Note("cs'16")                  True
            Note("d'4")                    False
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") True
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") True
            Note("gs'16 * 1")              True
            Note("a'16 * 1")               True
            Note("as'16 * 1")              True
            Note("e'4")                    False
            Note("f'4")                    False
            AfterGraceContainer("fs'16")   True
            Note("fs'16")                  True

        """
        prototype = (AfterGraceContainer, GraceContainer, OnBeatGraceContainer)
        if isinstance(self.client, prototype):
            return True
        for component in Inspection(self.client).parentage():
            if isinstance(component, prototype):
                return True
        return False

    def grace_container(self) -> typing.Optional[GraceContainer]:
        r"""
        Gets grace container attached to leaf.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, staff[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     container = abjad.inspect(component).grace_container()
            ...     print(f"{repr(component):30} {repr(container)}")
            Staff("c'4 d'4 e'4 f'4")       None
            Note("c'4")                    None
            GraceContainer("cs'16")        None
            Note("cs'16")                  None
            Note("d'4")                    GraceContainer("cs'16")
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") None
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") None
            Note("gs'16 * 1")              None
            Note("a'16 * 1")               None
            Note("as'16 * 1")              None
            Note("e'4")                    None
            Note("f'4")                    None
            AfterGraceContainer("fs'16")   None
            Note("fs'16")                  None

        """
        return getattr(self.client, "_grace_container", None)

    def has_effective_indicator(
        self,
        prototype: typings.Prototype = None,
        *,
        attributes: typing.Dict = None,
    ) -> bool:
        r"""
        Is true when client has effective indicator.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef("alto"), staff[2])
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, staff[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        \clef "alto"
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     result = inspection.has_effective_indicator(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(result)}")
            Staff("c'4 d'4 e'4 f'4")       False
            Note("c'4")                    False
            GraceContainer("cs'16")        False
            Note("cs'16")                  False
            Note("d'4")                    False
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") False
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") False
            Note("gs'16 * 1")              False
            Note("a'16 * 1")               False
            Note("as'16 * 1")              False
            Note("e'4")                    True
            Note("f'4")                    True
            AfterGraceContainer("fs'16")   True
            Note("fs'16")                  True

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get effective indicator on component.")
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        return self.client._has_effective_indicator(
            prototype=prototype, attributes=attributes
        )

    def has_indicator(
        self,
        prototype: typings.Prototype = None,
        *,
        attributes: typing.Dict = None,
    ) -> bool:
        r"""
        Is true when client has one or more indicators.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef("alto"), staff[2])
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, staff[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        \clef "alto"
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     result = inspection.has_indicator(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(result)}")
            Staff("c'4 d'4 e'4 f'4")       False
            Note("c'4")                    False
            GraceContainer("cs'16")        False
            Note("cs'16")                  False
            Note("d'4")                    False
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") False
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") False
            Note("gs'16 * 1")              False
            Note("a'16 * 1")               False
            Note("as'16 * 1")              False
            Note("e'4")                    True
            Note("f'4")                    False
            AfterGraceContainer("fs'16")   False
            Note("fs'16")                  False

        ..  container:: example

            Set ``attributes`` dictionary to test indicator attributes:

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> abjad.attach(abjad.Clef('treble'), voice[0])
            >>> abjad.attach(abjad.Clef('alto'), voice[2])
            >>> abjad.show(voice) # doctest: +SKIP 

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    \clef "treble"
                    c'4
                    c'4
                    \clef "alto"
                    c'4
                    c'4
                }

            >>> attributes = {'name': 'alto'}
            >>> abjad.inspect(voice[0]).has_indicator(abjad.Clef)
            True

            >>> abjad.inspect(voice[0]).has_indicator(
            ...     abjad.Clef,
            ...     attributes=attributes,
            ...     )
            False

            >>> abjad.inspect(voice[2]).has_indicator(abjad.Clef)
            True

            >>> abjad.inspect(voice[2]).has_indicator(
            ...     abjad.Clef,
            ...     attributes=attributes,
            ...     )
            True


        """
        if not isinstance(self.client, Component):
            raise Exception("can only get indicator on component.")
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        return self.client._has_indicator(
            prototype=prototype, attributes=attributes
        )

    def indicator(
        self,
        prototype: typings.Prototype = None,
        *,
        default: typing.Any = None,
        unwrap: bool = True,
    ) -> typing.Any:
        r"""
        Gets indicator.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef("alto"), staff[0])
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, staff[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).indicator(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(result)}")
            Staff("c'4 d'4 e'4 f'4")       None
            Note("c'4")                    Clef('alto')
            GraceContainer("cs'16")        None
            Note("cs'16")                  None
            Note("d'4")                    None
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") None
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") None
            Note("gs'16 * 1")              None
            Note("a'16 * 1")               None
            Note("as'16 * 1")              None
            Note("e'4")                    None
            Note("f'4")                    None
            AfterGraceContainer("fs'16")   None
            Note("fs'16")                  None

        Raises exception when more than one indicator of ``prototype`` attach
        to client.

        Returns default when no indicator of ``prototype`` attaches to client.
        """
        if not isinstance(self.client, Component):
            raise Exception("can only get indicator on component.")
        indicators = self.client._get_indicators(
            prototype=prototype, unwrap=unwrap
        )
        if not indicators:
            return default
        elif len(indicators) == 1:
            return list(indicators)[0]
        else:
            raise Exception("multiple indicators attached to client.")

    def indicators(
        self,
        prototype: typings.Prototype = None,
        *,
        attributes: typing.Dict = None,
        unwrap: bool = True,
    ) -> typing.List:
        r"""
        Get indicators.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef("alto"), staff[0])
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, staff[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, staff[3])
            >>> for note in abjad.select(staff).notes():
            ...     abjad.attach(abjad.Staccato(), note)

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    c'4
                    \staccato
                    \grace {
                        cs'16
                        \staccato
                    }
                    d'4
                    \staccato
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            \staccato
                            gs'16 * 1
                            \staccato
                            a'16 * 1
                            \staccato
                            as'16 * 1
                            )
                            \staccato
                        }
                    \\
                        e'4
                        \staccato
                    >>
                    \afterGrace
                    f'4
                    \staccato
                    {
                        fs'16
                        \staccato
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).indicators()
            ...     print(f"{repr(component):30} {repr(result)}")
            Staff("c'4 d'4 e'4 f'4")       []
            Note("c'4")                    [Clef('alto'), Staccato()]
            GraceContainer("cs'16")        []
            Note("cs'16")                  [Staccato()]
            Note("d'4")                    [Staccato()]
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") []
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") [StartSlur(), Articulation('>'), Staccato()]
            Note("gs'16 * 1")              [Staccato()]
            Note("a'16 * 1")               [Staccato()]
            Note("as'16 * 1")              [StopSlur(), Staccato()]
            Note("e'4")                    [Staccato()]
            Note("f'4")                    [Staccato()]
            AfterGraceContainer("fs'16")   []
            Note("fs'16")                  [Staccato()]

        """
        # TODO: extend to any non-none client
        if not isinstance(self.client, Component):
            message = "can only get indicators on component"
            message += f" (not {self.client!r})."
            raise Exception(message)
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        result = self.client._get_indicators(
            prototype=prototype, attributes=attributes, unwrap=unwrap
        )
        return list(result)

    def leaf(self, n: int = 0) -> typing.Optional[Leaf]:
        r"""
        Gets leaf ``n``.

        :param n: constrained to -1, 0, 1 for previous, current, next leaf.

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

            Gets leaf **FROM** client when client is a leaf:

            >>> leaf = staff[0][1]

            >>> abjad.inspect(leaf).leaf(-1)
            Note("c'8")

            >>> abjad.inspect(leaf).leaf(0)
            Note("d'8")

            >>> abjad.inspect(leaf).leaf(1)
            Note("e'8")

        ..  container:: example

            Gets leaf **IN** client when client is a container:

            >>> voice = staff[0]

            >>> abjad.inspect(voice).leaf(-1)
            Note("f'8")

            >>> abjad.inspect(voice).leaf(0)
            Note("c'8")

            >>> abjad.inspect(voice).leaf(1)
            Note("d'8")

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, staff[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for current_leaf in abjad.select(staff).leaves():
            ...     previous_leaf = abjad.inspect(current_leaf).leaf(-1)
            ...     next_leaf = abjad.inspect(current_leaf).leaf(1)
            ...     print(f"previous leaf: {repr(previous_leaf)}")
            ...     print(f"current leaf:  {repr(current_leaf)}")
            ...     print(f"next leaf:     {repr(next_leaf)}")
            ...     print("---")
            previous leaf: None
            current leaf:  Note("c'4")
            next leaf:     Note("cs'16")
            ---
            previous leaf: Note("c'4")
            current leaf:  Note("cs'16")
            next leaf:     Note("d'4")
            ---
            previous leaf: Note("cs'16")
            current leaf:  Note("d'4")
            next leaf:     Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1")
            ---
            previous leaf: Note("d'4")
            current leaf:  Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1")
            next leaf:     Note("gs'16 * 1")
            ---
            previous leaf: Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1")
            current leaf:  Note("gs'16 * 1")
            next leaf:     Note("a'16 * 1")
            ---
            previous leaf: Note("gs'16 * 1")
            current leaf:  Note("a'16 * 1")
            next leaf:     Note("as'16 * 1")
            ---
            previous leaf: Note("a'16 * 1")
            current leaf:  Note("as'16 * 1")
            next leaf:     Note("e'4")
            ---
            previous leaf: Note("as'16 * 1")
            current leaf:  Note("e'4")
            next leaf:     Note("f'4")
            ---
            previous leaf: Note("e'4")
            current leaf:  Note("f'4")
            next leaf:     Note("fs'16")
            ---
            previous leaf: Note("f'4")
            current leaf:  Note("fs'16")
            next leaf:     None
            ---

        """
        if n not in (-1, 0, 1):
            message = "n must be -1, 0 or 1:\n"
            message += f"   {repr(n)}"
            raise Exception(message)
        if isinstance(self.client, Leaf):
            candidate = self.client._get_sibling_with_graces(n)
            if isinstance(candidate, Leaf):
                return candidate
            return self.client._leaf(n)
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
        r"""
        Gets lineage.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, voice[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, voice[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(voice).components():
            ...     lineage = abjad.inspect(component).lineage()
            ...     print(f"{repr(component)}:")
            ...     print(f"    {repr(lineage[:])}")
            Voice("c'4 d'4 e'4 f'4"):
                [Voice("c'4 d'4 e'4 f'4"), Note("c'4"), GraceContainer("cs'16"), Note("cs'16"), Note("d'4"), OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1"), Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1"), Note("gs'16 * 1"), Note("a'16 * 1"), Note("as'16 * 1"), Note("e'4"), Note("f'4"), AfterGraceContainer("fs'16"), Note("fs'16")]
            Note("c'4"):
                [Voice("c'4 d'4 e'4 f'4"), Note("c'4")]
            GraceContainer("cs'16"):
                [Voice("c'4 d'4 e'4 f'4"), GraceContainer("cs'16"), Note("cs'16")]
            Note("cs'16"):
                [Voice("c'4 d'4 e'4 f'4"), GraceContainer("cs'16"), Note("cs'16")]
            Note("d'4"):
                [Voice("c'4 d'4 e'4 f'4"), Note("d'4")]
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1"):
                [OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1"), Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1"), Note("gs'16 * 1"), Note("a'16 * 1"), Note("as'16 * 1")]
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1"):
                [OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1"), Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1")]
            Note("gs'16 * 1"):
                [OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1"), Note("gs'16 * 1")]
            Note("a'16 * 1"):
                [OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1"), Note("a'16 * 1")]
            Note("as'16 * 1"):
                [OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1"), Note("as'16 * 1")]
            Note("e'4"):
                [Voice("c'4 d'4 e'4 f'4"), Note("e'4")]
            Note("f'4"):
                [Voice("c'4 d'4 e'4 f'4"), Note("f'4")]
            AfterGraceContainer("fs'16"):
                [Voice("c'4 d'4 e'4 f'4"), AfterGraceContainer("fs'16"), Note("fs'16")]
            Note("fs'16"):
                [Voice("c'4 d'4 e'4 f'4"), AfterGraceContainer("fs'16"), Note("fs'16")]

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get lineage on component.")
        return Lineage(self.client)

    def logical_tie(self) -> LogicalTie:
        r"""
        Gets logical tie.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, voice[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, voice[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for leaf in abjad.select(voice).leaves():
            ...     lt = abjad.inspect(leaf).logical_tie()
            ...     print(f"{repr(leaf):30} {repr(lt)}")
            Note("c'4")                    LogicalTie([Note("c'4")])
            Note("cs'16")                  LogicalTie([Note("cs'16")])
            Note("d'4")                    LogicalTie([Note("d'4")])
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") LogicalTie([Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1")])
            Note("gs'16 * 1")              LogicalTie([Note("gs'16 * 1")])
            Note("a'16 * 1")               LogicalTie([Note("a'16 * 1")])
            Note("as'16 * 1")              LogicalTie([Note("as'16 * 1")])
            Note("e'4")                    LogicalTie([Note("e'4")])
            Note("f'4")                    LogicalTie([Note("f'4")])
            Note("fs'16")                  LogicalTie([Note("fs'16")])

        """
        if not isinstance(self.client, Leaf):
            raise Exception("can only get logical tie on leaf.")
        return self.client._get_logical_tie()

    def markup(
        self, *, direction: enums.VerticalAlignment = None
    ) -> typing.List[Markup]:
        """
        Gets markup.
        """
        # TODO: extend to any non-none client
        if not isinstance(self.client, Component):
            raise Exception("can only get markup on component.")
        result = self.client._get_markup(direction=direction)
        return list(result)

    def measure_number(self) -> int:
        r"""
        Gets measure number.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, voice[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, voice[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(voice).components():
            ...     measure_number = abjad.inspect(component).measure_number()
            ...     print(f"{repr(component):30} {measure_number}")
            Voice("c'4 d'4 e'4 f'4")       1
            Note("c'4")                    1
            GraceContainer("cs'16")        1
            Note("cs'16")                  1
            Note("d'4")                    1
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") 1
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") 1
            Note("gs'16 * 1")              1
            Note("a'16 * 1")               1
            Note("as'16 * 1")              1
            Note("e'4")                    1
            Note("f'4")                    1
            AfterGraceContainer("fs'16")   1
            Note("fs'16")                  1

        ..  container:: example

            REGRESSION. Measure number of score-initial grace notes is set
            equal to 0:

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container = abjad.GraceContainer("b16")
            >>> abjad.attach(container, voice[0])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    \grace {
                        b16
                    }
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> for component in abjad.select(voice).components():
            ...     measure_number = abjad.inspect(component).measure_number()
            ...     print(f"{repr(component):30} {measure_number}")
            Voice("c'4 d'4 e'4 f'4")       1
            GraceContainer('b16')          0
            Note('b16')                    0
            Note("c'4")                    1
            Note("d'4")                    1
            Note("e'4")                    1
            Note("f'4")                    1

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get measure number on component.")
        self.client._update_measure_numbers()
        assert isinstance(self.client._measure_number, int)
        return self.client._measure_number

    def on_beat_grace_container(self) -> typing.Optional[OnBeatGraceContainer]:
        r"""
        Gets on-beat grace container attached to leaf.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, staff[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     container = inspection.on_beat_grace_container()
            ...     print(f"{repr(component):30} {repr(container)}")
            Staff("c'4 d'4 e'4 f'4")       None
            Note("c'4")                    None
            GraceContainer("cs'16")        None
            Note("cs'16")                  None
            Note("d'4")                    None
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") None
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") None
            Note("gs'16 * 1")              None
            Note("a'16 * 1")               None
            Note("as'16 * 1")              None
            Note("e'4")                    OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1")
            Note("f'4")                    None
            AfterGraceContainer("fs'16")   None
            Note("fs'16")                  None

        """
        return getattr(self.client, "_on_beat_grace_container", None)

    def parentage(self) -> Parentage:
        r"""
        Gets parentage.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, voice[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, voice[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(voice).components():
            ...     parentage = abjad.inspect(component).parentage()
            ...     print(f"{repr(component)}:")
            ...     print(f"    {repr(parentage[:])}")
            Voice("c'4 d'4 e'4 f'4"):
                (Voice("c'4 d'4 e'4 f'4"),)
            Note("c'4"):
                (Note("c'4"), Voice("c'4 d'4 e'4 f'4"))
            GraceContainer("cs'16"):
                (GraceContainer("cs'16"), Voice("c'4 d'4 e'4 f'4"))
            Note("cs'16"):
                (Note("cs'16"), GraceContainer("cs'16"), Voice("c'4 d'4 e'4 f'4"))
            Note("d'4"):
                (Note("d'4"), Voice("c'4 d'4 e'4 f'4"))
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1"):
                (OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1"),)
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1"):
                (Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1"), OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1"))
            Note("gs'16 * 1"):
                (Note("gs'16 * 1"), OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1"))
            Note("a'16 * 1"):
                (Note("a'16 * 1"), OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1"))
            Note("as'16 * 1"):
                (Note("as'16 * 1"), OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1"))
            Note("e'4"):
                (Note("e'4"), Voice("c'4 d'4 e'4 f'4"))
            Note("f'4"):
                (Note("f'4"), Voice("c'4 d'4 e'4 f'4"))
            AfterGraceContainer("fs'16"):
                (AfterGraceContainer("fs'16"), Voice("c'4 d'4 e'4 f'4"))
            Note("fs'16"):
                (Note("fs'16"), AfterGraceContainer("fs'16"), Voice("c'4 d'4 e'4 f'4"))

        """
        if not isinstance(self.client, Component):
            message = "can only get parentage on component"
            message += f" (not {self.client})."
            raise Exception(message)
        return Parentage(self.client)

    def pitches(self) -> typing.Optional[PitchSet]:
        r"""
        Gets pitches.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, voice[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, voice[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(voice).components():
            ...     pitches = abjad.inspect(component).pitches()
            ...     print(f"{repr(component):30} {repr(pitches)}")
            Voice("c'4 d'4 e'4 f'4")       PitchSet(["c'", "cs'", "d'", "e'", "f'", "fs'", "g'", "gs'", "a'", "as'"])
            Note("c'4")                    PitchSet(["c'"])
            GraceContainer("cs'16")        PitchSet(["cs'"])
            Note("cs'16")                  PitchSet(["cs'"])
            Note("d'4")                    PitchSet(["d'"])
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") PitchSet(["g'", "gs'", "a'", "as'"])
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") PitchSet(["g'"])
            Note("gs'16 * 1")              PitchSet(["gs'"])
            Note("a'16 * 1")               PitchSet(["a'"])
            Note("as'16 * 1")              PitchSet(["as'"])
            Note("e'4")                    PitchSet(["e'"])
            Note("f'4")                    PitchSet(["f'"])
            AfterGraceContainer("fs'16")   PitchSet(["fs'"])
            Note("fs'16")                  PitchSet(["fs'"])

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
            for slot in ("before", "open brackets", "opening"):
                lines = self.client._get_format_contributions_for_slot(
                    slot, bundle
                )
                result.extend(lines)
            line = f"    %%% {len(self.client)} components omitted %%%"
            result.append(line)
            for slot in ("closing", "close brackets", "after"):
                lines = self.client._get_format_contributions_for_slot(
                    slot, bundle
                )
                result.extend(lines)
            return "\n".join(result)
        elif isinstance(self.client, Leaf):
            return self.client._report_format_contributions()
        else:
            return f"only defined for components: {self.client}."

    def sounding_pitch(self) -> NamedPitch:
        r"""
        Gets sounding pitch of note.

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

            >>> for note in abjad.select(staff).notes():
            ...     pitch = abjad.inspect(note).sounding_pitch()
            ...     print(f"{repr(note):10} {repr(pitch)}")
            Note("d'8") NamedPitch("d''")
            Note("e'8") NamedPitch("e''")
            Note("f'8") NamedPitch("f''")
            Note("g'8") NamedPitch("g''")

        """
        if not isinstance(self.client, Note):
            raise Exception("can only get sounding pitch of note.")
        return self.client._get_sounding_pitch()

    def sounding_pitches(self) -> PitchSet:
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

            >>> for chord in abjad.select(staff).chords():
            ...     pitches = abjad.inspect(chord).sounding_pitches()
            ...     print(f"{repr(chord):20} {repr(pitches)}")
            Chord("<c' e'>4")    PitchSet(["c'''", "e'''"])
            Chord("<d' fs'>4")   PitchSet(["d'''", "fs'''"])

        """
        # TODO: extend to any non-none client
        if not isinstance(self.client, Chord):
            raise Exception("can only get sounding pitches of chord.")
        result = self.client._get_sounding_pitches()
        return PitchSet(result)

    def tabulate_wellformedness(
        self,
        allow_percussion_clef: bool = None,
        check_beamed_long_notes: bool = True,
        check_duplicate_ids: bool = True,
        check_empty_containers: bool = True,
        check_misdurated_measures: bool = True,
        check_misfilled_measures: bool = True,
        check_mispitched_ties: bool = True,
        check_misrepresented_flags: bool = True,
        check_missing_parents: bool = True,
        check_nested_measures: bool = True,
        check_notes_on_wrong_clef: bool = True,
        check_out_of_range_pitches: bool = True,
        check_overlapping_text_spanners: bool = True,
        check_unmatched_stop_text_spans: bool = True,
        check_unterminated_hairpins: bool = True,
        check_unterminated_text_spanners: bool = True,
    ) -> str:
        r"""
        Tabulates wellformedness.
        """
        manager = Wellformedness(allow_percussion_clef=allow_percussion_clef)
        triples = manager(self.client)
        strings = []
        for violators, total, check_name in triples:
            if eval(check_name) is not True:
                continue
            violator_count = len(violators)
            check_name = check_name.replace("check_", "")
            check_name = check_name.replace("_", " ")
            string = f"{violator_count} /\t{total} {check_name}"
            strings.append(string)
        return "\n".join(strings)

    def timespan(self, in_seconds: bool = False) -> Timespan:
        r"""
        Gets timespan.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container = abjad.GraceContainer("cs'16 ds'")
            >>> abjad.attach(container, voice[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, voice[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \grace {
                        cs'16
                        ds'16
                    }
                    d'4
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            gs'16 * 1
                            a'16 * 1
                            as'16 * 1
                            )
                        }
                    \\
                        e'4
                    >>
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(voice).components():
            ...     timespan = abjad.inspect(component).timespan()
            ...     print(f"{repr(component):30} {repr(timespan)}")
            Voice("c'4 d'4 e'4 f'4")       Timespan(Offset((0, 1)), Offset((1, 1)))
            Note("c'4")                    Timespan(Offset((0, 1)), Offset((1, 4)))
            GraceContainer("cs'16 ds'16")  Timespan(Offset((1, 4), displacement=Duration(-1, 8)), Offset((1, 4)))
            Note("cs'16")                  Timespan(Offset((1, 4), displacement=Duration(-1, 8)), Offset((1, 4), displacement=Duration(-1, 16)))
            Note("ds'16")                  Timespan(Offset((1, 4), displacement=Duration(-1, 16)), Offset((1, 4)))
            Note("d'4")                    Timespan(Offset((1, 4)), Offset((1, 2)))
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") Timespan(Offset((1, 2), displacement=Duration(1, 4)), Offset((1, 2), displacement=Duration(1, 4)))
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") Timespan(Offset((1, 2), displacement=Duration(1, 4)), Offset((1, 2), displacement=Duration(1, 4)))
            Note("gs'16 * 1")              Timespan(Offset((1, 2), displacement=Duration(1, 4)), Offset((1, 2), displacement=Duration(1, 4)))
            Note("a'16 * 1")               Timespan(Offset((1, 2), displacement=Duration(1, 4)), Offset((1, 2), displacement=Duration(1, 4)))
            Note("as'16 * 1")              Timespan(Offset((1, 2), displacement=Duration(1, 4)), Offset((1, 2), displacement=Duration(1, 4)))
            Note("e'4")                    Timespan(Offset((1, 2), displacement=Duration(1, 4)), Offset((3, 4)))
            Note("f'4")                    Timespan(Offset((3, 4)), Offset((1, 1)))
            AfterGraceContainer("fs'16")   Timespan(Offset((1, 1), displacement=Duration(-1, 16)), Offset((1, 1)))
            Note("fs'16")                  Timespan(Offset((1, 1), displacement=Duration(-1, 16)), Offset((1, 1)))

        ..  container:: example

            REGRESION.Gets timespan of selection:

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

            >>> abjad.inspect(staff[:3]).timespan()
            Timespan(Offset((0, 1)), Offset((3, 4)))

        """
        if isinstance(self.client, Component):
            return self.client._get_timespan(in_seconds=in_seconds)
        assert isinstance(self.client, collections.abc.Iterable), repr(
            self.client
        )
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

    def wellformed(
        self,
        allow_percussion_clef: bool = None,
        check_beamed_long_notes: bool = True,
        check_duplicate_ids: bool = True,
        check_empty_containers: bool = True,
        check_misdurated_measures: bool = True,
        check_misfilled_measures: bool = True,
        check_mismatched_enchained_hairpins: bool = True,
        check_mispitched_ties: bool = True,
        check_misrepresented_flags: bool = True,
        check_missing_parents: bool = True,
        check_nested_measures: bool = True,
        check_notes_on_wrong_clef: bool = True,
        check_out_of_range_pitches: bool = True,
        check_overlapping_text_spanners: bool = True,
        check_unmatched_stop_text_spans: bool = True,
        check_unterminated_hairpins: bool = True,
        check_unterminated_text_spanners: bool = True,
    ) -> bool:
        """
        Is true when client is wellformed.
        """
        manager = Wellformedness(allow_percussion_clef=allow_percussion_clef)
        for violators, total, check_name in manager(self.client):
            if eval(check_name) is not True:
                continue
            if violators:
                return False
        return True

    def wrapper(
        self,
        prototype: typings.Prototype = None,
        *,
        attributes: typing.Dict = None,
    ) -> typing.Optional[Wrapper]:
        r"""
        Gets wrapper.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef("alto"), staff[0])
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, staff[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, staff[3])
            >>> for note in abjad.select(staff).notes():
            ...     abjad.attach(abjad.Staccato(), note)

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    c'4
                    \staccato
                    \grace {
                        cs'16
                        \staccato
                    }
                    d'4
                    \staccato
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            \staccato
                            gs'16 * 1
                            \staccato
                            a'16 * 1
                            \staccato
                            as'16 * 1
                            )
                            \staccato
                        }
                    \\
                        e'4
                        \staccato
                    >>
                    \afterGrace
                    f'4
                    \staccato
                    {
                        fs'16
                        \staccato
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     wrapper = abjad.inspect(component).wrapper(abjad.Staccato)
            ...     print(f"{repr(component):30} {repr(wrapper)}")
            Staff("c'4 d'4 e'4 f'4")       None
            Note("c'4")                    Wrapper(indicator=Staccato(), tag=Tag())
            GraceContainer("cs'16")        None
            Note("cs'16")                  Wrapper(indicator=Staccato(), tag=Tag())
            Note("d'4")                    Wrapper(indicator=Staccato(), tag=Tag())
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") None
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") Wrapper(indicator=Staccato(), tag=Tag())
            Note("gs'16 * 1")              Wrapper(indicator=Staccato(), tag=Tag())
            Note("a'16 * 1")               Wrapper(indicator=Staccato(), tag=Tag())
            Note("as'16 * 1")              Wrapper(indicator=Staccato(), tag=Tag())
            Note("e'4")                    Wrapper(indicator=Staccato(), tag=Tag())
            Note("f'4")                    Wrapper(indicator=Staccato(), tag=Tag())
            AfterGraceContainer("fs'16")   None
            Note("fs'16")                  Wrapper(indicator=Staccato(), tag=Tag())

        Raises exception when more than one indicator of ``prototype`` attach
        to client.
        """
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        return self.indicator(prototype=prototype, unwrap=False)

    def wrappers(
        self,
        prototype: typings.Prototype = None,
        *,
        attributes: typing.Dict = None,
    ) -> typing.Optional[typing.List[Wrapper]]:
        r"""
        Gets wrappers.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef("alto"), staff[0])
            >>> container = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.OnBeatGraceContainer("g'16 gs' a' as'")
            >>> abjad.slur(container[:])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> abjad.attach(container, staff[2])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, staff[3])
            >>> for note in abjad.select(staff).notes():
            ...     abjad.attach(abjad.Staccato(), note)

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    c'4
                    \staccato
                    \grace {
                        cs'16
                        \staccato
                    }
                    d'4
                    \staccato
                    <<
                        {
                            \set fontSize = #-2
                            \once \override NoteColumn.force-hshift = 0.2
                            \slash
                            <g' \tweak Accidental.stencil ##f e'>16 * 1
                            - \accent
                            (
                            \staccato
                            gs'16 * 1
                            \staccato
                            a'16 * 1
                            \staccato
                            as'16 * 1
                            )
                            \staccato
                        }
                    \\
                        e'4
                        \staccato
                    >>
                    \afterGrace
                    f'4
                    \staccato
                    {
                        fs'16
                        \staccato
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).wrappers(abjad.Staccato)
            ...     print(f"{repr(component):30} {repr(result)}")
            Staff("c'4 d'4 e'4 f'4")       []
            Note("c'4")                    [Wrapper(indicator=Staccato(), tag=Tag())]
            GraceContainer("cs'16")        []
            Note("cs'16")                  [Wrapper(indicator=Staccato(), tag=Tag())]
            Note("d'4")                    [Wrapper(indicator=Staccato(), tag=Tag())]
            OnBeatGraceContainer("<g' \\tweak Accidental.stencil ##f e'>16 * 1 gs'16 * 1 a'16 * 1 as'16 * 1") []
            Note("<g' \\tweak Accidental.stencil ##f e'>16 * 1") [Wrapper(indicator=Staccato(), tag=Tag())]
            Note("gs'16 * 1")              [Wrapper(indicator=Staccato(), tag=Tag())]
            Note("a'16 * 1")               [Wrapper(indicator=Staccato(), tag=Tag())]
            Note("as'16 * 1")              [Wrapper(indicator=Staccato(), tag=Tag())]
            Note("e'4")                    [Wrapper(indicator=Staccato(), tag=Tag())]
            Note("f'4")                    [Wrapper(indicator=Staccato(), tag=Tag())]
            AfterGraceContainer("fs'16")   []
            Note("fs'16")                  [Wrapper(indicator=Staccato(), tag=Tag())]

        """
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        return self.indicators(prototype=prototype, unwrap=False)
