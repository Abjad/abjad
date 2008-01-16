class Brackets(object):

   def __init__(self, name = 'round'):
      self.name = name

   ### REPR ###

   def __repr__(self):
      return '%s %s' % (self.open, self.close)

   ### PROPERTIES ###

   @apply
   def name( ):
      def fget(self):
         return self._name
      def fset(self, name):
         if name in self.bracketNameToOpenClosePair.keys( ):
            self._name = name
         else:
            raise ValueError('bracket must be one of %s.' %
               sorted(self.bracketNameToOpenClosePair.keys( )))
      return property(**locals( ))

   @property
   def open(self):
      return self.bracketNameToOpenClosePair[self.name][0]
   
   @property
   def close(self):
      return self.bracketNameToOpenClosePair[self.name][-1]

   ### CONVERTERS ###

   bracketNameToOpenClosePair = {
      'round':          ('(', ')'),
      'curly':          ('{', '}'),
      'sequential':     ('{', '}'),
      'angle':          ('<', '>'),
      'chord':          ('<', '>'),
      'double-angle':   ('<<', '>>'),
      'simultaneous':   ('<<', '>>'),
      }

   ### COMPARISON ###

   def __eq__(self, arg):
      if isinstance(arg, str):
         return self.name == arg
      elif isinstance(arg, Brackets):
         return self.name == arg.name
      else:
         return False

   def __ne__(self, arg):
      return not self == arg
