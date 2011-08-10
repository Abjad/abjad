from abjad.tools.lilyfiletools._BlockNonattributed import _BlockNonattributed


class BookBlock(_BlockNonattributed):
   r'''.. versionadded:: 2.0

   Abjad model of LilyPond input file book block.
   '''

   def __init__(self):
      _BlockNonattributed.__init__(self)
      self._escaped_name = r'\book'
