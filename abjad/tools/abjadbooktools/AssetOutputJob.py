# -*- encoding: utf-8 -*-
from abjad.tools import abctools


class AssetOutputJob(abctools.AbjadObject):

    __slots__ = (
        '_asset_output_proxy',
        '_output_directory',
        '_parent_document_format',
        )

    def __init__(
        self,
        asset_output_proxy,
        output_directory,
        parent_document_format,
        ):
        self._asset_output_proxy = asset_output_proxy
        self._output_directory = output_directory
        self._parent_document_format = parent_document_format

    def __call__(self):
        if self.parent_document_format == 'latex':
            self.asset_output_proxy.render_for_latex(self.output_directory)

    @property
    def asset_output_proxy(self):
        return self._asset_output_proxy

    @property
    def output_directory(self):
        return self._output_directory

    @property
    def parent_document_format(self):
        return self._parent_document_format