from abc import abstractmethod
from abjad.tools import abctools


class OutputFormat(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_code_block_closing', '_code_block_opening', '_image_block')

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, code_block_opening, code_block_closing, image_block):
        self._code_block_opening = code_block_opening
        self._code_block_closing = code_block_closing
        self._image_block = image_block

    ### SPECIAL METHODS ###

    def __call__(self, code_block):
        pass

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def code_block_closing(self):
        return self._code_block_closing

    @property
    def code_block_opening(self):
        return self._code_block_opening

    @property
    def image_block(self):
        return self._image_block
