import collections
from abjad import mathtools
from abjad.system.AbjadObject import AbjadObject


class Parentage(AbjadObject, collections.Sequence):
    r'''
    Parentage of a component.

    ..  container:: example

        >>> score = abjad.Score()
        >>> string = r"""\new Voice = "Treble Voice" { e'4 }"""
        >>> treble_staff = abjad.Staff(string, name='Treble Staff')
        >>> score.append(treble_staff)
        >>> string = r"""\new Voice = "Bass Voice" { c4 }"""
        >>> bass_staff = abjad.Staff(string, name='Bass Staff')
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, bass_staff[0][0])
        >>> score.append(bass_staff)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \context Staff = "Treble Staff"
                {
                    \context Voice = "Treble Voice"
                    {
                        e'4
                    }
                }
                \context Staff = "Bass Staff"
                {
                    \context Voice = "Bass Voice"
                    {
                        \clef "bass"
                        c4
                    }
                }
            >>

        >>> bass_voice = score['Bass Voice']
        >>> note = bass_voice[0]
        >>> for component in abjad.inspect(note).parentage():
        ...     component
        ...
        Note('c4')
        Voice('c4', name='Bass Voice')
        <Staff-"Bass Staff"{1}>
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
        include_self=True,
        grace_notes=False,
        ):
        import abjad
        assert isinstance(component, (abjad.Component, type(None)))
        self._component = component
        if component is None:
            components = ()
        else:
            components = []
            if include_self:
                parent = component
            else:
                parent = component._parent
            prototype = (abjad.AfterGraceContainer, abjad.GraceContainer)
            while parent is not None:
                components.append(parent)
                if grace_notes and isinstance(parent, prototype):
                    parent = parent._carrier
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

    def __len__(self):
        """
        Gets number of components in parentage.

        Returns nonnegative integer.
        """
        return len(self.components)

    ### PRIVATE PROPERTIES ###

    @property
    def _prolations(self):
        import abjad
        prolations = []
        default = abjad.Multiplier(1)
        for parent in self:
            prolation = getattr(parent, 'implied_prolation', default)
            prolations.append(prolation)
        return prolations

    ### PRIVATE METHODS ###

    def _get_governor(self):
        import abjad
        for component in self:
            if (isinstance(component, abjad.Container) and
                not component.is_simultaneous):
                if component._parent is None:
                    return component
                if (isinstance(component._parent, abjad.Container) and
                    component._parent.is_simultaneous):
                    return component

    @staticmethod
    def _id_string(component):
        lhs = component.__class__.__name__
        rhs = getattr(component, 'name', None) or id(component)
        return f'{lhs}-{rhs!r}'

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
    def depth(self):
        """
        Length of proper parentage of component.

        Returns nonnegative integer.
        """
        return len(self[1:])

    @property
    def is_grace_note(self):
        r"""
        Is true when parentage contains a grace container.

        .. container:: example

            Grace notes:

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

            >>> for leaf in abjad.iterate(voice).leaves():
            ...     parentage = abjad.inspect(leaf).parentage()
            ...     print(leaf, parentage.is_grace_note)
            ...
            c'4 False
            c'16 True
            d'16 True
            d'4 False
            e'4 False
            f'4 False

        Returns true or false.
        """
        import abjad
        grace_container = self.get_first(prototype=abjad.GraceContainer)
        if grace_container is not None:
            return True
        return False

    @property
    def is_orphan(self):
        """
        Is true when component has no parent.

        Returns true or false.
        """
        return self.parent is None

    @property
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
            >>> logical_voice = parentage.logical_voice

            >>> for key, value in logical_voice.items():
            ...     print('%12s: %s' % (key, value))
            ...
            score: Score-'CustomScore'
            staff group:
            staff: Staff-'CustomStaff'
            voice: Voice-'CustomVoice'

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
        return logical_voice

    @property
    def parent(self):
        """
        Gets parent.

        Returns none when component has no parent.

        Returns component or none.
        """
        if 1 < len(self):
            return self[1]

    @property
    def prolation(self):
        """
        Gets prolation.

        Returns multiplier.
        """
        import abjad
        prolations = [abjad.Multiplier(1)] + self._prolations
        products = mathtools.cumulative_products(prolations)
        return products[-1]

    @property
    def root(self):
        """
        Gets root.

        Root defined equal to last component in parentage.

        Returns component.
        """
        return self[-1]

    @property
    def score_index(self):
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
            ...     leaf, parentage.score_index
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
            ...     leaf, parentage.score_index
            ...
            (Voice("c'8 d'8 e'8 f'8"), ())
            (Note("c'8"), (0,))
            (Note("cf''16"), (0,))
            (Note("bf'16"), (1,))
            (Note("d'8"), (1,))
            (Note("e'8"), (2,))
            (Note("f'8"), (3,))

            ..  todo:: Incorrect values returned for grace notes.

        Returns tuple of zero or more nonnegative integers.
        """
        result = []
        current = self[0]
        for parent in self[1:]:
            index = parent.index(current)
            result.insert(0, index)
            current = parent
        result = tuple(result)
        return result

    @property
    def tuplet_depth(self):
        r"""
        Gets tuplet depth.

        ..  container:: example

            Gets tuplet depth:

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

            >>> abjad.inspect(note).parentage().tuplet_depth
            1

            >>> abjad.inspect(tuplet).parentage().tuplet_depth
            0

            >>> abjad.inspect(staff).parentage().tuplet_depth
            0

        Returns nonnegative integer.
        """
        import abjad
        result = 0
        # should probably interate up to only first simultaneous container
        # in parentage.
        # note that we probably need a named idea for 'parentage
        # up to first simultaneous container'.
        for parent in self[1:]:
            if isinstance(parent, abjad.Tuplet):
                result += 1
        return result

    ### PUBLIC METHODS ###

    def get_first(self, prototype=None):
        """
        Gets first instance of ``prototype`` in parentage.

        Returns component or none.
        """
        import abjad
        if prototype is None:
            prototype = (abjad.Component,)
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        for component in self:
            if isinstance(component, prototype):
                return component
