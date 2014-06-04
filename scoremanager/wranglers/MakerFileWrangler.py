# -*- encoding: utf-8 -*-
from scoremanager.wranglers.FileWrangler import FileWrangler


class MakerFileWrangler(FileWrangler):
    r'''Maker file wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> wrangler = scoremanager.wranglers.MakerFileWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            MakerFileWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(MakerFileWrangler, self)
        superclass.__init__(session=session)
        self._basic_breadcrumb = 'maker files'
        self._extension = '.py'
        self._force_lowercase = False
        self._score_storehouse_path_infix_parts = ('makers',)
        self._user_storehouse_path = \
            self._configuration.user_library_makers_directory

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_score_maker_files = False