class Accidental(object):

   def __init__(self, string = ''):
      self.string = string

   ### REPR ###

   def __repr__(self):
      return 'Accidental(%s)' % self

   def __str__(self):
      return self.string

   ### PROPERTIES ###

   @property
   def adjustment(self):
      return self.accidentalStringToAdjustment[self.string]

   ### PREDICATES ###

   def hasNone(self):
      return self.string == ''

   ### OVERRIDES ###

   def __eq__(self, arg):
      #return isinstance(arg, Accidental) and self.string == arg.string
      if arg is None:
         return self.string == ''
      elif isinstance(arg, Accidental):
         return self.string == arg.string
      elif isinstance(arg, str):
         return self.string == arg
      return False

   def __ne__(self, arg):
      return not self == arg

   ### CONVERTERS ###

   accidentalStringToAdjustment = {
        '': 0,      '!': 0,
      'ff': -2,   'tqf': -1.5, 
       'f': -1,    'qf': -0.5,
      'ss': 2,    'tqs': 1.5,
       's': 1,     'qs': 0.5  }

   adjustmentToAccidentalString = {
       0: '',
      -2: 'ff',   -1.5: 'tqf',   
      -1: 'f',    -0.5: 'qf',
       2: 'ss',    1.5: 'tqs',    
       1: 's',     0.5: 'qs',
    -2.5: 'ff'
       }

   ### TODO - remove -2.5 after Lidercfeny ...
