from abjad.spanner.positionalhandler import _PositionalGrobHandlerSpanner


class Slur(_PositionalGrobHandlerSpanner):

   def __init__(self, music = None):
      _PositionalGrobHandlerSpanner.__init__(self, 'Slur', music)
      self.position = None

   ## PRIVATE ATTRIBUTES ##

   _positions = {'neutral':r'\slurNeutral', 'up':r'\slurUp', 
                 'down':r'\slurDown', None:None}

   ## PUBLIC METHODS ##

   def right(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         result.append('(')
      if self._isMyLastLeaf(leaf):
         result.append(')')   
      return result
