from abjad.tools.lilytools._BlockNonattributed import _BlockNonattributed


class BookBlock(_BlockNonattributed):
   r'''Abjad model of the LilyPond \book block.'''

   def __init__(self):
      _BlockNonattributed.__init__(self)
      self._escaped_name = r'\book'
