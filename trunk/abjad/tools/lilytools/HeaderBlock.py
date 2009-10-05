from abjad.tools.lilytools._BlockAttributed import _BlockAttributed


class HeaderBlock(_BlockAttributed):
   r'''Model of \header block in .ly input file.

   '''

   def __init__(self):
      _BlockAttributed.__init__(self)
      self._escaped_name = r'\header'
