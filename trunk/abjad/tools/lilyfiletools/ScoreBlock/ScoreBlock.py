from abjad.tools.lilyfiletools._BlockNonattributed import _BlockNonattributed


class ScoreBlock(_BlockNonattributed):
   r'''Abjad model of the LilyPond \score block.'''

   def __init__(self):
      _BlockNonattributed.__init__(self)
      self._escaped_name = r'\score'
