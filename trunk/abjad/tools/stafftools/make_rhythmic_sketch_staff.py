from abjad.tools.stafftools.Staff import Staff


def make_rhythmic_sketch_staff(music):
    '''Make rhythmic staff with transparent meter and transparent bar lines.'''

    staff = Staff(music)
    staff.context = 'RhythmicStaff'
    staff.override.time_signature.transparent = True
    staff.override.bar_line.transparent = True

    return staff
