# -*- encoding: utf-8 -*-
import abc
import code
import collections
import os
from abjad.tools.abctools import AbjadObject


class DocumentHandler(AbjadObject):
    r'''Abstract base class of all document handlers.
    '''

    ### INITIALIZER ###

    def __init__(self,
        document,
        output_directory_path=None,
        ):
        self._code_blocks = collections.OrderedDict()
        self._console = code.InteractiveConsole()
        self._document = document
        self._output_directory_path = output_directory_path

    ### SPECIAL METHODS ###

    def __call__(self):
        self._code_blocks = self.extract_code_blocks(
            self.document,
            self.source_to_code_block_mapping,
            )
 
    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def asset_output_directory_name(self):
        raise NotImplemented

    @property
    def asset_output_directory_path(self):
        return os.path.join(
            self.output_directory_path,
            self.asset_output_directory_name,
            )

    @property
    def asset_output_proxies(self):
        r'''All asset output proxies.
        '''
        result = []
        for code_block in self.source_to_code_block_mapping.iteritems():
            for output_proxy in code_block.output_proxies:
                if isinstance(output_proxy,
                    newabjadbooktools.AssetOutputProxy):
                    result.append(output_proxy)
        return result

    @property
    def source_to_code_block_mapping(self):
        return self._code_blocks

    @property
    def console(self):
        r'''Interactive console.
        '''
        return self._console

    @property
    def document(self):
        return self._document

    @property
    def has_asset_output_proxies(self):
        for code_block in self.source_to_code_block_mapping.iteritems():
            for output_proxy in code_block.output_proxies:
                if isinstance(output_proxy, 
                    newabjadbooktools.AssetOutputProxy):
                    return True
        return False

    @abc.abstractproperty
    def image_format(self):
        raise NotImplemented

    @property
    def output_directory_path(self):
        return self._output_directory_path
   
    ### PUBLIC METHODS ###

    def create_code_block(self,
        displayed_lines,
        options,
        source_location,
        ):
        from experimental.tools import newabjadbooktools
        code_block = newabjadbooktools.CodeBlock(
            displayed_lines,
            **options
            )
        self.source_to_code_block_mapping[source_location] = code_block

    def execute_code_blocks(self):
        console = code.InteractiveConsole()
        console.push('from abjad import *')
        try:
            import experimental
            console.push('from experimental import *')
        except ImportError:
            pass
        for source_location, code_block in \
            self.source_to_code_block_mapping.iteritems():
            output_proxies = code_block.execute(console)

    @abc.abstractmethod
    def extract_code_block_options(self, source):
        raise NotImplemented
    
    @abc.abstractmethod
    def extract_code_blocks(self):
        raise NotImplemented

    @abc.abstractmethod
    def rebuild_document(self):
        raise NotImplemented

    def write_assets_to_disk(self):
        from experimental.tools import newabjadbooktools
        assert os.path.exists(self.output_directory_path)
        if self.has_asset_output_proxies:
            asset_output_directory_path = os.path.join(
                self.output_directory_path,
                self.asset_output_directory_name,
                )
            if not os.path.exists(asset_output_directory_path):
                os.mkdir(asset_output_directory_path)
        for code_block in self.source_to_code_block_mapping.iteritems():
            for output_proxy in code_block.output_proxies:
                if not isinstance(output_proxy, 
                    newabjadbooktools.AssetOutputProxy):
                    continue
                output_proxy.write_asset_to_disk(self)
