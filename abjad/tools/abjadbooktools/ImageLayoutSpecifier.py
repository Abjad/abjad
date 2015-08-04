# -*- encoding: utf-8 -*-
from abjad.tools import abctools


class ImageLayoutSpecifier(abctools.AbjadValueObject):
    r'''An image layout specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Internals'

    __slots__ = (
        '_pages',
        '_with_columns',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pages=None,
        with_columns=None,
        ):
        self._pages = pages or None
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
        pages = options.get('pages', None) or None
        with_columns = options.get('with_columns', None) or None
        if all(_ is None for _ in (
            pages,
            with_columns,
            )):
            return None
        return cls(
            pages=pages,
            with_columns=with_columns,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def pages(self):
        r'''Gets page indices.

        Returns tuple of integers or none.
        '''
        return self._pages

    @property
    def with_columns(self):
        r'''Gets column count for table layout.

        Return integer or none.
        '''
        return self._with_columns