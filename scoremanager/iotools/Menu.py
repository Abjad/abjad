# -*- encoding: utf-8 -*-
import os
from abjad.tools import mathtools
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class Menu(ScoreManagerObject):
    r'''A menu.

    ..  container:: example

        ::

            >>> menu = scoremanager.iotools.Menu(
            ...     include_default_hidden_sections=False,
            ...     )
            >>> section = menu.make_command_section()
            >>> entry = section.append(('foo - add', 'add'))
            >>> entry = section.append(('foo - delete', 'delete'))
            >>> entry = section.append(('foo - modify', 'modify'))

        ::

            >>> menu
            <Menu (1)>

    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        session=None, 
        where=None,
        include_default_hidden_sections=True,
        should_clear_terminal=False,
        title=None,
        ):
        ScoreManagerObject.__init__(self, session=session)
        self._menu_sections = []
        if include_default_hidden_sections:
            self._make_default_hidden_sections()
        self.should_clear_terminal = should_clear_terminal
        self.title = title
        self.where = where

    ### SPECIAL METHODS ###

    def __len__(self):
        r'''Gets number of menu sections in menu.

        Returns nonnegative integer.
        '''
        return len(self.menu_sections)

    def __repr__(self):
        r'''Gets interpreter representation of menu.

        Returns string.
        '''
        return '<{} ({})>'.format(type(self).__name__, len(self))

    ### PRIVATE METHODS ###

    def _change_user_input_to_directive(self, user_input):
        user_input = stringtools.strip_diacritics_from_binary_string(
            user_input)
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
        elif 3 <= len(user_input) and 'score'.startswith(user_input):
            return 'score'
        else:
            for menu_section in self.menu_sections:
                for menu_entry in menu_section.menu_entries:
                    if menu_entry.matches(user_input):
                        return self._enclose_in_list(menu_entry.return_value)

    def _clear_terminal(self):
        if self.should_clear_terminal:
            self._session.io_manager.clear_terminal()

    def _display(
        self, 
        predetermined_user_input=None,
        ):
        self._clear_terminal()
        if not self._session.hide_hidden_commands:
            self.display_hidden_commands()
        else:
            menu_lines = self._make_menu_lines()
            self._session.io_manager.display(
                menu_lines,
                capitalize_first_character=False,
                )
        if predetermined_user_input is not None:
            return predetermined_user_input
        user_entered_lone_return = False
        user_input = self._session.io_manager.handle_user_input('')
        if user_input == '':
            user_entered_lone_return = True
        directive = self._change_user_input_to_directive(user_input)
        directive = self._strip_default_notice_from_strings(directive)
        self._session._hide_next_redraw = False
        io_manager = self._session.io_manager
        directive = \
            io_manager._handle_hidden_menu_section_return_value(directive)
        if directive is None and user_entered_lone_return:
            return 'user entered lone return'
        elif directive is None and not user_entered_lone_return:
            return
        elif directive == 'o':
            self.toggle_secondary_commands()
        elif directive == 'n':
            self.toggle_hidden_commands()
        elif directive == 'sce':
            self.edit_calling_code()
        elif directive == 'sdv':
            self._session.display_variables()
        elif directive == 'scl':
            self.display_calling_code_line_number()
        else:
            return directive

    def _enclose_in_list(self, expr):
        if self._has_ranged_section():
            return [expr]
        else:
            return expr

    def _get_first_nonhidden_return_value_in_menu(self):
        for menu_section in self.menu_sections:
            if menu_section.is_secondary:
                continue
            if menu_section.is_hidden:
                continue
            if menu_section._menu_entry_return_values:
                return menu_section._menu_entry_return_values[0]

    def _handle_argument_range_user_input(self, user_input):
        if not self._has_ranged_section():
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

    def _has_numbered_section(self):
        return any(x.is_numbered for x in self.menu_sections)

    def _has_ranged_section(self):
        return any(x.is_ranged for x in self.menu_sections)

    def _make_command_display_menu_section(self):
        section = self._make_section(
            is_hidden=True,
            return_value_attribute='key',
            )
        section.append(('commands - hidden', 'n'))
        section.append(('commands - secondary', 'o'))
        return section

    def _make_default_hidden_sections(self):
        sections = []
        sections.append(self._make_navigation_menu_section())
        sections.append(self._make_command_display_menu_section())
        sections.append(self._make_lilypond_menu_section())
        sections.append(self._make_python_menu_section())
        sections.append(self._make_repository_menu_section())
        sections.append(self._make_scores_tour_menu_section())
        sections.append(self._make_session_menu_section())
        sections.append(self._make_source_code_menu_section())
        sections.append(self._make_system_menu_section())
        return sections

    def _make_lilypond_menu_section(self):
        section = self._make_section(
            is_hidden=True,
            match_on_display_string=False,
            return_value_attribute='key',
            )
        section.append(('LilyPond - view log', 'lvl'))
        return section

    def _make_menu_lines(self):
        result = []
        result.extend(self._make_title_lines())
        result.extend(self._make_section_lines())
        return result

    def _make_navigation_menu_section(self):
        section = self._make_section(
            is_hidden=True,
            return_value_attribute='key',
            )
        section.append(('back - go', 'b'))
        section.append(('home - go', 'h'))
        section.append(('score - go', 's'))
        return section

    def _make_python_menu_section(self):
        section = self._make_section(
            is_hidden=True,
            match_on_display_string=False,
            return_value_attribute='key',
            )
        section.append(('Python - doctest', 'pyd'))
        section.append(('Python - interact', 'pyi'))
        section.append(('Python - test', 'pyt'))
        return section

    def _make_repository_menu_section(self):
        section = self._make_section(
            is_hidden=True,
            match_on_display_string=False,
            return_value_attribute='key',
            )
        section.append(('repository - add', 'radd'))
        section.append(('repository - commit', 'rci'))
        section.append(('repository - status', 'rst'))
        section.append(('repository - update', 'rup'))
        return section

    def _make_scores_tour_menu_section(self):
        section = self._make_section(
            is_hidden=True,
            match_on_display_string=False,
            return_value_attribute='key',
            )
        section.append(('scores - tour next', 'next'))
        section.append(('scores - tour prev', 'prev'))
        return section

    def _make_section(
        self, 
        is_secondary=False, 
        is_hidden=False,
        is_numbered=False, 
        is_ranged=False, 
        display_prepopulated_values=False,
        match_on_display_string=True,
        menu_entries=None,
        return_value_attribute='display_string',
        ):
        from scoremanager import iotools
        assert not (is_numbered and self._has_numbered_section())
        assert not (is_ranged and self._has_ranged_section())
        menu_section = iotools.MenuSection(
            is_secondary=is_secondary,
            is_hidden=is_hidden,
            is_numbered=is_numbered,
            is_ranged=is_ranged,
            display_prepopulated_values=display_prepopulated_values,
            match_on_display_string=match_on_display_string,
            return_value_attribute=return_value_attribute,
            )
        menu_section.menu_entries = menu_entries
        self.menu_sections.append(menu_section)
        return menu_section

    def _make_section_lines(self):
        menu_lines = []
        for menu_section in self.menu_sections:
            hide = self._session.hide_secondary_commands
            if hide and menu_section.is_secondary:
                continue
            if menu_section.is_hidden:
                continue
            section_menu_lines = menu_section._make_menu_lines()
            menu_lines.extend(section_menu_lines)
        if self.hide_current_run:
            menu_lines = []
        return menu_lines

    def _make_session_menu_section(self):
        section = self._make_section(
            is_hidden=True,
            match_on_display_string=False,
            return_value_attribute='key',
            )
        section.append(('session - display variables', 'sdv'))
        return section

    def _make_source_code_menu_section(self):
        section = self._make_section(
            is_hidden=True,
            match_on_display_string=False,
            return_value_attribute='key',
            )
        section.append(('source code - edit', 'sce'))
        section.append(('source code - location', 'scl'))
        section.append(('source code - track', 'sct'))
        return section

    def _make_system_menu_section(self):
        section = self._make_section(
            is_hidden=True,
            match_on_display_string=False,
            return_value_attribute='key',
            )
        section.append(('system - quit', 'q'))
        return section

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

    def _run(
        self, 
        clear=True, 
        predetermined_user_input=None, 
        pending_user_input=None,
        ):
        self._session.io_manager._assign_user_input(pending_user_input)
        clear, hide_current_run = clear, False
        while True:
            self.should_clear_terminal = clear
            self.hide_current_run = hide_current_run
            clear, hide_current_run = False, True
            result = self._display(
                predetermined_user_input=predetermined_user_input,
                )
            if self._session.is_complete:
                break
            elif result == 'r':
                clear, hide_current_run = True, False
            else:
                break
        return result

    # TODO: apply default notice at display time 
    #       so this can be completely removed
    def _strip_default_notice_from_strings(self, expr):
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
        r'''Menu hidden section.

        ::

            >>> menu.hidden_section is None
            True

        Returns menu section or none.
        '''
        for menu_section in self.menu_sections:
            if menu_section.is_hidden:
                return menu_section

    @property
    def menu_sections(self):
        r'''Menu sections.

        ::

            >>> for menu_section in menu.menu_sections:
            ...     menu_section
            <MenuSection (3)>

        Returns list.
        '''
        return self._menu_sections

    @apply
    def should_clear_terminal():
        def fget(self):
            r'''Is true when menu should clear terminal. Otherwise false:
    
            ::

                >>> menu.should_clear_terminal
                False

            Returns boolean.
            '''
            return self._should_clear_terminal
        def fset(self, should_clear_terminal):
            assert isinstance(should_clear_terminal, bool)
            self._should_clear_terminal = should_clear_terminal
        return property(**locals())

    @apply
    def title():
        def fget(self):
            r'''Menu title.

            ::

                >>> menu.title is None
                True

            Returns string or none.
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
            self._session.io_manager.display(
                lines, capitalize_first_character=False)
            self._session._hide_next_redraw = True
        else:
            self._session.enable_where = True

    def display_hidden_commands(self):
        self._session._push_breadcrumb('hidden commands')
        menu_lines = []
        title = self._session.menu_header
        title = stringtools.capitalize_string_start(title)
        menu_lines.append(title)
        menu_lines.append('')
        for menu_section in self.menu_sections:
            if not menu_section.is_hidden:
                continue
            for menu_entry in menu_section.menu_entries:
                key = menu_entry.key
                display_string = menu_entry.display_string
                menu_line = self._make_tab(1) + ' '
                menu_line += '{} ({})'.format(display_string, key)
                menu_lines.append(menu_line)
            menu_lines.append('')
        self._session.io_manager.display(
            menu_lines, 
            capitalize_first_character=False,
            clear_terminal=True,
            )
        self._session._pop_breadcrumb()

    def edit_calling_code(self):
        if self.where is not None:
            file_path = self.where[1]
            line_number = self.where[2]
            self._session.io_manager.open_file(
                file_path,
                line_number=line_number,
                )
        else:
            lines = []
            message = 'where-tracking not enabled.'
            message += " Use 'sct' for source code tracking."
            lines.append(message)
            lines.append('')
            self._session.io_manager.display(lines)
            self._session._hide_next_redraw = True

    def make_asset_section(self, menu_entries=None):
        asset_section = self._make_section(
            is_numbered=True,
            return_value_attribute='explicit',
            )
        return asset_section

    def make_attribute_section(self, menu_entries=None):
        attribute_section = self._make_section(
            is_numbered=True,
            return_value_attribute='explicit',
            display_prepopulated_values=True,
            )
        return attribute_section

    def make_command_section(
        self,
        is_secondary=False,
        match_on_display_string=True,
        menu_entries=None,
        ):
        command_section = self._make_section(
            is_secondary=is_secondary,
            match_on_display_string=match_on_display_string,
            return_value_attribute='key',
            )
        return command_section

    def make_keyed_attribute_section(
        self, 
        is_numbered=False, 
        menu_entries=None,
        ):
        keyed_attribute_section = self._make_section(
            return_value_attribute='key',
            is_numbered=is_numbered,
            display_prepopulated_values=True,
            )
        return keyed_attribute_section

    def make_numbered_list_section(self, menu_entries=None):
        numbered_list_section = self._make_section(
            is_numbered=True,
            is_ranged=True,
            return_value_attribute='display_string',
            )
        return numbered_list_section

    def make_numbered_section(self, menu_entries=None):
        numbered_section = self._make_section(
            is_numbered=True,
            return_value_attribute='number',
            )
        return numbered_section

    # TODO: move to Session
    def toggle_hidden_commands(self):
        if self._session._hide_hidden_commands:
            self._session._hide_hidden_commands = False
        else:
            self._session._hide_hidden_commands = True

    # TODO: move to Session
    def toggle_secondary_commands(self):
        if self._session.hide_secondary_commands:
            self._session._hide_secondary_commands = False
        else:
            self._session._hide_secondary_commands = True
        self._session._hide_hidden_commands = True
