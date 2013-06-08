import abc
from abjad.tools.abctools import AbjadObject


class ImageFormat(AbjadObject):
    '''An image format encapsulates the logic for saving and converting an
    image into its associated filetype.
    '''

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, source_file_path, destination_file_path):
        raise NotImplemented

