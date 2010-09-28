from abjad.components._Component import _Component
from abjad.tools import stringtools
from abjad.tools.contexttools.Mark import Mark


class Comment(Mark):
   r'''.. versionadded:: 1.1.2

   .. todo:: make Comment format slot user-settable.
   '''

   def __init__(self, comment_name_string, format_slot = 'opening'):
      Mark.__init__(self, target_context = _Component)
      #if self.target_context is None:
      #   self._is_cosmetic_mark = True
      self._comment_name_string = comment_name_string
      self._contents_repr_string = "'%s'" % comment_name_string
      self._format_slot = format_slot
      
   ## OVERLOADS ##
   
   def __copy__(self, *args):
      return type(self)(self._comment_name_string, target_context = self.target_context)

   __deepcopy__ = __copy__

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self._comment_name_string == arg._comment_name_string
      return False

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      command = stringtools.underscore_delimited_lowercase_to_lowercamelcase(
         self._comment_name_string)
      return r'%% %s' % command
