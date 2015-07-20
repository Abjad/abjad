import abjadbook


def setup(app):
    abjadbook.DoctreeDocumentHandler.setup_sphinx_extension(app)