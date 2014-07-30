# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from scoremanager.idetools.Controller import Controller
from scoremanager.idetools.PromptMakerMixin import PromptMakerMixin


class Getter(Controller, PromptMakerMixin):
    r'''Getter.
    '''

    ### CLASS VARIABLES ###

    # multiple inheritance breaks slots
    __slots__ = (
        '_all_prompts_are_done',
        '_allow_none',
        '_capitalize_prompts',
        '_current_prompt_is_done',
        '_evaluated_input',
        '_include_newlines',
        '_include_chevron',
        '_number_prompts',
        '_prompt_character',
        '_prompt_index',
        '_messages',
        '_prompts',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        session=None,
        allow_none=False,
        capitalize_prompts=True,
        include_chevron=True,
        include_newlines=False,
        number_prompts=False,
        prompt_character=']>',
        ):
        Controller.__init__(self, session=session)
        PromptMakerMixin.__init__(self)
        self._prompts = []
        self._allow_none = allow_none
        self._capitalize_prompts = capitalize_prompts
        self._include_chevron = include_chevron
        self._include_newlines = include_newlines
        self._number_prompts = number_prompts
        self._prompt_character = prompt_character

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Gets format of user input getter.

        Returns string.
        '''
        return repr(self)

    def __len__(self):
        r'''Gets number of prompts in user input getter menu.

        Returns nonnegative integer.
        '''
        return len(self.prompts)

    def __repr__(self):
        r'''Gets interpreter representation of user input getter.

        Returns string.
        '''
        return '<{} ({})>'.format(type(self).__name__, len(self))

    def __str__(self):
        r'''Gets string representation of user input getter.

        Returns string.
        '''
        return repr(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _current_prompt(self):
        return self.prompts[self._prompt_index]

    ### PRIVATE METHODS ###

    def _evaluate_input(self, input_, namespace):
        section = self._current_prompt.target_menu_section
        setup_statements = self._current_prompt.setup_statements
        if 'evaluated_input' in namespace:
            del(namespace['evaluated_input'])
        if self.allow_none and input_ in ('', 'None'):
            namespace['evaluated_input'] = None
        elif section is not None:
            evaluated_input = section._argument_range_string_to_numbers(
                input_)
            if (1 < len(evaluated_input) and
                self._current_prompt.disallow_range):
                evaluated_input = None
            namespace['evaluated_input'] = evaluated_input
        elif setup_statements:
            for setup_statement in self._current_prompt.setup_statements:
                try:
                    command = setup_statement.format(input_)
                    exec(command, namespace, namespace)
                    continue
                except (NameError, SyntaxError):
                    pass
                try:
                    command = setup_statement.format(repr(input_))
                    exec(command, namespace, namespace)
                except ValueError:
                    self.display_help()
        else:
            try:
                namespace['evaluated_input'] = eval(
                    input_, namespace, namespace)
            except (NameError, SyntaxError):
                namespace['evaluated_input'] = input_
        if not 'evaluated_input' in namespace:
            return
        if not self._validate_evaluated_input(namespace['evaluated_input']):
            self.display_help()
            return
        self._evaluated_input.append(namespace['evaluated_input'])
        self._prompt_index += 1
        self._current_prompt_is_done = True

    def _indent_and_number_message(self, message):
        if self.number_prompts:
            prompt_number = self._prompt_index + 1
            message = '({}/{}) {}'.format(
                prompt_number, len(self), message)
        return message

    def _load_message(self):
        message = self._current_prompt.message
        if self.capitalize_prompts:
            message = stringtools.capitalize_start(message)
        self._messages.append(message)

    def _move_to_previous_prompt(self):
        self._evaluated_input.pop()
        self._prompt_index = self._prompt_index - 1

    def _present_prompt(self, include_chevron=True):
        self._load_message()
        self._current_prompt_is_done = False
        namespace = {}
        while not self._current_prompt_is_done:
            message = self._messages[-1]
            message = self._indent_and_number_message(
                message)
            default_value = str(self._current_prompt.default_value)
            include_chevron = self._current_prompt.include_chevron
            input_ = self._io_manager._handle_input(
                message,
                default_value=default_value,
                include_chevron=include_chevron,
                include_newline=self.include_newlines,
                prompt_character=self.prompt_character,
                capitalize_prompt=self.capitalize_prompts,
                )
            if input_.endswith('!') and self._session.is_autoadding:
                input_ = input_.strip('!')
                self._session._is_autoadding = False
                self._session._pending_done = True
            elif input_.endswith('/'):
                is_autoadvancing = self._session.is_autoadvancing
                if is_autoadvancing:
                    self._session._autoadvance_depth = 0
                else:
                    self._session._autoadvance_depth = 1
                input_ = input_.strip('/')
            if input_ is None:
                self._prompt_index += 1
                break
            elif input_ == '?':
                self.display_help()
                continue
            elif input_ in self._command_to_method:
                self._command_to_method[input_]()
            assert isinstance(input_, str), repr(input_)
            directive = input_
            if self._session.is_backtracking:
                self._current_prompt_is_done = True
                self._all_prompts_are_done = True
                self._session._pending_redraw = True
            elif directive is None:
                continue
            elif directive == 'help':
                self.display_help()
            elif directive == 'previous':
                self._move_to_previous_prompt()
                break
            elif directive == 'skip':
                break
            elif isinstance(directive, str):
                self._evaluate_input(directive, namespace)
            else:
                self._io_manager._display_not_yet_implemented()

    def _present_prompts(self, include_chevron=True):
        self._prompt_index = 0
        self._messages = []
        self._evaluated_input = []
        self._all_prompts_are_done = False
        while (self._prompt_index < len(self) and
            not self._all_prompts_are_done):
            self._present_prompt(include_chevron=include_chevron)

    def _run(self, clear_terminal=False, title=False):
        with self._io_manager._controller(
            consume_local_backtrack=True,
            controller=self,
            is_in_confirmation_environment=True,
            ):
            self._present_prompts(include_chevron=self._include_chevron)
            if len(self._evaluated_input) == 1:
                result = self._evaluated_input[0]
            else:
                result = self._evaluated_input[:]
            if result == []:
                result = None
            return result

    def _validate_evaluated_input(self, evaluated_input):
        if evaluated_input is None and self.allow_none:
            return True
        validation_function = self._current_prompt.validation_function
        try:
            return validation_function(evaluated_input)
        except TypeError:
            return False

    ### PUBLIC PROPERTIES ###

    @property
    def allow_none(self):
        r'''Is true when user input getter allows none.
        Otherwise false.

        Returns boolean.
        '''
        return self._allow_none

    @property
    def capitalize_prompts(self):
        r'''Is true when user input getter capitalizes prompts.
        Otherwise false.

        Returns boolean.
        '''
        return self._capitalize_prompts


    @property
    def include_chevron(self):
        r'''Is true when user input getter incldues chevron.
        Otherwise false.

        Returns boolean.
        '''
        return self._include_chevron

    @property
    def include_newlines(self):
        r'''Is true when user input getter incldues newlines.
        Otherwise false.

        Returns boolean.
        '''
        return self._include_newlines

    @property
    def number_prompts(self):
        r'''Is true when user input getter numbers prompts.
        Otherwise false.

        Returns boolean.
        '''
        return self._number_prompts

    @property
    def prompt_character(self):
        r'''Gets user input getter prompt character.

        Returns string.
        '''
        return self._prompt_character

    @property
    def prompts(self):
        r'''Gets user input getter prompts.

        Returns list of prompts.
        '''
        return self._prompts

    ### PUBLIC METHODS ###

    def display_help(self):
        r'''Displays help.

        Returns none.
        '''
        lines = []
        lines.append(self._current_prompt.help_string)
        lines.append('')
        self._io_manager._display(lines)