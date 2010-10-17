from abjad.components.Staff import Staff


class RhythmicStaff(Staff):
   '''The Abjad model of a rhythmic staff.
   '''

   __slots__ = ( )

   def __init__(self, music = [ ], **kwargs):
      Staff.__init__(self, music, **kwargs)
      self.context = 'RhythmicStaff'
