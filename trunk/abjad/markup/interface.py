from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface


### TODO: should this be naem _TextScriptInterface instead?

### TODO: or should we remove grob-handling here
###       and impelement a separate _TextScriptInterface elsewhere?

class _MarkupInterface(_Interface, _GrobHandler):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TextScript')
      self._down = [ ]
      self._up = [ ]

   ### PRIVATE ATTRIBUTES ###

   @property
   def _right(self):
      result = [ ]
      for markup in self.up:
         result.append('^ \markup { %s }' % str(markup))
      for markup in self.down:
         result.append('_ \markup { %s }' % str(markup))
      return result

   ### PUBLIC ATTRIBUTES ###

   @apply
   def down( ):
      def fget(self):
         return self._down
      return property(**locals( ))

   @apply
   def up( ):
      def fget(self):
         return self._up
      return property(**locals( ))
