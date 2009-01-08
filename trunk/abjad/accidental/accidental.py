from abjad.core.abjadcore import _Abjad
#from abjad.core.grobhandler import _GrobHandler


#class _Accidental(_GrobHandler):
#class Accidental(_GrobHandler):
class Accidental(_Abjad):

   def __init__(self, string = ''):
      #_GrobHandler.__init__(self, 'Accidental')
      self._string = string

   ### OVERLOADS ###

   def __eq__(self, arg):
      if arg is None:
         return self._string == ''
      #elif isinstance(arg, _Accidental):
      elif isinstance(arg, Accidental):
         return self._string == arg._string
      elif isinstance(arg, str):
         return self._string == arg
      else:
         raise ValueError('can not compare to accidental.')

   def __ne__(self, arg):
      return not self == arg

   def __nonzero__(self):
      return True

   def __repr__(self):
      #return '_Accidental(%s)' % self
      return 'Accidental(%s)' % self

   def __str__(self):
      return self._string

   ### PUBLIC ATTRIBUTES ###

   @property
   def adjustment(self):
      return self.accidentalStringToAdjustment[self._string]

   ### DICTIONARIES ###

   accidentalStringToAdjustment = {
        '': 0,      '!': 0,
      'ff': -2,   'tqf': -1.5, 
       'f': -1,    'qf': -0.5,
      'ss': 2,    'tqs': 1.5,
       's': 1,     'qs': 0.5  }

   ### TODO - remove -2.5 after Lidercfeny ...

   adjustmentToAccidentalString = {
       0: '',
      -2: 'ff',   -1.5: 'tqf',   
      -1: 'f',    -0.5: 'qf',
       2: 'ss',    1.5: 'tqs',    
       1: 's',     0.5: 'qs',
    -2.5: 'ff'
       }

   ### PUBLIC METHODS ###

   def hasNone(self):
      return self._string == ''
