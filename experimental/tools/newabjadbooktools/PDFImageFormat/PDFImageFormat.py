from experimental.tools.newabjadbooktools.ImageFormat import ImageFormat


class PDFImageFormat(ImageFormat):

    @property
    def file_extension(self):
        return 'pdf'
