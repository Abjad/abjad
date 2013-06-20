import types
from abjad.tools import stringtools
from experimental.tools.scoremanagertools import predicates
from experimental.tools.scoremanagertools.menuing.Menu import Menu
from experimental.tools.scoremanagertools.menuing.UserInputGetterMixin \
    import UserInputGetterMixin


class UserInputGetterMenu(Menu, UserInputGetterMixin):

    ### INITIALIZER ###

    def __init__(self, session=None, where=None):
        Menu.__init__(self, session=session, where=where)
        UserInputGetterMixin.__init__(self)
        self._argument_lists = []
        self._chevron_inclusion_indicators = []
        self._default_values = []
        self._help_strings = []
        self._prompt_strings = []
        self._setup_statements = []
        self._validation_functions = []
        self.allow_none = False
        self.capitalize_prompts = True
        self.include_newlines = False
        self.number_prompts = False
        self.prompt_character = '>'

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, len(self._prompt_strings))

    ### PRIVATE METHODS ###

    def _apply__validation_functions_to_value(self, value):
        if self.allow_none and value is None:
            return True
        if self.prompt_index < len(self._validation_functions):
            input_test = self._validation_functions[self.prompt_index]
            return self._evaluate_test(input_test, value)
        return True

    def _change_user_response_to_value(self, user_response):
        _setup_statements = self._setup_statements[self.prompt_index]
        assert isinstance(_setup_statements, list)
        if _setup_statements:
            value = self._get_value_from_setup_statements(
                user_response, _setup_statements)
            if value is None and not user_response == 'None':
                return '!!!'
        else:
            value = self._get_value_from_direct_evaluation(user_response)
        return value

    def _display_help(self):
        if self.prompt_index < len(self._help_strings):
            lines = []
            lines.append(self._help_strings[self.prompt_index])
            lines.append('')
            self._io.display(lines)

    def _display_help(self):
        lines = []
        if self.prompt_index < len(self._help_strings):
            lines.append(self._help_strings[self.prompt_index])
        else:
            lines.append('help string not available.')
        lines.append('')
        self._io.display(lines)

    def _evaluate_test(self, test, argument):
        if isinstance(test, types.TypeType):
            return isinstance(argument, test)
        else:
            return test(argument)

    def _get_value_from_direct_evaluation(self, user_response):
        try:
            value = eval(user_response)
        except (NameError, SyntaxError):
            value = user_response
        return value

    def _get_value_from_setup_statements(
        self, user_response, _setup_statements):
        for setup_statement in _setup_statements:
            try:
                command = setup_statement.format(user_response)
                exec(command)
            except:
                try:
                    command = setup_statement.format(repr(user_response))
                    exec(command)
                except:
                    self._display_help()
                    return '!!!'
        return value

    def _indent_and_number_prompt(self, prompt):
        if self.number_prompts:
            prompt_number = self.prompt_index + 1
            total_prompts = len(self._prompt_strings)
            prompt = '({}/{}) {}'.format(prompt_number, total_prompts, prompt)
        return prompt

    def _load_prompt(self):
        prompt = self._prompt_strings[self.prompt_index]
        if self.capitalize_prompts:
            prompt = stringtools.capitalize_string_start(prompt)
        self._menu_lines.append(prompt)

    def _move_to_prev_prompt(self):
        self.values.pop()
        self.prompt_index = self.prompt_index - 1

    def _present_prompt_and_store_value(self, include_chevron=True):
        '''True when user response obtained. Or when user skips prompt.
        False when user quits system or aborts getter.
        '''
        self._load_prompt()
        while True:
            prompt = self._menu_lines[-1]
            default = str(self._default_values[self.prompt_index])
            include_chevron = self._chevron_inclusion_indicators[self.prompt_index]
            prompt = self._indent_and_number_prompt(prompt)
            user_response = self._io.handle_raw_input_with_default(
                prompt, 
                default=default,
                include_chevron=include_chevron, 
                include_newline=self.include_newlines,
                prompt_character=self.prompt_character, 
                capitalize_prompt=self.capitalize_prompts)
            if user_response is None:
                self.prompt_index = self.prompt_index + 1
                break
            user_response = self._handle_hidden_menu_section_return_value(
                user_response)
            if self._session.backtrack():
                return False
            elif user_response is None:
                continue
            elif user_response == 'help':
                self._display_help()
            elif user_response == 'prev':
                self._move_to_prev_prompt()
                break
            elif user_response == 'skip':
                break
            elif isinstance(user_response, str):
                if self._store_value(user_response):
                    break
            else:
                self._io.print_not_yet_implemented()
        return True

    def _present_prompts_and_store_values(self, include_chevron=True):
        self._clear_terminal()
        self._menu_lines, self.values, self.prompt_index = [], [], 0
        while self.prompt_index < len(self._prompt_strings):
            if not self._present_prompt_and_store_value(
                include_chevron=include_chevron):
                break

    def _run(self, user_input=None, include_chevron=True):
        self._io.assign_user_input(user_input=user_input)
        with self.backtracking:
            self._present_prompts_and_store_values(
                include_chevron=include_chevron)
        if len(self.values) == 1:
            return self.values[0]
        else:
            return self.values

    def _store_value(self, user_response):
        assert isinstance(user_response, str)
        if self.allow_none and user_response in ('', 'None'):
            value = None
        else:
            if self._try_to_store_value_from_argument_list(user_response):
                return True
            value = self._change_user_response_to_value(user_response)
            if value == '!!!':
                return False
            if not self._apply__validation_functions_to_value(value):
                self._display_help()
                return False
        self.values.append(value)
        self.prompt_index = self.prompt_index + 1
        return True

    def _store_value_from_argument_list(self, user_response, argument_list):
        from experimental.tools import scoremanagertools
        dummy_section = scoremanagertools.menuing.MenuSection()
        dummy_section.is_numbered = True
        dummy_section._is_dummy = True
        dummy_section.menu_entries = argument_list
        value = dummy_section._argument_range_string_to_numbers(
            user_response)
        self.values.append(value)
        self.prompt_index = self.prompt_index + 1

    def _try_to_store_value_from_argument_list(self, user_response):
        argument_list = self._argument_lists[self.prompt_index]
        if argument_list and self._apply__validation_functions_to_value(
            user_response):
            self._store_value_from_argument_list(user_response, argument_list)
            return True
        else:
            return False
