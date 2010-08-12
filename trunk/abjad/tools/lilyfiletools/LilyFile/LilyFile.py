import types


class LilyFile(list):
   '''Abjad model of LilyPond input .ly file.'''

   def __init__(self):
      list.__init__(self)
      self.default_paper_size = None
      self.global_staff_size = None

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
      result.extend(self._file_initial_scheme_settings)
      for x in self:
         if hasattr(x, 'format'):
            result.append(x.format)
         else:
            result.append(str(x))
      return result

   @property
   def _file_initial_scheme_settings(self):
      result = [ ]
      default_paper_size = self.default_paper_size
      if default_paper_size is not None:
         dimension, orientation = default_paper_size
         result.append("#(set-default-paper-size \"%s\" '%s)" %
            (dimension, orientation))
      global_staff_size = self.global_staff_size
      if global_staff_size is not None:
         result.append('#(set-global-staff-size %s)' % global_staff_size)
      if result:
         result = ['\n'.join(result)]
      return result

   ## PUBLIC ATTRIBUTES ##

   @apply
   def default_paper_size( ):
      def fget(self):
         return self._default_paper_size
      def fset(self, args):
         ## #(set-default-paper-size "11x17" 'landscape)
         assert args is None or len(args) == 2
         self._default_paper_size = args
      return property(**locals( ))

   @property
   def format(self):
      return '\n\n'.join(self._format_pieces)

   @apply
   def global_staff_size( ):
      def fget(self):
         return self._global_staff_size
      def fset(self, arg):
         assert isinstance(arg, (int, float, long, type(None))) 
         self._global_staff_size = arg
      return property(**locals( ))
