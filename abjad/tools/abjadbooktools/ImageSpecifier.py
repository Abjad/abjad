# -*- encoding: utf-8 -*-
from abjad.tools import abctools


class ImageSpecifier(abctools.AbjadValueObject):
    r'''An image specifier.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_no_stylesheet',
        '_no_trim',
        '_pages',
        '_stylesheet',
        '_with_columns',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        no_stylesheet=None,
        no_trim=None,
        pages=None,
        stylesheet=None,
        with_columns=None,
        ):
        self._no_stylesheet = bool(no_stylesheet) or None
        self._no_trim = bool(no_trim) or None
        self._pages = pages or None
        self._stylesheet = stylesheet
        if self._no_stylesheet:
            self._stylesheet = None
        if with_columns is not None:
            with_columns = int(with_columns)
            if with_columns < 1:
                with_columns = None
        self._with_columns = with_columns or None

    ### PUBLIC METHODS ###

    @classmethod
    def from_options(cls, **options):
        r'''Creates image specifier from `options` dictionary.

        Returns image specifier.
        '''
        no_stylesheet = options.get('no_stylesheet', None) or None
        no_trim = options.get('no_trim', None) or None
        pages = options.get('pages', None) or None
        stylesheet = options.get('stylesheet', None) or None
        with_columns = options.get('with_columns', None) or None
        if all(_ is None for _ in (
            no_stylesheet,
            no_trim,
            pages,
            stylesheet,
            with_columns,
            )):
            return None
        return cls(
            no_stylesheet=no_stylesheet,
            no_trim=no_trim,
            pages=pages,
            stylesheet=stylesheet,
            with_columns=with_columns,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def no_stylesheet(self):
        r'''Is true if no stylesheet should be used with image at all.
        Otherwise false.

        Returns boolean.
        '''
        return self._no_stylesheet

    @property
    def no_trim(self):
        r'''Is true if image should not be trimmed of whitespace. Otherwise
        false.

        Returns boolean.
        '''
        return self._no_trim

    @property
    def pages(self):
        r'''Gets page indices.

        Returns tuple of integers or none.
        '''
        return self._pages

    @property
    def stylesheet(self):
        r'''Gets stylesheet name to be used for image.

        Returns string or none.
        '''
        return self._stylesheet

    @property
    def with_columns(self):
        r'''Gets column count for table layout.

        Return integer or none.
        '''
        return self._with_columns