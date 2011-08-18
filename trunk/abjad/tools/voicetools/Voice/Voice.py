from abjad.tools.contexttools._Context import _Context


class Voice(_Context):
    r'''Abjad model of a voice:

    ::

        abjad> voice = Voice("c'8 d'8 e'8 f'8")
        abjad> f(voice)
        \new Voice {
            c'8
            d'8
            e'8
            f'8
        }

    Return voice object.
    '''

    __slots__ = ()

    def __init__(self, music = None, **kwargs):
        _Context.__init__(self, music)
        self.context = 'Voice'
        self._initialize_keyword_values(**kwargs)
