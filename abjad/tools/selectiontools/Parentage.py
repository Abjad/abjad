# -*- encoding: utf-8 -*-
import collections
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.selectiontools.SimultaneousSelection \
    import SimultaneousSelection


class Parentage(SimultaneousSelection):
    r'''The parentage of a component.

    ..  container:: example

        ::

            >>> score = Score()
            >>> string = r"""\new Voice = "Treble Voice" { e'4 }"""
            >>> treble_staff = Staff(string, name='Treble Staff')
            >>> score.append(treble_staff)
            >>> string = r"""\new Voice = "Bass Voice" { c4 }"""
            >>> bass_staff = Staff(string, name='Bass Staff')
            >>> clef = marktools.Clef('bass')
            >>> clef = attach(clef, bass_staff)
            >>> score.append(bass_staff)
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> f(score)
            \new Score <<
                \context Staff = "Treble Staff" {
                    \context Voice = "Treble Voice" {
                        e'4
                    }
                }
                \context Staff = "Bass Staff" {
                    \clef "bass"
                    \context Voice = "Bass Voice" {
                        c4
                    }
                }
            >>

        ::

            >>> bass_voice = score['Bass Voice']
            >>> note = bass_voice[0]
            >>> parentage = inspect(note).get_parentage()

        ::

            >>> for x in parentage: x
            ...
            Note('c4')
            Voice-"Bass Voice"{1}
            Staff-"Bass Staff"{1}
            Score<<2>>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_component', 
        '_root',
        )

    ### INITIALIZER ###

    def __init__(self, component=None, include_self=True):
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
            while parent is not None:
                music.append(parent)
                parent = parent._parent
            music = tuple(music)
        SimultaneousSelection.__init__(self, music)
        self._component = component

    ### PRIVATE PROPERTIES ###

    @property
    def _prolations(self):
        prolations = []
        default = durationtools.Multiplier(1)
        for parent in self:
            prolation = getattr(parent, 'implied_prolation', default)
            prolations.append(prolation)
        return prolations

    ### PRIVATE METHODS ###

    def _get_governor(self):
        from abjad.tools import scoretools
        from abjad.tools import scoretools
        for component in self:
            if isinstance(component, scoretools.Container) and \
                not component.is_simultaneous:
                if component._parent is None:
                    return component
                if isinstance(component._parent, scoretools.Container) and \
                    component._parent.is_simultaneous:
                    return component

    @staticmethod
    def _id_string(component):
        lhs = component.__class__.__name__
        rhs = getattr(component, 'name', None) or id(component)
        return '{}-{!r}'.format(lhs, rhs)

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
    def is_orphan(self):
        r'''True when component has no parent.
        Otherwise false.

        Returns boolean.
        '''
        return self.parent is None

    @property
    def logical_voice_indicator(self):
        r'''Logical voice indicator of component.

        ::

            >>> voice = Voice("c'4 d'4 e'4 f'4", name='CustomVoice')
            >>> staff = Staff([voice], name='CustomStaff')
            >>> score = Score([staff], name='CustomScore')
            >>> show(score) # doctest: +SKIP

        ..  doctest::

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

            >>> leaf = score.select_leaves()[0]
            >>> parentage = inspect(leaf).get_parentage()
            >>> indicator = parentage.logical_voice_indicator

        ::

            >>> for key, value in indicator.iteritems():
            ...     print '%12s: %s' % (key, value)
            ...
                     score: Score-'CustomScore'
               staff group: 
                     staff: Staff-'CustomStaff'
                     voice: Voice-'CustomVoice'

        Returns ordered dictionary.
        '''
        from abjad.tools import scoretools
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        from abjad.tools import scoretools
        from abjad.tools import scoretools
        keys = ('score', 'staff group', 'staff', 'voice')
        indicator = collections.OrderedDict.fromkeys(keys, '')
        for component in self:
            if isinstance(component, scoretools.Voice):
                if not indicator['voice']:
                    indicator['voice'] = self._id_string(component)
            elif isinstance(component, scoretools.Staff):
                if not indicator['staff']:
                    indicator['staff'] = self._id_string(component)
                    # explicit staff demands a nested voice:
                    # if no explicit voice has been found,
                    # create implicit voice here with random integer
                    if not indicator['voice']:
                        indicator['voice'] = id(component)
            elif isinstance(component, scoretools.StaffGroup):
                if not indicator['staff group']:
                    indicator['staff group'] = self._id_string(component)
            elif isinstance(component, scoretools.Score):
                if not indicator['score']:
                    indicator['score'] = self._id_string(component)
        return indicator

    @property
    def parent(self):
        r'''Parent of component.

        Returns none when component has no parent.

        Returns component or none.
        '''
        if 1 < len(self):
            return self[1]

    @property
    def prolation(self):
        r'''Prolation governing component.

        Returns multiplier.
        '''
        prolations = [durationtools.Multiplier(1)] + self._prolations
        products = mathtools.cumulative_products(prolations)
        return products[-1]

    @property
    def root(self):
        r'''Last element in parentage.

        Returns component.
        '''
        return self[-1]

    @property
    def score_index(self):
        r'''Score index of component.

        ::

            >>> staff_1 = Staff(r"\times 2/3 { c''2 b'2 a'2 }")
            >>> staff_2 = Staff("c'2 d'2")
            >>> score = Score([staff_1, staff_2])
            >>> show(score) # doctest: +SKIP

        ..  doctest::

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

            >>> leaves = score.select_leaves(allow_discontiguous_leaves=True)
            >>> for leaf in leaves:
            ...     parentage = inspect(leaf).get_parentage()
            ...     leaf, parentage.score_index
            ...
            (Note("c''2"), (0, 0, 0))
            (Note("b'2"), (0, 0, 1))
            (Note("a'2"), (0, 0, 2))
            (Note("c'2"), (1, 0))
            (Note("d'2"), (1, 1))

        Returns tuple of zero or more nonnegative integers.
        '''
        result = []
        cur = self[0]
        for parent in self[1:]:
            index = parent.index(cur)
            result.insert(0, index)
            cur = parent
        result = tuple(result)
        return result

    @property
    def tuplet_depth(self):
        r'''Tuplet depth of component.

        ::

            >>> tuplet = Tuplet(Multiplier(2, 3), "c'2 d'2 e'2")
            >>> staff = Staff([tuplet])
            >>> note = staff.select_leaves()[0]
            >>> show(staff) # doctest: +SKIP

        ::

            >>> inspect(note).get_parentage().tuplet_depth
            1

        ::

            >>> inspect(tuplet).get_parentage().tuplet_depth
            0

        ::

            >>> inspect(staff).get_parentage().tuplet_depth
            0

        Returns nonnegative integer.
        '''
        from abjad.tools import scoretools
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

    ### PUBLIC METHODS ###

    def get_first(self, component_classes=None):
        r'''Gets first instance of `component_classes` in parentage.

        Returns component or none.
        '''
        from abjad.tools import scoretools
        if component_classes is None:
            component_classes = (scoretools.Component,)
        if not isinstance(component_classes, tuple):
            component_classes = (component_classes,)
        for component in self:
            if isinstance(component, component_classes):
                return component
