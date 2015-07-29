# -*- encoding: utf-8 -*-
from abjad.tools import abctools


class ImageSpecifier(abctools.AbjadValueObject):
    r'''An image specifier.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_no_trim',
        '_no_stylesheet',
        '_pages',
        '_stylesheet',
        '_with_columns',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        no_trim=None,
        no_stylesheet=None,
        pages=None,
        stylesheet=None,
        with_columns=None,
        ):
        self._no_trim = bool(no_trim) or None
        self._no_stylesheet = bool(no_stylesheet) or None
        self._pages = pages or None
        self._stylesheet = stylesheet
        if with_columns < 1:
            with_columns = None
        self._with_columns = with_columns or None

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