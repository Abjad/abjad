from abjad.pianopedal.format import _PianoPedalSpannerFormatInterface
from abjad.spanner.spanner import Spanner


class PianoPedal(Spanner):

   def __init__(self, music = None):
      Spanner.__init__(self, music)
      self._format = _PianoPedalSpannerFormatInterface(self)
      self.type = 'sustain'
      self.style = 'mixed'

   ## PRIVATE ATTRIBUTES ##
   
   _styles = ['text', 'bracket', 'mixed']
         
   _types = {'sustain': (r'\sustainOn', r'\sustainOff'), 
              'sostenuto':(r'\sostenutoOn', r'\sostenutoOff'), 
              'corda': (r'\unaCorda', r'\treCorde')}

   ## PUBLIC ATTRIBUTES ##

   @apply
   def style( ):
      def fget(self):
         return self._style
      def fset(self, arg):
         if not arg in self._styles:
            raise ValueError("Style must be in %s" % self._styles)
         self._style = arg
      return property(**locals( ))         

   ## TODO: Rename PianoPedal 'type' to non-reserve word. ##

   @apply
   def type( ):
      def fget(self):
         return self._type
      def fset(self, arg):
         if not arg in self._types.keys( ):
            raise ValueError("Type must be in %s" % self._types.keys( ))
         self._type = arg
      return property(**locals( ))         
