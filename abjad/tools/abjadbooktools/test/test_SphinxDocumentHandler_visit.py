# -*- encoding: utf-8 -*-
from abjad.tools import abjadbooktools
from abjad.tools import systemtools
import docutils
import os
import posixpath
import shutil
import unittest


class SphinxDocumentHandlerTests(unittest.TestCase):

    class Namespace(object):
        pass

    def setUp(self):
        app = self.Namespace()
        config = self.Namespace()
        self.app = app
        self.app.config = config
        self.app.config.abjadbook_ignored_documents = ()
        self.app.builder = self.Namespace()
        self.app.builder.outdir = os.path.dirname(os.path.abspath(__file__))
        self.app.builder.imagedir = '_images'
        self.app.builder.imgpath = posixpath.join(
            '..', '_images', 'abjadbook')
        self.app.body = []
        image_directory = os.path.join(
            self.app.builder.outdir,
            self.app.builder.imagedir,
            )
        if os.path.exists(image_directory):
            shutil.rmtree(image_directory)

    def tearDown(self):
        image_directory = os.path.join(
            self.app.builder.outdir,
            self.app.builder.imagedir,
            )
        if os.path.exists(image_directory):
            shutil.rmtree(image_directory)

    def test_01(self):
        source = r'''
        ..  abjad::
            :hide:
            :no-stylesheet:

            show(Staff("c'1 g'1"))
        '''
        source = systemtools.TestManager.clean_string(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        node = document[0]
        try:
            abjadbooktools.SphinxDocumentHandler.visit_abjad_output_block_html(
                self.app, node)
        except docutils.nodes.SkipNode:
            pass