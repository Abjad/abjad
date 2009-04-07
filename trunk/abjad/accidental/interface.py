from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
import types


class _AccidentalInterface(_Interface, _GrobHandler):
   '''Manage LilyPond Accidental grob.
      Manage LilyPond set-accidental-style function.'''

   def __init__(self, client):
      '''Bind client and set style to None.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Accidental')
      self._style = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def opening(self):
      '''Format contribution at container opening.'''
      result = [ ]
      style = self.style
      if style:
         result.append(r"#(set-accidental-style '%s)" % style)
      return result

   @apply
   def style( ):
      '''LilyPond accidental style as string or None.'''
      def fget(self):
         return self._style
      def fset(self, arg):
         assert isinstance(arg, (str, types.NoneType))
         self._style = arg
      return property(**locals( ))
