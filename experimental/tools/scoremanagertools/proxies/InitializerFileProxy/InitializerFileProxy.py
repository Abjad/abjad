from experimental.tools.scoremanagertools.proxies.ParsableFileProxy import ParsableFileProxy
import collections
import os


class InitializerFileProxy(ParsableFileProxy):

    def __init__(self, path=None, session=None):
        ParsableFileProxy.__init__(self, path=path, session=session)
        self.safe_import_statements = []
        self.tag_lines = []
        self.parse()

    ### READ-ONLY PUBLIC PROPERTIES ##

    @property
    def extension(self):
        return '.py'

    @property
    def is_readable(self):
        return self.is_parsable

    @property
    def sections(self):
        return (
            (self.encoding_directives, True, 0),
            (self.docstring_lines, False, 1),
            (self.setup_statements, True, 2),
            (self.safe_import_statements, True, 1),
            (self.tag_lines, False, 1),
            (self.teardown_statements, True, 0),
            )

    ### PUBLIC METHODS ###

    def add_safe_import_statement(self, source_module_short_name, source_attribute_name):
        safe_import_import_statement = 'from experimental.tools.scoremanagertools.helpers import safe_import\n'
        if safe_import_import_statement not in self.setup_statements:
            self.setup_statements.append(safe_import_import_statement)
        safe_import_statement = 'safe_import(globals(), {!r}, {!r})\n'
        safe_import_statement = safe_import_statement.format(
            source_module_short_name, source_attribute_name)
        if safe_import_statement not in self.safe_import_statements:
            self.safe_import_statements.append(safe_import_statement)
        self.write_to_disk()

    def has_safe_import_statement(self, source_module_short_name, source_module_attribute_name):
        safe_import_line = 'safe_import(globals(), {!r}, {!r})\n'
        safe_import_line = safe_import_line.format(source_module_short_name, source_module_attribute_name)
        return self.has_line(safe_import_line)

    # TODO: move to TagsFileProxy
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
            result = 'tags = OrderedDict([\n    {}])'.format(lines)
        else:
            result = 'tags = OrderedDict([])'
        return result

    def parse(self, initializer_file_name=None):
        is_parsable = True
        if initializer_file_name is None:
            initializer_file_name = self.path
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

    def remove_safe_import_statement(self, source_module_short_name, source_attribute_name):
        safe_import_statement = 'safe_import(globals(), {!r}, {!r})\n'
        safe_import_statement = safe_import_statement.format(
            source_module_short_name, source_attribute_name)
        safe_import_statements = []
        for current_safe_import_statement in self.safe_import_statements:
            if not current_safe_import_statement == safe_import_statement:
                safe_import_statements.append(current_safe_import_statement)
        self.safe_import_statements[:] = safe_import_statements
        self.write_to_disk()

    # TODO: move to TagsFileProxy
    def restore_interactively(self, prompt=True):
        from experimental.tools import scoremanagertools
        getter = self.make_getter(where=self.where())
        getter.append_yes_no_string('handmade')
        result = getter.run()
        if self.backtrack():
            return
        if 'yes'.startswith(result.lower()):
            material_package_maker_class_name = None
            getter = self.make_getter(where=self.where())
            getter.append_yes_no_string('should have illustration')
            result = getter.run()
            if self.backtrack():
                return
            should_have_illustration = 'yes'.startswith(result.lower())
        else:
            material_package_maker_wrangler = scoremanagertools.wranglers.MaterialPackageMakerWrangler(session=self.session)
            self.push_backtrack()
            material_package_maker_class_name = \
                material_package_maker_wrangler.select_material_proxy_class_name_interactively(
                    clear=False, cache=True)
            self.pop_backtrack()
            if self.backtrack():
                return
            should_have_illustration = True
        tags = collections.OrderedDict([])
        tags['should_have_illustration'] = should_have_illustration
        tags['material_package_maker_class_name'] = material_package_maker_class_name
        self.write_stub_to_disk()
        self.proceed('initializer restored.', is_interactive=prompt)

    # TODO: duplicate in TagsFileProxy
    def write_stub_to_disk(self):
        self.clear()
        self.write_to_disk()

    # TODO: move to TagsFileProxy
    def write_tags_to_disk(self, tags):
        self.parse()
        ordered_dict_import_statement = 'from collections import OrderedDict\n'
        if ordered_dict_import_statement not in self.setup_statements:
            self.setup_statements.append(ordered_dict_import_statement)
        tag_lines = self.make_tag_lines(tags)
        self.tag_lines = tag_lines[:]
        self.write_to_disk()
