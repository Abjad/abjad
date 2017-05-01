# -*- coding: utf-8 -*-
from abjad.tools import abctools


class ClassDocumenter(abctools.AbjadObject):
    """
    A class documenter.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_attributes',
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client):
        assert isinstance(client, type)
        self._client = client

    ### PUBLIC METHODS ###

    def build_rst(self):
        from abjad.tools import documentationtools
        return documentationtools.DocumentationManager()._get_class_rst(
            self.client)

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        """
        Gets client of documenter.
        """
        return self._client
