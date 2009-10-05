from abjad.tools.lilytools._BlockAttributed import _BlockAttributed


class LayoutBlock(_BlockAttributed):
   r'''Model of \layout block in .ly input file.

   '''

   def __init__(self):
      _BlockAttributed.__init__(self)
      self._escaped_name = r'\layout'
