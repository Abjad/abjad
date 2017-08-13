from abjad.tools import abctools


class CodeBlockSpecifier(abctools.AbjadValueObject):
    r'''A code block specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Internals'

    __slots__ = (
        '_allow_exceptions',
        '_hide',
        '_strip_prompt',
        '_text_width',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        allow_exceptions=None,
        hide=None,
        strip_prompt=None,
        text_width=None,
        ):
        self._allow_exceptions = bool(allow_exceptions) or None
        self._hide = bool(hide) or None
        self._strip_prompt = bool(strip_prompt) or None
        if text_width is not None:
            if text_width is True:
                text_width = 80
            try:
                text_width = int(text_width)
                if text_width < 1:
                    text_width = None
            except:
                text_width = None
        self._text_width = text_width

    ### PUBLIC METHODS ###

    @classmethod
    def from_options(cls, **options):
        r'''Creates code block specifier from `options` dictionary.

        Returns code block specifier.
        '''
        allow_exceptions = None
        if 'allow_exceptions' in options:
            allow_exceptions = options.pop('allow_exceptions')
        hide = None
        if 'hide' in options:
            hide = options.pop('hide')
        strip_prompt = None
        if 'strip_prompt' in options:
            strip_prompt = options.pop('strip_prompt')
        text_width = None
        if 'text_width' in options:
            text_width = options.pop('text_width')
        if all(_ is None for _ in (
            allow_exceptions,
            hide,
            strip_prompt,
            text_width,
            )):
            return None, options
        return cls(
            allow_exceptions=allow_exceptions,
            hide=hide,
            strip_prompt=strip_prompt,
            text_width=text_width,
            ), options

    ### PUBLIC PROPERTIES ###

    @property
    def allow_exceptions(self):
        r'''Is true if code block allows exceptions. Otherwise false.

        Returns true or false.
        '''
        return self._allow_exceptions

    @property
    def hide(self):
        r'''Is true if code block should be hidden. Otherwise false.

        Returns true or false.
        '''
        return self._hide

    @property
    def strip_prompt(self):
        r'''Is true if code block should strip Python prompt from output.
        Otherwise false.

        Returns true or false.
        '''
        return self._strip_prompt

    @property
    def text_width(self):
        r'''Gets text width wrap of code block.

        Returns integer or none.
        '''
        return self._text_width
