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
        self._chevrons = []
        self._defaults = []
        self._execs = []
        self._helps = []
        self._prompts = []
        self._tests = []
        self.allow_none = False
        self.capitalize_prompts = True
        self.include_newlines = False
        self.indent_level = 0
        self.number_prompts = False
        self.prompt_character = '>'

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, len(self.prompts))

    ### PRIVATE METHODS ###

    def _run(self, user_input=None, include_chevron=True):
        self._io.assign_user_input(user_input=user_input)
        with self.backtracking:
            self.present_prompts_and_store_values(
                include_chevron=include_chevron)
        if len(self.values) == 1:
            return self.values[0]
        else:
            return self.values

    ### PUBLIC PROPERTIES ###

    @property
    def argument_lists(self):
        return self._argument_lists

    @property
    def chevrons(self):
        return self._chevrons

    @property
    def defaults(self):
        return self._defaults

    @property
    def execs(self):
        return self._execs

    @property
    def helps(self):
        return self._helps

    @property
    def prompts(self):
        return self._prompts

    @property
    def tests(self):
        return self._tests

    ### PUBLIC METHODS ###

    def apply_tests_to_value(self, value):
        if self.allow_none and value is None:
            return True
        if self.prompt_index < len(self.tests):
            input_test = self.tests[self.prompt_index]
            return self.evaluate_test(input_test, value)
        return True

    def change_user_response_to_value(self, user_response):
        execs = self.execs[self.prompt_index]
        assert isinstance(execs, list)
        if execs:
            value = self.get_value_from_execs(user_response, execs)
            if value is None and not user_response == 'None':
                return '!!!'
        else:
            value = self.get_value_from_direct_evaluation(user_response)
        return value

    def display_help(self):
        if self.prompt_index < len(self.helps):
            lines = []
            lines.append(self.helps[self.prompt_index])
            lines.append('')
            self._io.display(lines)

    def display_help(self):
        lines = []
        if self.prompt_index < len(self.helps):
            lines.append(self.helps[self.prompt_index])
        else:
            lines.append('help string not available.')
        lines.append('')
        self._io.display(lines)

    def evaluate_test(self, test, argument):
        if isinstance(test, types.TypeType):
            return isinstance(argument, test)
        else:
            return test(argument)

    def get_value_from_direct_evaluation(self, user_response):
        try:
            value = eval(user_response)
        except (NameError, SyntaxError):
            value = user_response
        return value

    def get_value_from_execs(self, user_response, execs):
        for exec_string in execs:
            try:
                command = exec_string.format(user_response)
                exec(command)
            except:
                try:
                    command = exec_string.format(repr(user_response))
                    exec(command)
                except:
                    self.display_help()
                    return '!!!'
        return value

    def indent_and_number_prompt(self, prompt):
        if self.number_prompts:
            prompt_number = self.prompt_index + 1
            total_prompts = len(self.prompts)
            prompt = '({}/{}) {}'.format(prompt_number, total_prompts, prompt)
        if self.indent_level:
            return '{} {}'.format(self._make_tab(self.indent_level), prompt)
        else:
            return prompt

    def load_prompt(self):
        prompt = self.prompts[self.prompt_index]
        if self.capitalize_prompts:
            prompt = stringtools.capitalize_string_start(prompt)
        self._menu_lines.append(prompt)

    def make_is_integer_in_range(self, 
        start=None, stop=None, allow_none=False):
        return lambda expr: (expr is None and allow_none) or \
            (predicates.is_integer(expr) and
            (start is None or start <= expr) and
            (stop is None or expr <= stop))

    def move_to_prev_prompt(self):
        self.values.pop()
        self.prompt_index = self.prompt_index - 1

    def present_prompt_and_store_value(self, include_chevron=True):
        '''True when user response obtained. Or when user skips prompt.
        False when user quits system or aborts getter.
        '''
        self.load_prompt()
        while True:
            prompt = self._menu_lines[-1]
            default = str(self.defaults[self.prompt_index])
            include_chevron = self.chevrons[self.prompt_index]
            prompt = self.indent_and_number_prompt(prompt)
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
            user_response = self.handle_hidden_menu_section_return_value(
                user_response)
            if self._session.backtrack():
                return False
            elif user_response is None:
                continue
            elif user_response == 'help':
                self.display_help()
            elif user_response == 'prev':
                self.move_to_prev_prompt()
                break
            elif user_response == 'skip':
                break
            elif isinstance(user_response, str):
                if self.store_value(user_response):
                    break
            else:
                self._io.print_not_yet_implemented()
        return True

    def present_prompts_and_store_values(self, include_chevron=True):
        self.conditionally_clear_terminal()
        self._menu_lines, self.values, self.prompt_index = [], [], 0
        while self.prompt_index < len(self.prompts):
            if not self.present_prompt_and_store_value(
                include_chevron=include_chevron):
                break

    def store_value(self, user_response):
        assert isinstance(user_response, str)
        if self.allow_none and user_response in ('', 'None'):
            value = None
        else:
            if self.try_to_store_value_from_argument_list(user_response):
                return True
            value = self.change_user_response_to_value(user_response)
            if value == '!!!':
                return False
            if not self.apply_tests_to_value(value):
                self.display_help()
                return False
        self.values.append(value)
        self.prompt_index = self.prompt_index + 1
        return True

    def store_value_from_argument_list(self, user_response, argument_list):
        from experimental.tools import scoremanagertools
        dummy_section = scoremanagertools.menuing.MenuSection()
        dummy_section.is_numbered = True
        dummy_section._is_dummy = True
        dummy_section.menu_entries = argument_list
        value = dummy_section._argument_range_string_to_numbers(
            user_response)
        self.values.append(value)
        self.prompt_index = self.prompt_index + 1

    def try_to_store_value_from_argument_list(self, user_response):
        input_test = self.tests[self.prompt_index]
        argument_list = self.argument_lists[self.prompt_index]
        if argument_list and self.apply_tests_to_value(user_response):
            self.store_value_from_argument_list(user_response, argument_list)
            return True
        else:
            return False
