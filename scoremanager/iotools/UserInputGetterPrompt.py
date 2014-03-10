# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class UserInputGetterPrompt(AbjadObject):
    r'''User input getter prompt.

    Returns user input getter prompt.
    '''

    ### INITIALIZER ###

    def __init__(self, 
        prompt_string, 
        additional_help_template_arguments=None, 
        default_value=None, 
        help_template=None,
        include_chevron=True,
        setup_statements=None,
        target_menu_section=None,
        validation_function=None,
        ):
        AbjadObject.__init__(self)
        assert isinstance(prompt_string, str)
        assert isinstance(help_template, str)
        self._prompt_string = prompt_string
        self._additional_help_template_arguments = \
            additional_help_template_arguments or []
        self._default_value = default_value
        self._help_template = help_template
        self._include_chevron = include_chevron
        self._setup_statements = setup_statements or []
        self._target_menu_section = target_menu_section
        self._validation_function = validation_function

    ### PUBLIC PROPERTIES ###

    @property
    def additional_help_template_arguments(self):
        r'''Gets additional help template arugments of prompt.

        Returns list.
        '''
        return self._additional_help_template_arguments

    @property
    def default_value(self):
        r'''Gets default value of prompt.

        Returns object.
        '''
        return self._default_value

    @property
    def help_string(self):
        r'''Gets help string of prompt.

        Returns string.
        '''
        result = self.help_template.format(
            self.prompt_string,
            *self.additional_help_template_arguments
            )
        return result

    @property
    def help_template(self):
        r'''Gets help template of prompt.

        Returns something.
        '''
        return self._help_template

    @property
    def include_chevron(self):
        r'''Is true when prompt includes chevron. Otherwise false.

        Returns boolean.
        '''
        return self._include_chevron

    @property
    def prompt_string(self):
        r'''Gets prompt string.

        Returns string.
        '''
        return self._prompt_string

    @property
    def setup_statements(self):
        r'''Gets setup statements.

        Returns list of strings.
        '''
        return self._setup_statements

    @property
    def target_menu_section(self):
        r'''Gets target menu section of prompt.
        '''
        return self._target_menu_section

    @property
    def validation_function(self):
        r'''Gets validation function of prompt.

        Returns callable.
        '''
        return self._validation_function
