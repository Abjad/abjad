from abjad.spanner.grobhandler import _GrobHandlerSpanner
from abjad.tempo.indication import TempoIndication


class Tempo(_GrobHandlerSpanner):

   def __init__(self, music = None, indication = None):
      _GrobHandlerSpanner.__init__(self, 'MetronomeMark', music)
      self.indication = indication

   ## PUBLIC ATTRIBUTES ##

   @apply
   def indication( ):
      def fget(self):
         return self._indication
      def fset(self, arg):
         assert isinstance(arg, TempoIndication)
         self._indication = arg 
      return property(**locals( ))

   ## PUBLIC METHODS ##

   def after(self, leaf):
      result = [ ]
      result.extend(_GrobHandlerSpanner.after(self, leaf))
      if self._isMyLastLeaf(leaf):
         if self.indication:
            result.append(r'%%%% %s ends here' % self.indication.format[1:])
      return result

   def before(self, leaf):
      result = [ ]
      result.extend(_GrobHandlerSpanner.before(self, leaf))
      if self._isMyFirstLeaf(leaf):
         if self.indication:
            result.append(self.indication.format)
      return result
