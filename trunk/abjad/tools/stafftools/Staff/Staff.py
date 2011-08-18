from abjad.tools.contexttools._Context import _Context


class Staff(_Context):
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

    __slots__ = ()

    def __init__(self, music = None, **kwargs):
        _Context.__init__(self, music)
        self.context = 'Staff'
        self._initialize_keyword_values(**kwargs)
