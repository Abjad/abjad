# -*- coding: utf-8 -*-
from abjad.tools import documentationtools
from abjad.tools import scoretools
from abjad.tools import systemtools


class TestCase(systemtools.TestCase):

    def test_01(self):
        manager = documentationtools.DocumentationManager()
        documenter = documentationtools.PackageDocumenter(
            manager=manager,
            client=scoretools,
            )
        rst = documenter.build_rst()
        assert self.normalize("""
            ..  automodule:: abjad.tools.scoretools
        """) + '\n' == rst.rest_format
