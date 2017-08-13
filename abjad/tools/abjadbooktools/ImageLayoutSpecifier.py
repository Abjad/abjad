from abjad.tools import abctools


class ImageLayoutSpecifier(abctools.AbjadValueObject):
    r'''An image layout specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Internals'

    __slots__ = (
        '_pages',
        '_with_columns',
        '_with_thumbnail',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pages=None,
        with_columns=None,
        with_thumbnail=None,
        ):
        self._pages = pages or None
        if with_columns is not None:
            with_columns = int(with_columns)
            if with_columns < 1:
                with_columns = None
        self._with_columns = with_columns or None
        self._with_thumbnail = with_thumbnail or None

    ### PUBLIC METHODS ###

    @classmethod
    def from_options(cls, **options):
        r'''Creates image specifier from `options` dictionary.

        Returns image specifier.
        '''
        pages = None
        if 'pages' in options:
            pages = options.pop('pages')
        with_columns = None
        if 'with_columns' in options:
            with_columns = options.pop('with_columns')
        with_thumbnail = None
        if 'with_thumbnail' in options:
            with_thumbnail = options.pop('with_thumbnail')
        if all(_ is None for _ in (
            pages,
            with_columns,
            with_thumbnail,
            )):
            return None, options
        return cls(
            pages=pages,
            with_columns=with_columns,
            with_thumbnail=with_thumbnail,
            ), options

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

    @property
    def with_thumbnail(self):
        r'''Is true if image should have a thumbnail.

        Returns true or false.
        '''
        return self._with_thumbnail
