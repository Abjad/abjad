import abc
import os
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

    def __call__(self, code_block, image_dict):

        reformatted = []
        for result in code_block.processed_results:
            if isinstance(result, tuple):
                reformatted.append(
                    self.code_block_opening +
                    '\n'.join([(' ' * self.code_indent) + x for x in result]) +
                    self.code_block_closing)

            elif isinstance(result, dict):
                file_name = result['file_name']
                image_count = result['image_count']
                image_prefix = result['image_prefix']
                page_range = result['page_range']

                if page_range is None:
                    image_file_names = [v for k, v in sorted(image_dict[image_count].items())]
                    for image_file_name in image_file_names:
                        image_file_name = image_file_name.rpartition('.')[0]
                        reformatted.append(self.image_block.format(image_file_name))

                else:
                    for page_number, image_file_name in sorted(image_dict[image_count].items()):
                        if page_number in page_range:
                            image_file_name = image_file_name.rpartition('.')[0]
                            reformatted.append(self.image_block.format(image_file_name))
                        else:
                            os.remove(image_file_name)
                            
        return tuple(reformatted)

    ### READ-ONLY PUBLIC PROPERTIES ###

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
