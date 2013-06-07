import abc
import code
from abjad.tools.abctools import AbjadObject


class DocumentHandler(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, document):
        self._code_blocks = collections.OrderedDict()
        self._console = code.InteractiveConsole()
        self._document = document

    ### SPECIAL METHODS ###

    def __call__(self):
        self._code_blocks = self.extract_code_blocks(
            self.document,
            self.code_blocks,
            )
    
    ### PUBLIC METHODS ###

    def create_code_block(self,
        ordered_dict,
        displayed_lines,
        options,
        source_location,
        ):
        code_block = newabjadbooktools.CodeBlock(
            displayed_lines,
            **options
            )
        ordered_dict[source_location] = code_block

    @abc.abstractmethod
    def extract_code_block_options(self, source):
        raise NotImplemented
    
    @abc.abstractmethod
    def extract_code_blocks(self, document, ordered_dict):
        raise NotImplemented
