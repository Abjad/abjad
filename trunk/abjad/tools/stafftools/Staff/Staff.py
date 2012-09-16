from abjad.tools.contexttools.Context import Context


class Staff(Context):
    r'''Abjad model of a staff:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> f(staff)
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

    def __init__(self, music=None, context_name='Staff', name=None):
        Context.__init__(self, music=music)
        self._initialize_keyword_values(context_name=context_name, name=name)
