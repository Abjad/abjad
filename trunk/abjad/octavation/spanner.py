#from abjad.spanner.spanner import Spanner
from abjad.spanner.grobhandler import _GrobHandlerSpanner


#class Octavation(Spanner):
class Octavation(_GrobHandlerSpanner):

   def __init__(self, music = None, start = None, stop = 0):
      #Spanner.__init__(self, music)
      _GrobHandlerSpanner.__init__(self, 'OttavaBracket', music)
      self.start = start
      self.stop = stop

   ### PRIVATE METHODS ###

   ### TODO - test the shit out of the middleCPosition stuff, esp
   ###        clef changes in the middle of an octavation spanner

   def _after(self, leaf):
      result = [ ]
      result.extend(_GrobHandlerSpanner._after(self, leaf))
      if self._isMyLastLeaf(leaf):
         result.append(r'#(set-octavation %s)' % self.stop)
         #position = leaf.clef.middleCPosition - 7 * self.stop
         position = leaf.clef.effective.middleCPosition - 7 * self.stop
         result.append(r'\set Staff.middleCPosition = #%s' % position)
      return result

   def _before(self, leaf):
      result = [ ]
      result.extend(_GrobHandlerSpanner._before(self, leaf))
      if self._isMyFirstLeaf(leaf):
         result.append(r'#(set-octavation %s)' % self.start)
      if self._isMyFirstLeaf(leaf) or leaf.clef.change:
         #position = leaf.clef.middleCPosition - 7 * self.start
         position = leaf.clef.effective.middleCPosition - 7 * self.start
         result.append(r'\set Staff.middleCPosition = #%s' % position)
      return result

   ### PUBLIC ATTRIBUTES ###

   @apply
   def start( ):
      def fget(self):
         return self._start
      def fset(self, arg):
         self._start = arg
      return property(**locals( ))

   @apply
   def stop( ):
      def fget(self):
         return self._stop
      def fset(self, arg):
         self._stop = arg
      return property(**locals( ))
