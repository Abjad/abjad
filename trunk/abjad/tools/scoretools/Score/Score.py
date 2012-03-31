from abjad.tools.contexttools.Context import Context


class Score(Context):
    r'''Abjad model of a score:

    ::

        abjad> staff_1 = Staff("c'8 d'8 e'8 f'8")
        abjad> staff_2 = Staff("c'8 d'8 e'8 f'8")
        abjad> score = Score([staff_1, staff_2])
        abjad> f(score)
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

    def __init__(self, music=None, **kwargs):
        Context.__init__(self, music)
        self.context_name = 'Score'
        self.is_parallel = True
        self._initialize_keyword_values(**kwargs)
