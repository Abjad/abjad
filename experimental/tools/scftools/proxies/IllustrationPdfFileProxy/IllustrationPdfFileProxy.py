from experimental.tools.scftools.proxies.FileProxy import FileProxy
import os


class IllustrationPdfFileProxy(FileProxy):

    ### READ-ONLY PROPERTIES ###

    @property
    def extension(self):
        return '.pdf'

    ### PUBLIC METHODS ###

    def view(self):
        command = 'open {}'.format(self.path_name)
        os.system(command)
