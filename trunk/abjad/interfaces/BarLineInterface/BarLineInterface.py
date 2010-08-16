#from abjad.core import _FormatContributor
##from abjad.core import _GrobHandler
#from abjad.interfaces._Interface import _Interface
#import types
#
#
##class BarLineInterface(_Interface, _GrobHandler):
#class BarLineInterface(_Interface, _FormatContributor):
#   '''Manage bar lines.
#
#      ::
#
#         abjad> t = Note(0, (1, 4))
#         abjad> t.bar_line
#         <BarLineInterface>
#
#      Override LilyPond ``BarLine`` grob.
#
#      ::
#
#         abjad> t.bar_line.color = 'red'
#         abjad> print t.format
#         \once \override BarLine #'color = #red
#         c'4'''
#   
#   def __init__(self, _client):
#
#      raise DeprecationWarning
#
#      _Interface.__init__(self, _client)
#      #_GrobHandler.__init__(self, 'BarLine')
#      _FormatContributor.__init__(self)
#      self._kind = None
#
#   ## PRIVATE ATTRIBUTES ##
#
#   @property
#   def _closing(self):
#      '''Read-only list of container-closing or after-leaf
#      format contribution strings. ::
#
#         abjad> t = Note(0, (1, 4))
#         abjad> t.bar_line.kind = '||'
#         abjad> t.bar_line.closing
#         ['\\bar "||"']
#      '''
#
#      result = [ ]
#      if self.kind is not None:
#         result.append(r'\bar "%s"' % self.kind)
#      return result
#
#   ## PUBLIC ATTRIBUTES ##
#
#   @apply
#   def kind( ):
#      def fget(self):
#         r'''Read / write LilyPond bar_line string.
#
#         *  Default value: ``None``.
#         *  All values: LilyPond bar_line string, ``None``.
#
#            ::
#
#               abjad> t = Note(0, (1, 4))
#               abjad> t.bar_line.kind = '|.'
#               abjad> t.bar_line.kind
#               '|.'
#
#               abjad> print t.format
#               c'4
#               \bar "|."
#      '''
#
#         return self._kind
#      def fset(self, expr):
#         assert isinstance(expr, (str, type(None)))
#         self._kind = expr
#      return property(**locals( ))
