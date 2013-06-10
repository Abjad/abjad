import collections
from experimental.tools.newabjadbooktools.DocumentHandler import DocumentHandler


class TextualDocumentHandler(DocumentHandler):
    """Handles text-based documents containing <abjad></abjad> tags:
    
    ::

        >>> document = '''\
        ... Let's print something:
        ...
        ... <abjad>
        ... print "hello, world!"
        ... </abjad>
        ...
        ... And let's show some music too:
        ...
        ... <abjad>
        ... note = Note("c'4"))
        ... show(Note("c'4"))
        ... </abjad>
        ...
        ... That's it!
        ... '''

    ::

        >>> handler = newabjadbooktools.TextualDocumentHandler(document)
        >>> code_blocks = handler.extract_code_blocks() 
        >>> for location, code_block in code_blocks.items():
        ...     print location, code_block.displayed_lines
        ...
        (2, 4) ('print "hello, world!"',)
        (8, 11) ('note = Note("c\'4"))', 'show(Note("c\'4"))')

    The textual document handler also determines what options, if any, were
    chosen for a given code block:

    ::

        >>> document = '''\
        ... This code block is hidden:
        ... 
        ... <abjad>[hide=True]
        ... You can't see me!
        ... </abjad>
        ...
        ... ... and this code block isn't:
        ... 
        ... <abjad>[hide=False]
        ... Here I am!
        ... </abjad>
        ... '''

    ::

        >>> handler = newabjadbooktools.TextualDocumentHandler(document)
        >>> code_blocks = handler.extract_code_blocks()
        >>> for code_block in code_blocks.values():
        ...     print code_block.hide
        ...
        True
        False

    Return textual document handler.
    """

    ### PUBLIC METHODS ###

    def extract_code_block_options(self, source):
        options = {}
        line = source.strip()
        if '[' in line and line.endswith(']'):
            option_string = line.partition('[')[2][:-1]
            for part in option_string.split(','):
                part = part.strip()
                if '=' not in part:
                    continue
                key, sep, value = part.partition('=')
                key = key.lower().strip()
                value = value.lower().strip()
                if value == 'true':
                    options[key] = True
                elif value == 'false':
                    options[key] = False
        return options

    def extract_code_blocks(self, document=None, ordered_dict=None):
        if document is None:
            document = self.document
        if ordered_dict is None:
            ordered_dict = collections.OrderedDict()

        in_block = None
        starting_line_number = None
        current_block_lines = None
        current_block_options = None

        for i, line in enumerate(document.splitlines()): 
            if line.startswith('<abjad'):
                if in_block:
                    raise Exception('Extra opening tag at line {}.'.format(i))
                    
                current_block_options = self.extract_code_block_options(line)

                if line.startswith('<abjad>'):
                    in_block = True
                    current_block_lines = []
                    starting_line_number = i
                
                elif line.startswith('<abjadextract '):
                    starting_line_number = stopping_line_number = i
                    code_address = line.partition('<abjadextract ')[-1].partition(' \>')[0]
                    module_name, sep, attr_name = code_address.rpartition('.')
                    module = importlib.import_module(module_name)
                    attr = getattr(module, attr_name)
                    displayed_lines = inspect.getsource(attr).splitlines()
                    executed_lines = 'from {} import {}'.format(
                        module_name,
                        attr_name,
                        )
                    current_block_options['executed_lines'] = executed_lines
                    source_line_range = (
                        starting_line_number,
                        stopping_line_number,
                        )
                    self.create_code_block(
                        ordered_dict,
                        displayed_lines,
                        current_block_options,
                        source_line_range,
                        )

            elif line.startswith('</abjad>'):
                if not in_block:
                    raise Exception('Extra closing tag at line {}'.format(i))

                in_block = False
                stopping_line_number = i
                source_line_range = (
                    starting_line_number,
                    stopping_line_number,
                    )
                self.create_code_block(
                    ordered_dict,
                    current_block_lines,
                    current_block_options,
                    source_line_range,
                    )

            elif in_block:
                current_block_lines.append(line)

        if in_block:
            raise Exception('Unterminated tag at EOF.')

        return ordered_dict

    def process_output_proxies(self, ordered_dict, output_directory_path):
        pass

    def rebuild_document(self, document, ordered_dict, output_directory_path):
        lines = document.splitlines()
    
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def document_type(self):
        return 'text'
