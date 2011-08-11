from abjad.book.parser._AbjadTag import _AbjadTag


class _AbjadReSTTag(_AbjadTag):

    def __init__(self, lines, skip_rendering):
        _AbjadTag.__init__(self, lines, skip_rendering)
        self._target_open_tag = '::\n\n'
        self._target_close_tag = '\n'
        self._image_tag = '.. image:: images/%s.png\n'
