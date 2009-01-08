from abjad.core.abjadcore import _Abjad


#class _Clef(_Abjad):
class Clef(_Abjad):

   def __init__(self, name = 'treble'):
      self.name = name

   ### OVERLOADS ###

   def __eq__(self, arg):
      return arg == self.name
   
   def __repr__(self):
      #return '_Clef(%s)' % self.name
      return 'Clef(%s)' % self.name

   def __str__(self):
      return self.name

   ### PUBLIC ATTRIBUTES ###

   clefNameToMiddleCPosition = {
      'treble': -6,
      'bass':    6,
   }

   @property
   def format(self):
      return r'\clef %s' % self.name

   @property
   def middleCPosition(self):
      return self.clefNameToMiddleCPosition[self.name]
