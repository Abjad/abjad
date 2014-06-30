# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class Prompt(AbjadObject):
    r'''Prompt.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_value',
        '_disallow_range',
        '_help_template',
        '_help_template_arguments',
        '_include_chevron',
        '_message',
        '_setup_statements',
        '_target_menu_section',
        '_validation_function',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        default_value=None,
        disallow_range=False,
        help_template=None,
        help_template_arguments=None,
        include_chevron=True,
        message=None,
        setup_statements=None,
        target_menu_section=None,
        validation_function=None,
        ):
        AbjadObject.__init__(self)
        assert isinstance(message, str)
        assert isinstance(help_template, str)
        self._default_value = default_value
        self._disallow_range = disallow_range
        self._help_template = help_template
        self._help_template_arguments = help_template_arguments or []
        self._include_chevron = include_chevron
        self._message = message
        self._setup_statements = setup_statements or []
        self._target_menu_section = target_menu_section
        self._validation_function = validation_function

    ### PUBLIC PROPERTIES ###

    @property
    def default_value(self):
        r'''Gets default value of prompt.

        Returns object.
        '''
        return self._default_value

    @property
    def disallow_range(self):
        r'''Is true when prompt disallows argument range.

        Returns boolean.
        '''
        return self._disallow_range

    @property
    def help_string(self):
        r'''Gets help string of prompt.

        Returns string.
        '''
        result = self.help_template.format(
            self.message,
            *self.help_template_arguments
            )
        return result

    @property
    def help_template(self):
        r'''Gets help template of prompt.

        Returns something.
        '''
        return self._help_template

    @property
    def help_template_arguments(self):
        r'''Gets help template arugments of prompt.

        Returns list.
        '''
        return self._help_template_arguments

    @property
    def include_chevron(self):
        r'''Is true when prompt includes chevron. Otherwise false.

        Returns boolean.
        '''
        return self._include_chevron

    @property
    def message(self):
        r'''Gets prompt string.

        Returns string.
        '''
        return self._message

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