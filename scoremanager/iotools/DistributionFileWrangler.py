# -*- encoding: utf-8 -*-
from scoremanager.iotools.FileWrangler import FileWrangler


class DistributionFileWrangler(FileWrangler):
    r'''Distribution wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.iotools.Session()
            >>> wrangler = scoremanager.iotools.DistributionFileWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            DistributionFileWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import iotools
        superclass = super(DistributionFileWrangler, self)
        superclass.__init__(session=session)
        self._basic_breadcrumb = 'distribution files'
        self._score_storehouse_path_infix_parts = ('distribution',)

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_score_distribution_files = False