from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
import types


class _AccidentalInterface(_Interface, _GrobHandler):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Accidental')
      self._style = None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _opening(self):
      result = [ ]
      style = self.style
      if style:
         result.append(r"#(set-accidental-style '%s)" % style)
      return result

   ## PUBLIC ATTRIBUTES ##

   @apply
   def style( ):
      def fget(self):
         return self._style
      def fset(self, arg):
         assert isinstance(arg, (str, types.NoneType))
         self._style = arg
      return property(**locals( ))
