from abjad.tools.lilytools._BlockAttributed import _BlockAttributed


class PaperBlock(_BlockAttributed):
   r'''Model of \paper block in .ly input file.

   '''

   def __init__(self):
      _BlockAttributed.__init__(self)
      self._escaped_name = r'\paper'
