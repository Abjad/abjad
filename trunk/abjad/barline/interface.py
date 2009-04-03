from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface


class _BarLineInterface(_Interface, _GrobHandler):
   
   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'BarLine')
      self._type = None

   ## PUBLIC ATTRIBUTES ##

   ## TODO: Eliminate _BarlineInterface.after infavor of .closing ##
   ##       Train _LeafFormatter to look for .closing ##

   @property
   def after(self):
      from abjad.leaf.leaf import _Leaf
      result = [ ]
      if isinstance(self._client, _Leaf):
         if self.type is not None:
            result.append(r'\bar "%s"' % self.type)
      return result

   @property
   def closing(self):
      from abjad.container.container import Container
      result = [ ]
      if isinstance(self._client, Container):
         if self.type:
            result.append(r'\bar "%s"' % self.type)
      return result

   @apply
   def type( ):
      def fget(self):
         return self._type
      def fset(self, expr):
         self._type = expr
      return property(**locals())
