from abjad.tools.contexttools._Context import _Context


class StaffGroup(_Context):
    r'''Abjad model of staff group::

        abjad> staff_1 = Staff("c'4 d'4 e'4 f'4 g'1")
        abjad> staff_2 = Staff("g2 f2 e1")

    ::

        abjad> staff_group = scoretools.StaffGroup([staff_1, staff_2])

    ::

        abjad> f(staff_group)
        \new StaffGroup <<
            \new Staff {
                c'4
                d'4
                e'4
                f'4
                g'1
            }
            \new Staff {
                g2
                f2
                e1
            }
        >>

    Return staff group.
    '''

    def __init__(self, music = [], **kwargs):
        _Context.__init__(self, music)
        self.is_parallel = True
        self.context = 'StaffGroup'
        self._initialize_keyword_values(**kwargs)
