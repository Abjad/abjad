from abjad.book.parser._AbjadTag import _AbjadTag


class _AbjadHTMLTag(_AbjadTag):

    def __init__(self, lines, skip_rendering):
        _AbjadTag.__init__(self, lines, skip_rendering)
        self._target_open_tag = '<pre class="abjad">\n'
        self._target_close_tag = '</pre>\n'
        self._image_tag = '<img alt="" src="images/%s.png"/>\n'
