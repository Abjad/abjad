from abjad.tools.contexttools._Context import _Context


class Score(_Context):
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

    __slots__ = ()

    def __init__(self, music = None, **kwargs):
        _Context.__init__(self, music)
        self.context = 'Score'
        self.is_parallel = True
        self._initialize_keyword_values(**kwargs)
