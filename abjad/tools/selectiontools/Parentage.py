# -*- coding: utf-8 -*-
import collections
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.selectiontools.Selection import Selection


class Parentage(Selection):
    r'''Parentage of a component.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> score = abjad.Score()
            >>> string = r"""\new Voice = "Treble Voice" { e'4 }"""
            >>> treble_staff = abjad.Staff(string, name='Treble Staff')
            >>> score.append(treble_staff)
            >>> string = r"""\new Voice = "Bass Voice" { c4 }"""
            >>> bass_staff = abjad.Staff(string, name='Bass Staff')
            >>> clef = abjad.Clef('bass')
            >>> abjad.attach(clef, bass_staff[0][0])
            >>> score.append(bass_staff)
            >>> show(score) # doctest: +SKIP

        ..  docs::

            >>> f(score)
            \new Score <<
                \context Staff = "Treble Staff" {
                    \context Voice = "Treble Voice" {
                        e'4
                    }
                }
                \context Staff = "Bass Staff" {
                    \context Voice = "Bass Voice" {
                        \clef "bass"
                        c4
                    }
                }
            >>

        ::

            >>> bass_voice = score['Bass Voice']
            >>> note = bass_voice[0]
            >>> for component in abjad.inspect(note).get_parentage():
            ...     component
            ...
            Note('c4')
            Voice('c4', name='Bass Voice')
            <Staff-"Bass Staff"{1}>
            <Score<<2>>>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_component',
        '_root',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        component=None,
        include_self=True,
        with_grace_notes=False,
        ):
        from abjad.tools import scoretools
        assert isinstance(component, (scoretools.Component, type(None)))
        if component is None:
            music = ()
        else:
            music = []
            if include_self:
                parent = component
            else:
                parent = component._parent
            prototype = (
                scoretools.AfterGraceContainer,
                scoretools.GraceContainer,
                )
            while parent is not None:
                music.append(parent)
                if with_grace_notes and isinstance(parent, prototype):
                    parent = parent._carrier
                else:
                    parent = parent._parent
            music = tuple(music)
        Selection.__init__(self, music)
        self._component = component

    ### PRIVATE METHODS ###

    def _get_governor(self):
        from abjad.tools import scoretools
        for component in self:
            if (isinstance(component, scoretools.Container) and
                not component.is_simultaneous):
                if component._parent is None:
                    return component
                if (isinstance(component._parent, scoretools.Container) and
                    component._parent.is_simultaneous):
                    return component

    @staticmethod
    def _id_string(component):
        lhs = component.__class__.__name__
        rhs = getattr(component, 'name', None) or id(component)
        return '{}-{!r}'.format(lhs, rhs)

    ### PUBLIC METHODS ###

    def get_first(self, prototype=None):
        r'''Gets first instance of `prototype` in parentage.

        Returns component or none.
        '''
        from abjad.tools import scoretools
        if prototype is None:
            prototype = (scoretools.Component,)
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        for component in self:
            if isinstance(component, prototype):
                return component

    ### PRIVATE PROPERTIES ###

    @property
    def _prolations(self):
        prolations = []
        default = durationtools.Multiplier(1)
        for parent in self:
            prolation = getattr(parent, 'implied_prolation', default)
            prolations.append(prolation)
        return prolations

    ### PUBLIC PROPERTIES ###

    @property
    def component(self):
        r'''The component from which the selection was derived.

        Returns component.
        '''
        return self._component

    @property
    def depth(self):
        r'''Length of proper parentage of component.

        Returns nonnegative integer.
        '''
        return len(self[1:])

    @property
    def is_grace_note(self):
        r'''Is true when parentage contains a grace container.
        Otherwise false.

        .. container:: example

            Grace notes:

            ::

                >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
                >>> container = abjad.GraceContainer("c'16 d'16")
                >>> abjad.attach(container, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  docs::

                >>> f(voice)
                \new Voice {
                    c'4
                    \grace {
                        c'16
                        d'16
                    }
                    d'4
                    e'4
                    f'4
                }

            ::

                >>> for leaf in abjad.iterate(voice).by_leaf(
                ...     with_grace_notes=True,
                ...     ):
                ...     parentage = abjad.inspect(leaf).get_parentage()
                ...     print(leaf, parentage.is_grace_note)
                ...
                c'4 False
                c'16 True
                d'16 True
                d'4 False
                e'4 False
                f'4 False

        Returns true or false.
        '''
        from abjad.tools import scoretools
        grace_container = self.get_first(prototype=scoretools.GraceContainer)
        if grace_container is not None:
            return True
        return False

    @property
    def is_orphan(self):
        r'''Is true when component has no parent.
        Otherwise false.

        Returns true or false.
        '''
        return self.parent is None

    @property
    def logical_voice(self):
        r'''Gets logical voice.

        ..  container:: example

            Gets logical voice of note:

            ::

                >>> voice = abjad.Voice("c'4 d'4 e'4 f'4", name='CustomVoice')
                >>> staff = abjad.Staff([voice], name='CustomStaff')
                >>> score = abjad.Score([staff], name='CustomScore')
                >>> show(score) # doctest: +SKIP

            ..  docs::

                >>> f(score)
                \context Score = "CustomScore" <<
                    \context Staff = "CustomStaff" {
                        \context Voice = "CustomVoice" {
                            c'4
                            d'4
                            e'4
                            f'4
                        }
                    }
                >>

            ::

                >>> note = voice[0]
                >>> parentage = abjad.inspect(note).get_parentage()
                >>> logical_voice = parentage.logical_voice

            ::

                >>> for key, value in logical_voice.items():
                ...     print('%12s: %s' % (key, value))
                ...
                score: Score-'CustomScore'
                staff group:
                staff: Staff-'CustomStaff'
                voice: Voice-'CustomVoice'

        Returns ordered dictionary.
        '''
        from abjad.tools import scoretools
        keys = ('score', 'staff group', 'staff', 'voice')
        logical_voice = collections.OrderedDict.fromkeys(keys, '')
        for component in self:
            if isinstance(component, scoretools.Voice):
                if not logical_voice['voice']:
                    logical_voice['voice'] = self._id_string(component)
            elif isinstance(component, scoretools.Staff):
                if not logical_voice['staff']:
                    logical_voice['staff'] = self._id_string(component)
                    # explicit staff demands a nested voice:
                    # if no explicit voice has been found,
                    # create implicit voice here with random integer
                    if not logical_voice['voice']:
                        logical_voice['voice'] = id(component)
            elif isinstance(component, scoretools.StaffGroup):
                if not logical_voice['staff group']:
                    logical_voice['staff group'] = self._id_string(component)
            elif isinstance(component, scoretools.Score):
                if not logical_voice['score']:
                    logical_voice['score'] = self._id_string(component)
        return logical_voice

    @property
    def parent(self):
        r'''Gets parent.

        Returns none when component has no parent.

        Returns component or none.
        '''
        if 1 < len(self):
            return self[1]

    @property
    def prolation(self):
        r'''Gets prolation.

        Returns multiplier.
        '''
        prolations = [durationtools.Multiplier(1)] + self._prolations
        products = mathtools.cumulative_products(prolations)
        return products[-1]

    @property
    def root(self):
        r'''Gets root.

        Root defined equal to last component in parentage.

        Returns component.
        '''
        return self[-1]

    @property
    def score_index(self):
        r'''Gets score index.

        ..  todo:: Define score index for grace notes.

        ..  container:: example

            Gets note score indices:

            ::

                >>> staff_1 = abjad.Staff(r"\times 2/3 { c''2 b'2 a'2 }")
                >>> staff_2 = abjad.Staff("c'2 d'2")
                >>> score = abjad.Score([staff_1, staff_2])
                >>> show(score) # doctest: +SKIP

            ..  docs::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        \times 2/3 {
                            c''2
                            b'2
                            a'2
                        }
                    }
                    \new Staff {
                            c'2
                            d'2
                    }
                >>

            ::

                >>> selector = abjad.select().by_leaf(flatten=True)
                >>> leaves = selector(score)
                >>> for leaf in leaves:
                ...     parentage = abjad.inspect(leaf).get_parentage()
                ...     leaf, parentage.score_index
                ...
                (Note("c''2"), (0, 0, 0))
                (Note("b'2"), (0, 0, 1))
                (Note("a'2"), (0, 0, 2))
                (Note("c'2"), (1, 0))
                (Note("d'2"), (1, 1))

        ..  container:: example

            With grace notes:

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

            ::

                >>> leaves = abjad.iterate(voice).by_class(
                ...     with_grace_notes=True,
                ...     )
                >>> for leaf in leaves:
                ...     parentage = abjad.inspect(leaf).get_parentage()
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
        '''
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
        r'''Gets tuplet depth.

        ..  container:: example

            Gets tuplet depth:

            ::

                >>> tuplet = abjad.Tuplet((2, 3), "c'2 d'2 e'2")
                >>> staff = abjad.Staff([tuplet])
                >>> note = tuplet[0]
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \times 2/3 {
                        c'2
                        d'2
                        e'2
                    }
                }

            ::

                >>> abjad.inspect(note).get_parentage().tuplet_depth
                1

            ::

                >>> abjad.inspect(tuplet).get_parentage().tuplet_depth
                0

            ::

                >>> abjad.inspect(staff).get_parentage().tuplet_depth
                0

        Returns nonnegative integer.
        '''
        from abjad.tools import scoretools
        result = 0
        # should probably interate up to only first simultaneous container
        # in parentage.
        # note that we probably need a named idea for 'parentage
        # up to first simultaneous container'.
        for parent in self[1:]:
            if isinstance(parent, scoretools.Tuplet):
                result += 1
        return result
