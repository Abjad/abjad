import abc
import hashlib
from experimental.tools.newabjadbooktools.OutputProxy import OutputProxy


class AssetOutputProxy(OutputProxy):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def file_name_prefix(self):
        return self.__class__.__name__.partition('OutputProxy')[0].lower()

    @property
    def file_name_without_extension(self):
        md5 = hashlib.md5(self.payload).hexdigest()
        return '-'.join((self.file_name_prefix, md5))

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def get_absolute_asset_output_path(self, document_handler):
        raise NotImplemented

    @abc.abstractmethod
    def get_relative_asset_output_path(self, document_handler):
        raise NotImplemented

    def write_asset_to_disk(self, document_handler):
        pass
