# -*- encoding: utf-8 -*-
import math
import os
import re
import textwrap
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.idetools.Controller import Controller


class Menu(Controller):
    r'''Menu.

    ..  container:: example

        ::

            >>> session = scoremanager.idetools.Session()
            >>> menu = scoremanager.idetools.Menu(session=session)
            >>> commands = []
            >>> commands.append(('foo - add', 'add'))
            >>> commands.append(('foo - delete', 'delete'))
            >>> commands.append(('foo - modify', 'modify'))
            >>> section = menu.make_command_section(
            ...     commands=commands,
            ...     name='test',
            ...     )

        ::

            >>> menu
            <Menu (1)>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_asset_section',
        '_breadcrumb_callback',
        '_menu_sections',
        '_name',
        '_predetermined_input',
        '_subtitle',
        '_title',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        breadcrumb_callback=None,
        name=None,
        session=None,
        subtitle=None,
        title=None,
        ):
        Controller.__init__(self, session=session)
        self._breadcrumb_callback = breadcrumb_callback
        self._menu_sections = []
        self._name = name
        self._predetermined_input = None
        self._subtitle = subtitle
        self._title = title

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        r'''Gets menu section indexed by `expr`.

        Returns menu section with name equal to `expr` when `expr` is a string.

        Returns menu section at index `expr` when `expr` is an integer.
        '''
        if isinstance(expr, str):
            for section in self.menu_sections:
                if section.name == expr:
                    return section
            raise KeyError(expr)
        else:
            return self.menu_sections.__getitem__(expr)

    def __len__(self):
        r'''Gets number of menu sections in menu.

        Returns nonnegative integer.
        '''
        return len(self.menu_sections)

    def __repr__(self):
        r'''Gets interpreter representation of menu.

        Returns string.
        '''
        if self.name:
            string = '<{} {!r} ({})>'
            string = string.format(type(self).__name__, self.name, len(self))
        else:
            string = '<{} ({})>'
            string = string.format(type(self).__name__, len(self))
        return string

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._breadcrumb_callback == 'name':
            return self.name
        elif self._breadcrumb_callback:
            return self._breadcrumb_callback()

    @property
    def _wrangler_navigation_to_session_variable(self):
        result = {
            'd': '_is_navigating_to_distribution_files',
            'g': '_is_navigating_to_segments',
            'k': '_is_navigating_to_maker_files',
            'm': '_is_navigating_to_materials',
            'u': '_is_navigating_to_build_files',
            'y': '_is_navigating_to_stylesheets',
        }
        return result

    ### PRIVATE METHODS ###

    def _change_input_to_directive(self, input_):
        r'''Match against any asset section last.
        This avoids file name new-stylesheet.ily aliasing command (new).
        '''
        input_ = stringtools.strip_diacritics(input_)
        if self._user_enters_nothing(input_):
            default_value = None
            for section in self.menu_sections:
                if section._has_default_value:
                    default_value = section._default_value
            if default_value is not None:
                return self._enclose_in_list(default_value)
        elif input_ in ('**', 's', 'S', 'q', 'b', '??', '<return>'):
            self._session._pending_redraw = True
            return input_
        elif input_.startswith('!'):
            return input_
        asset_section = None
        for section in self.menu_sections:
            if section.is_information_section:
                continue
            if section.is_asset_section:
                asset_section = section
                continue
            for menu_entry in section:
                if menu_entry.matches(input_):
                    return self._enclose_in_list(menu_entry.return_value)
        if asset_section is not None:
            for menu_entry in asset_section:
                if menu_entry.matches(input_):
                    return self._enclose_in_list(menu_entry.return_value)
        asset_section = None
        for section in self.menu_sections:
            if section.is_information_section:
                continue
            if section.is_asset_section:
                asset_section = section
                continue
            for menu_entry in section:
                if menu_entry.matches(input_.lower()):
                    return self._enclose_in_list(menu_entry.return_value)
        if asset_section is not None:
            for menu_entry in asset_section:
                if menu_entry.matches(input_):
                    return self._enclose_in_list(menu_entry.return_value)
        if self._user_enters_argument_range(input_):
            return self._handle_argument_range_input(input_)

    def _enclose_in_list(self, expr):
        if self._has_ranged_section():
            return [expr]
        else:
            return expr

    def _get_first_nonhidden_return_value_in_menu(self):
        for section in self.menu_sections:
            if section.is_hidden:
                continue
            if section._menu_entry_return_values:
                return section._menu_entry_return_values[0]

    def _group_by_annotation(self, lines):
        new_lines = []
        current_annotation = ''
        pattern = re.compile('(.*)(\s+)\((.+)\)')
        tab = self._io_manager._make_tab()
        for line in lines:
            line = line.replace('', '')
            match = pattern.match(line)
            if match:
                display_string, _, annotation = match.groups()
                if not annotation == current_annotation:
                    current_annotation = annotation
                    new_line = '{}{}:'.format(tab, current_annotation)
                    new_lines.append(new_line)
                new_line = tab + display_string
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        return new_lines

    def _handle_argument_range_input(self, input_):
        if not self._has_ranged_section():
            return
        for section in self.menu_sections:
            if section.is_ranged:
                ranged_section = section
        entry_numbers = ranged_section._argument_range_string_to_numbers(
            input_)
        if not entry_numbers:
            return
        entry_indices = [entry_number - 1 for entry_number in entry_numbers]
        result = []
        for i in entry_indices:
            entry = ranged_section._menu_entry_return_values[i]
            result.append(entry)
        return result

    def _handle_directive(self, directive):
        if not self._is_in_open_environment():
            return directive
        if not isinstance(directive, str):
            return directive
        if directive in self._wrangler_navigation_to_session_variable:
            variable = self._wrangler_navigation_to_session_variable[directive]
            setattr(self._session, variable, True)
        return directive

    def _handle_user_input(self):
        input_ = self._io_manager._handle_input('')
        user_entered_lone_return = input_ == ''
        directive = None
        parts = input_.split()
        length = len(parts)
        for i in range(len(parts)):
            count = length - i
            candidate = ' '.join(parts[:count])
            directive = self._change_input_to_directive(candidate)
            if directive is not None:
                if count < length:
                    remaining_count = length - count
                    remaining_input = ' '.join(parts[-remaining_count:])
                    pending_input = self._session._pending_input or ''
                    pending_input = pending_input + remaining_input
                    self._session._pending_input = pending_input
                    self._session._pending_redraw = True
                break
        directive = self._strip_default_notice_from_strings(directive)
        directive = self._handle_directive(directive)
        if directive is None and user_entered_lone_return:
            result = '<return>'
        elif directive is None and not user_entered_lone_return:
            message = 'unknown command: {!r}.'
            message = message.format(input_)
            self._io_manager._display([message, ''])
            result = None
        else:
            result = directive
        return result

    def _has_numbered_section(self):
        return any(x.is_numbered for x in self.menu_sections)

    def _has_ranged_section(self):
        return any(x.is_ranged for x in self.menu_sections)

    def _is_in_open_environment(self):
        if self._session.is_in_confirmation_environment:
            return False
        if self._session.is_in_autoeditor:
            return False
        return True

    def _is_recognized_input(self, expr):
        if isinstance(expr, str):
            if expr in self._input_to_method:
                return True
        return False

    @staticmethod
    def _ljust(string, width):
        start_width = len(stringtools.strip_diacritics(string))
        if start_width < width:
            needed = width - start_width
            suffix = needed * ' '
            result = string + suffix
        else:
            result = string
        return result

    def _make_asset_lines(self):
        has_asset_section = False
        for section in self:
            if section.is_asset_section:
                has_asset_section = True
                break
        if not has_asset_section:
            return []
        assert section.is_asset_section
        lines = section._make_lines()
        if section.group_by_annotation:
            lines = self._group_by_annotation(lines)
        lines = self._make_bicolumnar(lines, strip=False)
        return lines

    def _make_available_command_section_lines(self):
        lines = []
        for section in self.menu_sections:
            if not section.is_command_section:
                continue
            for menu_entry in section:
                key = menu_entry.key
                display_string = menu_entry.display_string
                menu_line = self._make_tab(1)
                menu_line += '{} ({})'.format(display_string, key)
                lines.append(menu_line)
            lines.append('')
        if lines:
            lines.pop()
        lines = self._make_bicolumnar(lines, break_only_at_blank_lines=True)
        title = self._session.menu_header
        title = title + ' - available commands'
        title = stringtools.capitalize_start(title)
        lines[0:0] = [title, '']
        lines.append('')
        return lines

    def _make_bicolumnar(
        self, 
        lines, 
        break_only_at_blank_lines=False,
        strip=True,
        ):
        terminal_height = 40
        if len(lines) < terminal_height:
            return lines
        if strip:
            lines = [_.strip() for _ in lines]
        all_packages_lines = [_ for _ in lines if _.startswith('all')]
        lines = [_ for _ in lines if not _.startswith('all')]
        # remove consecutive '', '' that can result from comprehension above
        clean_lines = []
        for line in lines:
            if line == '':
                if clean_lines and clean_lines[-1] == '':
                    continue
            clean_lines.append(line)
        lines = clean_lines
        midpoint = int(len(lines)/2)
        if break_only_at_blank_lines:
            while lines[midpoint] != '':
                midpoint += 1
            assert lines[midpoint] == ''
        left_lines = lines[:midpoint]
        if break_only_at_blank_lines:
            right_lines = lines[midpoint+1:]
            assert len(left_lines) + len(right_lines) == len(lines) - 1
        else:
            right_lines = lines[midpoint:]
        left_count, right_count = len(left_lines), len(right_lines)
        #assert right_count <= left_count, repr((left_count, right_count))
        if strip:
            left_width = max(len(_.strip()) for _ in left_lines)
            right_width = max(len(_.strip()) for _ in right_lines)
        else:
            left_width = max(len(_) for _ in left_lines)
            right_width = max(len(_) for _ in right_lines)
        left_lines = [self._ljust(_, left_width) for _ in left_lines]
        right_lines = [self._ljust(_, right_width) for _ in right_lines]
        if strip:
            left_margin_width, gutter_width = 4, 4 
        else:
            left_margin_width, gutter_width = 0, 4 
        left_margin = left_margin_width * ' '
        gutter = gutter_width * ' '
        conjoined_lines = []
        for _ in sequencetools.zip_sequences(
            [left_lines, right_lines],
            truncate=False,
            ):
            if len(_) == 1:
                left_line = _[0]
                conjoined_line = left_margin + left_line
            elif len(_) == 2:
                left_line, right_line = _
                conjoined_line = left_margin + left_line + gutter + right_line
            conjoined_lines.append(conjoined_line)
        if all_packages_lines:
            blank_line = left_margin
            conjoined_lines.append(blank_line)
        for line in all_packages_lines:
            conjoined_line = left_margin + line
            conjoined_lines.append(conjoined_line)
        return conjoined_lines

    def _make_command_section_lines(self):
        result = []
        section_names = []
        for section in self.menu_sections:
            #print(section.name)
            # TODO: check for duplicate section names at initialization
            if section.name in section_names:
                message = '{!r} contains duplicate {!r}.'
                message = message.format(self, section)
                raise Exception(message)
            else:
                section_names.append(section.name)
            hide = not self._session.display_available_commands
            if hide and section.is_hidden:
                continue
            if section.is_asset_section:
                continue
            if section.name == 'material summary':
                continue
            section_menu_lines = section._make_lines()
            result.extend(section_menu_lines)
        return result

    def _make_material_summary_lines(self):
        try:
            section = self['material summary']
        except KeyError:
            return []
        lines = section._make_lines()
        return lines

    def _make_section(
        self,
        default_index=None,
        display_prepopulated_values=False,
        is_alphabetized=False,
        is_asset_section=False,
        is_attribute_section=False,
        is_command_section=False,
        is_hidden=False,
        is_information_section=False,
        is_material_summary_section=False,
        is_navigation_section=False,
        is_numbered=False,
        is_ranged=False,
        match_on_display_string=True,
        menu_entries=None,
        name=None,
        return_value_attribute='display_string',
        title=None,
        ):
        from scoremanager import idetools
        assert not (is_numbered and self._has_numbered_section())
        assert not (is_ranged and self._has_ranged_section())
        section = idetools.MenuSection(
            default_index=default_index,
            display_prepopulated_values=display_prepopulated_values,
            is_alphabetized=is_alphabetized,
            is_asset_section=is_asset_section,
            is_attribute_section=is_attribute_section,
            is_command_section=is_command_section,
            is_hidden=is_hidden,
            is_information_section=is_information_section,
            is_material_summary_section=is_material_summary_section,
            is_navigation_section=is_navigation_section,
            is_numbered=is_numbered,
            is_ranged=is_ranged,
            match_on_display_string=match_on_display_string,
            menu_entries=menu_entries,
            name=name,
            return_value_attribute=return_value_attribute,
            title=title,
            )
        self.menu_sections.append(section)
        self.menu_sections.sort(key=lambda x: x.name)
        noncommand_sections = [
            x for x in self.menu_sections
            if (not x.is_command_section and not x.is_navigation_section)
            ]
        for noncommand_section in noncommand_sections:
            self.menu_sections.remove(noncommand_section)
        for noncommand_section in noncommand_sections:
            self.menu_sections.insert(0, noncommand_section)
        return section

    def _make_tab(self, n=1):
        return 4 * n * ' '

    def _make_title_lines(self):
        result = []
        if self.title is not None:
            title = self.title
        else:
            title = self._session.menu_header
        result.append(stringtools.capitalize_start(title))
        if self.subtitle is not None:
            line = '  ' + self.subtitle
            result.append('')
            result.append(line)
        result.append('')
        return result

    def _make_visible_section_lines(self):
        lines = []
        lines.extend(self._make_title_lines())
        lines.extend(self._make_material_summary_lines())
        lines.extend(self._make_asset_lines())
        if lines and not all(_ == ' ' for _ in lines[-1]):
            lines.append('')
        lines.extend(self._make_command_section_lines())
        return lines

    def _redraw(self):
        self._session._pending_redraw = False
        self._io_manager.clear_terminal()
        if self._session.display_available_commands:
            lines = self._make_available_command_section_lines()
        else:
            lines = self._make_visible_section_lines()
        self._io_manager._display(lines, capitalize=False, is_menu=True)

    def _return_value_to_location_pair(self, return_value):
        for i, section in enumerate(self.menu_sections):
            if return_value in section._menu_entry_return_values:
                j = section._menu_entry_return_values.index(return_value)
                return i, j

    def _return_value_to_next_return_value_in_section(self, return_value):
        section_index, entry_index = self._return_value_to_location_pair(
            return_value)
        section = self.menu_sections[section_index]
        entry_index = (entry_index + 1) % len(section)
        return section._menu_entry_return_values[entry_index]

    def _run(self):
        with self._io_manager._controller(controller=self):
            while True:
                result = self._predetermined_input
                if not result:
                    if self._session.pending_redraw:
                        self._redraw()
                    result = self._handle_user_input()
                if self._session.is_quitting:
                    return result
                elif result == '<return>':
                    self._session._pending_redraw = True
                elif self._is_recognized_input(result):
                    self._input_to_method[result]()
                    return
                else:
                    return result

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

    def _user_enters_argument_range(self, input_):
        if ',' in input_:
            return True
        if '-' in input_:
            return True
        return False

    def _user_enters_nothing(self, input_):
        return (
            not input_ or 
            (3 <= len(input_) and '<return>'.startswith(input_))
            )

    ### PUBLIC PROPERTIES ###

    @property
    def menu_sections(self):
        r'''Gets menu sections.

        ..  container:: example

            ::

                >>> for section in menu.menu_sections:
                ...     section
                <MenuSection 'test' (3)>

        Returns list.
        '''
        return self._menu_sections

    @property
    def name(self):
        r'''Gets menu name.

        ..  container:: example

            ::

                >>> menu.name is None
                True

        Returns list.
        '''
        return self._name

    @property
    def subtitle(self):
        r'''Gets menu subtitle.

        ..  container:: example

            ::

                >>> menu.subtitle is None
                True

        Returns string or none.
        '''
        return self._subtitle

    @property
    def title(self):
        r'''Gets menu title.

        ..  container:: example

            ::

                >>> menu.title is None
                True

        Returns string or none.
        '''
        return self._title

    ### PUBLIC METHODS ###

    def make_asset_section(
        self,
        menu_entries=None,
        name='assets',
        ):
        r'''Makes asset section.

        With these attributes:

            * is asset section
            * is numbered
            * return value set to explicit

        Returns menu section.
        '''
        section = self._make_section(
            is_asset_section=True,
            is_numbered=True,
            menu_entries=menu_entries,
            name=name,
            return_value_attribute='explicit',
            )
        self._asset_section = section
        return section

    def make_attribute_section(
        self, 
        menu_entries=None, 
        name=None, 
        title=None,
        ):
        r'''Makes attribute section.

        With these attributes:

            * is attribute section
            * is numbered
            * displays prepopulated values
            * return value set to explicit

        Returns menu section.
        '''
        section = self._make_section(
            display_prepopulated_values=True,
            is_attribute_section=True,
            is_numbered=True,
            menu_entries=menu_entries,
            return_value_attribute='explicit',
            name=name,
            title=title,
            )
        return section

    def make_command_section(
        self,
        is_alphabetized=True,
        is_hidden=False,
        default_index=None,
        match_on_display_string=False,
        commands=None,
        name=None,
        ):
        r'''Makes command section.

        Menu section with these attributes:

            * is command section
            * is alphabetized
            * is not hidden
            * does NOT match on display string
            * return value attribute equal to ``'key'``

        Returns menu section.
        '''
        section = self._make_section(
            is_alphabetized=is_alphabetized,
            is_command_section=True,
            is_hidden=is_hidden,
            default_index=default_index,
            match_on_display_string=match_on_display_string,
            menu_entries=commands,
            name=name,
            return_value_attribute='key',
            )
        return section

    def make_information_section(
        self,
        menu_entries=None,
        name='information',
        ):
        r'''Makes information section.

        Menu section with these attributes:

            * is information section
            * not hidden
            * does not match on display string
            * return value attribute equal to ``'key'``

        Returns menu section.
        '''
        section = self._make_section(
            is_hidden=False,
            is_information_section=True,
            menu_entries=menu_entries,
            name=name,
            return_value_attribute='key',
            )
        return section

    def make_keyed_attribute_section(
        self,
        is_numbered=False,
        menu_entries=None,
        name=None,
        ):
        r'''Makes keyed attribute section.

        With these attributes:

            * not numbered

        Returns menu section.
        '''
        section = self._make_section(
            display_prepopulated_values=True,
            is_numbered=is_numbered,
            menu_entries=menu_entries,
            name=name,
            return_value_attribute='key',
            )
        return section

    def make_material_summary_section(
        self,
        lines=None,
        name='material summary',
        ):
        r'''Makes asset section.

        With these attributes:

            * is material summary section
            * is not numbered
            * return value set to explicit

        Returns menu section.
        '''
        section = self._make_section(
            is_material_summary_section=True,
            is_numbered=False,
            menu_entries=lines,
            name=name,
            return_value_attribute='explicit',
            )
        return section

    def make_navigation_section(
        self,
        is_hidden=False,
        match_on_display_string=True,
        commands=None,
        name=None,
        ):
        r'''Makes navigation section.

        Menu section with these attributes:

            * is navigation section
            * not hidden
            * match on display string
            * return value attribute equal to ``'key'``

        Returns menu section.
        '''
        section = self._make_section(
            is_hidden=is_hidden,
            is_navigation_section=True,
            match_on_display_string=match_on_display_string,
            menu_entries=commands,
            name=name,
            return_value_attribute='key',
            )
        return section

    def make_numbered_list_section(
        self,
        menu_entries=None,
        name=None,
        title=None,
        default_index=None,
        ):
        r'''Makes numbered list section.

        With these attributes:

            * asset section
            * numbered
            * ranged
            * return value equal to display string

        Returns menu section.
        '''
        section = self._make_section(
            is_asset_section=True,
            is_numbered=True,
            is_ranged=True,
            default_index=default_index,
            menu_entries=menu_entries,
            name=name,
            return_value_attribute='display_string',
            title=title,
            )
        return section

    def make_numbered_section(self, menu_entries=None, name=None):
        r'''Makes numbered section.

        With these attributes:

            * asset section
            * numbered
            * return value equal to item number

        Returns menu section.
        '''
        section = self._make_section(
            name=name,
            is_asset_section=True,
            is_numbered=True,
            menu_entries=menu_entries,
            return_value_attribute='number',
            )
        return section