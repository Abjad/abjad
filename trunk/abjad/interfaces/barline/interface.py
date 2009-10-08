from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
import types


class BarLineInterface(_Interface, _GrobHandler):
   '''Manage barlines.

      ::

         abjad> t = Note(0, (1, 4))
         abjad> t.barline
         <BarLineInterface>

      Override LilyPond ``BarLine`` grob.

      ::

         abjad> t.barline.color = 'red'
         abjad> print t.format
         \once \override BarLine #'color = #red
         c'4'''
   
   def __init__(self, _client):
      '''Bind to client and set ``kind`` to ``None``.'''

      _Interface.__init__(self, _client)
      _GrobHandler.__init__(self, 'BarLine')
      self._kind = None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _closing(self):
      '''Read-only list of container-closing or after-leaf
      format contribution strings. ::

         abjad> t = Note(0, (1, 4))
         abjad> t.barline.kind = '||'
         abjad> t.barline.closing
         ['\\bar "||"']
      '''

      result = [ ]
      if self.kind:
         result.append(r'\bar "%s"' % self.kind)
      return result

   ## PUBLIC ATTRIBUTES ##

   @apply
   def kind( ):
      def fget(self):
         r'''Read / write LilyPond barline string.

         *  Default value: ``None``.
         *  All values: LilyPond barline string, ``None``.

            ::

               abjad> t = Note(0, (1, 4))
               abjad> t.barline.kind = '|.'
               abjad> t.barline.kind
               '|.'

               abjad> print t.format
               c'4
               \bar "|."
      '''

         return self._kind
      def fset(self, expr):
         assert isinstance(expr, (str, types.NoneType))
         self._kind = expr
      return property(**locals( ))
