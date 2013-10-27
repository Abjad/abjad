# -*- encoding: utf-8 -*-
import abc
import hashlib
from experimental.tools.newabjadbooktools.OutputProxy import OutputProxy


class AssetOutputProxy(OutputProxy):
    r'''Abstract base class for all abjad-book asset output managers.

    An asset output proxy is an output proxy with both a textual 
    representation in a document, and a filesystem representation on disk.

    Examples include notation, charts and graphs.
    '''

    ### PUBLIC ATTRIBUTES ###

    @property
    def file_name_prefix(self):
        r'''Prefix for files generated from an output proxy.

        Based on the name of the output proxy's class.

        Returns string.
        '''
        return self.__class__.__name__.partition('OutputProxy')[0].lower()

    @property
    def file_name_without_extension(self):
        r'''File name without extension for files generated from an output
        proxy.

        Based on the class of the output proxy and a hash of the textual
        contents of the proxy's payload.

        Returns string.
        '''
        md5 = hashlib.md5(self.payload).hexdigest()
        return '-'.join((self.file_name_prefix, md5))

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def get_asset_output_absolute_file_path(self, document_handler):
        raise NotImplemented

    @abc.abstractmethod
    def get_asset_output_relative_file_path(self, document_handler):
        raise NotImplemented

    @abc.abstractmethod
    def write_asset_to_disk(self, document_handler):
        raise NotImplemented
