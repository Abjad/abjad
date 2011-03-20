from abjad.components._Component import _Component
from abjad.tools.marktools.Mark import Mark
import copy


class Annotation(Mark):
   r'''.. versionadded:: 1.1.2

   User-defined annotation::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")

   ::

      abjad> f(staff)
      \new Staff {
         c'8
         d'8
         e'8
         f'8
      }

   ::

      abjad> marktools.Annotation('annotation contents')(staff[0])
      Annotation('annotation contents')(c'8)

   ::

      abjad> f(staff)
      \new Staff {
         c'8
         d'8
         e'8
         f'8
      }

   Annotations contribute no formatting.

   Annotations implement ``__slots__``.
   '''

   __slots__ = ('_contents', '_format_slot', )

   _format_slot = None

   def __init__(self, contents):
      Mark.__init__(self)
      self._contents = copy.copy(contents)
      
   ## OVERLOADS ##
   
   def __copy__(self, *args):
      return type(self)(self.contents_string)

   __deepcopy__ = __copy__

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self.contents_string == arg.contents_string
      return False

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents_repr_string(self):
      return repr(self.contents_string)
   
   ## PUBLIC ATTRIBUTES ##

   @apply
   def contents_string( ):
      def fget(self):
         '''Get contents string of annotation::

            abjad> annotation = marktools.Annotation('annotation contents')
            abjad> annotation.contents_string
            'annotation contents'

         Set contents string of annotation::
   
            abjad> annotation.contents_string = 'new annotation contents'
            abjad> annotation.contents_string
            'new annotation contents'
         '''
         return self._contents
      def fset(self, contents_string):
         assert isinstance(contents_string, str)
         self._contents = contents_string
      return property(**locals( ))
