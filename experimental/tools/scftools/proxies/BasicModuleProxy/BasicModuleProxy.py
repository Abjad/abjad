from experimental.tools.scftools.proxies.MaterialModuleProxy import MaterialModuleProxy


class BasicModuleProxy(MaterialModuleProxy):

    def __init__(self, module_importable_name, session=None):
        MaterialModuleProxy.__init__(self, module_importable_name, session=session)
        self.body_lines = []
        self.parse()

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def sections(self):
        return (
            (self.encoding_directives, False, 0),
            (self.docstring_lines, False, 1),
            (self.setup_statements, True, 2),
            (self.body_lines, False, 0),
            )

    ### PUBLIC METHODS ###

    def parse(self):
        is_parsable = True
        output_material_module = file(self.path_name, 'r')
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
