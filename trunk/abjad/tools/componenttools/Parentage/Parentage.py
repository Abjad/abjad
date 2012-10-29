from abjad.tools.abctools.Selection import Selection


class Parentage(Selection):
    r'''Abjad model of Component parentage:

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

    Return Parentage instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_component',)

    ### INITIALIZER ###

    def __init__(self, component):
        from abjad.tools import componenttools 

        assert isinstance(component, componenttools.Component)
        music = componenttools.get_improper_parentage_of_component(component)
        Selection.__init__(self, music) 
        self._component = component

    ### PUBLIC READ-ONLY ATTRIBUTES ###

    @property
    def component(self):
        '''The component from which the selection was derived.'''
        return self._component


