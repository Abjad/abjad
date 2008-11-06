from abjad.context.context import _Context


class Staff(_Context):

   def __init__(self, music = None):
      music = music or [ ]
      _Context.__init__(self, music)
      self.invocation = 'Staff'

def RhythmicStaff(music):
   result = Staff(music)
   result.invocation.type = 'RhythmicStaff'
   return result

#def PianoStaff(music):
#   result = Container(music)
#   result.context.set('PianoStaff')
#   result.brackets.set('<<', '>>')
#   return result
#
#def GrandStaff(music):
#   result = Container(music)
#   result.context.set('GrandStaff')
#   result.brackets.set('<<', '>>')
#   return result
