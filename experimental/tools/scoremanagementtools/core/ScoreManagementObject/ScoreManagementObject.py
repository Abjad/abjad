import abc
import inspect
import os
import pprint
import readline
import sys
import types
from abjad.tools import iotools
from abjad.tools import markuptools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools.scoremanagementtools.core.ScoreManagementToolsConfiguration import \
    ScoreManagementToolsConfiguration


class ScoreManagementObject(AbjadObject):

    ### CLASS ATTRIBUTES ###

    configuration = ScoreManagementToolsConfiguration()

    ### INITIALIZER ###

    def __init__(self, session=None):
        from experimental.tools import scoremanagementtools
        self._session = session or scoremanagementtools.core.Session()

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _human_readable_class_name(self):
        return self.change_string_to_human_readable_string(self._class_name)

    @property
    def _spaced_class_name(self):
        return stringtools.uppercamelcase_to_space_delimited_lowercase(self._class_name)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def backtracking_source(self):
        return

    @property
    def breadcrumb(self):
        return 'score management object'

    @property
    def breadcrumb_stack(self):
        return self.session.breadcrumb_stack

#    @property
#    def configuration(self):
#        return self._configuration

#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def editors_package_importable_name(self):
#        return self.dot_join(['scoremanagementtools', 'editors'])
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def editors_package_path_name(self):
#        return os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'editors')

    @property
    def help_item_width(self):
        return 5

