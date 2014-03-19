# -*- encoding: utf-8 -*-
import abc
import os
from abjad.tools import abctools


class OutputFormat(abctools.AbjadObject):
    r'''Output format.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_code_block_closing', 
        '_code_block_opening', 
        '_code_indent', 
        '_image_block', 
        '_image_format',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self, 
        code_block_opening, 
        code_block_closing, 
        code_indent, 
        image_block, 
        image_format,
        ):
        self._code_block_opening = code_block_opening
        self._code_block_closing = code_block_closing
        self._code_indent = code_indent
        self._image_block = image_block
        self._image_format = image_format

    ### SPECIAL METHODS ###

    def __call__(self, code_block, image_dict):
        r'''Calls output format with `code_block` and `image_dict`.
        '''

        reformatted = []
        for result in code_block.processed_results:
            if isinstance(result, tuple):
                reformatted.append(
                    self.code_block_opening +
                    '\n'.join([(' ' * self.code_indent) + x for x in result]) +
                    self.code_block_closing)
                for x in result:
                    if 'Error:' in x or 'Exception:' in x:
                        print '\nAbjadBookError:\n\n{}'.format(
                            '\n'.join(reformatted))
                        break

            elif isinstance(result, dict):
                file_name = result['file_name']
                image_count = result['image_count']
                image_prefix = result['image_prefix']
                page_range = result['page_range']
                scale = result['scale']
                if scale is None:
                    scale = 1.0

                if page_range is None:
                    try:
                        image_file_names = [v for k, v in sorted(
                            image_dict[image_count].items())]
                        for image_file_name in image_file_names:
                            image_file_name = image_file_name.rpartition('.')[0]
                            image_block = self.image_block.format(
                                image_file_name=image_file_name,
                                scale=scale,
                                )
                            reformatted.append(image_block)
                    except KeyError:
                        print '\nAbjadBookError:\n\n{}'.format(
                            '\n'.join(reformatted))

                else:
                    try:
                        for page_number, image_file_name in sorted(
                            image_dict[image_count].items()):
                            if page_number in page_range:
                                image_file_name = \
                                    image_file_name.rpartition('.')[0]
                                image_block = self.image_block.format(
                                    image_file_name=image_file_name,
                                    scale=scale,
                                    )
                                reformatted.append(image_block)
                            else:
                                os.remove(image_file_name)
                    except KeyError:
                        print '\nAbjadBookError:\n\n{}'.format(
                            '\n'.join(reformatted))

        return tuple(reformatted)

    ### PUBLIC PROPERTIES ###

    @property
    def code_block_closing(self):
        r'''Code block closing.
        '''
        return self._code_block_closing

    @property
    def code_block_opening(self):
        r'''Code block opening.
        '''
        return self._code_block_opening

    @property
    def code_indent(self):
        r'''Code indent.
        '''
        return self._code_indent

    @property
    def image_block(self):
        r'''Image block.
        '''
        return self._image_block

    @property
    def image_format(self):
        r'''Image format.
        '''
        return self._image_format
