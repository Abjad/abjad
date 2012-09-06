def make_rhythmic_sketch_staff(music):
    '''Make rhythmic staff with transparent meter and transparent bar lines.
    '''
    from abjad.tools import stafftools

    staff = stafftools.Staff(music)
    staff.context_name = 'RhythmicStaff'
    staff.override.time_signature.transparent = True
    staff.override.bar_line.transparent = True

    return staff
