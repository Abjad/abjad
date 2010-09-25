from abjad.core import _Immutable


class SchemePair(tuple, _Immutable):
   '''Abjad model of Scheme pair:

   ::

      abjad> schemetools.SchemePair('spacing', 4)
      SchemePair('spacing', 4)
   '''

   def __new__(klass, *args):
      if len(args) != 2:
         raise Exception('Scheme pairs may contain only two values.')
      self = tuple.__new__(klass, args)
      return self

   def __getnewargs__(self):
      return tuple(self)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return '(%s)' % self._output_string
   
   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      #return ', '.join([str(x) for x in self])
      result = [ ]
      for x in self:
         if isinstance(x, str):
            result.append("'%s'" % x)
         else:
            result.append(str(x))
      result = ', '.join(result)
      return result

   @property
   def _output_string(self):
      vals = [ ]
      for x in self:
          if isinstance(x, type(True)) and x:
              vals.append("#t")
          elif isinstance(x, type(True)):
              vals.append("#f")
          else:
              vals.append(x)
      return '%s . %s' % (vals[0], vals[1])

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      '''LilyPond input format of Scheme pair:
   
      ::

         abjad> scheme_pair = schemetools.SchemePair('spacing', 4)
         abjad> scheme_pair.format
         "#'(spacing . 4)"
      '''
      return "#'%s" % self.__str__( )
