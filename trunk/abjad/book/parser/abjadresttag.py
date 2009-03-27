from abjad.book.parser.abjadtag import _AbjadTag

class AbjadReSTTag(_AbjadTag):
   def __init__(self, lines):
      _AbjadTag.__init__(self, lines)
      self._target_open_tag = '::\n\n'
      self._target_close_tag = '\n'
      self._image_tag = '.. image:: images/%s.png\n'

