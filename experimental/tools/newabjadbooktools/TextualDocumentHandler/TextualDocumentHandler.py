from experimental.tools.newabjadbooktools.DocumentHandler import DocumentHandler


class TextualDocumentHandler(DocumentHandler):
    '''Handles text-based documents containing <abjad></abjad> tags.'''

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

    def extract_code_blocks(self, document, ordered_dict):
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
                block.append(line)

        if in_block:
            raise Exception('Unterminated tag at EOF.')

        return ordered_dict
