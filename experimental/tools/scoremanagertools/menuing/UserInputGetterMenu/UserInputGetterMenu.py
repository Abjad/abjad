import types
from abjad.tools import stringtools
from experimental.tools.scoremanagertools import predicates
from experimental.tools.scoremanagertools.menuing.Menu import Menu
from experimental.tools.scoremanagertools.menuing.UserInputGetterMixin \
    import UserInputGetterMixin


class UserInputEvaluationError(Exception):
    pass


class UserInputGetterMenu(Menu, UserInputGetterMixin):
    '''User input getter menu.

    .. note:: add docstring.

    Return user input getter.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None, where=None):
        Menu.__init__(self, session=session, where=where)
        UserInputGetterMixin.__init__(self)
        self._prompts = []
        self.allow_none = False
        self.capitalize_prompts = True
        self.include_newlines = False
        self.number_prompts = False
        self.prompt_character = '>'

    ### SPECIAL METHODS ###

    def __len__(self):
        '''Number of prompts in user input getter menu.

        Return nonnegative integer.
        '''
        return len(self.prompts)
        
    def __repr__(self):
        '''Interpreter representation of user input getter.

        Return string.
        '''
        return '<{} ({})>'.format(type(self).__name__, len(self))

    ### PRIVATE PROPERTIES ###

    @property
    def _current_prompt(self):
        return self.prompts[self._prompt_index]

    ### PRIVATE METHODS ###

    def _display_help(self):
        lines = []
        lines.append(self._current_prompt.help_string)
        lines.append('')
        self._io.display(lines)

    def _evaluate_and_store_user_input(self, user_input):
        try:
            evaluated_user_input = self._evaluate_user_input(user_input)
        except UserInputEvaluationError:
            return
        if not self._validate_evaluated_user_input(evaluated_user_input):
            self._display_help()
            return
        self._evaluated_user_input.append(evaluated_user_input)
        self._prompt_index += 1
        self._is_done = True

    def _evaluate_user_input(self, user_input):
        evaluated_user_input = None
        target_menu_section = self._current_prompt.target_menu_section
        setup_statements = self._current_prompt.setup_statements
        if self.allow_none and user_input in ('', 'None'):
            evaluated_user_input = None
        elif target_menu_section is not None:
            evaluated_user_input = \
                target_menu_section._argument_range_string_to_numbers(
                user_input)
        elif setup_statements:
            for setup_statement in self._current_prompt.setup_statements:
                try:
                    command = setup_statement.format(user_input)
                    exec(command)
                    continue
                except (NameError, SyntaxError):
                    pass
                try:
                    command = setup_statement.format(repr(user_input))
                    exec(command)
                except ValueError:
                    self._display_help()
                    raise UserInputEvaluationError
        else:
            try:
                evaluated_user_input = eval(user_input)
            except (NameError, SyntaxError):
                evaluated_user_input = user_input
        return evaluated_user_input

    def _indent_and_number_prompt_string(self, prompt_string):
        if self.number_prompts:
            prompt_number = self._prompt_index + 1
            prompt_string = '({}/{}) {}'.format(
                prompt_number, len(self), prompt_string)
        return prompt_string

    def _load_prompt_string(self):
        prompt_string = self._current_prompt.prompt_string
        if self.capitalize_prompts:
            prompt_string = stringtools.capitalize_string_start(prompt_string)
        self._prompt_strings.append(prompt_string)

    def _move_to_prev_prompt(self):
        self._evaluated_user_input.pop()
        self._prompt_index = self._prompt_index - 1

    def _present_prompt_and_store_evaluated_user_input(
        self, include_chevron=True):
        '''True when user response obtained. Or when user skips prompt.
        False when user quits system or aborts getter.
        '''
        self._load_prompt_string()
        self._is_done = False
        while not self._is_done:
            prompt_string = self._prompt_strings[-1]
            prompt_string = self._indent_and_number_prompt_string(
                prompt_string)
            default_value = str(self._current_prompt.default_value)
            include_chevron = self._current_prompt.include_chevron
            user_input = self._io.handle_raw_input_with_default(
                prompt_string, 
                default_value=default_value,
                include_chevron=include_chevron, 
                include_newline=self.include_newlines,
                prompt_character=self.prompt_character, 
                capitalize_prompt=self.capitalize_prompts)
            if user_input is None:
                self._prompt_index += 1
                break
            user_input = self._handle_hidden_menu_section_return_value(
                user_input)
            if self._session.backtrack():
                return False
            elif user_input is None:
                continue
            elif user_input == 'help':
                self._display_help()
            elif user_input == 'prev':
                self._move_to_prev_prompt()
                break
            elif user_input == 'skip':
                break
            elif isinstance(user_input, str):
                self._evaluate_and_store_user_input(user_input)
            else:
                self._io.print_not_yet_implemented()
        return True

    def _present_prompts_and_store_evaluated_user_inputs(
        self, include_chevron=True):
        self._clear_terminal()
        self._prompt_index = 0
        self._prompt_strings = []
        self._evaluated_user_input = []
        while self._prompt_index < len(self):
            if not self._present_prompt_and_store_evaluated_user_input(
                include_chevron=include_chevron):
                break

    def _run(self, user_input=None, include_chevron=True):
        self._io.assign_user_input(user_input=user_input)
        with self.backtracking:
            self._present_prompts_and_store_evaluated_user_inputs(
                include_chevron=include_chevron)
        if len(self._evaluated_user_input) == 1:
            return self._evaluated_user_input[0]
        return self._evaluated_user_input[:]

    def _validate_evaluated_user_input(self, evaluated_user_input):
        if evaluated_user_input is None and self.allow_none:
            return True
        validation_function = self._current_prompt.validation_function
        return validation_function(evaluated_user_input)

    ### PUBLIC PROPERTIES ###

    @apply
    def allow_none():
        def fget(self):
            return self._allow_none
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._allow_none = expr
        return property(**locals())

    @apply
    def capitalize_prompts():
        def fget(self):
            return self._capitalize_prompts
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._capitalize_prompts = expr
        return property(**locals())

    @apply
    def include_newlines():
        def fget(self):
            return self._include_newlines
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._include_newlines = expr
        return property(**locals())

    @apply
    def number_prompts():
        def fget(self):
            return self._number_prompts
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._number_prompts = expr
        return property(**locals())

    @property
    def prompts(self):
        return self._prompts

    @apply
    def prompt_character():
        def fget(self):
            return self._prompt_character
        def fset(self, expr):
            assert isinstance(expr, str)
            self._prompt_character = expr
        return property(**locals())
