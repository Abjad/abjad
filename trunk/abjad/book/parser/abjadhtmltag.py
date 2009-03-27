from abjad.book.parser.abjadtag import _AbjadTag

class AbjadHTMLTag(_AbjadTag):
   def __init__(self, lines):
      _AbjadTag.__init__(self, lines)
      self._target_open_tag = '<pre class="abjad">\n'
      self._target_close_tag = '</pre>\n'
      self._image_tag = '<img alt="" src="images/%s.png"/>\n'


