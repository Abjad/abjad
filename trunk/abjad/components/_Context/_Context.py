from abjad.components.Container import Container
from abjad.components._Context._ContextFormatter import _ContextFormatter


class _Context(Container):

   def __init__(self, music = None):
      Container.__init__(self, music)
      self._formatter = _ContextFormatter(self)
      self._engraver_consists = set([ ])
      self._engraver_removals = set([ ])

   ## OVERLOADS ##

   def __repr__(self):
      '''.. versionchanged:: 1.1.2
      Named contexts now print name at the interpreter.'''
      if 0 < len(self):
         summary = str(len(self))
      else:
         summary = ' '
      if self.parallel:
         open, close = '<<', '>>'
      else:
         open, close = '{', '}'
      name = self.name
      if name is not None:
         name = '-"%s"' % name
      else:
         name = ''
      return '%s%s%s%s%s' % (self.context, name, open, summary, close)

   ## PUBLIC ATTRIBUTES ##

   @apply
   def context( ):
      def fget(self):
         '''Read / write name of context as a string.'''
         return self._context
      def fset(self, arg):
         assert isinstance(arg, str)
         self._context = arg
      return property(**locals( ))

   @property
   def engraver_consists(self):
      r'''.. versionadded:: 1.1.2
      
      Unordered set of LilyPond engravers to include in context definition.
   
      Manage with add, update, other standard set commands. ::

         abjad> staff = Staff([ ])
         abjad> staff.engraver_consists.add('Horizontal_bracket_engraver')
         abjad> f(staff)
         \new Staff \with {
                 \consists Horizontal_bracket_engraver
         } {
         }
      '''
      return self._engraver_consists

   @property
   def engraver_removals(self):
      r'''.. versionadded:: 1.1.2
      
      Unordered set of LilyPond engravers to remove from context.
   
      Manage with add, update, other standard set commands. ::

         abjad> staff = Staff([ ])
         abjad> staff.engraver_consists.add('Time_signature_engraver')
         abjad> f(staff)
         \new Staff \with {
                 \remove Time_signature_engraver
         } {
         }
      '''
      return self._engraver_removals
