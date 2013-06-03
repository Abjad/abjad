from abjad.tools.abctools.AbjadObject import AbjadObject


class ParseableFileMixin(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        AbjadObject.__init__(self)
        self.encoding_directives = []
        self.docstring_lines = []
        self.setup_statements = []
        self.teardown_statements = []

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
        return ()

    ### PUBLIC METHODS ###

    def clear(self):
        for section, is_sorted, blank_line_count  in self.file_sections:
            section[:] = []

    def write_to_disk(self):
        initializer = file(self.filesystem_path, 'w')
        formatted_lines = self._format_lines()
        formatted_lines = ''.join(formatted_lines)
        initializer.write(formatted_lines)
