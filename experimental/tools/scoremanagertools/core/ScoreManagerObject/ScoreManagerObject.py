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
from experimental.tools.scoremanagertools.core.ScoreManagerConfiguration import \
    ScoreManagerConfiguration


class ScoreManagerObject(AbjadObject):

    ### CLASS ATTRIBUTES ###

    configuration = ScoreManagerConfiguration()

    ### INITIALIZER ###

    def __init__(self, session=None):
        from experimental.tools import scoremanagertools
        self._session = session or scoremanagertools.core.Session()

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _backtracking_source(self):
        return

    @property
    def _human_readable_class_name(self):
        return self.change_string_to_human_readable_string(self._class_name)

    @property
    def _spaced_class_name(self):
        return stringtools.uppercamelcase_to_space_delimited_lowercase(self._class_name)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def session(self):
        return self._session

    @property
    def source_file_name(self):
        source_file_name = inspect.getfile(type(self))
        source_file_name = source_file_name.strip('c')
        return source_file_name

    @property
    def transcript(self):
        return self.session.transcript

    @property
    def transcript_signature(self):
        return self.session.complete_transcript.signature

    @property
    def ts(self):
        return self.transcript_signature

    ### PUBLIC METHODS ###

    def asset_path_to_directory_path(self, asset_path):
        if self.is_path(asset_path):
            return asset_path
        else:
            return self.package_path_to_directory_path(asset_path)

    def asset_path_to_human_readable_name(self, asset_path):
        asset_path = os.path.normpath(asset_path)
        asset_name = os.path.basename(asset_path)
        asset_name = self.strip_file_extension_from_string(asset_name)
        return self.change_string_to_human_readable_string(asset_name)

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
            self.session.breadcrumb_cache_stack.append(self.session._breadcrumb_stack[:])
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
    def conditionally_make_empty_package(self, package_path):
        if package_path is None:
            return
        directory_path = self.package_path_to_directory_path(
            package_path)
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
            initializer_file_name = os.path.join(directory_path, '__init__.py')
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

    def directory_path_to_package_path(self, directory_path):
        if directory_path is None:
            return
        #directory_path = directory_path.rstrip(os.path.sep)
        directory_path = os.path.normpath(directory_path)
        if directory_path.endswith('.py'):
            directory_path = directory_path[:-3]
        if directory_path.startswith(self.configuration.score_manager_tools_directory_path):
            prefix_length = len(os.path.dirname(self.configuration.score_manager_tools_directory_path)) + 1
        elif directory_path.startswith(self.configuration.score_external_materials_directory_path):
            prefix_length = \
                len(os.path.dirname(self.configuration.score_external_materials_directory_path)) + 1
        elif directory_path.startswith(self.configuration.score_external_chunks_directory_path):
            prefix_length = len(os.path.dirname(self.configuration.score_external_chunks_directory_path)) + 1
        elif directory_path.startswith(self.configuration.score_external_specifiers_directory_path):
            prefix_length = \
                len(os.path.dirname(self.configuration.score_external_specifiers_directory_path)) + 1
        elif directory_path.startswith(self.configuration.scores_directory_path):
            prefix_length = len(self.configuration.scores_directory_path) + 1
        else:
            return
        package_path = directory_path[prefix_length:]
        package_path = package_path.replace(os.path.sep, '.')
        return package_path

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

    def expr_to_parent_package_name(self, expr):
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

    def get_tag_from_path(self, path, tag_name):
        tags_file_name = os.path.join(path, 'tags.py')
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

    def is_path(self, expr):
        if isinstance(expr, str):
            if os.path.sep in expr:
                return True
        return False

    def list_public_directory_paths_in_subtree(self, subtree_path):
        result = []
        for subtree_path, directory_names, file_names in os.walk(subtree_path):
            if '.svn' not in subtree_path:
                for directory_name in directory_names:
                    if '.svn' not in directory_name:
                        if directory_name[0].isalpha():
                            result.append(os.path.join(subtree_path, directory_name))
        return result

    def list_public_directory_paths_with_initializers_in_subtree(self, subtree_path):
        result = []
        for directory_path in self.list_public_directory_paths_in_subtree(subtree_path):
            if '__init__.py' in os.listdir(directory_path):
                result.append(directory_path)
        return result

    def list_score_package_names(self, head=None):
        result = []
        for name in os.listdir(self.configuration.scores_directory_path):
            if name[0].isalpha():
                if head and name == head:
                    return [name]
                elif not head:
                    result.append(name)
        return result

    def make_getter(self, where=None):
        from experimental.tools import scoremanagertools
        return scoremanagertools.menuing.UserInputGetter(where=where, session=self.session)

    def make_menu(self, is_hidden=False, is_internally_keyed=False, is_keyed=True,
        is_numbered=False, is_parenthetically_numbered=False, is_ranged=False, where=None):
        from experimental.tools import scoremanagertools
        menu = scoremanagertools.menuing.Menu(where=where, session=self.session)
        section = menu.make_section(
            is_hidden=is_hidden, is_internally_keyed=is_internally_keyed, is_keyed=is_keyed,
            is_numbered=is_numbered, is_parenthetically_numbered=is_parenthetically_numbered,
            is_ranged=is_ranged)
        return menu, section

    def module_path_to_file_path(self, module_path):
        if module_path is not None:
            file_path = self.package_path_to_directory_path(module_path) + '.py'
            return file_path

    def package_exists(self, package_path):
        assert isinstance(package_path, str)
        directory_path = self.package_path_to_directory_path(package_path)
        return os.path.exists(directory_path)

    def package_path_to_directory_path(self, package_path):
        if package_path is None:
            return
        package_path_parts = package_path.split('.')
        if package_path_parts[0] == \
            self.configuration.score_manager_tools_package_name:
            directory_parts = [self.configuration.score_manager_tools_directory_path] + \
                package_path_parts[1:]
        elif package_path_parts[0] == \
            self.configuration.score_external_materials_package_path:
            directory_parts = \
                [self.configuration.score_external_materials_directory_path] + \
                package_path_parts[1:]
        elif package_path_parts[0] == \
            self.configuration.score_external_chunks_package_path:
            directory_parts = \
                [self.configuration.score_external_chunks_directory_path] + \
                package_path_parts[1:]
        elif package_path_parts[0] == \
            self.configuration.score_external_specifiers_package_path:
            directory_parts = \
                [self.configuration.score_external_specifiers_directory_path] + \
                package_path_parts[1:]
        else:
            directory_parts = [self.configuration.scores_directory_path] + package_path_parts[:]
        directory = os.path.join(*directory_parts)
        return directory

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
            return self.session._breadcrumb_stack.pop()

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
                self.session._breadcrumb_stack.append(breadcrumb)
            else:
                self.session._breadcrumb_stack.append(self.breadcrumb)

    def remove_package_path_from_sys_modules(self, package_path):
        '''Total hack. But works.'''
        command = "if '{}' in sys.modules: del(sys.modules['{}'])".format(
            package_path, package_path)
        exec(command)

    def restore_breadcrumbs(self, cache=False):
        if cache:
            self.session._breadcrumb_stack[:] = self.session.breadcrumb_cache_stack.pop()

    def strip_file_extension_from_string(self, file_name):
        if '.' in file_name:
            return file_name[:file_name.rindex('.')]
        return file_name

    def strip_py_extension(self, string):
        if isinstance(string, str) and string.endswith('.py'):
            return string[:-3]
        else:
            return string

    def where(self):
        if self.session.enable_where:
            return inspect.stack()[1]
