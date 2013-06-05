from abjad.tools import mathtools
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.menuing.MenuSection import MenuSection
from experimental.tools.scoremanagertools.menuing.MenuSectionAggregator import MenuSectionAggregator


class Menu(MenuSectionAggregator):

    ### INITIALIZER ###

    def __init__(self, session=None, where=None):
        MenuSectionAggregator.__init__(self, session=session, where=where)
        self.sections.append(self.make_default_hidden_section(session=session, where=where))
        self.explicit_title = None

    ### SPECIAL METHODS ###

    def __len__(self):
        return len(self.sections)

    ### PRIVATE METHODS ###

    def _run(self, clear=True, automatically_determined_user_input=None, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        clear, hide_current_run = clear, False
        while True:
            self.should_clear_terminal, self.hide_current_run = clear, hide_current_run
            clear, hide_current_run = False, True
            result = self.conditionally_display_menu(
                automatically_determined_user_input=automatically_determined_user_input)
            if self._session.is_complete:
                break
            elif result == 'r':
                clear, hide_current_run = True, False
            else:
                break
        return result

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
                if section.menu_token_return_values:
                    return section.menu_token_return_values[0]

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
        return any([section.is_numbered for section in self.sections])

    @property
    def has_ranged_section(self):
        return any([section.is_ranged for section in self.sections])

    @property
    def hidden_section(self):
        for section in self.sections:
            if section.is_hidden:
                return section

    # TODO: remove?
    @property
    def menu_token_bodies(self):
        result = []
        for section in self.sections:
            result.extend(section.menu_token_bodies)
        return result

    # TODO: remove?
    @property
    def menu_token_keys(self):
        result = []
        for section in self.sections:
            result.extend(section.menu_token_keys)
        return result

    # TODO: remove?
    @property
    def menu_token_return_values(self):
        result = []
        for section in self.sections:
            result.extend(section.menu_token_return_values)
        return result

    @property
    def menu_tokens(self):
        result = []
        for section in self.sections:
            result.extend(section.tokens)
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
                title = self._session.menu_header
            menu_lines.append(stringtools.capitalize_string_start(title))
            menu_lines.append('')
        return menu_lines

    @property
    def numbered_section(self):
        for section in self.sections:
            if section.is_numbered:
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
                if not self._session.nonnumbered_menu_sections_are_hidden or \
                    section.is_numbered:
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
        elif user_input == 'r':
            return 'r'
        else:
            for menu_token in self.menu_tokens:
                if menu_token.body == 'redraw':
                    continue
                return_value = menu_token.user_input_to_return_value(user_input)
                if return_value is not None:
                    return self.conditionally_enclose_in_list(return_value)

    def conditionally_display_menu(self, automatically_determined_user_input=None):
        self.conditionally_clear_terminal()
        self._io.display(self.menu_lines, capitalize_first_character=False)
        if automatically_determined_user_input is not None:
            return automatically_determined_user_input
        user_response = self._io.handle_raw_input_with_default('', default=self.prompt_default)
        directive = self.change_user_input_to_directive(user_response)
        directive = self.strip_default_indicators_from_strings(directive)
        self._session.hide_next_redraw = False
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
            entry = self.ranged_section.menu_token_return_values[i]
            result.append(entry)
        return result

    def make_section(self, is_hidden=False, is_internally_keyed=False, is_keyed=False,
        is_numbered=False, is_ranged=False, tokens=None,
        return_value_attribute='body'):
        assert not (is_numbered and self.has_numbered_section)
        assert not (is_ranged and self.has_ranged_section)
        section = MenuSection(
            is_hidden=is_hidden, 
            is_internally_keyed=is_internally_keyed,
            is_keyed=is_keyed, 
            is_numbered=is_numbered,
            is_ranged=is_ranged,
            tokens=tokens, 
            return_value_attribute=return_value_attribute,
            session=self._session, 
            where=self.where,
            )
        self.sections.append(section)
        return section

    def return_value_to_location_pair(self, return_value):
        for i, section in enumerate(self.sections):
            if return_value in section.menu_token_return_values:
                return (i, section.menu_token_return_values.index(return_value))

    def return_value_to_next_return_value_in_section(self, return_value):
        section_index, entry_index = self.return_value_to_location_pair(return_value)
        section = self.sections[section_index]
        entry_index = (entry_index + 1) % len(section)
        return section.menu_token_return_values[entry_index]

    # TODO: apply default indicators at display time so this can be completely removed
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

    def user_enters_argument_range(self, user_input):
        if ',' in user_input:
            return True
        if '-' in user_input:
            return True
        return False

    def user_enters_nothing(self, user_input):
        return not user_input or (3 <= len(user_input) and 'default'.startswith(user_input))
