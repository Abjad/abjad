from abjad.tools.selectiontools.Selection import Selection


class Parentage(Selection):
    r'''Abjad model of component parentage:

    ::

        >>> score = Score()
        >>> score.append(Staff(r"""\new Voice = "Treble Voice" { c'4 }""",
        ...     name='Treble Staff'))
        >>> score.append(Staff(r"""\new Voice = "Bass Voice" { b,4 }""",
        ...     name='Bass Staff'))

    ::

        >>> f(score)
        \new Score <<
            \context Staff = "Treble Staff" {
                \context Voice = "Treble Voice" {
                    c'4
                }
            }
            \context Staff = "Bass Staff" {
                \context Voice = "Bass Voice" {
                    b,4
                }
            }
        >>

    ::

        >>> for x in componenttools.Parentage(score): x
        ...
        Score<<2>>

    ::

        >>> for x in componenttools.Parentage(score['Bass Voice'][0]): x
        ...
        Note('b,4')
        Voice-"Bass Voice"{1}
        Staff-"Bass Staff"{1}
        Score<<2>>

    Parentage is treated as a selection of the component's improper parentage.

    Return parentage instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_component', '_root')

    ### INITIALIZER ###

    def __init__(self, component):
        from abjad.tools import componenttools
        assert isinstance(component, componenttools.Component)
        music = componenttools.get_improper_parentage_of_component(component)
        Selection.__init__(self, music)
        self._component = component


    ### PRIVATE METHODS ###

    def _mark_spanner_format_contributions_for_update(self):
        for component in self:
            component._spanner_format_contributions_are_current = False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def component(self):
        '''The component from which the selection was derived.
        '''
        return self._component

    @property
    def containment_signature(self):
        r'''.. versionadded:: 1.1

        Containment signature of component::

            >>> score = Score(
            ... r"""\context Staff = "CustomStaff" { """
            ...     r"""\context Voice = "CustomVoice" { c' d' e' f' } }""")
            >>> score.name = 'CustomScore'


        ::

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

            >>> score.leaves[0].parentage.containment_signature
            ContainmentSignature(Note-..., Voice-'CustomVoice', Staff-..., Score-'CustomScore')

        Return containment signature object.
        '''
        from abjad.tools import componenttools
        from abjad.tools import scoretools
        from abjad.tools import stafftools
        from abjad.tools import voicetools
        signature = componenttools.ContainmentSignature()
        signature._self = self[0]._id_string
        for component in self:
            if isinstance(component, voicetools.Voice) and signature._voice is None:
                signature._voice = component._id_string
            elif isinstance(component, stafftools.Staff) and signature._staff is None:
                # leaves inside different staves have diff containment signatures regardless of staff name
                signature._staff = '{}-{}'.format(component._class_name, id(component))
            elif isinstance(component, scoretools.StaffGroup) and signature._staff_group is None:
                signature._staff_group = component._id_string
            elif isinstance(component, scoretools.Score) and signature._score is None:
                signature._score = component._id_string
        else:
            # root components must be the same object for containment signatures to compare true
            signature._root = id(component)
            signature._root_str = component._id_string
        return signature

    @property
    def depth(self):
        '''Length of proper parentage of component.

        Return nonnegative integer.
        '''
        return len(self[1:])

    @property
    def is_orphan(self):
        '''True when component has no parent.
        Otherwise false.

        Return boolean.
        '''
        return self.parent is None

    @property
    def parent(self):
        '''Parent of component or none when component is orphan.

        Return component or none.
        '''
        if 1 < len(self):
            return self[1]

    @property
    def parentage_signature(self):
        r'''.. versionadded:: 1.1

        Parentage signature of component::

            >>> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
            >>> staff = Staff([tuplet])
            >>> note = staff.leaves[0]
            >>> print note.parentage.parentage_signature
                staff: Staff-...
                self: Note-...

        Return parentage signature.
        '''
        from abjad.tools import componenttools
        from abjad.tools import scoretools
        from abjad.tools import stafftools
        from abjad.tools import voicetools
        signature = componenttools.ContainmentSignature()
        signature._self = self[0]._id_string
        for component in self:
            if isinstance(component, voicetools.Voice) and not signature._voice:
                signature._voice = component._id_string
            elif isinstance(component, stafftools.Staff) and not signature._staff:
                signature._staff = component._id_string
            elif isinstance(component, scoretools.StaffGroup) and not signature._staff_group:
                signature._staff_group = component._id_string
            elif isinstance(component, scoretools.Score) and not signature._score:
                signature._score = component._id_string
        else:
            # root components must be manifestly equal to compare true
            signature._root = id(component)
            signature._root_str = component._id_string
        return signature

    @property
    def root(self):
        '''Last element in parentage.
        '''
        return self[-1]

    @property
    def score_index(self):
        r'''Score index of component::

            >>> staff_1 = Staff(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { f'8 g'8 a'8 }")
            >>> staff_2 = Staff(r"\times 2/3 { b'8 c''8 d''8 }")
            >>> score = Score([staff_1, staff_2])

        ::

            >>> f(score)
            \new Score <<
                \new Staff {
                    \times 2/3 {
                        c'8
                        d'8
                        e'8
                    }
                    \times 2/3 {
                        f'8
                        g'8
                        a'8
                    }
                }
                \new Staff {
                    \times 2/3 {
                        b'8
                        c''8
                        d''8
                    }
                }
            >>

        ::

            >>> for leaf in score.leaves:
            ...     leaf, leaf.parentage.score_index
            ...
            (Note("c'8"), (0, 0, 0))
            (Note("d'8"), (0, 0, 1))
            (Note("e'8"), (0, 0, 2))
            (Note("f'8"), (0, 1, 0))
            (Note("g'8"), (0, 1, 1))
            (Note("a'8"), (0, 1, 2))
            (Note("b'8"), (1, 0, 0))
            (Note("c''8"), (1, 0, 1))
            (Note("d''8"), (1, 0, 2))

        Return tuple of zero or more nonnegative integers.
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
        '''Tuplet-depth of component::

            >>> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
            >>> staff = Staff([tuplet])
            >>> note = staff.leaves[0]

        ::

            >>> note.parentage.tuplet_depth
            1

        ::

            >>> tuplet.parentage.tuplet_depth
            0

        ::

            >>> staff.parentage.tuplet_depth
            0

        Return nonnegative integer.
        '''
        from abjad.tools import tuplettools
        from abjad.tools import componenttools
        result = 0
        # should probably interate up to only first parallel container in parentage.
        # note that we probably need a named idea for 'parentage up to first parallel container'.
        for parent in self[1:]:
            if isinstance(parent, tuplettools.Tuplet):
                result += 1
        return result
