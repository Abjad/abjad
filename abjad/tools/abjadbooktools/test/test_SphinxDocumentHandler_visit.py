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

    def test_03(self):
        source = r'''
        ..  abjad::
            :hide:
            :no-stylesheet:

            staff = Staff("c'1 d'1 e'1 f'1 g'1")
            for note in staff[:-1]:
                attach(indicatortools.PageBreak(), note)

            show(staff)
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
                <a href="../_images/abjadbook/abjadbook/lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55-page1.png" alt="View source." title="View source." />
                </a>
            </div>
            <div class="abjad-book-image">
                <a href="../_images/abjadbook/abjadbook/lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55-page2.png" alt="View source." title="View source." />
                </a>
            </div>
            <div class="abjad-book-image">
                <a href="../_images/abjadbook/abjadbook/lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55-page3.png" alt="View source." title="View source." />
                </a>
            </div>
            <div class="abjad-book-image">
                <a href="../_images/abjadbook/abjadbook/lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55-page4.png" alt="View source." title="View source." />
                </a>
            </div>
            <div class="abjad-book-image">
                <a href="../_images/abjadbook/abjadbook/lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55-page5.png" alt="View source." title="View source." />
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55.ly',
            'lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55-page1.png',
            'lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55-page2.png',
            'lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55-page3.png',
            'lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55-page4.png',
            'lilypond-bf1926937db1ea744a00fc8500b830de53cb3e55-page5.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_04(self):
        source = r'''
        ..  abjad::
            :hide:
            :no-stylesheet:
            :pages: 2-4

            staff = Staff("c'1 d'1 e'1 f'1 g'1")
            for note in staff[:-1]:
                attach(indicatortools.PageBreak(), note)

            show(staff)
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
                <a href="../_images/abjadbook/abjadbook/lilypond-f54a53044475253bf691da944368cc4990c206bb.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-f54a53044475253bf691da944368cc4990c206bb-page2.png" alt="View source." title="View source." />
                </a>
            </div>
            <div class="abjad-book-image">
                <a href="../_images/abjadbook/abjadbook/lilypond-f54a53044475253bf691da944368cc4990c206bb.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-f54a53044475253bf691da944368cc4990c206bb-page3.png" alt="View source." title="View source." />
                </a>
            </div>
            <div class="abjad-book-image">
                <a href="../_images/abjadbook/abjadbook/lilypond-f54a53044475253bf691da944368cc4990c206bb.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-f54a53044475253bf691da944368cc4990c206bb-page4.png" alt="View source." title="View source." />
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-f54a53044475253bf691da944368cc4990c206bb.ly',
            'lilypond-f54a53044475253bf691da944368cc4990c206bb-page1.png',
            'lilypond-f54a53044475253bf691da944368cc4990c206bb-page2.png',
            'lilypond-f54a53044475253bf691da944368cc4990c206bb-page3.png',
            'lilypond-f54a53044475253bf691da944368cc4990c206bb-page4.png',
            'lilypond-f54a53044475253bf691da944368cc4990c206bb-page5.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_05(self):
        source = r'''
        ..  abjad::
            :hide:
            :no-stylesheet:
            :pages: 2-4
            :with-columns: 2

            staff = Staff("c'1 d'1 e'1 f'1 g'1")
            for note in staff[:-1]:
                attach(indicatortools.PageBreak(), note)

            show(staff)
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
            <div class="table-row">
                <a class="table-cell thumbnail" href="../_images/abjadbook/abjadbook/lilypond-6c8a81c25dea52a05a5fbbf0283e6d11a2e8b1ed.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-6c8a81c25dea52a05a5fbbf0283e6d11a2e8b1ed-page2.png" alt="View source." title="View source." />
                </a>
                <a class="table-cell thumbnail" href="../_images/abjadbook/abjadbook/lilypond-6c8a81c25dea52a05a5fbbf0283e6d11a2e8b1ed.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-6c8a81c25dea52a05a5fbbf0283e6d11a2e8b1ed-page3.png" alt="View source." title="View source." />
                </a>
            </div>
            <div class="table-row">
                <a class="table-cell thumbnail" href="../_images/abjadbook/abjadbook/lilypond-6c8a81c25dea52a05a5fbbf0283e6d11a2e8b1ed.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-6c8a81c25dea52a05a5fbbf0283e6d11a2e8b1ed-page4.png" alt="View source." title="View source." />
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-6c8a81c25dea52a05a5fbbf0283e6d11a2e8b1ed.ly',
            'lilypond-6c8a81c25dea52a05a5fbbf0283e6d11a2e8b1ed-page1.png',
            'lilypond-6c8a81c25dea52a05a5fbbf0283e6d11a2e8b1ed-page2.png',
            'lilypond-6c8a81c25dea52a05a5fbbf0283e6d11a2e8b1ed-page3.png',
            'lilypond-6c8a81c25dea52a05a5fbbf0283e6d11a2e8b1ed-page4.png',
            'lilypond-6c8a81c25dea52a05a5fbbf0283e6d11a2e8b1ed-page5.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)