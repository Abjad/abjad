from abjad.staffgroup.staffgroup import StaffGroup


def PianoStaff(music):
   result = StaffGroup(music)
   result.context = 'PianoStaff'
   result.invocation = 'PianoStaff'
   return result
