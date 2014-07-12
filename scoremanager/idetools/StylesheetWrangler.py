# -*- encoding: utf-8 -*-
from scoremanager.idetools.FileWrangler import FileWrangler


class StylesheetWrangler(FileWrangler):
    r'''Stylesheet wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.idetools.Session()
            >>> wrangler = scoremanager.idetools.StylesheetWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            StylesheetWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import idetools
        superclass = super(StylesheetWrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = \
            self._configuration.example_stylesheets_directory
        self._asset_identifier = 'stylesheet'
        self._basic_breadcrumb = 'stylesheets'
        self._extension = '.ily'
        self._in_library = True
        self._score_storehouse_path_infix_parts = ('stylesheets',)
        self._user_storehouse_path = \
            self._configuration.stylesheets_library

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_stylesheets = False

    @staticmethod
    def _file_name_callback(file_name):
        file_name = file_name.replace(' ', '-')
        file_name = file_name.replace('_', '-')
        return file_name

    def _is_valid_directory_entry(self, directory_entry):
        superclass = super(StylesheetWrangler, self)
        if superclass._is_valid_directory_entry(directory_entry):
            if directory_entry.endswith('.ily'):
                return True
        return False