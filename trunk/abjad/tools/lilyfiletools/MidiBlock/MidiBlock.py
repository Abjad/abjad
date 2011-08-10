from abjad.tools.lilyfiletools._BlockAttributed import _BlockAttributed


class MidiBlock(_BlockAttributed):
   r'''.. versionadded:: 2.0
   
   Abjad model of LilyPond input file midi block.
   '''

   def __init__(self):
      _BlockAttributed.__init__(self)
      self._escaped_name = r'\midi'
      self.is_formatted_when_empty = True
