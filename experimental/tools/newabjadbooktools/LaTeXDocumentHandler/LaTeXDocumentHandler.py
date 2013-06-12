from experimental.tools.newabjadbooktools.TextualDocumentHandler import TextualDocumentHandler


class LaTeXDocumentHandler(TextualDocumentHandler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def image_format(self):
        from experimental.tools import newabjadbooktools
        return newabjadbooktools.PDFImageFormat()
