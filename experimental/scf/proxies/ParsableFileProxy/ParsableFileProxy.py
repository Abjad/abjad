from scf.proxies.FileProxy import FileProxy


class ParsableFileProxy(FileProxy):

    def __init__(self, path_name=None, session=None):
        FileProxy.__init__(self, path_name=path_name, session=session)
        self.encoding_directives = []
        self.docstring_lines = []
        self.setup_statements = []
        self.teardown_statements = []

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def formatted_lines(self):
        lines = []
        for section, is_sorted, blank_line_count in self.sections:
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

    # TODO: move down to ModuleProxy?
    @property
    def is_exceptionless(self):
        #self.execute_file_lines()
        try:
            self.execute_file_lines()
            return True
        except:
            return False

    @property
    def is_parsable(self):
        return self.parse()

    @property
    def is_readable(self):
        if self.is_parsable:
            if self.is_exceptionless:
                return True
        return False

    # TODO: rename to something more explicit to avoid conflict with Menu.sections
    # TODO: perhaps just ParsableFileProxy.section_tokens?
    @property
    def sections(self):
        return ()

    ### PUBLIC METHODS ###

    def clear(self):
        for section, is_sorted, blank_line_count  in self.sections:
            section[:] = []

    # TODO: move down to ModuleProxy?
    def execute_file_lines(self):
        if self.path_name:
            file_pointer = open(self.path_name, 'r')
            file_contents_string = file_pointer.read()
            file_pointer.close()
            #print file_contents_string
            exec(file_contents_string)

    # TODO: move up to FileProxy
    def write_to_disk(self):
        initializer = file(self.path_name, 'w')
        initializer.write(self.format)
