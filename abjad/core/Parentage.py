import collections
import typing
from abjad import mathtools
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.utilities.Multiplier import Multiplier


class Parentage(collections.abc.Sequence):
    r'''
    Parentage of a component.

    ..  container:: example

        >>> score = abjad.Score()
        >>> string = r"""\new Voice = "Treble_Voice" { e'4 }"""
        >>> treble_staff = abjad.Staff(string, name='Treble_Staff')
        >>> score.append(treble_staff)
        >>> string = r"""\new Voice = "Bass_Voice" { c4 }"""
        >>> bass_staff = abjad.Staff(string, name='Bass_Staff')
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

        >>> bass_voice = score['Bass_Voice']
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

    __documentation_section__ = 'Selections'

    __slots__ = (
        '_component',
        '_components',
        '_root',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        component=None,
        grace_notes=False,
        ):
        import abjad
        assert isinstance(component, (abjad.Component, type(None)))
        self._component = component
        if component is None:
            components = ()
        else:
            components = []
            parent = component
            prototype = (abjad.AfterGraceContainer, abjad.GraceContainer)
            while parent is not None:
                components.append(parent)
                if grace_notes and isinstance(parent, prototype):
                    parent = parent._main_leaf
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
        rhs = getattr(component, 'name', None) or id(component)
        return f'{lhs}-{rhs!r}'

    def _prolations(self):
        prolations = []
        default = Multiplier(1)
        for parent in self:
            prolation = getattr(parent, 'implied_prolation', default)
            prolations.append(prolation)
        return prolations

    ### PUBLIC PROPERTIES ###

    @property
    def component(self):
        """
        The component from which the selection was derived.

        Returns component.
        """
        return self._component

    @property
    def components(self):
        """
        Gets components.

        Returns tuple.
        """
        return self._components

    @property
    def orphan(self) -> bool:
        """
        Is true when component has no parent.
        """
        return self.parent is None

    @property
    def parent(self):
        """
        Gets parent.

        Returns none when component has no parent.

        Returns component or none.
        """
        return self.get(n=1)

    @property
    def prolation(self) -> Multiplier:
        """
        Gets prolation.
        """
        prolations = [Multiplier(1)] + self._prolations()
        products = mathtools.cumulative_products(prolations)
        return products[-1]

    @property
    def root(self):
        """
        Gets root.

        Root defined equal to last component in parentage.

        Returns component.
        """
        return self.get(n=-1)

    ### PUBLIC METHODS ###

    def count(self, prototype=None) -> int:
        r"""
        Gets number of ``prototype`` in parentage.

        ..  container:: example

            Gets tuplet count:

            >>> tuplet = abjad.Tuplet((2, 3), "c'2 d'2 e'2")
            >>> staff = abjad.Staff([tuplet])
            >>> note = tuplet[0]
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 2/3 {
                        c'2
                        d'2
                        e'2
                    }
                }

            >>> abjad.inspect(note).parentage().count(abjad.Tuplet)
            1

            >>> abjad.inspect(tuplet).parentage().count(abjad.Tuplet)
            1

            >>> abjad.inspect(staff).parentage().count(abjad.Tuplet)
            0

        ..  container:: example

            Gets voice count:

            >>> outer_red_voice = abjad.Voice("e''8 d''", name='Red_Voice')
            >>> inner_red_voice = abjad.Voice("c''4 b' c''8", name='Red_Voice')
            >>> inner_blue_voice = abjad.Voice("e'4 f' e'8", name='Blue_Voice')
            >>> container = abjad.Container(
            ...     [inner_red_voice, inner_blue_voice],
            ...     is_simultaneous=True,
            ...     )
            >>> outer_red_voice.append(container)
            >>> outer_red_voice.extend("d''8")
            >>> abjad.override(outer_red_voice).note_head.color = 'red'
            >>> literal = abjad.LilyPondLiteral(r'\voiceOne')
            >>> abjad.attach(literal, outer_red_voice[0])
            >>> abjad.override(inner_blue_voice).note_head.color = 'blue'
            >>> literal = abjad.LilyPondLiteral(r'\voiceTwo')
            >>> abjad.attach(literal, inner_blue_voice[0])
            >>> dynamic = abjad.Dynamic('f')
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

        """
        from .Component import Component
        n = 0
        if prototype is None:
            prototype = Component
        for component in self:
            if isinstance(component, prototype):
                n += 1
        return n

    def get(self, prototype=None, n=0):
        r"""
        Gets instance ``n`` of ``prototype`` in parentage.

        ..  container:: example

            >>> outer_red_voice = abjad.Voice("e''8 d''", name='Red_Voice')
            >>> inner_red_voice = abjad.Voice("c''4 b' c''8", name='Red_Voice')
            >>> inner_blue_voice = abjad.Voice("e'4 f' e'8", name='Blue_Voice')
            >>> container = abjad.Container(
            ...     [inner_red_voice, inner_blue_voice],
            ...     is_simultaneous=True,
            ...     )
            >>> outer_red_voice.append(container)
            >>> outer_red_voice.extend("d''8")
            >>> abjad.override(outer_red_voice).note_head.color = 'red'
            >>> literal = abjad.LilyPondLiteral(r'\voiceOne')
            >>> abjad.attach(literal, outer_red_voice[0])
            >>> abjad.override(inner_blue_voice).note_head.color = 'blue'
            >>> literal = abjad.LilyPondLiteral(r'\voiceTwo')
            >>> abjad.attach(literal, inner_blue_voice[0])
            >>> dynamic = abjad.Dynamic('f')
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

        Returns component or none.
        """
        import abjad
        if prototype is None:
            prototype = (abjad.Component,)
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

    def logical_voice(self):
        r"""
        Gets logical voice.

        ..  container:: example

            Gets logical voice of note:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4", name='CustomVoice')
            >>> staff = abjad.Staff([voice], name='CustomStaff')
            >>> score = abjad.Score([staff], name='CustomScore')
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \context Score = "CustomScore"
                <<
                    \context Staff = "CustomStaff"
                    {
                        \context Voice = "CustomVoice"
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
                    ('score', "Score-'CustomScore'"),
                    ('staff', "Staff-'CustomStaff'"),
                    ('staff group', ''),
                    ('voice', "Voice-'CustomVoice'"),
                    ]
                )

        ..  container:: example

            REGRESSION. Graces notes inhabit same logical voice as their
            client:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4", name='CustomVoice')
            >>> note = abjad.Note("cs'16")
            >>> grace_container = abjad.GraceContainer([note])
            >>> abjad.attach(grace_container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \context Voice = "CustomVoice"
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    e'4
                    f'4
                }

            >>> voice_1 = abjad.inspect(voice[1]).parentage().logical_voice()
            >>> abjad.f(voice_1)
            abjad.OrderedDict(
                [
                    ('score', ''),
                    ('staff', ''),
                    ('staff group', ''),
                    ('voice', "Voice-'CustomVoice'"),
                    ]
                )

            >>> voice_2 = abjad.inspect(note).parentage(grace_notes=True).logical_voice()
            >>> abjad.f(voice_2)
            abjad.OrderedDict(
                [
                    ('score', ''),
                    ('staff', ''),
                    ('staff group', ''),
                    ('voice', "Voice-'CustomVoice'"),
                    ]
                )

            >>> voice_1 == voice_2
            True

        Returns ordered dictionary.
        """
        import abjad
        keys = ('score', 'staff group', 'staff', 'voice')
        logical_voice = collections.OrderedDict.fromkeys(keys, '')
        for component in self:
            if isinstance(component, abjad.Voice):
                if not logical_voice['voice']:
                    logical_voice['voice'] = self._id_string(component)
            elif isinstance(component, abjad.Staff):
                if not logical_voice['staff']:
                    logical_voice['staff'] = self._id_string(component)
                    # explicit staff demands a nested voice:
                    # if no explicit voice has been found,
                    # create implicit voice here with random integer
                    if not logical_voice['voice']:
                        logical_voice['voice'] = id(component)
            elif isinstance(component, abjad.StaffGroup):
                if not logical_voice['staff group']:
                    logical_voice['staff group'] = self._id_string(component)
            elif isinstance(component, abjad.Score):
                if not logical_voice['score']:
                    logical_voice['score'] = self._id_string(component)
        logical_voice = abjad.OrderedDict(logical_voice)
        return logical_voice

    def outermost_voice_content(self) -> typing.Optional[bool]:
        r"""
        Is true when component is immediate child of outermost voice.

        ..  container:: example

            >>> outer_red_voice = abjad.Voice("e''8 d''", name='Red_Voice')
            >>> inner_red_voice = abjad.Voice("c''4 b' c''8", name='Red_Voice')
            >>> inner_blue_voice = abjad.Voice("e'4 f' e'8", name='Blue_Voice')
            >>> container = abjad.Container(
            ...     [inner_red_voice, inner_blue_voice],
            ...     is_simultaneous=True,
            ...     )
            >>> outer_red_voice.append(container)
            >>> outer_red_voice.extend("d''8")
            >>> abjad.override(outer_red_voice).note_head.color = 'red'
            >>> literal = abjad.LilyPondLiteral(r'\voiceOne')
            >>> abjad.attach(literal, outer_red_voice[0])
            >>> abjad.override(inner_blue_voice).note_head.color = 'blue'
            >>> literal = abjad.LilyPondLiteral(r'\voiceTwo')
            >>> abjad.attach(literal, inner_blue_voice[0])
            >>> dynamic = abjad.Dynamic('f')
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

            >>> for component in abjad.iterate(outer_red_voice).components():
            ...     parentage = abjad.inspect(component).parentage()
            ...     print(component, parentage.outermost_voice_content())
            ...
            <Voice-"Red_Voice"{4}> False
            e''8 True
            d''8 True
            <<<2>>> True
            Voice("c''4 b'4 c''8", name='Red_Voice') False
            c''4 False
            b'4 False
            c''8 False
            Voice("e'4 f'4 e'8", name='Blue_Voice') False
            e'4 False
            f'4 False
            e'8 False
            d''8 True

        ..  container:: example

            Innermost context functions as voice when no voice is found:

            >>> string = r"c'8 d' r \times 2/3 { e' r f' } g' a' r"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    d'8
                    r8
                    \times 2/3 {
                        e'8
                        r8
                        f'8
                    }
                    g'8
                    a'8
                    r8
                }

            >>> for component in abjad.iterate(staff).components():
            ...     parentage = abjad.inspect(component).parentage()
            ...     print(component, parentage.outermost_voice_content())
            ...
            <Staff{7}> False
            c'8 True
            d'8 True
            r8 True
            Tuplet(Multiplier(2, 3), "e'8 r8 f'8") True
            e'8 False
            r8 False
            f'8 False
            g'8 True
            a'8 True
            r8 True

        """
        from .Context import Context
        from .Voice import Voice
        context = self.get(Voice, -1) or self.get(Context)
        if context is not None:
            return self.component._parent is context
        return None

    def score_index(self) -> typing.Tuple[int, ...]:
        r"""
        Gets score index.

        ..  todo:: Define score index for grace notes.

        ..  container:: example

            Gets note score indices:

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

            >>> for leaf in abjad.select(score).leaves():
            ...     parentage = abjad.inspect(leaf).parentage()
            ...     leaf, parentage.score_index()
            ...
            (Note("c''2"), (0, 0, 0))
            (Note("b'2"), (0, 0, 1))
            (Note("a'2"), (0, 0, 2))
            (Note("c'2"), (1, 0))
            (Note("d'2"), (1, 1))

        ..  container:: example

            With grace notes:

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

            >>> leaves = abjad.iterate(voice).components()
            >>> for leaf in leaves:
            ...     parentage = abjad.inspect(leaf).parentage()
            ...     leaf, parentage.score_index()
            ...
            (Voice("c'8 d'8 e'8 f'8"), ())
            (Note("c'8"), (0,))
            (GraceContainer("cf''16 bf'16"), ())
            (Note("cf''16"), (0,))
            (Note("bf'16"), (1,))
            (Note("d'8"), (1,))
            (Note("e'8"), (2,))
            (Note("f'8"), (3,))

            ..  todo:: Incorrect values returned for grace notes.

        Returns tuple of zero or more nonnegative integers.
        """
        result: typing.List[int] = []
        current = self[0]
        for parent in self[1:]:
            index = parent.index(current)
            result.insert(0, index)
            current = parent
        return tuple(result)
