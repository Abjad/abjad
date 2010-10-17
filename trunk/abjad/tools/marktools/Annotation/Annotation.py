from abjad.components._Component import _Component
#from abjad.tools.contexttools.ContextMark import ContextMark
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

   _format_slot = None

   def __init__(self, contents):
      #ContextMark.__init__(self, target_context = _Component)
      Mark.__init__(self)
      self._contents = contents
      
   ## OVERLOADS ##
   
   def __copy__(self, *args):
      #return type(self)(self.contents, target_context = self.target_context)
      return type(self)(self.contents)

   __deepcopy__ = __copy__

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self.contents == arg.contents
      return False
   
   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, repr(self.contents))

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
