import collections
import typing
from abjad import mathtools
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.utilities.Multiplier import Multiplier
from abjad.utilities.OrderedDict import OrderedDict
from .AfterGraceContainer import AfterGraceContainer
from .Component import Component
from .Context import Context
from .GraceContainer import GraceContainer
from .Score import Score
from .Staff import Staff
from .StaffGroup import StaffGroup
from .Voice import Voice


class Parentage(collections.abc.Sequence):
    r'''
    Parentage of a component.

    ..  container:: example

        >>> score = abjad.Score()
        >>> string = r"""\new Voice = "Treble_Voice" { e'4 }"""
        >>> treble_staff = abjad.Staff(string, name="Treble_Staff")
        >>> score.append(treble_staff)
        >>> string = r"""\new Voice = "Bass_Voice" { c4 }"""
        >>> bass_staff = abjad.Staff(string, name="Bass_Staff")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, bass_staff[0][0])
        >>> score.append(bass_staff)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        e'4
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        c4
                    }
                }
            >>

        >>> bass_voice = score["Bass_Voice"]
        >>> note = bass_voice[0]
        >>> for component in abjad.inspect(note).parentage():
        ...     component
        ...
        Note('c4')
        Voice('c4', name='Bass_Voice')
        <Staff-"Bass_Staff"{1}>
        <Score<<2>>>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = "Selections"

    __slots__ = ("_component", "_components")

    ### INITIALIZER ###

    def __init__(self, component=None):
        assert isinstance(component, (Component, type(None)))
        self._component = component
        if component is None:
            components = ()
        else:
            components = []
            parent = component
            prototype = (AfterGraceContainer, GraceContainer)
            while parent is not None:
                components.append(parent)
                if isinstance(parent, prototype):
                    if parent._main_leaf is not None:
                        parent = parent._main_leaf._parent
                    else:
                        parent = None
                else:
                    parent = parent._parent
            components = tuple(components)
        self._components = components

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        """
        Gets ``argument``.

        Returns component or tuple of components.
        """
        return self.components.__getitem__(argument)

    def __len__(self) -> int:
        """
        Gets number of components in parentage.
        """
        return len(self.components)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
    def _id_string(component):
        lhs = component.__class__.__name__
        rhs = getattr(component, "name", None) or id(component)
        return f"{lhs}-{rhs!r}"

    def _prolations(self):
        prolations = []
        default = Multiplier(1)
        for parent in self:
            prolation = getattr(parent, "implied_prolation", default)
            prolations.append(prolation)
        return prolations

    ### PUBLIC PROPERTIES ###

    @property
    def component(self) -> Component:
        r"""
        Gets component.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container_1 = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container_1, voice[1])
            >>> container_2 = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container_2, voice[3])
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
                    e'4
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> abjad.inspect(voice).parentage().component
            Voice("c'4 d'4 e'4 f'4")

            >>> abjad.inspect(container_1).parentage().component
            GraceContainer("cs'16")

            >>> abjad.inspect(container_1[0]).parentage().component
            Note("cs'16")

            >>> abjad.inspect(container_2).parentage().component
            AfterGraceContainer("fs'16")

            >>> abjad.inspect(container_2[0]).parentage().component
            Note("fs'16")

        """
        return self._component

    @property
    def components(self) -> typing.Tuple[Component]:
        r"""
        Gets components.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container_1 = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container_1, voice[1])
            >>> container_2 = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container_2, voice[3])
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
                    e'4
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> abjad.inspect(voice).parentage().components
            (Voice("c'4 d'4 e'4 f'4"),)

            >>> abjad.inspect(container_1).parentage().components
            (GraceContainer("cs'16"), Voice("c'4 d'4 e'4 f'4"))

            >>> abjad.inspect(container_1[0]).parentage().components
            (Note("cs'16"), GraceContainer("cs'16"), Voice("c'4 d'4 e'4 f'4"))

            >>> abjad.inspect(container_2).parentage().components
            (AfterGraceContainer("fs'16"), Voice("c'4 d'4 e'4 f'4"))

            >>> abjad.inspect(container_2[0]).parentage().components
            (Note("fs'16"), AfterGraceContainer("fs'16"), Voice("c'4 d'4 e'4 f'4"))

        """
        return self._components

    @property
    def orphan(self) -> bool:
        r"""
        Is true when component has no parent.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container_1 = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container_1, voice[1])
            >>> container_2 = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container_2, voice[3])
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
                    e'4
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> abjad.inspect(voice).parentage().orphan
            True

            >>> abjad.inspect(container_1).parentage().orphan
            False

            >>> abjad.inspect(container_1[0]).parentage().orphan
            False

            >>> abjad.inspect(container_2).parentage().orphan
            False

            >>> abjad.inspect(container_2[0]).parentage().orphan
            False

        """
        return self.parent is None

    @property
    def parent(self) -> typing.Optional[Component]:
        r"""
        Gets parent.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container_1 = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container_1, voice[1])
            >>> container_2 = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container_2, voice[3])
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
                    e'4
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> abjad.inspect(voice).parentage().parent is None
            True

            >>> abjad.inspect(container_1).parentage().parent
            Voice("c'4 d'4 e'4 f'4")

            >>> abjad.inspect(container_1[0]).parentage().parent
            GraceContainer("cs'16")

            >>> abjad.inspect(container_2).parentage().parent
            Voice("c'4 d'4 e'4 f'4")

            >>> abjad.inspect(container_2[0]).parentage().parent
            AfterGraceContainer("fs'16")

        """
        return self.get(n=1)

    @property
    def prolation(self) -> Multiplier:
        r"""
        Gets prolation.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice(
            ...     r"\times 2/3 { c'4 d' e' } \times 2/3 { f' g' a' }"
            ... )
            >>> container_1 = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container_1, voice[0][1])
            >>> container_2 = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container_2, voice[1][2])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    \times 2/3 {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        f'4
                        g'4
                        \afterGrace
                        a'4
                        {
                            fs'16
                        }
                    }
                }

            >>> abjad.inspect(voice).parentage().prolation
            Multiplier(1, 1)

            >>> abjad.inspect(container_1).parentage().prolation
            Multiplier(2, 3)

            >>> abjad.inspect(container_1[0]).parentage().prolation
            Multiplier(2, 3)

            >>> abjad.inspect(container_2).parentage().prolation
            Multiplier(2, 3)

            >>> abjad.inspect(container_2[0]).parentage().prolation
            Multiplier(2, 3)

        """
        prolations = [Multiplier(1)] + self._prolations()
        products = mathtools.cumulative_products(prolations)
        return products[-1]

    @property
    def root(self) -> Component:
        r"""
        Gets root.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container_1 = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container_1, voice[1])
            >>> container_2 = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container_2, voice[3])
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
                    e'4
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }


            >>> abjad.inspect(voice).parentage().root
            Voice("c'4 d'4 e'4 f'4")

            >>> abjad.inspect(container_1).parentage().root
            Voice("c'4 d'4 e'4 f'4")

            >>> abjad.inspect(container_1[0]).parentage().root
            Voice("c'4 d'4 e'4 f'4")

            >>> abjad.inspect(container_2).parentage().root
            Voice("c'4 d'4 e'4 f'4")

            >>> abjad.inspect(container_2[0]).parentage().root
            Voice("c'4 d'4 e'4 f'4")

        """
        root = self.get(n=-1)
        assert isinstance(root, Component), repr(root)
        return root

    ### PUBLIC METHODS ###

    def count(self, prototype=None) -> int:
        r"""
        Gets number of ``prototype`` in parentage.

        ..  container:: example

            Gets tuplet count:

            >>> staff = abjad.Staff(
            ...     r"\times 2/3 { c'2 \times 2/3 { d'8 e' f' } } \times 2/3 { c'4 d' e' }"
            ... )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 2/3 {
                        c'2
                        \times 2/3 {
                            d'8
                            e'8
                            f'8
                        }
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.inspect(component).parentage()
            ...     count = parentage.count(abjad.Tuplet)
            ...     print(f"{repr(component):55} {repr(count)}")
            <Staff{2}>                                              0
            Tuplet(Multiplier(2, 3), "c'2 { 2/3 d'8 e'8 f'8 }")     1
            Note("c'2")                                             1
            Tuplet(Multiplier(2, 3), "d'8 e'8 f'8")                 2
            Note("d'8")                                             2
            Note("e'8")                                             2
            Note("f'8")                                             2
            Tuplet(Multiplier(2, 3), "c'4 d'4 e'4")                 1
            Note("c'4")                                             1
            Note("d'4")                                             1
            Note("e'4")                                             1

        ..  container:: example

            Gets voice count:

            >>> outer_red_voice = abjad.Voice("e''8 d''", name="Red_Voice")
            >>> inner_red_voice = abjad.Voice("c''4 b' c''8", name="Red_Voice")
            >>> inner_blue_voice = abjad.Voice("e'4 f' e'8", name="Blue_Voice")
            >>> container = abjad.Container(
            ...     [inner_red_voice, inner_blue_voice],
            ...     simultaneous=True,
            ... )
            >>> outer_red_voice.append(container)
            >>> outer_red_voice.extend("d''8")
            >>> abjad.override(outer_red_voice).note_head.color = "red"
            >>> literal = abjad.LilyPondLiteral(r"\voiceOne")
            >>> abjad.attach(literal, outer_red_voice[0])
            >>> abjad.override(inner_blue_voice).note_head.color = "blue"
            >>> literal = abjad.LilyPondLiteral(r"\voiceTwo")
            >>> abjad.attach(literal, inner_blue_voice[0])
            >>> dynamic = abjad.Dynamic("f")
            >>> abjad.attach(dynamic, outer_red_voice[0])
            >>> abjad.show(outer_red_voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(outer_red_voice)
                \context Voice = "Red_Voice"
                \with
                {
                    \override NoteHead.color = #red
                }
                {
                    \voiceOne
                    e''8
                    \f
                    d''8
                    <<
                        \context Voice = "Red_Voice"
                        {
                            c''4
                            b'4
                            c''8
                        }
                        \context Voice = "Blue_Voice"
                        \with
                        {
                            \override NoteHead.color = #blue
                        }
                        {
                            \voiceTwo
                            e'4
                            f'4
                            e'8
                        }
                    >>
                    d''8
                }

            >>> for leaf in abjad.iterate(outer_red_voice).leaves():
            ...     depth = abjad.inspect(leaf).parentage().count(abjad.Voice)
            ...     print(leaf, depth)
            ...
            e''8 1
            d''8 1
            c''4 2
            b'4 2
            c''8 2
            e'4 2
            f'4 2
            e'8 2
            d''8 1

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container_1 = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container_1, voice[1])
            >>> container_2 = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container_2, voice[3])
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
                    e'4
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> abjad.inspect(voice).parentage().count(abjad.Voice)
            1

            >>> abjad.inspect(container_1).parentage().count(abjad.Voice)
            1

            >>> abjad.inspect(container_1[0]).parentage().count(abjad.Voice)
            1

            >>> abjad.inspect(container_2).parentage().count(abjad.Voice)
            1

            >>> abjad.inspect(container_2[0]).parentage().count(abjad.Voice)
            1

        """
        n = 0
        if prototype is None:
            prototype = Component
        for component in self:
            if isinstance(component, prototype):
                n += 1
        return n

    def get(self, prototype=None, n=0) -> typing.Optional[Component]:
        r"""
        Gets instance ``n`` of ``prototype`` in parentage.

        ..  container:: example

            >>> outer_red_voice = abjad.Voice("e''8 d''", name="Red_Voice")
            >>> inner_red_voice = abjad.Voice("c''4 b' c''8", name="Red_Voice")
            >>> inner_blue_voice = abjad.Voice("e'4 f' e'8", name="Blue_Voice")
            >>> container = abjad.Container(
            ...     [inner_red_voice, inner_blue_voice],
            ...     simultaneous=True,
            ... )
            >>> outer_red_voice.append(container)
            >>> outer_red_voice.extend("d''8")
            >>> abjad.override(outer_red_voice).note_head.color = "red"
            >>> literal = abjad.LilyPondLiteral(r"\voiceOne")
            >>> abjad.attach(literal, outer_red_voice[0])
            >>> abjad.override(inner_blue_voice).note_head.color = "blue"
            >>> literal = abjad.LilyPondLiteral(r"\voiceTwo")
            >>> abjad.attach(literal, inner_blue_voice[0])
            >>> dynamic = abjad.Dynamic("f")
            >>> abjad.attach(dynamic, outer_red_voice[0])
            >>> abjad.show(outer_red_voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(outer_red_voice)
                \context Voice = "Red_Voice"
                \with
                {
                    \override NoteHead.color = #red
                }
                {
                    \voiceOne
                    e''8
                    \f
                    d''8
                    <<
                        \context Voice = "Red_Voice"
                        {
                            c''4
                            b'4
                            c''8
                        }
                        \context Voice = "Blue_Voice"
                        \with
                        {
                            \override NoteHead.color = #blue
                        }
                        {
                            \voiceTwo
                            e'4
                            f'4
                            e'8
                        }
                    >>
                    d''8
                }

            ..  container:: example

                >>> leaf = abjad.inspect(inner_red_voice).leaf(0)
                >>> leaf
                Note("c''4")

                >>> parentage = abjad.inspect(leaf).parentage()

                Returns self when ``n=0``:

                >>> parentage.get(abjad.Component, 0)
                Note("c''4")

                Returns parents with positive ``n``:

                >>> parentage.get(abjad.Component, 1)
                Voice("c''4 b'4 c''8", name='Red_Voice')

                >>> parentage.get(abjad.Component, 2)
                <<<2>>>

                >>> parentage.get(abjad.Component, 3)
                <Voice-"Red_Voice"{4}>

                Returns none with ``n`` greater than score depth:

                >>> parentage.get(abjad.Component, 4) is None
                True

                >>> parentage.get(abjad.Component, 5) is None
                True

                >>> parentage.get(abjad.Component, 99) is None
                True

                Returns score root with ``n=-1``:

                >>> parentage.get(abjad.Component, -1)
                <Voice-"Red_Voice"{4}>

                With other negative ``n``: 

                >>> parentage.get(abjad.Component, -2)
                <<<2>>>

                >>> parentage.get(abjad.Component, -3)
                Voice("c''4 b'4 c''8", name='Red_Voice')

                >>> parentage.get(abjad.Component, -4)
                Note("c''4")

                Returns none for sufficiently negative ``n``:

                >>> parentage.get(abjad.Component, -5) is None
                True

                >>> parentage.get(abjad.Component, -7) is None
                True

                >>> parentage.get(abjad.Component, -99) is None
                True

            ..  container:: example

                Works with nested voices and tuplets:

                >>> leaf = abjad.inspect(inner_red_voice).leaf(0)
                >>> parentage = abjad.inspect(leaf).parentage()
                >>> leaf
                Note("c''4")

                Nonnegative ``n``:

                >>> parentage.get(abjad.Voice, 0)
                Voice("c''4 b'4 c''8", name='Red_Voice')

                >>> parentage.get(abjad.Voice, 1)
                <Voice-"Red_Voice"{4}>

                >>> parentage.get(abjad.Voice, 2) is None
                True

                >>> parentage.get(abjad.Voice, 9) is None
                True

                Negative ``n``:

                >>> parentage.get(abjad.Voice, -1)
                <Voice-"Red_Voice"{4}>

                >>> parentage.get(abjad.Voice, -2)
                Voice("c''4 b'4 c''8", name='Red_Voice')

                >>> parentage.get(abjad.Voice, -3) is None
                True

                >>> parentage.get(abjad.Voice, -99) is None
                True

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container_1 = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container_1, voice[1])
            >>> container_2 = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container_2, voice[3])
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
                    e'4
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> abjad.inspect(voice).parentage().get(abjad.Voice, 0)
            Voice("c'4 d'4 e'4 f'4")

            >>> abjad.inspect(container_1).parentage().get(abjad.Voice, 0)
            Voice("c'4 d'4 e'4 f'4")

            >>> abjad.inspect(container_1[0]).parentage().get(abjad.Voice, 0)
            Voice("c'4 d'4 e'4 f'4")

            >>> abjad.inspect(container_2).parentage().get(abjad.Voice, 0)
            Voice("c'4 d'4 e'4 f'4")

            >>> abjad.inspect(container_2[0]).parentage().get(abjad.Voice, 0)
            Voice("c'4 d'4 e'4 f'4")

        """
        if prototype is None:
            prototype = (Component,)
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        if 0 <= n:
            i = 0
            for component in self:
                if isinstance(component, prototype):
                    if i == n:
                        return component
                    i += 1
        else:
            i = -1
            for component in reversed(self):
                if isinstance(component, prototype):
                    if i == n:
                        return component
                    i -= 1
        return None

    def logical_voice(self) -> OrderedDict:
        r"""
        Gets logical voice.

        ..  container:: example

            Gets logical voice of note:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4", name="Music_Voice")
            >>> staff = abjad.Staff([voice], name="Music_Staff")
            >>> score = abjad.Score([staff], name="Score")
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \context Score = "Score"
                <<
                    \context Staff = "Music_Staff"
                    {
                        \context Voice = "Music_Voice"
                        {
                            c'4
                            d'4
                            e'4
                            f'4
                        }
                    }
                >>

            >>> note = voice[0]
            >>> parentage = abjad.inspect(note).parentage()
            >>> logical_voice = parentage.logical_voice()
            >>> abjad.f(logical_voice)
            abjad.OrderedDict(
                [
                    ('score', "Score-'Score'"),
                    ('staff', "Staff-'Music_Staff'"),
                    ('staff group', ''),
                    ('voice', "Voice-'Music_Voice'"),
                    ]
                )

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container_1 = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container_1, voice[1])
            >>> container_2 = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container_2, voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \context Voice = "Music_Voice"
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    e'4
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> lv = abjad.inspect(voice).parentage().logical_voice()
            >>> abjad.f(lv)
            abjad.OrderedDict(
                [
                    ('score', ''),
                    ('staff', ''),
                    ('staff group', ''),
                    ('voice', "Voice-'Music_Voice'"),
                    ]
                )

            >>> lv = abjad.inspect(container_1).parentage().logical_voice()
            >>> abjad.f(lv)
            abjad.OrderedDict(
                [
                    ('score', ''),
                    ('staff', ''),
                    ('staff group', ''),
                    ('voice', "Voice-'Music_Voice'"),
                    ]
                )

            >>> lv = abjad.inspect(container_1[0]).parentage().logical_voice()
            >>> abjad.f(lv)
            abjad.OrderedDict(
                [
                    ('score', ''),
                    ('staff', ''),
                    ('staff group', ''),
                    ('voice', "Voice-'Music_Voice'"),
                    ]
                )

            >>> lv = abjad.inspect(container_2).parentage().logical_voice()
            >>> abjad.f(lv)
            abjad.OrderedDict(
                [
                    ('score', ''),
                    ('staff', ''),
                    ('staff group', ''),
                    ('voice', "Voice-'Music_Voice'"),
                    ]
                )

            >>> lv = abjad.inspect(container_2[0]).parentage().logical_voice()
            >>> abjad.f(lv)
            abjad.OrderedDict(
                [
                    ('score', ''),
                    ('staff', ''),
                    ('staff group', ''),
                    ('voice', "Voice-'Music_Voice'"),
                    ]
                )

        """
        keys = ("score", "staff group", "staff", "voice")
        logical_voice = collections.OrderedDict.fromkeys(keys, "")
        for component in self:
            if isinstance(component, Voice):
                if not logical_voice["voice"]:
                    logical_voice["voice"] = self._id_string(component)
            elif isinstance(component, Staff):
                if not logical_voice["staff"]:
                    logical_voice["staff"] = self._id_string(component)
                    # explicit staff demands a nested voice:
                    # if no explicit voice has been found,
                    # create implicit voice here with random integer
                    if not logical_voice["voice"]:
                        logical_voice["voice"] = str(id(component))
            elif isinstance(component, StaffGroup):
                if not logical_voice["staff group"]:
                    logical_voice["staff group"] = self._id_string(component)
            elif isinstance(component, Score):
                if not logical_voice["score"]:
                    logical_voice["score"] = self._id_string(component)
        logical_voice_ = OrderedDict(logical_voice)
        return logical_voice_

    def score_index(self) -> typing.Tuple[typing.Union[int, str], ...]:
        r"""
        Gets score index.

        ..  container:: example

            >>> staff_1 = abjad.Staff(r"\times 2/3 { c''2 b'2 a'2 }")
            >>> staff_2 = abjad.Staff("c'2 d'2")
            >>> score = abjad.Score([staff_1, staff_2])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    {
                        \times 2/3 {
                            c''2
                            b'2
                            a'2
                        }
                    }
                    \new Staff
                    {
                        c'2
                        d'2
                    }
                >>

            >>> for component in abjad.select(score).components():
            ...     parentage = abjad.inspect(component).parentage()
            ...     component, parentage.score_index()
            ...
            (<Score<<2>>>, ())
            (<Staff{1}>, (0,))
            (Tuplet(Multiplier(2, 3), "c''2 b'2 a'2"), (0, 0))
            (Note("c''2"), (0, 0, 0))
            (Note("b'2"), (0, 0, 1))
            (Note("a'2"), (0, 0, 2))
            (Staff("c'2 d'2"), (1,))
            (Note("c'2"), (1, 0))
            (Note("d'2"), (1, 1))

            Score root sets score index to ``()``.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container_1 = abjad.GraceContainer("cs'16")
            >>> abjad.attach(container_1, voice[1])
            >>> container_2 = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container_2, voice[3])
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
                    e'4
                    \afterGrace
                    f'4
                    {
                        fs'16
                    }
                }

            >>> for component in abjad.select(voice).components():
            ...     parentage = abjad.inspect(component).parentage()
            ...     component, parentage.score_index()
            (Voice("c'4 d'4 e'4 f'4"), ())
            (Note("c'4"), (0,))
            (GraceContainer("cs'16"), (1, -1))
            (Note("cs'16"), (1, -1, 0))
            (Note("d'4"), (1,))
            (Note("e'4"), (2,))
            (Note("f'4"), (3,))
            (AfterGraceContainer("fs'16"), (3, 1))
            (Note("fs'16"), (3, 1, 0))

            Grace containers set score index to -1 (left of their main note).

            After-grace containers set score index to 1 (right of their main
            note).

        """
        result: typing.List[typing.Union[int, str]] = []
        current = self[0]
        for parent in self[1:]:
            if isinstance(current, AfterGraceContainer):
                tuple_ = type(self)(current._main_leaf).score_index()
                list_ = list(tuple_) + [1]
                result[0:0] = list_
            elif isinstance(current, GraceContainer):
                tuple_ = type(self)(current._main_leaf).score_index()
                list_ = list(tuple_) + [-1]
                result[0:0] = list_
            else:
                index = parent.index(current)
                result.insert(0, index)
            current = parent
        return tuple(result)
