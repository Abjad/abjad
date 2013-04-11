from abjad.tools import iotools
from abjad.tools import mathtools
from abjad.tools import stringtools
from experimental.tools.scftools.menuing.MenuSection import MenuSection
from experimental.tools.scftools.menuing.MenuSectionAggregator import MenuSectionAggregator


class Menu(MenuSectionAggregator):

    def __init__(self, session=None, where=None):
        MenuSectionAggregator.__init__(self, session=session, where=where)
        self.sections.append(self.make_default_hidden_section(session=session, where=where))
        self.explicit_title = None

    ### SPECIAL METHODS ###

    def __len__(self):
        return len(self.sections)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def default_value(self):
        for section in self.sections:
            if section.has_default_value:
                return section.default_value

    @property
    def first_nonhidden_return_value_in_menu(self):
        for section in self.sections:
            if not section.is_hidden:
                if section.menu_entry_return_values:
                    return section.menu_entry_return_values[0]

    @property
    def has_default_valued_section(self):
        return any([section.has_default_value for section in self.sections])

    @property
    def has_hidden_section(self):
        return any([section.is_hidden for section in self.sections])

    @property
    def has_keyed_section(self):
        return any([section.is_keyed for section in self.sections])

    @property
    def has_numbered_section(self):
        return any([section.is_numbered or section.is_parenthetically_numbered for section in self.sections])

    @property
    def has_ranged_section(self):
        return any([section.is_ranged for section in self.sections])

    @property
    def hidden_section(self):
        for section in self.sections:
            if section.is_hidden:
                return section

    @property
    def menu_entry_bodies(self):
        result = []
        for section in self.sections:
            result.extend(section.menu_entry_bodies)
        return result

    @property
    def menu_entry_keys(self):
        result = []
        for section in self.sections:
            result.extend(section.menu_entry_keys)
        return result

    @property
    def menu_entry_return_values(self):
        result = []
        for section in self.sections:
            result.extend(section.menu_entry_return_values)
        return result

    @property
    def menu_lines(self):
        result = []
        result.extend(self.menu_title_lines)
        result.extend(self.section_lines)
        return result

    @property
    def menu_title_lines(self):
        menu_lines = []
        if not self.hide_current_run:
            if self.explicit_title is not None:
                title = self.explicit_title
            else:
                title = self.session.menu_header
            menu_lines.append(stringtools.capitalize_string_start(title))
            menu_lines.append('')
        return menu_lines

    @property
    def numbered_section(self):
        for section in self.sections:
            if section.is_numbered or section.is_parenthetically_numbered:
                return section

    @property
    def ranged_section(self):
        for section in self.sections:
            if section.is_ranged:
                return section

    @property
    def section_lines(self):
        menu_lines = []
        for section in self.sections:
            section_menu_lines = section.make_menu_lines()
            if not section.is_hidden:
                if not self.session.nonnumbered_menu_sections_are_hidden or \
                    section.is_numbered or section.is_parenthetically_numbered:
                    menu_lines.extend(section_menu_lines)
        if self.hide_current_run:
            menu_lines = []
        return menu_lines

    @property
    def tokens(self):
        result = []
        for section in self.sections:
            result.extend(section.tokens)
        return result

    @property
    def unpacked_menu_entries(self):
        result = []
        for section in self.sections:
            result.extend(section.unpacked_menu_entries_optimized)
        return result

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def explicit_title():
        def fget(self):
            return self._explicit_title
        def fset(self, explicit_title):
            assert isinstance(explicit_title, (str, type(None)))
            self._explicit_title = explicit_title
        return property(**locals())

    ### PUBLIC METHODS ###

    def change_user_input_to_directive(self, user_input):
        user_input = stringtools.strip_diacritics_from_binary_string(user_input)
        user_input = user_input.lower()
        if self.user_enters_nothing(user_input) and self.default_value:
            return self.conditionally_enclose_in_list(self.default_value)
        elif self.user_enters_argument_range(user_input):
            return self.handle_argument_range_user_input(user_input)
        else:
            for number, key, body, return_value, section in self.unpacked_menu_entries:
                body = stringtools.strip_diacritics_from_binary_string(body).lower()
                if  (mathtools.is_integer_equivalent_expr(user_input) and int(user_input) == number) or \
                    (user_input == key) or \
                    (user_input == body) or \
                    (3 <= len(user_input) and body.startswith(user_input)):
                    return self.conditionally_enclose_in_list(return_value)

    def conditionally_display_menu(self, flamingo_input=None):
        self.conditionally_clear_terminal()
        self.display(self.menu_lines, capitalize_first_character=False)
        if flamingo_input is not None:
            return flamingo_input
        user_response = self.handle_raw_input_with_default('SCF', default=self.prompt_default)
        user_input = self.split_multipart_user_response(user_response)
        directive = self.change_user_input_to_directive(user_input)
        directive = self.strip_default_indicators_from_strings(directive)
        self.session.hide_next_redraw = False
        directive = self.handle_hidden_key(directive)
        return directive

    def conditionally_enclose_in_list(self, expr):
        if self.has_ranged_section:
            return [expr]
        else:
            return expr

    def handle_argument_range_user_input(self, user_input):
        if not self.has_ranged_section:
            return
        entry_numbers = self.ranged_section.argument_range_string_to_numbers_optimized(user_input)
        if entry_numbers is None:
            return None
        entry_indices = [entry_number - 1 for entry_number in entry_numbers]
        result = []
        for i in entry_indices:
            entry = self.ranged_section.menu_entry_return_values[i]
            result.append(entry)
        return result

    def make_section(self, is_hidden=False, is_internally_keyed=False, is_keyed=True,
        is_numbered=False, is_parenthetically_numbered=False, is_ranged=False):
        assert not (is_numbered and self.has_numbered_section)
        assert not (is_parenthetically_numbered and self.has_numbered_section)
        assert not (is_ranged and self.has_ranged_section)
        section = MenuSection(is_hidden=is_hidden, is_internally_keyed=is_internally_keyed,
            is_keyed=is_keyed, is_numbered=is_numbered,
            is_parenthetically_numbered=is_parenthetically_numbered, is_ranged=is_ranged,
            session=self.session, where=self.where)
        self.sections.append(section)
        return section

    def return_value_to_location_pair(self, return_value):
        for i, section in enumerate(self.sections):
            if return_value in section.menu_entry_return_values:
                return (i, section.menu_entry_return_values.index(return_value))

    def return_value_to_next_return_value_in_section(self, return_value):
        section_index, entry_index = self.return_value_to_location_pair(return_value)
        section = self.sections[section_index]
        entry_index = (entry_index + 1) % len(section)
        return section.menu_entry_return_values[entry_index]

    def run(self, clear=True, flamingo_input=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        clear, hide_current_run = clear, False
        while True:
            self.should_clear_terminal, self.hide_current_run = clear, hide_current_run
            clear, hide_current_run = False, True
            result = self.conditionally_display_menu(flamingo_input=flamingo_input)
            if self.session.is_complete:
                break
            elif result == 'r':
                clear, hide_current_run = True, False
            else:
                break
        return result

    def split_multipart_user_response(self, user_response):
        self.session.transcribe_next_command = True
        if ' ' in user_response:
            parts = user_response.split(' ')
            key_parts, rest_parts = [], []
            for i, part in enumerate(parts):
                if not part.endswith((',', '-')):
                    break
            key_parts = parts[:i+1]
            rest_parts = parts[i+1:]
            key = ' '.join(key_parts)
            rest = ' '.join(rest_parts)
            if rest:
                self.session.transcribe_next_command = False
            if isinstance(self.session.user_input, str) and rest:
                self.session.user_input = rest + ' ' + self.session.user_input
            elif isinstance(self.session.user_input, str) and not rest:
                self.session.user_input = self.session.user_input
            else:
                self.session.user_input = rest
        else:
            key = user_response
        return key

    # TODO: apply default indicators at display time so this can be completely removed
    def strip_default_indicators_from_strings(self, expr):
        if isinstance(expr, list):
            cleaned_list = []
            for element in expr:
                if element.endswith(' (default)'):
                    element = element.replace(' (default)', '')
                cleaned_list.append(element)
            return cleaned_list
        #elif expr is not None:
        elif isinstance(expr, str):
            if expr.endswith(' (default)'):
                expr = expr.replace(' (default)', '')
            return expr
        else:
            return expr

    def user_enters_argument_range(self, user_input):
        if ',' in user_input:
            return True
        if '-' in user_input:
            return True
        return False

    def user_enters_nothing(self, user_input):
        return not user_input or (3 <= len(user_input) and 'default'.startswith(user_input))
