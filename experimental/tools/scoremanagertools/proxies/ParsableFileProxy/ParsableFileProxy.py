from experimental.tools.scoremanagertools.proxies.FileProxy import FileProxy


class ParsableFileProxy(FileProxy):

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        FileProxy.__init__(self, filesystem_path=filesystem_path, session=session)
        self.encoding_directives = []
        self.docstring_lines = []
        self.setup_statements = []
        self.teardown_statements = []

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def file_sections(self):
        return ()

    # TODO: make into method
    @property
    def formatted_lines(self):
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

    # TODO: make into method
    @property
    def is_parsable(self):
        return self.parse()

    ### PUBLIC METHODS ###

    def clear(self):
        for section, is_sorted, blank_line_count  in self.file_sections:
            section[:] = []

    def write_to_disk(self):
        initializer = file(self.filesystem_path, 'w')
        formatted_lines = ''.join(self.formatted_lines)
        initializer.write(formatted_lines)
