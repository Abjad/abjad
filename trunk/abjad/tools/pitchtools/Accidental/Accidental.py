from abjad.core.abjadcore import _Abjad


class Accidental(_Abjad):
   '''Any sharp, quarter-sharp, flat, quarter-flat, etc.

   ::

      abjad> t = pitchtools.Accidental('s')
      abjad> t
      Accidental(s)
   '''

   def __init__(self, arg = ''):
      if arg in self._alphabetic_strings:
         self._string = arg
      elif arg in self._names:
         alphabetic_string = self._name_to_alphabetic_string[arg]
         self._string = alphabetic_string
      elif arg in self._semitones:
         alphabetic_string = self._semitones_to_alphabetic_string[arg]
         self._string = alphabetic_string
      elif isinstance(arg, Accidental):
         self._string = arg.string 
      elif isinstance(arg, type(None)):
         self._string = ''
      else:
         raise ValueError('can not initialize accidental from value: %s' % arg)

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.string == arg.string:
            return True
      return False

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
      return '%s(%s)' % (self.__class__.__name__, self.name)

   def __str__(self):
      return self.string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _alphabetic_strings(self):
      return self._alphabetic_string_to_symbolic_string.keys( )

   @property
   def _names(self):
      return self._name_to_alphabetic_string.keys( )

   @property
   def _semitones(self):
      return self._semitones_to_alphabetic_string.keys( )

   ## PUBLIC ATTRIBUTES ##

   @property
   def adjustment(self):
      '''.. note::
         deprecated. Use accidental `semitones` instead.
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
   def is_adjusted(self):
      return not self.semitones == 0

   @property
   def name(self):
      return self._alphabetic_string_to_name[self.string]

   @property
   def semitones(self):
      '''Read-only number of semitones to which this accidental is equal.

      ::

         abjad> pitchtools.Accidental('s').semitones
         1

      ::

         abjad> pitchtools.Accidental('f').semitones
         -1
      '''
      return self._alphabetic_string_to_semitones[self.string]

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
      return property(**locals( ))

   @property
   def symbolic_string(self):
      symbolic_string = self._alphabetic_string_to_symbolic_string[self.string]
      return symbolic_string

   ## DICTIONARIES ##

   _alphabetic_string_to_name = {
      'ss'  : 'double sharp',
      'tqs' : 'three-quarters sharp',
      's'   : 'sharp',
      'qs'  : 'quarter-sharp',
      ''    : 'natural',
      '!'   : 'forced natural',
      'qf'  : 'quarter-flat',
      'f'   : 'flat',
      'tqf' : 'three-quarters flat',
      'ff'  : 'double flat',
   }

   _alphabetic_string_to_semitones = {
        '': 0,      '!': 0,
      'ff': -2,   'tqf': -1.5, 
       'f': -1,    'qf': -0.5,
      'ss': 2,    'tqs': 1.5,
       's': 1,     'qs': 0.5,
   }

   _alphabetic_string_to_symbolic_string = {
        '': '',       '!': '!',
      'ff': 'bb',   'tqf': 'b+', 
       'f': 'b',     'qf': 'b-',
      'ss': '##',   'tqs': '#+',
       's': '#',     'qs': '#-',
   }

   _name_to_alphabetic_string = {
      'double sharp'          : 'ss',
      'three-quarters sharp'  : 'tqs',
      'sharp'                 : 's',
      'quarter sharp'         : 'qs',
      'natural'               : '',
      'forced natural'        : '!',
      'quarter flat'          : 'qf',
      'flat'                  : 'f',
      'three-quarters flat'   : 'tqf',
      'double flat'           :  'ff',
   }

   _semitones_to_alphabetic_string = {
       0: '',
      -2: 'ff',   -1.5: 'tqf',   
      -1: 'f',    -0.5: 'qf',
       2: 'ss',    1.5: 'tqs',    
       1: 's',     0.5: 'qs',
    -2.5: 'ff',
   }