#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def makers_directory_name(self):
#        return os.path.join(self.score_management_tools_package_path_name, 'makers')
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def makers_package_importable_name(self):
#        return self.dot_join([self.configuration.score_management_tools_package_importable_name, 'makers'])
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def score_external_chunks_package_importable_name(self):
#        return os.path.basename(os.environ.get('SCORE_MANAGEMENT_TOOLS_CHUNKS_PATH'))
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def score_external_chunks_package_path_name(self):
#        return os.environ.get('SCORE_MANAGEMENT_TOOLS_CHUNKS_PATH')
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def score_external_materials_package_importable_name(self):
#        return os.path.basename(os.environ.get('SCORE_MANAGEMENT_TOOLS_MATERIALS_PATH'))
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def score_external_materials_package_path_name(self):
#        return os.environ.get('SCORE_MANAGEMENT_TOOLS_MATERIALS_PATH')
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def score_external_package_importable_names(self):
#        return (
#            self.configuration.score_external_chunks_package_importable_name,
#            self.configuration.score_external_materials_package_importable_name,
#            self.configuration.score_external_specifiers_package_importable_name,
#            )
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def score_external_package_path_names(self):
#        return (
#            self.configuration.score_external_chunks_package_path_name,
#            self.configuration.score_external_materials_package_path_name,
#            self.configuration.score_external_specifiers_package_path_name,
#            )
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def score_external_specifiers_package_importable_name(self):
#        return os.path.basename(os.environ.get('SCORE_MANAGEMENT_TOOLS_SPECIFIERS_PATH'))
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def score_external_specifiers_package_path_name(self):
#        return os.environ.get('SCORE_MANAGEMENT_TOOLS_SPECIFIERS_PATH')
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def score_internal_chunks_package_importable_name_infix(self):
#        return 'mus.chunks'
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def score_internal_materials_package_importable_name_infix(self):
#        return 'mus.materials'
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def score_internal_specifiers_package_importable_name_infix(self):
#        return 'mus.specifiers'
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def score_management_tools_fully_qualified_package_name(self):
#        return 'experimental.tools.scoremanagementtools'
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def score_management_tools_package_importable_name(self):
#        return os.path.basename(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'))
#
#    # TODO: move to public property of (privately referenced) configuration class
#    @property
#    def score_management_tools_package_path_name(self):
#        return os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH')

    # TODO: move to public property of (privately referenced) configuration class
    @property
    def scores_directory_name(self):
        return os.environ.get('SCORES')

    @property
    def session(self):
        return self._session

    @property
    def source_file_name(self):
        source_file_name = inspect.getfile(type(self))
        source_file_name = source_file_name.strip('c')
        return source_file_name

    # TODO: move to public property of (privately referenced) configuration class
    @property
    def specifier_classes_package_importable_name(self):
        return self.dot_join(['scoremanagementtools', 'specifiers'])

    # TODO: move to public property of (privately referenced) configuration class
    @property
    def specifier_classes_package_path_name(self):
        return os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'specifiers')

    # TODO: move to public property of (privately referenced) configuration class
    @property
    def stylesheets_directory_name(self):
        return os.path.join(self.configuration.score_management_tools_package_path_name, 'stylesheets')

    # TODO: move to public property of (privately referenced) configuration class
    @property
    def stylesheets_package_importable_name(self):
        return self.dot_join([self.configuration.score_management_tools_package_importable_name, 'stylesheets'])

    @property
    def transcript(self):
        return self.session.transcript

    @property
    def transcript_signature(self):
        return self.session.complete_transcript.signature

    @property
    def ts(self):
        return self.transcript_signature

    # TODO: move to public property of (privately referenced) configuration class
    @property
    def user_makers_directory_name(self):
        return os.environ.get('SCORE_MANAGEMENT_TOOLS_USER_MAKERS_PATH')

    # TODO: move to public property of (privately referenced) configuration class
    @property
    def user_makers_package_importable_name(self):
        return os.environ.get('SCORE_MANAGEMENT_TOOLS_USER_MAKERS_IMPORTABLE_NAME')

    ### PUBLIC METHODS ###

    def asset_full_name_to_importable_name(self, asset_full_name):
        if self.is_path_name(asset_full_name):
            return self.path_name_to_package_importable_name(asset_full_name)
        else:
            return asset_full_name

    def asset_full_name_to_path_name(self, asset_full_name):
        if self.is_path_name(asset_full_name):
            return asset_full_name
        else:
            return self.package_importable_name_to_path_name(asset_full_name)

    def assign_user_input(self, user_input=None):
        if user_input is not None:
            if self.session.user_input:
                self.session.user_input = user_input + ' ' + self.session.user_input
            else:
                self.session.user_input = user_input

    def backtrack(self, source=None):
        return self.session.backtrack(source=source)

    def cache_breadcrumbs(self, cache=False):
        if cache:
            self.session.breadcrumb_cache_stack.append(self.session.breadcrumb_stack[:])
            self.session._breadcrumb_stack[:] = []

    def change_expr_to_menu_token(self, expr):
        return (None, self.get_one_line_menuing_summary(expr), None, expr)

    def change_string_to_human_readable_string(self, string):
        if not string:
            return string
        elif string[0].isupper():
            return stringtools.uppercamelcase_to_space_delimited_lowercase(string)
        else:
            return string.replace('_', ' ')

    def conditionally_add_terminal_newlines(self, lines):
        terminated_lines = []
        for line in lines:
            if not line.endswith('\n'):
                line = line + '\n'
            terminated_lines.append(line)
        terminated_lines = type(lines)(terminated_lines)
        return terminated_lines

    def conditionally_clear_terminal(self):
        if self.session.is_displayable:
            iotools.clear_terminal()

    # TODO: write test
    def conditionally_make_empty_package(self, package_importable_name):
        if package_importable_name is None:
            return
        package_directory_name = self.package_importable_name_to_path_name(
            package_importable_name)
        if not os.path.exists(package_directory_name):
            os.mkdir(package_directory_name)
            initializer_file_name = os.path.join(package_directory_name, '__init__.py')
            file_reference = file(initializer_file_name, 'w')
            file_reference.write('')
            file_reference.close()

    def confirm(self, prompt_string='ok?', include_chevron=False):
        getter = self.make_getter(where=self.where())
        getter.append_yes_no_string(prompt_string)
        getter.include_newlines = False
        result = getter.run(include_chevron=include_chevron)
        if self.backtrack():
            return
        return 'yes'.startswith(result.lower())

    def debug(self, value, annotation=None):
        if annotation is None:
            print 'debug: {!r}'.format(value)
        else:
            print 'debug ({}): {!r}'.format(annotation, value)

    def display(self, lines, capitalize_first_character=True):
        assert isinstance(lines, (str, list))
        if isinstance(lines, str):
            lines = [lines]
        if not self.session.hide_next_redraw:
            if capitalize_first_character:
                lines = [stringtools.capitalize_string_start(line) for line in lines]
            if lines:
                if self.session.transcribe_next_command:
                    self.session.complete_transcript.append_lines(lines)
            if self.session.is_displayable:
                for line in lines:
                    print line

    def dot_join(self, expr):
        return '.'.join(expr)

    def expr_to_parent_package_short_name(self, expr):
        module_path = expr.__module__
        parts = module_path.split('.')
        for part in reversed(parts):
            if not part == expr.__class__.__name__:
                return part

    def get_one_line_menuing_summary(self, expr):
        if isinstance(expr, (types.ClassType, abc.ABCMeta)):
            return expr.__name__
        elif getattr(expr, 'one_line_menuing_summary', None):
            return expr.one_line_menuing_summary
        elif getattr(expr, '_one_line_menuing_summary', None):
            return expr._one_line_menuing_summary
        elif isinstance(expr, type(type)):
            return expr.__name__
        elif isinstance(expr, str):
            return expr
        else:
            return repr(expr)

    def get_tag_from_path_name(self, path_name, tag_name):
        tags_file_name = os.path.join(path_name, 'tags.py')
        if os.path.isfile(tags_file_name):
            tags_file = open(tags_file_name, 'r')
            tags_file_string = tags_file.read()
            tags_file.close()
            exec(tags_file_string)
            result = locals().get('tags') or OrderedDict([])
            return result.get(tag_name)

    def get_tools_package_qualified_repr(self, expr):
        return getattr(expr, '_tools_package_qualified_repr', repr(expr))

    def handle_raw_input(self, prompt, include_chevron=True, include_newline=True, prompt_character='>',
        capitalize_prompt=True):
        if capitalize_prompt:
            prompt = stringtools.capitalize_string_start(prompt)
        if include_chevron:
            prompt = prompt + prompt_character + ' '
        else:
            prompt = prompt + ' '
        if self.session.is_displayable:
            user_response = raw_input(prompt)
            if include_newline:
                if not user_response == 'help':
                    print ''
        else:
            user_response = self.pop_next_user_response_from_user_input()
        if self.session.transcribe_next_command:
            self.session.command_history.append(user_response)
        if user_response == '.':
            last_semantic_command = self.session.last_semantic_command
            user_response = last_semantic_command
        if self.session.transcribe_next_command:
            menu_chunk = []
            menu_chunk.append('{}{}'.format(prompt, user_response))
            if include_newline:
                if not user_response == 'help':
                    menu_chunk.append('')
            self.session.complete_transcript.append_lines(menu_chunk)
        return user_response

    def handle_raw_input_with_default(self, prompt, default=None, include_chevron=True, include_newline=True,
        prompt_character='>', capitalize_prompt=True):
        if default in (None, 'None'):
            default = ''
        readline.set_startup_hook(lambda: readline.insert_text(default))
        try:
            return self.handle_raw_input(prompt, include_chevron=include_chevron,
                include_newline=include_newline, prompt_character=prompt_character,
                capitalize_prompt=capitalize_prompt)
        finally:
            readline.set_startup_hook()

    def is_module_name(self, expr):
        if isinstance(expr, str):
            if os.path.sep not in expr:
                return True
        return False

    def is_path_name(self, expr):
        if isinstance(expr, str):
            if os.path.sep in expr:
                return True
        return False

    def list_public_directory_path_names_in_subtree(self, subtree_path_name):
        result = []
        for subtree_path_name, directory_names, file_names in os.walk(subtree_path_name):
            if '.svn' not in subtree_path_name:
                for directory_name in directory_names:
                    if '.svn' not in directory_name:
                        if directory_name[0].isalpha():
                            result.append(os.path.join(subtree_path_name, directory_name))
        return result

    def list_public_package_path_names_in_subtree(self, subtree_path_name):
        result = []
        for directory_path_name in self.list_public_directory_path_names_in_subtree(subtree_path_name):
            if '__init__.py' in os.listdir(directory_path_name):
                result.append(directory_path_name)
        return result

    def list_score_package_short_names(self, head=None):
        result = []
        for name in os.listdir(self.scores_directory_name):
            if name[0].isalpha():
                if head and name == head:
                    return [name]
                elif not head:
                    result.append(name)
        return result

    def make_getter(self, where=None):
        from experimental.tools import scoremanagementtools
        return scoremanagementtools.menuing.UserInputGetter(where=where, session=self.session)

    def make_menu(self, is_hidden=False, is_internally_keyed=False, is_keyed=True,
        is_numbered=False, is_parenthetically_numbered=False, is_ranged=False, where=None):
        from experimental.tools import scoremanagementtools
        menu = scoremanagementtools.menuing.Menu(where=where, session=self.session)
        section = menu.make_section(
            is_hidden=is_hidden, is_internally_keyed=is_internally_keyed, is_keyed=is_keyed,
            is_numbered=is_numbered, is_parenthetically_numbered=is_parenthetically_numbered,
            is_ranged=is_ranged)
        return menu, section

    def module_importable_name_to_path_name(self, module_importable_name):
        if module_importable_name is not None:
            path_name = self.package_importable_name_to_path_name(module_importable_name) + '.py'
            return path_name

    def package_exists(self, package_importable_name):
        assert isinstance(package_importable_name, str)
        path_name = self.package_importable_name_to_path_name(package_importable_name)
        return os.path.exists(path_name)

    def package_importable_name_to_path_name(self, package_importable_name):
        if package_importable_name is None:
            return
        package_importable_name_parts = package_importable_name.split('.')
        if package_importable_name_parts[0] == \
            self.configuration.score_management_tools_package_importable_name:
            directory_parts = [self.configuration.score_management_tools_package_path_name] + \
                package_importable_name_parts[1:]
        elif package_importable_name_parts[0] == \
            self.configuration.score_external_materials_package_importable_name:
            directory_parts = \
                [self.configuration.score_external_materials_package_path_name] + \
                package_importable_name_parts[1:]
        elif package_importable_name_parts[0] == \
            self.configuration.score_external_chunks_package_importable_name:
            directory_parts = \
                [self.configuration.score_external_chunks_package_path_name] + \
                package_importable_name_parts[1:]
        elif package_importable_name_parts[0] == \
            self.configuration.score_external_specifiers_package_importable_name:
            directory_parts = \
                [self.configuration.score_external_specifiers_package_path_name] + \
                package_importable_name_parts[1:]
        else:
            directory_parts = [self.scores_directory_name] + package_importable_name_parts[:]
        directory = os.path.join(*directory_parts)
        return directory

    def path_name_to_human_readable_base_name(self, path_name):
        path_name = path_name.rstrip(os.path.sep)
        base_name = os.path.basename(path_name)
        base_name = self.strip_extension_from_base_name(base_name)
        return self.change_string_to_human_readable_string(base_name)

    def path_name_to_package_importable_name(self, path_name):
        if path_name is None:
            return
        path_name = path_name.rstrip(os.path.sep)
        if path_name.endswith('.py'):
            path_name = path_name[:-3]
        if path_name.startswith(self.configuration.score_management_tools_package_path_name):
            prefix_length = len(os.path.dirname(self.configuration.score_management_tools_package_path_name)) + 1
        elif path_name.startswith(self.configuration.score_external_materials_package_path_name):
            prefix_length = len(os.path.dirname(self.configuration.score_external_materials_package_path_name)) + 1
        elif path_name.startswith(self.configuration.score_external_chunks_package_path_name):
            prefix_length = len(os.path.dirname(self.configuration.score_external_chunks_package_path_name)) + 1
        elif path_name.startswith(self.configuration.score_external_specifiers_package_path_name):
            prefix_length = len(os.path.dirname(self.configuration.score_external_specifiers_package_path_name)) + 1
        elif path_name.startswith(self.scores_directory_name):
            prefix_length = len(self.scores_directory_name) + 1
        else:
            return
        package_importable_name = path_name[prefix_length:]
        package_importable_name = package_importable_name.replace(os.path.sep, '.')
        return package_importable_name

    def pluralize_string(self, string):
        if string.endswith('y'):
            return string[:-1] + 'ies'
        elif string.endswith(('s', 'sh', 'x', 'z')):
            return string + 'es'
        else:
            return string + 's'

    def pop_backtrack(self):
        return self.session.backtracking_stack.pop()

    def pop_breadcrumb(self, rollback=True):
        if rollback:
            return self.breadcrumb_stack.pop()

    def pop_next_user_response_from_user_input(self):
        self.session.last_command_was_composite = False
        if self.session.user_input is None:
            return None
        elif self.session.user_input == '':
            self.session.user_input = None
            return None
        elif '\n' in self.session.user_input:
            raise ValueError('no longer implemented.')
        elif self.session.user_input.startswith('{{'):
            index = self.session.user_input.find('}}')
            user_response = self.session.user_input[2:index]
            user_input = self.session.user_input[index+2:].strip()
            self.session.last_command_was_composite = True
        else:
            user_input = self.session.user_input.split(' ')
            first_parts, rest_parts = [], []
            for i, part in enumerate(user_input):
                if not part.endswith((',', '-')):
                    break
            first_parts = user_input[:i+1]
            rest_parts = user_input[i+1:]
            user_response = ' '.join(first_parts)
            user_input = ' '.join(rest_parts)
        user_response = user_response.replace('~', ' ')
        self.session.user_input = user_input
        return user_response

    def print_not_yet_implemented(self):
        self.display(['not yet implemented', ''])
        self.proceed()

    def proceed(self, lines=None, is_interactive=True):
        assert isinstance(lines, (tuple, list, str, type(None)))
        if not is_interactive:
            return
        if isinstance(lines, str):
            lines = [lines]
        elif lines is None:
            lines = []
        if lines:
            lines.append('')
            self.display(lines)
        self.handle_raw_input('press return to continue.', include_chevron=False)
        self.conditionally_clear_terminal()

    def pt(self):
        pprint.pprint(self.transcript)
        print len(self.transcript)

    def ptc(self):
        self.session.complete_transcript.ptc()

    def push_backtrack(self):
        if self.session.backtracking_stack:
            last_number = self.session.backtracking_stack[-1]
            self.session.backtracking_stack.append(last_number + 1)
        else:
            self.session.backtracking_stack.append(0)

    def push_breadcrumb(self, breadcrumb=None, rollback=True):
        if rollback:
            if breadcrumb is not None:
                self.breadcrumb_stack.append(breadcrumb)
            else:
                self.breadcrumb_stack.append(self.breadcrumb)

    def remove_package_importable_name_from_sys_modules(self, package_importable_name):
        '''Total hack. But works.'''
        command = "if '{}' in sys.modules: del(sys.modules['{}'])".format(
            package_importable_name, package_importable_name)
        exec(command)

    def restore_breadcrumbs(self, cache=False):
        if cache:
            self.session._breadcrumb_stack[:] = self.session.breadcrumb_cache_stack.pop()

    def strip_extension_from_base_name(self, base_name):
        if '.' in base_name:
            return base_name[:base_name.rindex('.')]
        return base_name

    def strip_py_extension(self, string):
        if isinstance(string, str) and string.endswith('.py'):
            return string[:-3]
        else:
            return string

    def where(self):
        if self.session.enable_where:
            return inspect.stack()[1]
