from abjad.tools.componenttools._Component import _Component
from abjad.tools.marktools.Mark import Mark


class Comment(Mark):
   r'''.. versionadded:: 2.0

   User-defined comment::
   
      abjad> note = Note("c'4")

   ::

      abjad> marktools.Comment('this is a comment')(note)
      Comment('this is a comment')(c'4)

   ::

      abjad> f(note)
      % this is a comment
      c'4

   Comments implement ``__slots__``.
   '''

   __slots__ = ('_comment_name_string', '_format_slot', )

   def __init__(self, comment_name_string, format_slot = 'opening'):
      Mark.__init__(self)
      self._comment_name_string = comment_name_string
      self._format_slot = format_slot
      
   ## OVERLOADS ##
   
   def __copy__(self, *args):
      return type(self)(self._comment_name_string)

   __deepcopy__ = __copy__

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self._comment_name_string == arg._comment_name_string
      return False

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents_repr_string(self):
      return repr(self._comment_name_string)

   ## PUBLIC ATTRIBUTES ##

   @apply
   def contents_string( ):
      def fget(self):
         r'''Get contents string of comment::

            abjad> comment = marktools.Comment('comment contents string')
            abjad> comment.contents_string
            'comment contents string'

         Set contents string of comment::

            abjad> comment.contents_string = 'new comment contents string'
            abjad> comment.contents_string
            'new comment contents string'

         Set string.
         '''
         return self._comment_name_string
      def fset(self, contents_string):
         assert isinstance(contents_string, str)
         self._comment_name_string = contents_string
      return property(**locals( ))

   @property
   def format(self):
      '''Read-only LilyPond input format of comment:

      ::

         abjad> comment = marktools.Comment('this is a comment.')
         abjad> comment.format
         '% this is a comment.'

      Return string.
      '''
      from abjad.tools import iotools
      command = iotools.underscore_delimited_lowercase_to_lowercamelcase(self._comment_name_string)
      return r'%% %s' % command
