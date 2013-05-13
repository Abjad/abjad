import os
from experimental.tools.scoremanagertools.proxies.FileProxy import FileProxy


class IllustrationPdfFileProxy(FileProxy):

    ### CLASS ATTRIBUTES ###

    extension = '.pdf'

    ### PUBLIC METHODS ###

    def view(self):
        command = 'open {}'.format(self.file_path)
        os.system(command)
