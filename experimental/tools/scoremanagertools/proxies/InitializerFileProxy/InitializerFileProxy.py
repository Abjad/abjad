import collections
import os
from experimental.tools.scoremanagertools.proxies.ParsableFileProxy import ParsableFileProxy


# TODO: maybe rewire to inherit from ModuleProxy?
class InitializerFileProxy(ParsableFileProxy):

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        ParsableFileProxy.__init__(self, filesystem_path=filesystem_path, session=session)
        self.safe_import_statements = []
        self.tag_lines = []
        self.parse()

    ### CLASS VARIABLES ###

    extension = '.py'

    ### READ-ONLY PUBLIC PROPERTIES ##

    @property
    def file_sections(self):
        return (
            (self.encoding_directives, True, 0),
            (self.docstring_lines, False, 1),
            (self.setup_statements, True, 2),
            (self.safe_import_statements, True, 1),
            (self.tag_lines, False, 1),
            (self.teardown_statements, True, 0),
            )

    ### PUBLIC METHODS ###

    def has_line(self, line):
        file_reference = open(self.filesystem_path, 'r')
        for file_line in file_reference.readlines():
            if file_line == line:
                file_reference.close()
                return True
        file_reference.close()
        return False

    def interactively_restore(self, prompt=True):
        from experimental.tools import scoremanagertools
        getter = self._io.make_getter(where=self._where)
        getter.append_yes_no_string('handmade')
        result = getter._run()
        if self._session.backtrack():
            return
        if 'yes'.startswith(result.lower()):
            material_package_maker_class_name = None
            getter = self._io.make_getter(where=self._where)
            getter.append_yes_no_string('should have illustration')
            result = getter._run()
            if self._session.backtrack():
                return
            should_have_illustration = 'yes'.startswith(result.lower())
        else:
            material_package_maker_wrangler = scoremanagertools.wranglers.MaterialPackageMakerWrangler(
                session=self._session)
            with self.backtracking:
                material_package_maker_class_name = \
                    material_package_maker_wrangler.select_material_proxy_class_name_interactively(
                        clear=False, cache=True)
            if self._session.backtrack():
                return
            should_have_illustration = True
        tags = collections.OrderedDict([])
        tags['should_have_illustration'] = should_have_illustration
        tags['material_package_maker_class_name'] = material_package_maker_class_name
        self.write_stub_to_disk()
        self._io.proceed('initializer restored.', is_interactive=prompt)

    def make_tag_lines(self, tags):
        if tags:
            lines = []
            for key, value in sorted(tags.iteritems()):
                key = repr(key)
                if hasattr(value, '_get_multiline_repr'):
                    repr_lines = value._get_multiline_repr(include_tools_package=True)
                    value = '\n    '.join(repr_lines)
                    lines.append('({}, {})'.format(key, value))
                else:
                    value = getattr(value, '_tools_package_qualified_repr', repr(value))
                    lines.append('({}, {})'.format(key, value))
            lines = ',\n    '.join(lines)
            result = 'tags = collections.OrderedDict([\n    {}])'.format(lines)
        else:
            result = 'tags = collections.OrderedDict([])'
        return result

    def parse(self, initializer_file_name=None):
        is_parsable = True
        if initializer_file_name is None:
            initializer_file_name = self.filesystem_path
        if not os.path.exists(initializer_file_name):
            return
        initializer = file(initializer_file_name, 'r')
        encoding_directives = []
        docstring_lines = []
        setup_statements = []
        safe_import_statements = []
        tag_lines = []
        teardown_statements = []
        current_section = None
        for line in initializer.readlines():
            if line == '\n':
                continue
            elif line.startswith('# -*-'):
                current_section = 'encoding'
            elif line.startswith("'''"):
                current_section = 'docstring'
            elif line.startswith(('from', 'import')):
                current_section = 'setup'
            elif line.startswith('tags ='):
                current_section = 'tags'
            elif line.startswith('safe_import'):
                current_section = 'protected imports'
            elif line.startswith('rm'):
                current_section = 'teardown'
            if current_section == 'encoding':
                encoding_directives.append(line)
            elif current_section == 'docstring':
                docstring_lines.append(line)
            elif current_section == 'setup':
                setup_statements.append(line)
            elif current_section == 'tags':
                tag_lines.append(line)
            elif current_section == 'protected imports':
                safe_import_statements.append(line)
            elif current_section == 'teardown':
                teardown_statements.append(line)
            else:
                is_parsable = False
        initializer.close()
        self.encoding_directives = encoding_directives[:]
        self.docstring_lines = docstring_lines[:]
        self.setup_statements = setup_statements[:]
        self.safe_import_statements = safe_import_statements[:]
        self.tag_lines = tag_lines[:]
        self.teardown_statements = teardown_statements[:]
        return is_parsable

    def read_file(self):
        return self.parse()

    def write_stub_to_disk(self):
        self.clear()
        self.write_to_disk()

    def write_tags_to_disk(self, tags):
        self.parse()
        ordered_dict_import_statement = 'import collections\n'
        if ordered_dict_import_statement not in self.setup_statements:
            self.setup_statements.append(ordered_dict_import_statement)
        tag_lines = self.make_tag_lines(tags)
        self.tag_lines = tag_lines[:]
        self.write_to_disk()
