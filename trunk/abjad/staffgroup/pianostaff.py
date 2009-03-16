from abjad.staffgroup.staffgroup import StaffGroup


def PianoStaff(music):
   result = StaffGroup(music)
   result.invocation.type = 'PianoStaff'
   return result
