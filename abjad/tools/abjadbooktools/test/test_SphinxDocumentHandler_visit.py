# -*- encoding: utf-8 -*-
from abjad.tools import abjadbooktools
from abjad.tools import systemtools
import docutils
import os
import posixpath
import shutil
import unittest


class SphinxDocumentHandlerTests(unittest.TestCase):

    maxDiff = None

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
        self.images_directory = os.path.join(
            self.app.builder.outdir,
            self.app.builder.imagedir,
            )
        self.abjadbook_images_directory = os.path.join(
            self.images_directory,
            'abjadbook',
            )
        if os.path.exists(self.images_directory):
            shutil.rmtree(self.images_directory)

    def tearDown(self):
        if os.path.exists(self.images_directory):
            shutil.rmtree(self.images_directory)

    def test_01(self):
        source = r'''
        ..  abjad::
            :hide:
            :no-stylesheet:

            show(Staff("c'4 d'4 e'4 f'4"))
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
        actual = '\n'.join(self.app.body)
        expected = systemtools.TestManager.clean_string(r'''
        <div class="abjad-book-image">
            <a href="../_images/abjadbook/abjadbook/lilypond-cae93b80d6f6c70eab16244f682fce8f2f5a1821.ly">
                <img src="../_images/abjadbook/abjadbook/lilypond-cae93b80d6f6c70eab16244f682fce8f2f5a1821.png" alt="View source." title="View source." />
            </a>
        </div>
        ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-cae93b80d6f6c70eab16244f682fce8f2f5a1821.ly',
            'lilypond-cae93b80d6f6c70eab16244f682fce8f2f5a1821.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_02(self):
        source = r'''
        ..  abjad::
            :hide:
            :no-stylesheet:
            :no-trim:

            show(Staff("c'4 d'4 e'4 f'4"))
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
        actual = '\n'.join(self.app.body)
        expected = systemtools.TestManager.clean_string(r'''
        <div class="abjad-book-image">
            <a href="../_images/abjadbook/abjadbook/lilypond-868cc561d54bf8b577ddf5fbc9ca6ab1a22a8c02.ly">
                <img src="../_images/abjadbook/abjadbook/lilypond-868cc561d54bf8b577ddf5fbc9ca6ab1a22a8c02.png" alt="View source." title="View source." />
            </a>
        </div>
        ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-868cc561d54bf8b577ddf5fbc9ca6ab1a22a8c02.ly',
            'lilypond-868cc561d54bf8b577ddf5fbc9ca6ab1a22a8c02.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)