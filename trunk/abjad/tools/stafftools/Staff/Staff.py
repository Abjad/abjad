from abjad.tools.contexttools.Context import Context


class Staff(Context):
    r'''Abjad model of a staff:

    ::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    Return staff object.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, music=None, **kwargs):
        Context.__init__(self, music)
        self.context_name = 'Staff'
        self._initialize_keyword_values(**kwargs)
