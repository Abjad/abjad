from abjad.components._Component import _Component
from abjad.tools.marktools.Mark import Mark


class Annotation(Mark):
   r'''.. versionadded:: 1.1.2

   User-defined annotation that makes no format contribution::

      abjad> staff = Staff(macros.scale(4))
      abjad> annotation = marktools.Annotation('annotation contents')(staff[0])
      abjad> annotation
      Annotation('annotation contents')

   Annotation replaces elements added to history interface.
   '''

   __slots__ = ('_contents', '_format_slot', )

   _format_slot = None

   def __init__(self, contents):
      Mark.__init__(self)
      self._contents = contents
      
   ## OVERLOADS ##
   
   def __copy__(self, *args):
      return type(self)(self.contents)

   __deepcopy__ = __copy__

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self.contents == arg.contents
      return False

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents_repr_string(self):
      return repr(self.contents)
   
   ## PUBLIC ATTRIBUTES ##

   @property
   def contents(self):
      '''Read-only contents of annotation:

      ::

         abjad> annotation = marktools.Annotation('annotation contents')
         abjad> annotation.contents
         'annotation contents'
      '''
      return self._contents
