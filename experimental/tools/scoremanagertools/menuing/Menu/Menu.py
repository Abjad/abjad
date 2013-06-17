from abjad.tools import iotools
from abjad.tools import mathtools
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.core.ScoreManagerObject \
    import ScoreManagerObject
from experimental.tools.scoremanagertools.menuing.MenuSection \
    import MenuSection


class Menu(ScoreManagerObject):
    '''Menu.

    Return menu.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None, where=None):
        ScoreManagerObject.__init__(self, session=session)
        self._menu_sections = []
        hidden_section = self.make_default_hidden_section(
            session=session, where=where)
        self.menu_sections.append(hidden_section)
        self.explicit_title = None
        self.prompt_default = None
        self.should_clear_terminal = False
        self.where = where

    ### SPECIAL METHODS ###

    def __len__(self):
        return len(self.menu_sections)

    def __repr__(self):
        return '<{} ({})>'.format(self._class_name, len(self))

    ### PRIVATE METHODS ###

    def _make_tab(self, n):
        return 4 * n * ' '

    def _run(self, 
            clear=True, 
            automatically_determined_user_input=None, 
            user_input=None):
        self._io.assign_user_input(user_input=user_input)
        clear, hide_current_run = clear, False
        while True:
            self.should_clear_terminal = clear
            self.hide_current_run = hide_current_run
            clear, hide_current_run = False, True
            result = self.display_menu(
                automatically_determined_user_input=\
                automatically_determined_user_input)
            if self._session.is_complete:
                break
            elif result == 'r':
                clear, hide_current_run = True, False
            else:
                break
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def default_value(self):
        for menu_section in self.menu_sections:
            if menu_section._has_default_value:
                return menu_section._default_value

    @apply
    def explicit_title():
        def fget(self):
            return self._explicit_title
        def fset(self, explicit_title):
            assert isinstance(explicit_title, (str, type(None)))
            self._explicit_title = explicit_title
        return property(**locals())

    @property
    def first_nonhidden_return_value_in_menu(self):
        for menu_section in self.menu_sections:
            if not menu_section.is_hidden:
                if menu_section._menu_entry_return_values:
                    return menu_section._menu_entry_return_values[0]

    @property
    def has_default_valued_section(self):
        return any(x._has_default_value for x in self.menu_sections)

    @property
    def has_hidden_section(self):
        return any(x.is_hidden for x in self.menu_sections)

    @property
    def has_numbered_section(self):
        return any(x.is_numbered for x in self.menu_sections)

    @property
    def has_ranged_section(self):
        return any(x.is_ranged for x in self.menu_sections)

    @property
    def hidden_section(self):
        for menu_section in self.menu_sections:
            if menu_section.is_hidden:
                return menu_section

    @property
    def menu_lines(self):
        result = []
        result.extend(self.menu_title_lines)
        result.extend(self.section_lines)
        return result

    @property
    def menu_sections(self):
        return self._menu_sections

    @property
    def menu_title_lines(self):
        menu_lines = []
        if not self.hide_current_run:
            if self.explicit_title is not None:
                title = self.explicit_title
            else:
                title = self._session.menu_header
            menu_lines.append(stringtools.capitalize_string_start(title))
            menu_lines.append('')
        return menu_lines

    # TODO: probably remove
    @property
    def menu_entry_display_strings(self):
        result = []
        for menu_section in self.menu_sections:
            result.extend(menu_section._menu_entry_display_strings)
        return result

    # TODO: probably remove
    @property
    def menu_entry_keys(self):
        result = []
        for menu_section in self.menu_sections:
            result.extend(menu_section._menu_entry_keys)
        return result

    # TODO: make private
    @property
    def menu_entry_return_values(self):
        result = []
        for menu_section in self.menu_sections:
            result.extend(menu_section._menu_entry_return_values)
        return result

    @property
    def menu_entries(self):
        result = []
        for menu_section in self.menu_sections:
            result.extend(menu_section.menu_entries)
        return result

    @property
    def numbered_section(self):
        for menu_section in self.menu_sections:
            if menu_section.is_numbered:
                return menu_section

    @apply
    def prompt_default():
        def fget(self):
            return self._prompt_default
        def fset(self, prompt_default):
            assert isinstance(prompt_default, (str, type(None)))
            self._prompt_default = prompt_default
        return property(**locals())

    @property
    def ranged_section(self):
        for menu_section in self.menu_sections:
            if menu_section.is_ranged:
                return menu_section

    @property
    def section_lines(self):
        menu_lines = []
        for menu_section in self.menu_sections:
            section_menu_lines = menu_section.make_menu_lines()
            if not menu_section.is_hidden:
                if not self._session.nonnumbered_menu_sections_are_hidden or \
                    menu_section.is_numbered:
                    menu_lines.extend(section_menu_lines)
        if self.hide_current_run:
            menu_lines = []
        return menu_lines

    @apply
    def should_clear_terminal():
        def fget(self):
            return self._should_clear_terminal
        def fset(self, should_clear_terminal):
            assert isinstance(should_clear_terminal, bool)
            self._should_clear_terminal = should_clear_terminal
        return property(**locals())

    ### PUBLIC METHODS ###

    def change_user_input_to_directive(self, user_input):
        user_input = stringtools.strip_diacritics_from_binary_string(
            user_input)
        user_input = user_input.lower()
        if self.user_enters_nothing(user_input) and self.default_value:
            return self.enclose_in_list(self.default_value)
        elif self.user_enters_argument_range(user_input):
            return self.handle_argument_range_user_input(user_input)
        elif user_input == 'r':
            return 'r'
        else:
            for menu_entry in self.menu_entries:
                if menu_entry.display_string == 'redraw':
                    continue
                if menu_entry.matches(user_input):
                    return self.enclose_in_list(
                        menu_entry.return_value)

    def conditionally_clear_terminal(self):
        if not self._session.hide_next_redraw:
            if self.should_clear_terminal:
                if self._session.is_displayable:
                    iotools.clear_terminal()

    def display_calling_code_line_number(self):
        lines = []
        if self.where is not None:
            line = '{} file: {}'.format(self._make_tab(1), self.where[1])
            lines.append(line)
            line = '{} line: {}'.format(self._make_tab(1), self.where[2])
            lines.append(line)
            line = '{} meth: {}'.format(self._make_tab(1), self.where[3])
            lines.append(line)
            lines.append('')
            self._io.display(lines, capitalize_first_character=False)
        else:
            lines.append("where-tracking not enabled. " + 
                "Use 'tw' to toggle where-tracking.")
            lines.append('')
            self._io.display(lines)
        self._session.hide_next_redraw = True

    def display_hidden_menu_section(self):
        menu_lines = []
        for menu_section in self.menu_sections:
            if menu_section.is_hidden:
                for menu_entry in menu_section.menu_entries:
                    key = menu_entry.key
                    display_string = menu_entry.display_string
                    menu_line = self._make_tab(1) + ' '
                    menu_line += '{} ({})'.format(display_string, key)
                    menu_lines.append(menu_line)
                menu_lines.append('')
        self._io.display(menu_lines, capitalize_first_character=False)
        self._session.hide_next_redraw = True

    def display_menu(self, 
        automatically_determined_user_input=None):
        self.conditionally_clear_terminal()
        self._io.display(self.menu_lines, capitalize_first_character=False)
        if automatically_determined_user_input is not None:
            return automatically_determined_user_input
        user_response = self._io.handle_raw_input_with_default(
            '', default=self.prompt_default)
        directive = self.change_user_input_to_directive(user_response)
        directive = self.strip_default_indicators_from_strings(directive)
        self._session.hide_next_redraw = False
        directive = self.handle_hidden_menu_section_return_value(directive)
        return directive

    def enclose_in_list(self, expr):
        if self.has_ranged_section:
            return [expr]
        else:
            return expr

    def exec_statement(self):
        lines = []
        statement = self._io.handle_raw_input('XCF', include_newline=False)
        command = 'from abjad import *'
        exec(command)
        try:
            result = None
            command = 'result = {}'.format(statement)
            exec(command)
            lines.append('{!r}'.format(result))
        except:
            lines.append('expression not executable.')
        lines.append('')
        self._io.display(lines)
        self._session.hide_next_redraw = True

    def grep_directories(self):
        regex = self._io.handle_raw_input('regex')
        command = 'grep -Irn "{}" * | grep -v svn'.format(regex)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self._io.display(lines, capitalize_first_character=False)

    def handle_argument_range_user_input(self, user_input):
        if not self.has_ranged_section:
            return
        entry_numbers = \
            self.ranged_section.argument_range_string_to_numbers(
            user_input)
        if entry_numbers is None:
            return None
        entry_indices = [entry_number - 1 for entry_number in entry_numbers]
        result = []
        for i in entry_indices:
            entry = self.ranged_section._menu_entry_return_values[i]
            result.append(entry)
        return result

    def handle_hidden_menu_section_return_value(self, directive):
        if isinstance(directive, list) and len(directive) == 1:
            key = directive[0]
        else:
            key = directive
        if key in ('b', 'back'):
            self._session.is_backtracking_locally = True
        elif key == 'exec':
            self.exec_statement()
        elif key == 'grep':
            self.grep_directories()
        elif key == 'here':
            self.interactively_edit_calling_code()
        elif key == 'hidden':
            self.display_hidden_menu_section()
        elif key == 'next':
            self._session.is_navigating_to_next_score = True
            self._session.is_backtracking_to_score_manager = True
        elif key == 'prev':
            self._session.is_navigating_to_prev_score = True
            self._session.is_backtracking_to_score_manager = True
        elif key in ('q', 'quit'):
            self._session.user_specified_quit = True
#        # TODO: make this redraw!
#        elif key == 'r':
#            pass
        elif isinstance(key, str) and \
            3 <= len(key) and 'score'.startswith(key):
            if self._session.is_in_score:
                self._session.is_backtracking_to_score = True
        elif isinstance(key, str) and \
            3 <= len(key) and 'home'.startswith(key):
            self._session.is_backtracking_to_score_manager = True
        elif key == 'tm':
            self.toggle_menu()
        elif key == 'tw':
            self._session.enable_where = not self._session.enable_where
        elif key == 'where':
            self.display_calling_code_line_number()
        else:
            return directive

    def interactively_edit_calling_code(self):
        if self.where is not None:
            file_name = self.where[1]
            line_number = self.where[2]
            command = 'vim +{} {}'.format(line_number, file_name)
            os.system(command)
        else:
            lines = []
            lines.append("where-tracking not enabled. " +
                "Use 'tw' to toggle where-tracking.")
            lines.append('')
            self._io.display(lines)
            self._session.hide_next_redraw = True

    def make_default_hidden_section(self, session=None, where=None):
        from experimental.tools import scoremanagertools
        hidden_section = scoremanagertools.menuing.MenuSection(
            session=session,
            where=where,
            )
        hidden_section.return_value_attribute = 'key'
        hidden_section.is_hidden = True
        hidden_section.append(('back', 'b'))
        hidden_section.append(('exec statement', 'exec'))
        hidden_section.append(('grep directories', 'grep'))
        hidden_section.append(('edit client source', 'here'))
        hidden_section.append(('show hidden items', 'hidden'))
        hidden_section.append(('home', 'home'))
        hidden_section.append(('next score', 'next'))
        hidden_section.append(('prev score', 'prev'))
        hidden_section.append(('quit', 'q'))
        hidden_section.append(('redraw', 'r'))
        hidden_section.append(('score', 'score'))
        hidden_section.append(('toggle menu', 'tm'))
        hidden_section.append(('toggle where', 'tw'))
        hidden_section.append(('show menu client', 'where'))
        return hidden_section

    def make_section(self, 
        is_hidden=False, 
        is_numbered=False, 
        is_ranged=False, 
        menu_entries=None,
        return_value_attribute='display_string',
        ):
        from experimental import scoremanagertools
        assert not (is_numbered and self.has_numbered_section)
        assert not (is_ranged and self.has_ranged_section)
        menu_section = scoremanagertools.menuing.MenuSection(
            is_hidden=is_hidden,
            is_numbered=is_numbered,
            is_ranged=is_ranged,
            menu_entries=menu_entries,
            return_value_attribute=return_value_attribute,
            session=self._session,
            where=self.where,
            )
        self.menu_sections.append(menu_section)
        return menu_section

    def return_value_to_location_pair(self, return_value):
        for i, menu_section in enumerate(self.menu_sections):
            if return_value in menu_section._menu_entry_return_values:
                j = menu_section._menu_entry_return_values.index(return_value)
                return i, j

    def return_value_to_next_return_value_in_section(self, return_value):
        section_index, entry_index = self.return_value_to_location_pair(
            return_value)
        menu_section = self.menu_sections[section_index]
        entry_index = (entry_index + 1) % len(menu_section)
        return menu_section._menu_entry_return_values[entry_index]

    # TODO: apply default indicators at display time 
    #       so this can be completely removed
    def strip_default_indicators_from_strings(self, expr):
        if isinstance(expr, list):
            cleaned_list = []
            for element in expr:
                if element.endswith(' (default)'):
                    element = element.replace(' (default)', '')
                cleaned_list.append(element)
            return cleaned_list
        elif isinstance(expr, str):
            if expr.endswith(' (default)'):
                expr = expr.replace(' (default)', '')
            return expr
        else:
            return expr

    def toggle_menu(self):
        if self._session.nonnumbered_menu_sections_are_hidden:
            self._session.nonnumbered_menu_sections_are_hidden = False
        else:
            self._session.nonnumbered_menu_sections_are_hidden = True

    def user_enters_argument_range(self, user_input):
        if ',' in user_input:
            return True
        if '-' in user_input:
            return True
        return False

    def user_enters_nothing(self, user_input):
        return not user_input or (3 <= len(user_input) and \
            'default'.startswith(user_input))
