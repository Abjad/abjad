from scf.proxies.FileProxy import FileProxy


class IllustrationLyFileProxy(FileProxy):

    ### READ-ONLY PROPERTIES ###

    @property
    def extension(self):
        return '.ly'
