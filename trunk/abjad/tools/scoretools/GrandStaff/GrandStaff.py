from abjad.tools.scoretools.StaffGroup.StaffGroup import StaffGroup


class GrandStaff(StaffGroup):
    r'''Abjad model of grand staff::

        abjad> staff_1 = Staff("c'4 d'4 e'4 f'4 g'1")
        abjad> staff_2 = Staff("g2 f2 e1")

    ::

        abjad> grand_staff = scoretools.GrandStaff([staff_1, staff_2])

    ::

        abjad> f(grand_staff)
        \new GrandStaff <<
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

    Return grand staff.
    '''

    def __init__(self, music):
        StaffGroup.__init__(self, music)
        self.context = 'GrandStaff'
