class LilyFile(list):
   '''Abjad model of LilyPond input .ly file.'''

   ## OVERLOADS ##

   def __repr__(self):
      if not len(self):
         return '%s( )' % self.__class__.__name__
      else:
         return '%s(%s)' % (self.__class__.__name__, len(self))

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_pieces(self):
      result = [ ]
      for x in self:
         if hasattr(x, 'format'):
            result.append(x.format)
         else:
            result.append(str(x))
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return '\n\n'.join(self._format_pieces)
