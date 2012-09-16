from abjad.tools.contexttools.Context import Context


class StaffGroup(Context):
    r'''Abjad model of staff group::

        >>> staff_1 = Staff("c'4 d'4 e'4 f'4 g'1")
        >>> staff_2 = Staff("g2 f2 e1")

    ::

        >>> staff_group = scoretools.StaffGroup([staff_1, staff_2])

    ::

        >>> f(staff_group)
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

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, music=None, context_name='StaffGroup', name=None):
        Context.__init__(self, music=music)
        self.is_parallel = True
        self._initialize_keyword_values(context_name=context_name, name=name)
