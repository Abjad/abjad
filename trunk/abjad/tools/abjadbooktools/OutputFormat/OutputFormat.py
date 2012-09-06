import abc
from abjad.tools import abctools


class OutputFormat(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_code_block_closing', '_code_block_opening', '_code_indent', '_image_block', '_image_format')

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, code_block_opening, code_block_closing, code_indent, image_block, image_format):
        self._code_block_opening = code_block_opening
        self._code_block_closing = code_block_closing
        self._code_indent = code_indent
        self._image_block = image_block
        self._image_format = image_format

    ### SPECIAL METHODS ###

    def __call__(self, code_block):
        reformatted = []
        for result in code_block.processed_results:
            if isinstance(result, tuple):
                reformatted.append(
                    self.code_block_opening +
                    '\n'.join([(' ' * self.code_indent) + x for x in result]) +
                    self.code_block_closing)
            elif isinstance(result, str):
                reformatted.append(self.image_block.format(result))
        return tuple(reformatted)

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def code_block_closing(self):
        return self._code_block_closing

    @property
    def code_block_opening(self):
        return self._code_block_opening

    @property
    def code_indent(self):
        return self._code_indent

    @property
    def image_block(self):
        return self._image_block

    @property
    def image_format(self):
        return self._image_format
