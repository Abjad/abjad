from abjad.tools.abctools.Selection import Selection


class Lineage(Selection):
    r'''Abjad model of Component lineage:

    ::

        >>> score = Score()
        >>> score.append(Staff(r"""\new Voice = "Treble Voice" { c'4 }""",
        ... name='Treble Staff'))
        >>> score.append(Staff(r"""\new Voice = "Bass Voice" { b,4 }""",
        ... name='Bass Staff'))
    
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

        >>> for x in componenttools.Lineage(score): x
        ...
        Score<<2>>
        Staff-"Treble Staff"{1}
        Voice-"Treble Voice"{1}
        Note("c'4")
        Staff-"Bass Staff"{1}
        Voice-"Bass Voice"{1}
        Note('b,4')

    ::

        >>> for x in componenttools.Lineage(score['Bass Voice']): x
        ...
        Score<<2>>
        Staff-"Bass Staff"{1}
        Voice-"Bass Voice"{1}
        Note('b,4')

    Return Lineage instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_component',)

    ### INITIALIZER ###

    def __init__(self, component):
        from abjad.tools import componenttools

        assert isinstance(component, componenttools.Component)
        music = componenttools.get_lineage_of_component(component)
        Selection.__init__(self, music)
        self._component = component

    ### PUBLIC READ-ONLY ATTRIBUTES ###

    @property
    def component(self):
        '''The component from which the selection was derived.'''
        return self._component

