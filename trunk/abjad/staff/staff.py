from .. context.context import Context

class Staff(Context):

   def __init__(self, music = None):
      music = music or [ ]
      Context.__init__(self, music)
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
