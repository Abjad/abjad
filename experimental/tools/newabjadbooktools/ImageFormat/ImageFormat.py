import abc
from abjad.tools.abctools import AbjadObject


class ImageFormat(AbjadObject):
    r'''An image format encapsulates the logic for saving and converting an
    image into its associated filetype.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def file_extension(self):
        raise NotImplemented
