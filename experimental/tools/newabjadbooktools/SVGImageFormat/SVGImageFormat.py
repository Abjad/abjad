from experimental.tools.newabjadbooktools.ImageFormat import ImageFormat


class SVGImageFormat(ImageFormat):

    @property
    def file_extension(self):
        return 'svg'
