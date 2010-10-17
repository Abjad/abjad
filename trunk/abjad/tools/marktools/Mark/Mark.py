class Mark(object):
   '''.. versionadded:: 1.1.2

   Mark models articulations, annotations, comments, LilyPond commands
   and other symbols that attach directly to a note, rest or chord.
   '''

   __slots__ = ('_contents_repr_string', '_start_component', )

   def __init__(self):
      self._contents_repr_string = ' '
      self._start_component = None

   ## OVERLOADS ##

   def __call__(self, *args):
      if len(args) == 0:
         return self.detach_mark( )
      elif len(args) == 1:
         return self.attach_mark(args[0])
      else:
         raise ValueError('must call mark with at most 1 argument.')

   def __copy__(self, *args):
      return type(self)( )

   __deepcopy__ = __copy__

   def __delattr__(self, *args):
      raise AttributeError('can not delete %s attributes.' % self.__class__.__name__)

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)%s' % (self.__class__.__name__, 
         self._contents_repr_string, self._attachment_repr_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _attachment_repr_string(self):
      if self.start_component is None:
         return ''
      else:
         return '(%s)' % str(self.start_component)

   ## MANGLED METHODS ##

   def __bind_start_component(self, start_component):
      assert isinstance(start_component, _Component)
      self.__unbind_start_component( )
      start_component._marks_for_which_component_functions_as_start_component.append(self)
      self._start_component = start_component
      ## unnecessary next line?
      #self._start_component._mark_entire_score_tree_for_later_update('marks')

   def __unbind_start_component(self):
      start_component = self._start_component
      if start_component is not None:
         try:
            start_component._marks_for_which_component_functions_as_start_component.remove(self)
         except ValueError:
            pass
      self._start_component = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def start_component(self):
      return self._start_component

   ## PUBLIC METHODS ##

   def attach_mark(self, start_component):
      self.__bind_start_component(start_component)
      return self

   def detach_mark(self):
      self.__unbind_start_component( )
      #self.__unbind_effective_context( )
      return self
