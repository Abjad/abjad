from abjad.tools.abctools.AbjadObject import AbjadObject


class ParseableModuleMixin(AbjadObject):

    ### INITIALIZER ###

    def __init__(self):
        AbjadObject.__init__(self)
        self.encoding_directives = []
        self.docstring_lines = []
        self.setup_statements = []
        self.teardown_statements = []
        self.body_line = []
        self.parse()

    ### PRIVATE METHODS ###

    def _format_lines(self):
        lines = []
        for section, is_sorted, blank_line_count in self.file_sections:
            if section:
                section = section[:]
                if is_sorted:
                    section.sort()
                lines.extend(section)
                for x in range(blank_line_count):
                    lines.append('\n')
        if lines:
            lines[-1] = lines[-1].strip('\n')
        return lines

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def file_sections(self):
        return (
            (self.encoding_directives, False, 0),
            (self.docstring_lines, False, 1),
            (self.setup_statements, True, 2),
            (self.body_lines, False, 0),
            )


    ### PUBLIC METHODS ###

    def clear(self):
        for section, is_sorted, blank_line_count  in self.file_sections:
            section[:] = []

    def parse(self):
        is_parsable = True
        output_material_module = file(self.filesystem_path, 'r')
        encoding_directives = []
        docstring_lines = []
        setup_statements = []
        body_lines = []
        current_section = None
        for line in output_material_module.readlines():
            if line == '\n':
                if current_section == 'docstring':
                    current_section = 'setup'
                else:
                    current_section = 'body'
                continue
            elif line.startswith('# -*-'):
                current_section = 'encoding'
            elif line.startswith("'''"):
                current_section = 'docstring'
            elif line.startswith(('from', 'import')):
                current_section = 'setup'
            else:
                current_section = 'body'
            if current_section == 'encoding':
                encoding_directives.append(line)
            elif current_section == 'docstring':
                docstring_lines.append(line)
            elif current_section == 'setup':
                setup_statements.append(line)
            elif current_section == 'body':
                body_lines.append(line)
            else:
                is_parsable = False
        output_material_module.close()
        self.encoding_directives = encoding_directives
        self.docstring_lines = docstring_lines
        self.setup_statements = setup_statements
        self.body_lines = body_lines
        return is_parsable

    def write_to_disk(self):
        initializer = file(self.filesystem_path, 'w')
        formatted_lines = self._format_lines()
        formatted_lines = ''.join(formatted_lines)
        initializer.write(formatted_lines)
