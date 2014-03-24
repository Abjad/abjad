# -*- encoding: utf-8 -*-
from scoremanager.wranglers.Wrangler import Wrangler


class FileWrangler(Wrangler):
    r'''File wrangler.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        Wrangler.__init__(self, session=session)