# -*- coding: utf-8 -*-
from abjad.tools import abctools


class Documenter(abctools.AbjadObject):
    """
    A documenter.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        '_manager',
        )

    ### INITIALIZER ###

    def __init__(self, manager, client):
        self._manager = manager
        self._client = client

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        """
        Gets client of documenter.
        """
        return self._client

    @property
    def manager(self):
        """
        Gets manager of documenter.
        """
        return self._manager
