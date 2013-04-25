from experimental.tools.scoremanagertools.proxies.FileProxy import FileProxy
import os


class IllustrationPdfFileProxy(FileProxy):

    ### READ-ONLY PROPERTIES ###

    @property
    def extension(self):
        return '.pdf'

    ### PUBLIC METHODS ###

    def view(self):
        command = 'open {}'.format(self.path)
        os.system(command)
