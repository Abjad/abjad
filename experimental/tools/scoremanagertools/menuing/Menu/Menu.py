import os
from abjad.tools import iotools
from abjad.tools import mathtools
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.core.ScoreManagerObject \
    import ScoreManagerObject
from experimental.tools.scoremanagertools.menuing.MenuSection \
    import MenuSection


class Menu(ScoreManagerObject):
    '''Menu:

    ::

        >>> score_manager = scoremanagertools.scoremanager.ScoreManager()
        >>> menu = score_manager._make_svn_menu()
        >>> menu
        <Menu (2)>

    Return menu.
    '''

    ### INITIALIZER ###

    def __init__(self, 
        session=None, 
        where=None,
        should_clear_terminal=False,
        title=None,
        ):
        ScoreManagerObject.__init__(self, session=session)
        hidden_section = self._make_default_hidden_section()
        self._menu_sections = [hidden_section]
        self.should_clear_terminal = should_clear_terminal
        self.title = title
        self.where = where

    ### SPECIAL METHODS ###

    def __len__(self):
        '''Number of menu sections in menu.

        Return nonnegative integer.
        '''
        return len(self.menu_sections)

    def __repr__(self):
        '''Interpreter representation of menu.

        Return string.
        '''
        return '<{} ({})>'.format(self._class_name, len(self))

    ### PRIVATE PROPERTIES ###

    @property
    def _first_nonhidden_return_value_in_menu(self):
        for menu_section in self.menu_sections:
            if not menu_section.is_hidden:
                if menu_section._menu_entry_return_values:
                    return menu_section._menu_entry_return_values[0]

    @property
    def _has_numbered_section(self):
        return any(x.is_numbered for x in self.menu_sections)

    @property
    def _has_ranged_section(self):
        return any(x.is_ranged for x in self.menu_sections)

    ### PRIVATE METHODS ###

    def _change_user_input_to_directive(self, user_input):
        user_input = stringtools.strip_diacritics_from_binary_string(
            user_input)
        user_input = user_input.lower()
        if self._user_enters_nothing(user_input):
            default_value = None
            for menu_section in self.menu_sections:
                if menu_section._has_default_value:
                    default_value = menu_section._default_value
            if default_value is not None:
                return self._enclose_in_list(default_value)
        elif self._user_enters_argument_range(user_input):
            return self._handle_argument_range_user_input(user_input)
        elif user_input == 'r':
            return 'r'
        else:
            for menu_section in self.menu_sections:
                for menu_entry in menu_section.menu_entries:
                    if menu_entry.display_string == 'redraw':
                        continue
                    if menu_entry.matches(user_input):
                        return self._enclose_in_list(
                            menu_entry.return_value)

    def _clear_terminal(self):
        if not self._session.hide_next_redraw:
            if self.should_clear_terminal:
                if self._session.is_displayable:
                    iotools.clear_terminal()

    def _display(self, 
        automatically_determined_user_input=None):
        self._clear_terminal()
        self._io.display(self._make_menu_lines(), 
            capitalize_first_character=False)
        if automatically_determined_user_input is not None:
            return automatically_determined_user_input
        user_input = self._io.handle_raw_input_with_default('')
        directive = self._change_user_input_to_directive(user_input)
        directive = self._strip_default_indicators_from_strings(directive)
        self._session.hide_next_redraw = False
        directive = self._handle_hidden_menu_section_return_value(directive)
        return directive

    def _enclose_in_list(self, expr):
        if self._has_ranged_section:
            return [expr]
        else:
            return expr

    def _handle_argument_range_user_input(self, user_input):
        if not self._has_ranged_section:
            return
        for menu_section in self.menu_sections:
            if menu_section.is_ranged:
                ranged_section = menu_section
        entry_numbers = ranged_section._argument_range_string_to_numbers(
            user_input)
        if not entry_numbers:
            return
        entry_indices = [entry_number - 1 for entry_number in entry_numbers]
        result = []
        for i in entry_indices:
            entry = ranged_section._menu_entry_return_values[i]
            result.append(entry)
        return result

    def _handle_hidden_menu_section_return_value(self, directive):
        if isinstance(directive, list) and len(directive) == 1:
            key = directive[0]
        else:
            key = directive
        if key in ('b', 'back'):
            self._session.is_backtracking_locally = True
        elif key == 'cmds':
            self.toggle_menu_commands()
        elif key == 'exec':
            self.interactively_exec_statement()
        elif key == 'grep':
            self.interactively_grep_directories()
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
        elif key == 'tw':
            self._session.enable_where = not self._session.enable_where
        elif key == 'where':
            self.display_calling_code_line_number()
        else:
            return directive

    def _make_default_hidden_section(self):
        from experimental.tools import scoremanagertools
        hidden_section = scoremanagertools.menuing.MenuSection()
        hidden_section.return_value_attribute = 'key'
        hidden_section.is_hidden = True
        hidden_section.append(('back', 'b'))
        hidden_section.append(('exec statement', 'exec'))
        hidden_section.append(('grep directories', 'grep'))
        hidden_section.append(('edit client source', 'here'))
        hidden_section.append(('display hidden menu section', 'hidden'))
        hidden_section.append(('home', 'home'))
        hidden_section.append(('next score', 'next'))
        hidden_section.append(('prev score', 'prev'))
        hidden_section.append(('quit', 'q'))
        hidden_section.append(('redraw', 'r'))
        hidden_section.append(('current score', 'score'))
        hidden_section.append(('show/hide commands', 'cmds'))
        hidden_section.append(('toggle where', 'tw'))
        hidden_section.append(('display calling code line number', 'where'))
        return hidden_section

    def _make_menu_lines(self):
        result = []
        result.extend(self._make_title_lines())
        result.extend(self._make_section_lines())
        return result

    def _make_section_lines(self):
        menu_lines = []
        for menu_section in self.menu_sections:
            section_menu_lines = menu_section._make_menu_lines()
            if not menu_section.is_hidden:
                if not self._session.nonnumbered_menu_sections_are_hidden or \
                    menu_section.is_numbered:
                    menu_lines.extend(section_menu_lines)
        if self.hide_current_run:
            menu_lines = []
        return menu_lines

    def _make_tab(self, n):
        return 4 * n * ' '

    def _make_title_lines(self):
        result = []
        if not self.hide_current_run:
            if self.title is not None:
                title = self.title
            else:
                title = self._session.menu_header
            result.append(stringtools.capitalize_string_start(title))
            result.append('')
        return result

    def _return_value_to_location_pair(self, return_value):
        for i, menu_section in enumerate(self.menu_sections):
            if return_value in menu_section._menu_entry_return_values:
                j = menu_section._menu_entry_return_values.index(return_value)
                return i, j

    def _return_value_to_next_return_value_in_section(self, return_value):
        section_index, entry_index = self._return_value_to_location_pair(
            return_value)
        menu_section = self.menu_sections[section_index]
        entry_index = (entry_index + 1) % len(menu_section)
        return menu_section._menu_entry_return_values[entry_index]

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
            result = self._display(
                automatically_determined_user_input=\
                automatically_determined_user_input)
            if self._session.is_complete:
                break
            elif result == 'r':
                clear, hide_current_run = True, False
            else:
                break
        return result

    # TODO: apply default indicators at display time 
    #       so this can be completely removed
    def _strip_default_indicators_from_strings(self, expr):
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

    def _user_enters_argument_range(self, user_input):
        if ',' in user_input:
            return True
        if '-' in user_input:
            return True
        return False

    def _user_enters_nothing(self, user_input):
        return not user_input or (3 <= len(user_input) and \
            'default'.startswith(user_input))

    ### PUBLIC PROPERTIES ###

    @property
    def hidden_section(self):
        '''Menu hidden section:

        ::

                >>> menu.hidden_section
                <MenuSection (14)>

        ::

                >>> for menu_entry in menu.hidden_section.menu_entries:
                ...     menu_entry
                <MenuEntry: 'back'>
                <MenuEntry: 'exec statement'>
                <MenuEntry: 'grep directories'>
                <MenuEntry: 'edit client source'>
                <MenuEntry: 'display hidden menu section'>
                <MenuEntry: 'home'>
                <MenuEntry: 'next score'>
                <MenuEntry: 'prev score'>
                <MenuEntry: 'quit'>
                <MenuEntry: 'redraw'>
                <MenuEntry: 'current score'>
                <MenuEntry: 'show/hide commands'>
                <MenuEntry: 'toggle where'>
                <MenuEntry: 'display calling code line number'>

        Return menu section or none.
        '''
        for menu_section in self.menu_sections:
            if menu_section.is_hidden:
                return menu_section

    @property
    def menu_sections(self):
        '''Menu sections:

        ::

            >>> for menu_section in menu.menu_sections:
            ...     menu_section
            <MenuSection (14)>
            <MenuSection (4)>

        Return list.
        '''
        return self._menu_sections

    @apply
    def should_clear_terminal():
        def fget(self):
            '''True when menu should clear terminal. Otherwise false:
    
            ::

                >>> menu.should_clear_terminal
                False

            Return boolean.
            '''
            return self._should_clear_terminal
        def fset(self, should_clear_terminal):
            assert isinstance(should_clear_terminal, bool)
            self._should_clear_terminal = should_clear_terminal
        return property(**locals())

    @property
    def storage_format(self):
        '''Menu storage format:

        ::
    
            >>> z(menu)
            menuing.Menu(
                should_clear_terminal=False
                )

        Return string.
        '''
        return super(Menu, self).storage_format

    @apply
    def title():
        def fget(self):
            '''Menu title:

            ::

                >>> menu.title is None
                True

            Return string or none.
            '''
            return self._title
        def fset(self, title):
            assert isinstance(title, (str, type(None)))
            self._title = title
        return property(**locals())

    ### PUBLIC METHODS ###

    def display_calling_code_line_number(self):
        lines = []
        if self.where is not None:
            file_path = self.where[1]
            file_name = os.path.basename(file_path)
            line = '{}   file: {}'.format(self._make_tab(1), file_name)
            lines.append(line)
            line = '{} method: {}'.format(self._make_tab(1), self.where[3])
            lines.append(line)
            line = '{}   line: {}'.format(self._make_tab(1), self.where[2])
            lines.append(line)
            lines.append('')
            self._io.display(lines, capitalize_first_character=False)
            self._session.hide_next_redraw = True
        else:
            self._session.enable_where = True

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

    def interactively_exec_statement(self):
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

    def interactively_grep_directories(self):
        regex = self._io.handle_raw_input('regex')
        command = 'grep -Irn "{}" * | grep -v svn'.format(regex)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self._io.display(lines, capitalize_first_character=False)

    def make_section(self, 
        is_hidden=False, 
        is_numbered=False, 
        is_ranged=False, 
        menu_entries=None,
        return_value_attribute='display_string',
        ):
        from experimental import scoremanagertools
        assert not (is_numbered and self._has_numbered_section)
        assert not (is_ranged and self._has_ranged_section)
        menu_section = scoremanagertools.menuing.MenuSection(
            is_hidden=is_hidden,
            is_numbered=is_numbered,
            is_ranged=is_ranged,
            return_value_attribute=return_value_attribute,
            )
        menu_section.menu_entries = menu_entries
        self.menu_sections.append(menu_section)
        return menu_section

    def toggle_menu_commands(self):
        if self._session.nonnumbered_menu_sections_are_hidden:
            self._session.nonnumbered_menu_sections_are_hidden = False
        else:
            self._session.nonnumbered_menu_sections_are_hidden = True
