from abjad.tools import abctools


class ImageRenderSpecifier(abctools.AbjadValueObject):
    r'''An image render specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Internals'

    __slots__ = (
        '_no_resize',
        '_no_stylesheet',
        '_no_trim',
        '_stylesheet',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        no_resize=None,
        no_stylesheet=None,
        no_trim=None,
        stylesheet=None,
        ):
        self._no_resize = bool(no_resize) or None
        self._no_stylesheet = bool(no_stylesheet) or None
        self._no_trim = bool(no_trim) or None
        self._stylesheet = stylesheet
        if self._no_stylesheet:
            self._stylesheet = None

    ### PUBLIC METHODS ###

    @classmethod
    def from_options(cls, **options):
        r'''Creates image specifier from `options` dictionary.

        Returns image specifier.
        '''
        no_resize = None
        if 'no_resize' in options:
            no_resize = options.pop('no_resize')
        no_stylesheet = None
        if 'no_stylesheet' in options:
            no_stylesheet = options.pop('no_stylesheet')
        no_trim = None
        if 'no_trim' in options:
            no_trim = options.pop('no_trim')
        stylesheet = None
        if 'stylesheet' in options:
            stylesheet = options.pop('stylesheet')
        if all(_ is None for _ in (
            no_resize,
            no_stylesheet,
            no_trim,
            stylesheet,
            )):
            return None, options
        return cls(
            no_resize=no_resize,
            no_stylesheet=no_stylesheet,
            no_trim=no_trim,
            stylesheet=stylesheet,
            ), options

    ### PUBLIC PROPERTIES ###

    @property
    def no_resize(self):
        r'''Is true if image should not be resized.
        Otherwise false.

        Returns true or false.
        '''
        return self._no_resize

    @property
    def no_stylesheet(self):
        r'''Is true if no stylesheet should be used with image at all.
        Otherwise false.

        Returns true or false.
        '''
        return self._no_stylesheet

    @property
    def no_trim(self):
        r'''Is true if image should not be trimmed of whitespace. Otherwise
        false.

        Returns true or false.
        '''
        return self._no_trim

    @property
    def stylesheet(self):
        r'''Gets stylesheet name to be used for image.

        Returns string or none.
        '''
        return self._stylesheet
