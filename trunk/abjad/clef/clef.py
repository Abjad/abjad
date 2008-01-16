class Clef(object):

   def __init__(self, name = 'treble'):
      self.name = name

   def __repr__(self):
      return 'Clef(%s)' % self.name

   def __str__(self):
      return self.name

   def __eq__(self, arg):
      return arg == self.name
   
   clefNameToMiddleCPosition = {
      'treble': -6,
      'bass':    6,
   }

   @property
   def middleCPosition(self):
      return self.clefNameToMiddleCPosition[self.name]

   @property
   def format(self):
      return r'\clef %s' % self.name
