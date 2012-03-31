from abjad.tools.contexttools.Context import Context


class Voice(Context):
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

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, music=None, **kwargs):
        Context.__init__(self, music)
        self.context_name = 'Voice'
        self._initialize_keyword_values(**kwargs)
