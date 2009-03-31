from abjad.staffgroup.staffgroup import StaffGroup


def PianoStaff(music):
   result = StaffGroup(music)
   result.context = 'PianoStaff'
   return result
