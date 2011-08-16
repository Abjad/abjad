from abjad.tools.stafftools.Staff import Staff


def make_invisible_staff(music):
    '''Staff constructor that hides meter, bar line and staff lines.

    .. versionchanged:: 2.0
        Invisible staff class changed to invisible staff function.
    '''

    staff = Staff(music)
    staff.context = 'RhythmicStaff'
    staff.meter.transparent = True
    staff.bar_line.transparent = True
    staff.staff.transparent = True

    return staff
