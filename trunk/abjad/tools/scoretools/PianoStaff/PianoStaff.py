from abjad.tools.scoretools.StaffGroup.StaffGroup import StaffGroup


class PianoStaff(StaffGroup):
    r'''Abjad model of piano staff::

        abjad> staff_1 = Staff("c'4 d'4 e'4 f'4 g'1")
        abjad> staff_2 = Staff("g2 f2 e1")

    ::

        abjad> piano_staff = scoretools.PianoStaff([staff_1, staff_2])

    ::

        abjad> f(piano_staff)
        \new PianoStaff <<
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

    Return piano staff.
    '''

    def __init__(self, music):
        StaffGroup.__init__(self, music)
        self.context = 'PianoStaff'
