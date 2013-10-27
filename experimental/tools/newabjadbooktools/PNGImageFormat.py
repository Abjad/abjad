# -*- encoding: utf-8 -*-
from experimental.tools.newabjadbooktools.ImageFormat import ImageFormat


class PNGImageFormat(ImageFormat):

    @property
    def file_extension(self):
        return 'png'
