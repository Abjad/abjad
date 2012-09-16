from abjad.tools.contexttools.Context import Context


class Score(Context):
    r'''Abjad model of a score:

    ::

        >>> staff_1 = Staff("c'8 d'8 e'8 f'8")
        >>> staff_2 = Staff("c'8 d'8 e'8 f'8")
        >>> score = Score([staff_1, staff_2])
        >>> f(score)
        \new Score <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
        >>

    Return score object.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, music=None, context_name='Score', name=None):
        Context.__init__(self, music=music)
        self.is_parallel = True
        self._initialize_keyword_values(context_name=context_name, name=name)
