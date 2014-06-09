# -*- encoding: utf-8 -*-
import os
from abjad.tools import stringtools
from scoremanager.wranglers.FileWrangler import FileWrangler


class MakerFileWrangler(FileWrangler):
    r'''Maker file wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.iotools.Session()
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
        from scoremanager import wranglers
        superclass = super(MakerFileWrangler, self)
        superclass.__init__(session=session)
        self._basic_breadcrumb = 'maker files'
        self._extension = '.py'
        self._force_lowercase = False
        self._in_user_library = True
        self._score_storehouse_path_infix_parts = ('makers',)
        self._user_storehouse_path = \
            self._configuration.user_library_makers_directory

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_score_maker_files = False

    def _is_valid_directory_entry(self, directory_entry):
        name, extension = os.path.splitext(directory_entry)
        if stringtools.is_upper_camel_case(name):
            if extension == '.py':
                return True
        return False