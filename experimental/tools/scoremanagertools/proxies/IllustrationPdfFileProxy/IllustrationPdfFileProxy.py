import os
from experimental.tools.scoremanagertools.proxies.FileProxy import FileProxy


class IllustrationPdfFileProxy(FileProxy):

    ### READ-ONLY PROPERTIES ###

    @property
    def extension(self):
        return '.pdf'

    ### PUBLIC METHODS ###

    def view(self):
        command = 'open {}'.format(self.file_path)
        os.system(command)
