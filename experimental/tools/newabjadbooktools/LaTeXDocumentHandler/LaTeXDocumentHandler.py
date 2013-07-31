# -*- encoding: utf-8 -*-
from experimental.tools.newabjadbooktools.TextualDocumentHandler \
    import TextualDocumentHandler


class LaTeXDocumentHandler(TextualDocumentHandler):

    ### PUBLIC PROPERTIES ###

    @property
    def image_format(self):
        from experimental.tools import newabjadbooktools
        return newabjadbooktools.PDFImageFormat()
