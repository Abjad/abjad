from abjad.core.abjadcore import _Abjad


class _Brackets(_Abjad):

   def __init__(self, name = 'round'):
      self.name = name

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, str):
         return self.name == arg
      elif isinstance(arg, _Brackets):
         return self.name == arg.name
      else:
         return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s %s' % (self.open, self.close)

   ## PRIVATE METHODS ##

   _bracketNameToOpenClosePair = {
      'round':          ('(', ')'),
      'curly':          ('{', '}'),
      'sequential':     ('{', '}'),
      'angle':          ('<', '>'),
      'chord':          ('<', '>'),
      'double-angle':   ('<<', '>>'),
      'simultaneous':   ('<<', '>>'),
      }

   ## PUBLIC ATTRIBUTES ##

   @property
   def close(self):
      return self._bracketNameToOpenClosePair[self.name][-1]

   @apply
   def name( ):
      def fget(self):
         return self._name
      def fset(self, name):
         if name in self._bracketNameToOpenClosePair.keys( ):
            self._name = name
         else:
            raise ValueError('bracket must be one of %s.' %
               sorted(self._bracketNameToOpenClosePair.keys( )))
      return property(**locals( ))

   @property
   def open(self):
      return self._bracketNameToOpenClosePair[self.name][0]
