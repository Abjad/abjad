from abjad.core.abjadcore import _Abjad


class Accidental(_Abjad):
   '''Any sharp, quarter-sharp, flat, quarter-flat, etc.

      ::

         abjad> t = Accidental('s')
         abjad> t
         Accidental(s)'''

   def __init__(self, arg = ''):
      if isinstance(arg, str):
         self.string = arg
      elif isinstance(arg, Accidental):
         self.string = arg.string 

   ## OVERLOADS ##

   def __eq__(self, arg):
      return self.string == Accidental(arg).string

   def __ge__(self, arg):
      return self.adjustment >= arg.adjustment

   def __gt__(self, arg):
      return self.adjustment > arg.adjustment
   
   def __le__(self, arg):
      return self.adjustment <= arg.adjustment

   def __lt__(self, arg):
      return self.adjustment < arg.adjustment
   
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
      '''Read-only number of semitones by which this accidental \
         acts on the note it modifies::

            abjad> t = Accidental('s')
            abjad> t.adjustment
            1

         ::

            abjad> t = Accidental('f')
            abjad> t.adjustment 
            -1'''

      return self.accidentalStringToAdjustment[self.string]

   @property
   def format(self):
      '''Read-only *LilyPond* format of accidental.

         ::
      
            abjad> t = Accidental('s')
            abjad> t.format
            's' 
      '''

      return self.string

   @apply
   def string( ):
      def fget(self):
         '''Read / write *LilyPond* accidental string.
      
            ::
         
               abjad> t = Accidental('s')
               abjad> t.string
               's' '''

         return self._string
      def fset(self, arg):
         assert isinstance(arg, str)
         self._string = arg
      return property(**locals( ))

   ## DICTIONARIES ##

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

   ## PUBLIC METHODS ##

   def hasNone(self):
      '''Read-only boolean ``True`` when ``self.string == ''``.

         ::

            abjad> t = Accidental( )
            abjad> t.hasNone( )
            True

         ::

            abjad> t = Accidental('s')
            abjad> t.hasNone( )
            False'''

      return self.string == ''
