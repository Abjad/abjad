import os
from experimental.tools.scoremanagertools.proxies.FileProxy import FileProxy


class IllustrationPdfFileProxy(FileProxy):

    ### CLASS VARIABLES ###

    extension = '.pdf'

    ### PUBLIC METHODS ###

    def interactively_view(self):
        command = 'open {}'.format(self.filesystem_path)
        os.system(command)
