from abjad.tools.contexttools.Context import Context


class Voice(Context):
    r'''Abjad model of a voice:

    ::

        >>> voice = Voice("c'8 d'8 e'8 f'8")
        >>> f(voice)
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

    def __init__(self, music=None, context_name='Voice', name=None):
        Context.__init__(self, music=music)
        self._initialize_keyword_values(context_name=context_name, name=name)
