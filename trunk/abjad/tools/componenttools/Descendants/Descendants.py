from abjad.tools.abctools.ScoreSelection import ScoreSelection


class Descendants(ScoreSelection):
    r'''Abjad model of Component descendants:

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

        >>> for x in componenttools.Descendants(score): x
        ...
        Score<<2>>
        Staff-"Treble Staff"{1}
        Voice-"Treble Voice"{1}
        Note("c'4")
        Staff-"Bass Staff"{1}
        Voice-"Bass Voice"{1}
        Note('b,4')

    ::

        >>> for x in componenttools.Descendants(score['Bass Voice']): x
        ...
        Voice-"Bass Voice"{1}
        Note('b,4')

    Descendants is treated as the selection of the component's improper descendants.

    Return Descendants instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_component',)

    ### INITIALIZER ###

    def __init__(self, component):
        from abjad.tools import componenttools

        assert isinstance(component, componenttools.Component)
        music = componenttools.get_improper_descendents_of_component(component)
        ScoreSelection.__init__(self, music)
        self._component = component

    ### PUBLIC READ-ONLY ATTRIBUTES ###

    @property
    def component(self):
        '''The component from which the selection was derived.'''
        return self._component

