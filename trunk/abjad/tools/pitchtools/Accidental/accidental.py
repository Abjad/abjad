from abjad.core.abjadcore import _Abjad


class Accidental(_Abjad):
   '''Any sharp, quarter-sharp, flat, quarter-flat, etc.

   ::

      abjad> t = pitchtools.Accidental('s')
      abjad> t
      Accidental(s)
   '''

   def __init__(self, arg = ''):
      if isinstance(arg, str):
         self.string = arg
      elif isinstance(arg, Accidental):
         self.string = arg.string 

   ## OVERLOADS ##

   def __eq__(self, arg):
      return self.string == Accidental(arg).string

   def __ge__(self, arg):
      return self.semitones >= arg.semitones

   def __gt__(self, arg):
      return self.semitones > arg.semitones
   
   def __le__(self, arg):
      return self.semitones <= arg.semitones

   def __lt__(self, arg):
      return self.semitones < arg.semitones
   
   def __ne__(self, arg):
      return not self == arg

   def __nonzero__(self):
      return True

   def __repr__(self):
      return 'Accidental(%s)' % self

   def __str__(self):
      return self.string

   ## PUBLIC ATTRIBUTES ##

   @property
   def adjustment(self):
      '''.. note::
         deprecated. Use accidental `semitones` instead.

      Read-only number of semitones to which this accidental is equal.

      ::

         abjad> t = pitchtools.Accidental('s')
         abjad> t.adjustment
         1

      ::

         abjad> t = pitchtools.Accidental('f')
         abjad> t.adjustment 
         -1
      '''
      return self.semitones

   @property
   def format(self):
      '''Read-only LilyPond format of accidental.

      ::
   
         abjad> t = pitchtools.Accidental('s')
         abjad> t.format
         's' 

      ::

         abjad> t = pitchtools.Accidental('f')
         abjad> t.format
         'f'
      '''
      return self.string

   @property
   def semitones(self):
      '''Read-only number of semitones to which this accidental is equal.
      '''
      return self.accidental_string_to_semitones[self.string]

   @apply
   def string( ):
      def fget(self):
         '''Read / write LilyPond accidental string.
      
         ::
      
            abjad> t = pitchtools.Accidental('s')
            abjad> t.string
            's'

         ::

            abjad> t = pitchtools.Accidental('f')
            abjad> t.string
            'f' 
         '''
         return self._string
      def fset(self, arg):
         assert isinstance(arg, str)
         self._string = arg
      return property(**locals( ))

   ## DICTIONARIES ##

   #accidentalStringToAdjustment = {
   accidental_string_to_semitones = {
        '': 0,      '!': 0,
      'ff': -2,   'tqf': -1.5, 
       'f': -1,    'qf': -0.5,
      'ss': 2,    'tqs': 1.5,
       's': 1,     'qs': 0.5  }

   #adjustmentToAccidentalString = {
   semitones_to_accidental_string = {
       0: '',
      -2: 'ff',   -1.5: 'tqf',   
      -1: 'f',    -0.5: 'qf',
       2: 'ss',    1.5: 'tqs',    
       1: 's',     0.5: 'qs',
    -2.5: 'ff'
       }
