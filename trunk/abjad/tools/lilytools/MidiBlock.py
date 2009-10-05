from abjad.tools.lilytools._BlockAttributed import _BlockAttributed


class MidiBlock(_BlockAttributed):
   r'''Model of \midi block in .ly input file.

   '''

   def __init__(self):
      _BlockAttributed.__init__(self)
      self._escaped_name = r'\midi'
