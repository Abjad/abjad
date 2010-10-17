from abjad.components._Component import _Component
from abjad.tools import stringtools
#from abjad.tools.contexttools.ContextMark import ContextMark
from abjad.tools.marktools.Mark import Mark


#class Comment(ContextMark):
class Comment(Mark):
   r'''.. versionadded:: 1.1.2

   Abjad model of user comment::
   
      abjad> marktools.Comment('this is a comment.')
      Comment('this is a comment.')
   '''

   def __init__(self, comment_name_string, format_slot = 'opening'):
      #ContextMark.__init__(self, target_context = _Component)
      Mark.__init__(self)
      self._comment_name_string = comment_name_string
      self._contents_repr_string = "'%s'" % comment_name_string
      self._format_slot = format_slot
      
   ## OVERLOADS ##
   
   def __copy__(self, *args):
      return type(self)(self._comment_name_string)

   __deepcopy__ = __copy__

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self._comment_name_string == arg._comment_name_string
      return False

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      '''Read-only LilyPond input format of comment:

      ::

         abjad> comment = marktools.Comment('this is a comment.')
         abjad> comment.format
         '% this is a comment.'
      '''
      command = stringtools.underscore_delimited_lowercase_to_lowercamelcase(
         self._comment_name_string)
      return r'%% %s' % command
