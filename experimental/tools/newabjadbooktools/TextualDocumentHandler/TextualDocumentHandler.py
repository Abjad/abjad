import collections
import os
from experimental.tools.newabjadbooktools.DocumentHandler \
    import DocumentHandler


class TextualDocumentHandler(DocumentHandler):
    """Abstract base class for handlers of text-based documents containing
    <abjad></abjad> tags:
    
    ::

        >>> document = '''Let's print something:
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

        >>> document_handler = newabjadbooktools.ReSTDocumentHandler(
        ...     document,
        ...     document_file_name='foo.rst',
        ...     output_directory_path='.',
        ...     )
        >>> source_to_code_block_mapping = \
        ...     document_handler.extract_code_blocks() 
        >>> for location, code_block in source_to_code_block_mapping.items():
        ...     print location, code_block.displayed_lines
        ...
        (2, 4) ('print "hello, world!"',)
        (8, 11) ('note = Note("c\'4"))', 'show(Note("c\'4"))')

    The textual document handler also determines what options, if any, were
    chosen for a given code block:

    ::

        >>> document = '''This code block is hidden:
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

        >>> document_handler = newabjadbooktools.ReSTDocumentHandler(
        ...     document,
        ...     document_file_name='baz.rst',
        ...     output_directory_path='.',
        ...     )
        >>> source_to_code_block_mapping = \
        ...     document_handler.extract_code_blocks()
        >>> for code_block in source_to_code_block_mapping.values():
        ...     print code_block.hide
        ...
        True
        False

    Return textual document handler.
    """

    ### INITIALIZER ###

    def __init__(self,
        document,
        document_file_name=None,
        output_directory_path=None,
        ):
        DocumentHandler.__init__(self,
            document,
            output_directory_path=output_directory_path,
            ) 
        self._document_file_name=document_file_name

    ### PUBLIC PROPERTIES ###

    @property
    def asset_output_directory_name(self):
        '''Textual document handler asset output directory name:

        ::

            >>> document_handler.asset_output_directory_name
            'assets'
            
        Return string.
        '''
        return 'assets'

    @property
    def document_file_name(self):
        '''Textual document handler document file name:

        ::

            >>> document_handler.document_file_name
            'baz.rst'

        Return string.
        '''
        return self._document_file_name

    ### PUBLIC METHODS ###

    def extract_code_block_options(self, source_line):
        '''Extract code block options:

        ::

            >>> source_line = '<abjad>'
            >>> document_handler.extract_code_block_options(source_line)
            {}

        ::

            >>> source_line = '<abjad>[hide=True]'
            >>> document_handler.extract_code_block_options(source_line)
            {'hide': True}
            
        ::

            >>> source_line = '<abjad>[strip_prompt=true, hide=false]'
            >>> document_handler.extract_code_block_options(source_line)
            {'hide': False, 'strip_prompt': True}

        Return dictionary.
        '''
        options = {}
        line = source_line.strip()
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

    def extract_code_blocks(self):
        r"""Extract code blocks:

        ::

            >>> document = '''Let's print something:
            ...
            ... <abjad>
            ... print "hello, world!"
            ... </abjad>
            ...
            ... This is just a simple Python string:
            ...
            ... <abjad>
            ... just_a_string = \'\'\'
            ... show(Nothing!)
            ... \'\'\'
            ... </abjad>
            ...
            ... And let's show some music too:
            ...
            ... <abjad>
            ... show(Note("c'4"))
            ... </abjad>
            ...
            ... That's it!
            ... '''

        ::

            >>> document_handler = newabjadbooktools.ReSTDocumentHandler(
            ...     document,
            ...     document_file_name='foo.rst',
            ...     output_directory_path='.',
            ...     )
            >>> source_to_code_block_mapping = \
            ...     document_handler.extract_code_blocks() 

        ::

            >>> for location in source_to_code_block_mapping.iterkeys():
            ...     print location
            ...
            (2, 4)
            (8, 12)
            (16, 18)

        ::

            >>> for code_block in source_to_code_block_mapping.itervalues():
            ...     print code_block.storage_format
            ...
            newabjadbooktools.CodeBlock(
                ('print "hello, world!"',),
                allow_exceptions=False,
                hide=False,
                strip_prompt=False
                )
            newabjadbooktools.CodeBlock(
                ("just_a_string = '''", 'show(Nothing!)', "'''"),
                allow_exceptions=False,
                hide=False,
                strip_prompt=False
                )
            newabjadbooktools.CodeBlock(
                ('show(Note("c\'4"))',),
                allow_exceptions=False,
                hide=False,
                strip_prompt=False
                )

        Return mapping.
        """
        in_block = False
        starting_line_number = None
        current_block_lines = None
        current_block_options = None

        for i, line in enumerate(self.document.splitlines()): 
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
                    code_address = line.partition(
                        '<abjadextract ')[-1].partition(' \>')[0]
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
                    current_block_lines,
                    current_block_options,
                    source_line_range,
                    )

            elif in_block:
                current_block_lines.append(line)

        if in_block:
            raise Exception('Unterminated tag at EOF.')

        return self.source_to_code_block_mapping

    def rebuild_document(self):
        old_lines = self.document.splitlines()
        new_lines = []

        def format_output_proxies(output_proxies):
            result = []
            for i, output_proxy in enumerate(output_proxies):
                result.extend(
                    output_proxy.generate_document_representation(self))
                if i < (len(output_proxies) - 1):
                    result.append('')
            return result

        previous_last_line_number = 0
        for line_range, code_block in sorted(
            self.source_to_code_block_mapping.items()):

            first_line_number = line_range[0]
            last_line_number = line_range[1] + 1
            new_lines.extend(
                old_lines[previous_last_line_number:first_line_number])
            previous_last_line_number = last_line_number
            new_lines.extend(format_output_proxies(code_block.output_proxies))
            if last_line_number < len(old_lines):
                if old_lines[last_line_number] and \
                    not old_lines[last_line_number][0].isspace():
                    new_lines.append('')

        if previous_last_line_number < len(old_lines):
            new_lines.extend(
                old_lines[previous_last_line_number:len(old_lines)])

        return new_lines
    
    def write_rebuilt_document_to_disk(self):
        assert isinstance(self.document_file_name, str) and \
            self.document_file_name
        assert os.path.exists(self.output_directory_path)
        rebuilt_document = '\n'.join(self.rebuild_document())
        document_file_path = os.path.join(
            self.output_directory_path,
            self.document_file_name,
            )
        previous_document = None
        if os.path.exists(document_file_path):
            with open(document_file_path, 'r') as f:
                previous_document = f.read()
        if previous_document != rebuilt_document:
            with open(document_file_path, 'w') as f:
                f.write(rebuilt_document)
         
