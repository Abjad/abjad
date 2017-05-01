# -*- coding: utf-8 -*-
from abjad.tools import documentationtools
from abjad.tools import scoretools
from abjad.tools import systemtools


class TestCase(systemtools.TestCase):

    def test_01(self):
        manager = documentationtools.DocumentationManager()
        documenter = documentationtools.FunctionDocumenter(
            manager=manager,
            client=scoretools.make_notes,
            )
        rst = documenter.build_rst()
        assert self.normalize("""
            ..  currentmodule:: abjad.tools.scoretools

            make_notes
            ==========

            ..  autofunction:: make_notes
        """) + '\n' == rst.rest_format
