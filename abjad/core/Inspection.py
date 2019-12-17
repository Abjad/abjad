import collections
import typing

from abjad import enums, typings
from abjad.indicators.TimeSignature import TimeSignature
from abjad.markups import Markup
from abjad.pitch.NamedPitch import NamedPitch
from abjad.pitch.PitchSet import PitchSet
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.system.Tag import Tag
from abjad.system.Wrapper import Wrapper
from abjad.timespans import Timespan
from abjad.top.iterate import iterate
from abjad.utilities.Duration import Duration

from .AfterGraceContainer import AfterGraceContainer
from .BeforeGraceContainer import BeforeGraceContainer
from .Chord import Chord
from .Component import Component
from .Container import Container
from .Descendants import Descendants
from .Leaf import Leaf
from .Lineage import Lineage
from .LogicalTie import LogicalTie
from .Note import Note
from .OnBeatGraceContainer import OnBeatGraceContainer
from .Parentage import Parentage
from .Selection import Selection
from .Staff import Staff
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
        self, client: typing.Union[Component, typing.Iterable[Component]] = None,
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
    def client(self,) -> typing.Union[Component, typing.Iterable[Component], None]:
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

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     container = abjad.inspect(component).after_grace_container()
            ...     print(f"{repr(component):30} {repr(container)}")
            <Staff{1}>                     None
            <Voice-"Music_Voice"{4}>       None
            Note("c'4")                    None
            BeforeGraceContainer("cs'16")        None
            Note("cs'16")                  None
            Note("d'4")                    None
            <<<2>>>                        None
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") None
            Chord("<e' g'>16")             None
            Note("gs'16")                  None
            Note("a'16")                   None
            Note("as'16")                  None
            Voice("e'4", name='Music_Voice') None
            Note("e'4")                    None
            Note("f'4")                    AfterGraceContainer("fs'16")
            AfterGraceContainer("fs'16")   None
            Note("fs'16")                  None

        """
        return getattr(self.client, "_after_grace_container", None)

    def annotation(
        self, annotation: typing.Any, default: typing.Any = None, unwrap: bool = True,
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

    def before_grace_container(self) -> typing.Optional[BeforeGraceContainer]:
        r"""
        Gets before-grace container attached to leaf.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     container = abjad.inspect(component).before_grace_container()
            ...     print(f"{repr(component):30} {repr(container)}")
            <Staff{1}>                     None
            <Voice-"Music_Voice"{4}>       None
            Note("c'4")                    None
            BeforeGraceContainer("cs'16")        None
            Note("cs'16")                  None
            Note("d'4")                    BeforeGraceContainer("cs'16")
            <<<2>>>                        None
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") None
            Chord("<e' g'>16")             None
            Note("gs'16")                  None
            Note("a'16")                   None
            Note("as'16")                  None
            Voice("e'4", name='Music_Voice') None
            Note("e'4")                    None
            Note("f'4")                    None
            AfterGraceContainer("fs'16")   None
            Note("fs'16")                  None

        """
        return getattr(self.client, "_before_grace_container", None)

    def contents(self,) -> typing.Optional[Selection]:
        r"""
        Gets contents.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     contents = abjad.inspect(component).contents()
            ...     print(f"{repr(component)}:")
            ...     for component_ in contents:
            ...         print(f"    {repr(component_)}")
            <Staff{1}>:
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
            <Voice-"Music_Voice"{4}>:
                <Voice-"Music_Voice"{4}>
                Note("c'4")
                Note("d'4")
                <<<2>>>
                Note("f'4")
            Note("c'4"):
                Note("c'4")
            BeforeGraceContainer("cs'16"):
                BeforeGraceContainer("cs'16")
                Note("cs'16")
            Note("cs'16"):
                Note("cs'16")
            Note("d'4"):
                Note("d'4")
            <<<2>>>:
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Voice("e'4", name='Music_Voice')
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
            Chord("<e' g'>16"):
                Chord("<e' g'>16")
            Note("gs'16"):
                Note("gs'16")
            Note("a'16"):
                Note("a'16")
            Note("as'16"):
                Note("as'16")
            Voice("e'4", name='Music_Voice'):
                Voice("e'4", name='Music_Voice')
                Note("e'4")
            Note("e'4"):
                Note("e'4")
            Note("f'4"):
                Note("f'4")
            AfterGraceContainer("fs'16"):
                AfterGraceContainer("fs'16")
                Note("fs'16")
            Note("fs'16"):
                Note("fs'16")

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     contents = abjad.inspect(component).contents()
            ...     print(f"{repr(component)}:")
            ...     for component_ in contents:
            ...         print(f"    {repr(component_)}")
            <Staff{4}>:
                <Staff{4}>
                TremoloContainer("c'16 e'16")
                Note("cs'4")
                TremoloContainer("d'16 f'16")
                Note("ds'4")
            TremoloContainer("c'16 e'16"):
                TremoloContainer("c'16 e'16")
                Note("c'16")
                Note("e'16")
            Note("c'16"):
                Note("c'16")
            Note("e'16"):
                Note("e'16")
            Note("cs'4"):
                Note("cs'4")
            TremoloContainer("d'16 f'16"):
                TremoloContainer("d'16 f'16")
                Note("d'16")
                Note("f'16")
            Note("d'16"):
                Note("d'16")
            Note("f'16"):
                Note("f'16")
            Note("ds'4"):
                Note("ds'4")

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get contents of component.")
        return self.client._get_contents()

    def descendants(self,) -> typing.Union[Descendants, Selection]:
        r"""
        Gets descendants.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     descendants = abjad.inspect(component).descendants()
            ...     print(f"{repr(component)}:")
            ...     for component_ in descendants:
            ...         print(f"    {repr(component_)}")
            <Staff{1}>:
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                Note("c'4")
                BeforeGraceContainer("cs'16")
                Note("cs'16")
                Note("d'4")
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
                Voice("e'4", name='Music_Voice')
                Note("e'4")
                Note("f'4")
                AfterGraceContainer("fs'16")
                Note("fs'16")
            <Voice-"Music_Voice"{4}>:
                <Voice-"Music_Voice"{4}>
                Note("c'4")
                BeforeGraceContainer("cs'16")
                Note("cs'16")
                Note("d'4")
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
                Voice("e'4", name='Music_Voice')
                Note("e'4")
                Note("f'4")
                AfterGraceContainer("fs'16")
                Note("fs'16")
            Note("c'4"):
                Note("c'4")
            BeforeGraceContainer("cs'16"):
                BeforeGraceContainer("cs'16")
                Note("cs'16")
            Note("cs'16"):
                Note("cs'16")
            Note("d'4"):
                Note("d'4")
            <<<2>>>:
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
                Voice("e'4", name='Music_Voice')
                Note("e'4")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
            Chord("<e' g'>16"):
                Chord("<e' g'>16")
            Note("gs'16"):
                Note("gs'16")
            Note("a'16"):
                Note("a'16")
            Note("as'16"):
                Note("as'16")
            Voice("e'4", name='Music_Voice'):
                Voice("e'4", name='Music_Voice')
                Note("e'4")
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

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     duration = abjad.inspect(component).duration()
            ...     print(f"{repr(component):30} {repr(duration)}")
            <Staff{1}>                     Duration(1, 1)
            <Voice-"Music_Voice"{4}>       Duration(1, 1)
            Note("c'4")                    Duration(1, 4)
            BeforeGraceContainer("cs'16")        Duration(1, 16)
            Note("cs'16")                  Duration(1, 16)
            Note("d'4")                    Duration(1, 4)
            <<<2>>>                        Duration(1, 4)
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") Duration(1, 4)
            Chord("<e' g'>16")             Duration(1, 16)
            Note("gs'16")                  Duration(1, 16)
            Note("a'16")                   Duration(1, 16)
            Note("as'16")                  Duration(1, 16)
            Voice("e'4", name='Music_Voice') Duration(1, 4)
            Note("e'4")                    Duration(1, 4)
            Note("f'4")                    Duration(1, 4)
            AfterGraceContainer("fs'16")   Duration(1, 16)
            Note("fs'16")                  Duration(1, 16)

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     duration = abjad.inspect(component).duration()
            ...     print(f"{repr(component):30} {repr(duration)}")
            <Staff{4}>                     Duration(1, 1)
            TremoloContainer("c'16 e'16")  Duration(1, 4)
            Note("c'16")                   Duration(1, 8)
            Note("e'16")                   Duration(1, 8)
            Note("cs'4")                   Duration(1, 4)
            TremoloContainer("d'16 f'16")  Duration(1, 4)
            Note("d'16")                   Duration(1, 8)
            Note("f'16")                   Duration(1, 8)
            Note("ds'4")                   Duration(1, 4)

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
        assert isinstance(self.client, collections.abc.Iterable), repr(self.client)
        durations = [Inspection(_).duration(in_seconds=in_seconds) for _ in self.client]
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

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     clef = abjad.inspect(component).effective(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(clef)}")
            <Staff{1}>                     None
            <Voice-"Music_Voice"{4}>       None
            Note("c'4")                    None
            BeforeGraceContainer("cs'16")        None
            Note("cs'16")                  None
            Note("d'4")                    None
            <<<2>>>                        Clef('alto')
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") Clef('alto')
            Chord("<e' g'>16")             Clef('alto')
            Note("gs'16")                  Clef('alto')
            Note("a'16")                   Clef('alto')
            Note("as'16")                  Clef('alto')
            Voice("e'4", name='Music_Voice') Clef('alto')
            Note("e'4")                    Clef('alto')
            Note("f'4")                    Clef('alto')
            AfterGraceContainer("fs'16")   Clef('alto')
            Note("fs'16")                  Clef('alto')

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> abjad.attach(abjad.Clef("alto"), staff[-1][0])
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        \clef "alto"
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     clef = abjad.inspect(component).effective(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(clef)}")
            <Staff{4}>                     None
            TremoloContainer("c'16 e'16")  None
            Note("c'16")                   None
            Note("e'16")                   None
            Note("cs'4")                   None
            TremoloContainer("d'16 f'16")  Clef('alto')
            Note("d'16")                   Clef('alto')
            Note("f'16")                   Clef('alto')
            Note("ds'4")                   Clef('alto')

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

            Use synthetic offsets to hide a clef before the start of a staff
            like this:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> abjad.attach(
            ...     abjad.Clef("treble", hide=True),
            ...     staff[0],
            ...     synthetic_offset=-1,
            ...     )
            >>> abjad.attach(abjad.Clef("alto"), staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> for leaf in staff:
            ...     clef = abjad.inspect(leaf).effective(abjad.Clef)
            ...     (leaf, clef)
            ...
            (Note("c'4"), Clef('alto'))
            (Note("d'4"), Clef('alto'))
            (Note("e'4"), Clef('alto'))
            (Note("f'4"), Clef('alto'))

            >>> abjad.inspect(staff[0]).effective(abjad.Clef)
            Clef('alto')

            >>> abjad.inspect(staff[0]).effective(abjad.Clef, n=-1)
            Clef('treble', hide=True)

            >>> abjad.inspect(staff[0]).effective(abjad.Clef, n=-2) is None
            True

            Note that ``hide=True`` is set on the offset clef to prevent
            duplicate clef commands in LilyPond output.

            Note also that the order of attachment (offset versus non-offset)
            makes no difference.

        ..  container:: example

            Here's how to hide a clef after the end of a staff:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> abjad.attach(abjad.Clef("treble"), staff[0])
            >>> abjad.attach(
            ...     abjad.Clef("alto", hide=True),
            ...     staff[-1],
            ...     synthetic_offset=1,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "treble"
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> for leaf in staff:
            ...     clef = abjad.inspect(leaf).effective(abjad.Clef)
            ...     (leaf, clef)
            ...
            (Note("c'4"), Clef('treble'))
            (Note("d'4"), Clef('treble'))
            (Note("e'4"), Clef('treble'))
            (Note("f'4"), Clef('treble'))

            >>> abjad.inspect(staff[-1]).effective(abjad.Clef)
            Clef('treble')

            >>> abjad.inspect(staff[-1]).effective(abjad.Clef, n=1)
            Clef('alto', hide=True)

            >>> abjad.inspect(staff[-1]).effective(abjad.Clef, n=2) is None
            True

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
            >>> staff = abjad.Staff([voice])
            >>> start_text_span = abjad.StartTextSpan()
            >>> abjad.attach(start_text_span, voice[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, voice[2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \new Voice
                    {
                        c'4
                        \startTextSpan
                        d'4
                        e'4
                        \stopTextSpan
                        f'4
                    }
                }

            >>> for note in abjad.select(staff).notes():
            ...     note, abjad.inspect(note).effective(abjad.StartTextSpan)
            ...
            (Note("c'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))
            (Note("d'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))
            (Note("e'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))
            (Note("f'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))

            >>> for note in abjad.select(staff).notes():
            ...     note, abjad.inspect(note).effective(abjad.StopTextSpan)
            ...
            (Note("c'4"), None)
            (Note("d'4"), None)
            (Note("e'4"), StopTextSpan(command='\\stopTextSpan'))
            (Note("f'4"), StopTextSpan(command='\\stopTextSpan'))

            >>> attributes = {'parameter': 'TEXT_SPANNER'}
            >>> for note in abjad.select(staff).notes():
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

        ..  container:: example

            REGRESSION. Matching start-beam and stop-beam indicators work
            correctly:

            >>> voice = abjad.Voice("c'8 d'8 e'8 f'8 g'4 a'4")
            >>> abjad.attach(abjad.StartBeam(), voice[0])
            >>> abjad.attach(abjad.StopBeam(), voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'8
                    [
                    d'8
                    e'8
                    f'8
                    ]
                    g'4
                    a'4
                }

            >>> for leaf in abjad.select(voice).leaves():
            ...     start_beam = abjad.inspect(leaf).effective(abjad.StartBeam)
            ...     stop_beam = abjad.inspect(leaf).effective(abjad.StopBeam)
            ...     leaf, start_beam, stop_beam
            (Note("c'8"), StartBeam(), None)
            (Note("d'8"), StartBeam(), None)
            (Note("e'8"), StartBeam(), None)
            (Note("f'8"), StartBeam(), StopBeam())
            (Note("g'4"), StartBeam(), StopBeam())
            (Note("a'4"), StartBeam(), StopBeam())

            # TODO: make this work.

        ..  container:: example

            REGRESSION. Bar lines work like this:

            >>> voice = abjad.Voice("c'2 d'2 e'2 f'2")
            >>> score = abjad.Score([voice])
            >>> abjad.attach(abjad.BarLine("||"), voice[1])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Voice
                    {
                        c'2
                        d'2
                        \bar "||"
                        e'2
                        f'2
                    }
                >>

            >>> for leaf in abjad.select(score).leaves():
            ...     bar_line = abjad.inspect(leaf).effective(abjad.BarLine)
            ...     leaf, bar_line
            (Note("c'2"), None)
            (Note("d'2"), BarLine('||', format_slot='after'))
            (Note("e'2"), BarLine('||', format_slot='after'))
            (Note("f'2"), BarLine('||', format_slot='after'))

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

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     staff = abjad.inspect(component).effective_staff()
            ...     print(f"{repr(component):30} {repr(staff)}")
            <Staff{1}>                     <Staff{1}>
            <Voice-"Music_Voice"{4}>       <Staff{1}>
            Note("c'4")                    <Staff{1}>
            BeforeGraceContainer("cs'16")        <Staff{1}>
            Note("cs'16")                  <Staff{1}>
            Note("d'4")                    <Staff{1}>
            <<<2>>>                        <Staff{1}>
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") <Staff{1}>
            Chord("<e' g'>16")             <Staff{1}>
            Note("gs'16")                  <Staff{1}>
            Note("a'16")                   <Staff{1}>
            Note("as'16")                  <Staff{1}>
            Voice("e'4", name='Music_Voice') <Staff{1}>
            Note("e'4")                    <Staff{1}>
            Note("f'4")                    <Staff{1}>
            AfterGraceContainer("fs'16")   <Staff{1}>
            Note("fs'16")                  <Staff{1}>

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

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     wrapper = inspection.effective_wrapper(abjad.Clef)
            ...     print(f"{repr(component):}")
            ...     print(f"    {repr(wrapper)}")
            <Staff{1}>
                None
            <Voice-"Music_Voice"{4}>
                None
            Note("c'4")
                None
            BeforeGraceContainer("cs'16")
                None
            Note("cs'16")
                None
            Note("d'4")
                None
            <<<2>>>
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Chord("<e' g'>16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Note("gs'16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Note("a'16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Note("as'16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Voice("e'4", name='Music_Voice')
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
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
        return self.effective(prototype, attributes=attributes, n=n, unwrap=False)

    def grace(self) -> bool:
        r"""
        Is true when client is grace music.

        Grace music defined equal to grace container, after-grace container and
        contents of those containers.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).grace()
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{1}>                     False
            <Voice-"Music_Voice"{4}>       False
            Note("c'4")                    False
            BeforeGraceContainer("cs'16")        True
            Note("cs'16")                  True
            Note("d'4")                    False
            <<<2>>>                        False
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") True
            Chord("<e' g'>16")             True
            Note("gs'16")                  True
            Note("a'16")                   True
            Note("as'16")                  True
            Voice("e'4", name='Music_Voice') False
            Note("e'4")                    False
            Note("f'4")                    False
            AfterGraceContainer("fs'16")   True
            Note("fs'16")                  True


        """
        prototype = (
            AfterGraceContainer,
            BeforeGraceContainer,
            OnBeatGraceContainer,
        )
        if isinstance(self.client, prototype):
            return True
        for component in Inspection(self.client).parentage():
            if isinstance(component, prototype):
                return True
        return False

    def has_effective_indicator(
        self, prototype: typings.Prototype = None, *, attributes: typing.Dict = None,
    ) -> bool:
        r"""
        Is true when client has effective indicator.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     result = inspection.has_effective_indicator(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{1}>                     False
            <Voice-"Music_Voice"{4}>       False
            Note("c'4")                    False
            BeforeGraceContainer("cs'16")        False
            Note("cs'16")                  False
            Note("d'4")                    False
            <<<2>>>                        True
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") True
            Chord("<e' g'>16")             True
            Note("gs'16")                  True
            Note("a'16")                   True
            Note("as'16")                  True
            Voice("e'4", name='Music_Voice') True
            Note("e'4")                    True
            Note("f'4")                    True
            AfterGraceContainer("fs'16")   True
            Note("fs'16")                  True

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> abjad.attach(abjad.Clef("alto"), staff[-1][0])
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        \clef "alto"
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     result = inspection.has_effective_indicator(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{4}>                     False
            TremoloContainer("c'16 e'16")  False
            Note("c'16")                   False
            Note("e'16")                   False
            Note("cs'4")                   False
            TremoloContainer("d'16 f'16")  True
            Note("d'16")                   True
            Note("f'16")                   True
            Note("ds'4")                   True

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get effective indicator on component.")
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        return self.client._has_effective_indicator(
            prototype=prototype, attributes=attributes
        )

    def has_indicator(
        self, prototype: typings.Prototype = None, *, attributes: typing.Dict = None,
    ) -> bool:
        r"""
        Is true when client has one or more indicators.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     result = inspection.has_indicator(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{1}>                     False
            <Voice-"Music_Voice"{4}>       False
            Note("c'4")                    False
            BeforeGraceContainer("cs'16")        False
            Note("cs'16")                  False
            Note("d'4")                    False
            <<<2>>>                        False
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") False
            Chord("<e' g'>16")             True
            Note("gs'16")                  False
            Note("a'16")                   False
            Note("as'16")                  False
            Voice("e'4", name='Music_Voice') False
            Note("e'4")                    False
            Note("f'4")                    False
            AfterGraceContainer("fs'16")   False
            Note("fs'16")                  False

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> abjad.attach(abjad.Clef("alto"), staff[-1][0])
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        \clef "alto"
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     result = inspection.has_indicator(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{4}>                     False
            TremoloContainer("c'16 e'16")  False
            Note("c'16")                   False
            Note("e'16")                   False
            Note("cs'4")                   False
            TremoloContainer("d'16 f'16")  False
            Note("d'16")                   True
            Note("f'16")                   False
            Note("ds'4")                   False

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
        if isinstance(prototype, Tag):
            raise Exception("do not attach tags; use tag=None keyword.")
        if not isinstance(self.client, Component):
            raise Exception("can only get indicator on component.")
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        return self.client._has_indicator(prototype=prototype, attributes=attributes)

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

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).indicator(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{1}>                     None
            <Voice-"Music_Voice"{4}>       None
            Note("c'4")                    None
            BeforeGraceContainer("cs'16")        None
            Note("cs'16")                  None
            Note("d'4")                    None
            <<<2>>>                        None
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") None
            Chord("<e' g'>16")             Clef('alto')
            Note("gs'16")                  None
            Note("a'16")                   None
            Note("as'16")                  None
            Voice("e'4", name='Music_Voice') None
            Note("e'4")                    None
            Note("f'4")                    None
            AfterGraceContainer("fs'16")   None
            Note("fs'16")                  None

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> abjad.attach(abjad.Clef("alto"), staff[-1][0])
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        \clef "alto"
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).indicator(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{4}>                     None
            TremoloContainer("c'16 e'16")  None
            Note("c'16")                   None
            Note("e'16")                   None
            Note("cs'4")                   None
            TremoloContainer("d'16 f'16")  None
            Note("d'16")                   Clef('alto')
            Note("f'16")                   None
            Note("ds'4")                   None

        Raises exception when more than one indicator of ``prototype`` attach
        to client.

        Returns default when no indicator of ``prototype`` attaches to client.
        """
        if not isinstance(self.client, Component):
            raise Exception("can only get indicator on component.")
        indicators = self.client._get_indicators(prototype=prototype, unwrap=unwrap)
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

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> for note in abjad.select(staff).notes():
            ...     abjad.attach(abjad.Staccato(), note)

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \staccato
                        \grace {
                            cs'16
                            \staccato
                        }
                        d'4
                        \staccato
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                \staccato
                                a'16
                                \staccato
                                as'16
                                )
                                ]
                                \staccato
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                                \staccato
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        \staccato
                        {
                            fs'16
                            \staccato
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).indicators()
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{1}>                     []
            <Voice-"Music_Voice"{4}>       []
            Note("c'4")                    [Staccato()]
            BeforeGraceContainer("cs'16")  []
            Note("cs'16")                  [Staccato()]
            Note("d'4")                    [Staccato()]
            <<<2>>>                        []
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") [LilyPondLiteral('\\set fontSize = #-3', format_slot='opening')]
            Chord("<e' g'>16")             [StartBeam(), LilyPondLiteral('\\slash', format_slot='opening'), StartSlur(), LilyPondLiteral('\\voiceOne', format_slot='opening'), Clef('alto'), Articulation('>')]
            Note("gs'16")                  [Staccato()]
            Note("a'16")                   [Staccato()]
            Note("as'16")                  [StopBeam(), StopSlur(), Staccato()]
            Voice("e'4", name='Music_Voice') []
            Note("e'4")                    [LilyPondLiteral('\\voiceTwo', format_slot='opening'), Staccato()]
            Note("f'4")                    [LilyPondLiteral('\\oneVoice', format_slot='absolute_before'), Staccato()]
            AfterGraceContainer("fs'16")   []
            Note("fs'16")                  [Staccato()]

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> abjad.attach(abjad.Clef("alto"), staff[-1][0])
            >>> staff.append("ds'4")
            >>> for note in abjad.select(staff).notes():
            ...     abjad.attach(abjad.Staccato(), note)

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        \staccato
                        e'16
                        \staccato
                    }
                    cs'4
                    \staccato
                    \repeat tremolo 2 {
                        \clef "alto"
                        d'16
                        \staccato
                        f'16
                        \staccato
                    }
                    ds'4
                    \staccato
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).indicators()
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{4}>                     []
            TremoloContainer("c'16 e'16")  []
            Note("c'16")                   [Staccato()]
            Note("e'16")                   [Staccato()]
            Note("cs'4")                   [Staccato()]
            TremoloContainer("d'16 f'16")  []
            Note("d'16")                   [Clef('alto'), Staccato()]
            Note("f'16")                   [Staccato()]
            Note("ds'4")                   [Staccato()]

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

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
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
            next leaf:     Chord("<e' g'>16")
            ---
            previous leaf: Note("d'4")
            current leaf:  Chord("<e' g'>16")
            next leaf:     Note("gs'16")
            ---
            previous leaf: Chord("<e' g'>16")
            current leaf:  Note("gs'16")
            next leaf:     Note("a'16")
            ---
            previous leaf: Note("gs'16")
            current leaf:  Note("a'16")
            next leaf:     Note("as'16")
            ---
            previous leaf: Note("a'16")
            current leaf:  Note("as'16")
            next leaf:     Note("e'4")
            ---
            previous leaf: Note("as'16")
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

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for current_leaf in abjad.select(staff).leaves():
            ...     previous_leaf = abjad.inspect(current_leaf).leaf(-1)
            ...     next_leaf = abjad.inspect(current_leaf).leaf(1)
            ...     print(f"previous leaf: {repr(previous_leaf)}")
            ...     print(f"current leaf:  {repr(current_leaf)}")
            ...     print(f"next leaf:     {repr(next_leaf)}")
            ...     print("---")
            previous leaf: None
            current leaf:  Note("c'16")
            next leaf:     Note("e'16")
            ---
            previous leaf: Note("c'16")
            current leaf:  Note("e'16")
            next leaf:     Note("cs'4")
            ---
            previous leaf: Note("e'16")
            current leaf:  Note("cs'4")
            next leaf:     Note("d'16")
            ---
            previous leaf: Note("cs'4")
            current leaf:  Note("d'16")
            next leaf:     Note("f'16")
            ---
            previous leaf: Note("d'16")
            current leaf:  Note("f'16")
            next leaf:     Note("ds'4")
            ---
            previous leaf: Note("f'16")
            current leaf:  Note("ds'4")
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

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     lineage = abjad.inspect(component).lineage()
            ...     print(f"{repr(component)}:")
            ...     for component_ in lineage:
            ...         print(f"    {repr(component_)}")
            <Staff{1}>:
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                Note("c'4")
                BeforeGraceContainer("cs'16")
                Note("cs'16")
                Note("d'4")
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
                Voice("e'4", name='Music_Voice')
                Note("e'4")
                Note("f'4")
                AfterGraceContainer("fs'16")
                Note("fs'16")
            <Voice-"Music_Voice"{4}>:
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                Note("c'4")
                BeforeGraceContainer("cs'16")
                Note("cs'16")
                Note("d'4")
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
                Voice("e'4", name='Music_Voice')
                Note("e'4")
                Note("f'4")
                AfterGraceContainer("fs'16")
                Note("fs'16")
            Note("c'4"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                Note("c'4")
            BeforeGraceContainer("cs'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                BeforeGraceContainer("cs'16")
                Note("cs'16")
            Note("cs'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                BeforeGraceContainer("cs'16")
                Note("cs'16")
            Note("d'4"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                Note("d'4")
            <<<2>>>:
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
                Voice("e'4", name='Music_Voice')
                Note("e'4")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
            Chord("<e' g'>16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
            Note("gs'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Note("gs'16")
            Note("a'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Note("a'16")
            Note("as'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Note("as'16")
            Voice("e'4", name='Music_Voice'):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                Voice("e'4", name='Music_Voice')
                Note("e'4")
            Note("e'4"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                Voice("e'4", name='Music_Voice')
                Note("e'4")
            Note("f'4"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                Note("f'4")
            AfterGraceContainer("fs'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                AfterGraceContainer("fs'16")
                Note("fs'16")
            Note("fs'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                AfterGraceContainer("fs'16")
                Note("fs'16")

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get lineage on component.")
        return Lineage(self.client)

    def logical_tie(self) -> LogicalTie:
        r"""
        Gets logical tie.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for leaf in abjad.select(staff).leaves():
            ...     lt = abjad.inspect(leaf).logical_tie()
            ...     print(f"{repr(leaf):30} {repr(lt)}")
            Note("c'4")                    LogicalTie([Note("c'4")])
            Note("cs'16")                  LogicalTie([Note("cs'16")])
            Note("d'4")                    LogicalTie([Note("d'4")])
            Chord("<e' g'>16")             LogicalTie([Chord("<e' g'>16")])
            Note("gs'16")                  LogicalTie([Note("gs'16")])
            Note("a'16")                   LogicalTie([Note("a'16")])
            Note("as'16")                  LogicalTie([Note("as'16")])
            Note("e'4")                    LogicalTie([Note("e'4")])
            Note("f'4")                    LogicalTie([Note("f'4")])
            Note("fs'16")                  LogicalTie([Note("fs'16")])

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for leaf in abjad.select(staff).leaves():
            ...     lt = abjad.inspect(leaf).logical_tie()
            ...     print(f"{repr(leaf):30} {repr(lt)}")
            Note("c'16")                   LogicalTie([Note("c'16")])
            Note("e'16")                   LogicalTie([Note("e'16")])
            Note("cs'4")                   LogicalTie([Note("cs'4")])
            Note("d'16")                   LogicalTie([Note("d'16")])
            Note("f'16")                   LogicalTie([Note("f'16")])
            Note("ds'4")                   LogicalTie([Note("ds'4")])

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

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     measure_number = abjad.inspect(component).measure_number()
            ...     print(f"{repr(component):30} {measure_number}")
            <Staff{1}>                     1
            <Voice-"Music_Voice"{4}>       1
            Note("c'4")                    1
            BeforeGraceContainer("cs'16")        1
            Note("cs'16")                  1
            Note("d'4")                    1
            <<<2>>>                        1
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") 1
            Chord("<e' g'>16")             1
            Note("gs'16")                  1
            Note("a'16")                   1
            Note("as'16")                  1
            Voice("e'4", name='Music_Voice') 1
            Note("e'4")                    1
            Note("f'4")                    1
            AfterGraceContainer("fs'16")   1
            Note("fs'16")                  1

        ..  container:: example

            REGRESSION. Measure number of score-initial grace notes is set
            equal to 0:

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container = abjad.BeforeGraceContainer("b16")
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
            BeforeGraceContainer('b16')          0
            Note('b16')                    0
            Note("c'4")                    1
            Note("d'4")                    1
            Note("e'4")                    1
            Note("f'4")                    1

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     measure_number = abjad.inspect(component).measure_number()
            ...     print(f"{repr(component):30} {measure_number}")
            <Staff{4}>                     1
            TremoloContainer("c'16 e'16")  1
            Note("c'16")                   1
            Note("e'16")                   1
            Note("cs'4")                   1
            TremoloContainer("d'16 f'16")  1
            Note("d'16")                   1
            Note("f'16")                   1
            Note("ds'4")                   1

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get measure number on component.")
        self.client._update_measure_numbers()
        assert isinstance(self.client._measure_number, int)
        return self.client._measure_number

    def parentage(self) -> Parentage:
        r"""
        Gets parentage.

        ..  container:: example

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.inspect(component).parentage()
            ...     print(f"{repr(component)}:")
            ...     for component_ in parentage[:]:
            ...         print(f"    {repr(component_)}")
            <Staff{1}>:
                <Staff{1}>
            <Voice-"Music_Voice"{4}>:
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("c'4"):
                Note("c'4")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            BeforeGraceContainer("cs'16"):
                BeforeGraceContainer("cs'16")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("cs'16"):
                Note("cs'16")
                BeforeGraceContainer("cs'16")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("d'4"):
                Note("d'4")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            <<<2>>>:
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Chord("<e' g'>16"):
                Chord("<e' g'>16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("gs'16"):
                Note("gs'16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("a'16"):
                Note("a'16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("as'16"):
                Note("as'16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Voice("e'4", name='Music_Voice'):
                Voice("e'4", name='Music_Voice')
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("e'4"):
                Note("e'4")
                Voice("e'4", name='Music_Voice')
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("f'4"):
                Note("f'4")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            AfterGraceContainer("fs'16"):
                AfterGraceContainer("fs'16")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("fs'16"):
                Note("fs'16")
                AfterGraceContainer("fs'16")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.inspect(component).parentage()
            ...     print(f"{repr(component)}:")
            ...     print(f"    {repr(parentage[:])}")
            <Staff{4}>:
                (<Staff{4}>,)
            TremoloContainer("c'16 e'16"):
                (TremoloContainer("c'16 e'16"), <Staff{4}>)
            Note("c'16"):
                (Note("c'16"), TremoloContainer("c'16 e'16"), <Staff{4}>)
            Note("e'16"):
                (Note("e'16"), TremoloContainer("c'16 e'16"), <Staff{4}>)
            Note("cs'4"):
                (Note("cs'4"), <Staff{4}>)
            TremoloContainer("d'16 f'16"):
                (TremoloContainer("d'16 f'16"), <Staff{4}>)
            Note("d'16"):
                (Note("d'16"), TremoloContainer("d'16 f'16"), <Staff{4}>)
            Note("f'16"):
                (Note("f'16"), TremoloContainer("d'16 f'16"), <Staff{4}>)
            Note("ds'4"):
                (Note("ds'4"), <Staff{4}>)

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

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     pitches = abjad.inspect(component).pitches()
            ...     print(f"{repr(component):30} {repr(pitches)}")
            <Staff{1}>                     PitchSet(["c'", "cs'", "d'", "e'", "f'", "fs'", "g'", "gs'", "a'", "as'"])
            <Voice-"Music_Voice"{4}>       PitchSet(["c'", "cs'", "d'", "e'", "f'", "fs'", "g'", "gs'", "a'", "as'"])
            Note("c'4")                    PitchSet(["c'"])
            BeforeGraceContainer("cs'16")        PitchSet(["cs'"])
            Note("cs'16")                  PitchSet(["cs'"])
            Note("d'4")                    PitchSet(["d'"])
            <<<2>>>                        PitchSet(["e'", "g'", "gs'", "a'", "as'"])
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") PitchSet(["e'", "g'", "gs'", "a'", "as'"])
            Chord("<e' g'>16")             PitchSet(["e'", "g'"])
            Note("gs'16")                  PitchSet(["gs'"])
            Note("a'16")                   PitchSet(["a'"])
            Note("as'16")                  PitchSet(["as'"])
            Voice("e'4", name='Music_Voice') PitchSet(["e'"])
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
            slot "absolute before":
            slot "before":
                grob overrides:
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
            slot "opening":
                commands:
                    \clef "alto"
            slot "contents slot":
                leaf body:
                    c'8
            slot "closing":
            slot "after":
            slot "absolute after":

        """
        if isinstance(self.client, Container):
            bundle = LilyPondFormatManager.bundle_format_contributions(self.client)
            result: typing.List[str] = []
            for slot in ("before", "open brackets", "opening"):
                lines = self.client._get_format_contributions_for_slot(slot, bundle)
                result.extend(lines)
            line = f"    %%% {len(self.client)} components omitted %%%"
            result.append(line)
            for slot in ("closing", "close brackets", "after"):
                lines = self.client._get_format_contributions_for_slot(slot, bundle)
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
        check_beamed_long_notes: bool = True,
        check_duplicate_ids: bool = True,
        check_empty_containers: bool = True,
        check_missing_parents: bool = True,
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
        manager = Wellformedness()
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

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     timespan = abjad.inspect(component).timespan()
            ...     print(f"{repr(component):30} {repr(timespan)}")
            <Staff{1}>                     Timespan(Offset((0, 1)), Offset((1, 1)))
            <Voice-"Music_Voice"{4}>       Timespan(Offset((0, 1)), Offset((1, 1)))
            Note("c'4")                    Timespan(Offset((0, 1)), Offset((1, 4)))
            BeforeGraceContainer("cs'16")        Timespan(Offset((1, 4), displacement=Duration(-1, 16)), Offset((1, 4)))
            Note("cs'16")                  Timespan(Offset((1, 4), displacement=Duration(-1, 16)), Offset((1, 4)))
            Note("d'4")                    Timespan(Offset((1, 4)), Offset((1, 2)))
            <<<2>>>                        Timespan(Offset((1, 2)), Offset((3, 4)))
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") Timespan(Offset((1, 2)), Offset((1, 2), displacement=Duration(1, 4)))
            Chord("<e' g'>16")             Timespan(Offset((1, 2)), Offset((1, 2), displacement=Duration(1, 16)))
            Note("gs'16")                  Timespan(Offset((1, 2), displacement=Duration(1, 16)), Offset((1, 2), displacement=Duration(1, 8)))
            Note("a'16")                   Timespan(Offset((1, 2), displacement=Duration(1, 8)), Offset((1, 2), displacement=Duration(3, 16)))
            Note("as'16")                  Timespan(Offset((1, 2), displacement=Duration(3, 16)), Offset((1, 2), displacement=Duration(1, 4)))
            Voice("e'4", name='Music_Voice') Timespan(Offset((1, 2)), Offset((3, 4)))
            Note("e'4")                    Timespan(Offset((1, 2), displacement=Duration(1, 4)), Offset((3, 4)))
            Note("f'4")                    Timespan(Offset((3, 4)), Offset((1, 1)))
            AfterGraceContainer("fs'16")   Timespan(Offset((1, 1), displacement=Duration(-1, 16)), Offset((1, 1)))
            Note("fs'16")                  Timespan(Offset((1, 1), displacement=Duration(-1, 16)), Offset((1, 1)))

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     timespan = abjad.inspect(component).timespan()
            ...     print(f"{repr(component):30} {repr(timespan)}")
            <Staff{4}>                     Timespan(Offset((0, 1)), Offset((1, 1)))
            TremoloContainer("c'16 e'16")  Timespan(Offset((0, 1)), Offset((1, 4)))
            Note("c'16")                   Timespan(Offset((0, 1)), Offset((1, 8)))
            Note("e'16")                   Timespan(Offset((1, 8)), Offset((1, 4)))
            Note("cs'4")                   Timespan(Offset((1, 4)), Offset((1, 2)))
            TremoloContainer("d'16 f'16")  Timespan(Offset((1, 2)), Offset((3, 4)))
            Note("d'16")                   Timespan(Offset((1, 2)), Offset((5, 8)))
            Note("f'16")                   Timespan(Offset((5, 8)), Offset((3, 4)))
            Note("ds'4")                   Timespan(Offset((3, 4)), Offset((1, 1)))

        ..  container:: example

            REGRESION. Works with selection:

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
        assert isinstance(self.client, collections.abc.Iterable), repr(self.client)
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
        check_beamed_long_notes: bool = True,
        check_duplicate_ids: bool = True,
        check_empty_containers: bool = True,
        check_missing_parents: bool = True,
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
        manager = Wellformedness()
        for violators, total, check_name in manager(self.client):
            if eval(check_name) is not True:
                continue
            if violators:
                return False
        return True

    def wrapper(
        self, prototype: typings.Prototype = None, *, attributes: typing.Dict = None,
    ) -> typing.Optional[Wrapper]:
        r"""
        Gets wrapper.

        ..  container:: example

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> for note in abjad.select(staff).notes():
            ...     abjad.attach(abjad.Staccato(), note)

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \staccato
                        \grace {
                            cs'16
                            \staccato
                        }
                        d'4
                        \staccato
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                \staccato
                                a'16
                                \staccato
                                as'16
                                )
                                ]
                                \staccato
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                                \staccato
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        \staccato
                        {
                            fs'16
                            \staccato
                        }
                    }
                }

            REGRESSION. Works with grace notes (and containers):

            >>> for component in abjad.select(staff).components():
            ...     wrapper = abjad.inspect(component).wrapper(abjad.Staccato)
            ...     print(f"{repr(component):30} {repr(wrapper)}")
            <Staff{1}>                     None
            <Voice-"Music_Voice"{4}>       None
            Note("c'4")                    Wrapper(indicator=Staccato(), tag=Tag())
            BeforeGraceContainer("cs'16")        None
            Note("cs'16")                  Wrapper(indicator=Staccato(), tag=Tag())
            Note("d'4")                    Wrapper(indicator=Staccato(), tag=Tag())
            <<<2>>>                        None
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") None
            Chord("<e' g'>16")             None
            Note("gs'16")                  Wrapper(indicator=Staccato(), tag=Tag())
            Note("a'16")                   Wrapper(indicator=Staccato(), tag=Tag())
            Note("as'16")                  Wrapper(indicator=Staccato(), tag=Tag())
            Voice("e'4", name='Music_Voice') None
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
        self, prototype: typings.Prototype = None, *, attributes: typing.Dict = None,
    ) -> typing.Optional[typing.List[Wrapper]]:
        r"""
        Gets wrappers.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> for note in abjad.select(staff).notes():
            ...     abjad.attach(abjad.Staccato(), note)

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \staccato
                        \grace {
                            cs'16
                            \staccato
                        }
                        d'4
                        \staccato
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                \staccato
                                a'16
                                \staccato
                                as'16
                                )
                                ]
                                \staccato
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                                \staccato
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        \staccato
                        {
                            fs'16
                            \staccato
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).wrappers(abjad.Staccato)
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{1}>                     []
            <Voice-"Music_Voice"{4}>       []
            Note("c'4")                    [Wrapper(indicator=Staccato(), tag=Tag())]
            BeforeGraceContainer("cs'16")        []
            Note("cs'16")                  [Wrapper(indicator=Staccato(), tag=Tag())]
            Note("d'4")                    [Wrapper(indicator=Staccato(), tag=Tag())]
            <<<2>>>                        []
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") []
            Chord("<e' g'>16")             []
            Note("gs'16")                  [Wrapper(indicator=Staccato(), tag=Tag())]
            Note("a'16")                   [Wrapper(indicator=Staccato(), tag=Tag())]
            Note("as'16")                  [Wrapper(indicator=Staccato(), tag=Tag())]
            Voice("e'4", name='Music_Voice') []
            Note("e'4")                    [Wrapper(indicator=Staccato(), tag=Tag())]
            Note("f'4")                    [Wrapper(indicator=Staccato(), tag=Tag())]
            AfterGraceContainer("fs'16")   []
            Note("fs'16")                  [Wrapper(indicator=Staccato(), tag=Tag())]

        """
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        return self.indicators(prototype=prototype, unwrap=False)
