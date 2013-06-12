import abc
import code
import collections
import os
from abjad.tools.abctools import AbjadObject


class DocumentHandler(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, document,
        output_directory_path=None,
        ):
        self._code_blocks = collections.OrderedDict()
        self._console = code.InteractiveConsole()
        self._document = document
        self._output_directory_path = output_directory_path

    ### SPECIAL METHODS ###

    def __call__(self):
        self._code_blocks = self.extract_code_blocks(
            self.document,
            self.code_blocks,
            )
    
    ### PUBLIC METHODS ###

    def create_code_block(self,
        displayed_lines,
        options,
        source_location,
        ):
        from experimental.tools import newabjadbooktools
        code_block = newabjadbooktools.CodeBlock(
            displayed_lines,
            **options
            )
        self.code_blocks[source_location] = code_block

    def execute_code_blocks(self):
        console = code.InteractiveConsole()
        console.push('from abjad import *')
        try:
            import experimental
            console.push('from experimental import *')
        except ImportError:
            pass
        for source_location, code_block in self.code_blocks.iteritems():
            output_proxies = code_block.execute(console)

    @abc.abstractmethod
    def extract_code_block_options(self, source):
        raise NotImplemented
    
    @abc.abstractmethod
    def extract_code_blocks(self):
        raise NotImplemented

    @abc.abstractmethod
    def process_output_proxies(self):
        raise NotImplemented

    @abc.abstractmethod
    def rebuild_document(self):
        raise NotImplemented

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def asset_output_directory_name(self):
        raise NotImplemented

    @property
    def code_blocks(self):
        return self._code_blocks

    @property
    def console(self):
        return self._console

    @property
    def document(self):
        return self._document

    @abc.abstractproperty
    def image_format(self):
        raise NotImplemented

    @property
    def output_directory_path(self):
        return self._output_directory_path

