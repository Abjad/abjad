class SchemeVector(list):
   '''Abjad representation of Scheme vector.'''

   def __init__(self, *args):
      list.__init__(self, args)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return '(%s)' % self._output_string
   
   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in self])

   @property
   def _output_string(self):
      return ' '.join([str(x) for x in self])

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      '''LilyPond input representation of scheme vector.'''
      return "#'%s" % self
