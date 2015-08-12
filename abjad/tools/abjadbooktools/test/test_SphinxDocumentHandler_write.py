# -*- encoding: utf-8 -*-
import docutils
import os
import posixpath
import platform
import shutil
import unittest
from abjad.tools import abjadbooktools
from abjad.tools import systemtools


@unittest.skipIf(
    platform.python_implementation() != 'CPython',
    'Only for CPython.',
    )
class SphinxDocumentHandlerTests(unittest.TestCase):

    maxDiff = None

    class Namespace(object):
        pass

    def setUp(self):
        import abjad
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
        self.app.builder.srcdir = os.path.join(
            abjad.__path__[0],
            'docs',
            'source',
            )
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
                <a href="../_images/abjadbook/abjadbook/lilypond-0088e89b7def5c05b2a96e22136edef1cd638d75.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-0088e89b7def5c05b2a96e22136edef1cd638d75.png" alt="View source." title="View source." />
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-0088e89b7def5c05b2a96e22136edef1cd638d75.ly',
            'lilypond-0088e89b7def5c05b2a96e22136edef1cd638d75.png',
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
                <a href="../_images/abjadbook/abjadbook/lilypond-32d88a2354ecb601e788a6d43e67625f59dc61d1.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-32d88a2354ecb601e788a6d43e67625f59dc61d1.png" alt="View source." title="View source." />
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-32d88a2354ecb601e788a6d43e67625f59dc61d1.ly',
            'lilypond-32d88a2354ecb601e788a6d43e67625f59dc61d1.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_03(self):
        source = r'''
        ..  abjad::
            :hide:
            :stylesheet: non-proportional.ly
            :no-trim:

            show(Staff("c'4 d'4 e'4 f'4"))
        '''
        source = systemtools.TestManager.clean_string(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        abjadbooktools.SphinxDocumentHandler.on_builder_inited(self.app)
        node = document[0]
        try:
            abjadbooktools.SphinxDocumentHandler.visit_abjad_output_block_html(
                self.app, node)
        except docutils.nodes.SkipNode:
            pass
        actual = '\n'.join(self.app.body)
        expected = systemtools.TestManager.clean_string(r'''
            <div class="abjad-book-image">
                <a href="../_images/abjadbook/abjadbook/lilypond-eabd6888954618b38ced28351cc4a53e950f5a08.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-eabd6888954618b38ced28351cc4a53e950f5a08.png" alt="View source." title="View source." />
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'default.ly',
            'external-settings-file-1.ly',
            'external-settings-file-2.ly',
            'lilypond-eabd6888954618b38ced28351cc4a53e950f5a08.ly',
            'lilypond-eabd6888954618b38ced28351cc4a53e950f5a08.png',
            'non-proportional.ly',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_04(self):
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
                <a href="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page1.png" alt="View source." title="View source." />
                </a>
            </div>
            <div class="abjad-book-image">
                <a href="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page2.png" alt="View source." title="View source." />
                </a>
            </div>
            <div class="abjad-book-image">
                <a href="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page3.png" alt="View source." title="View source." />
                </a>
            </div>
            <div class="abjad-book-image">
                <a href="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page4.png" alt="View source." title="View source." />
                </a>
            </div>
            <div class="abjad-book-image">
                <a href="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page5.png" alt="View source." title="View source." />
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly',
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page1.png',
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page2.png',
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page3.png',
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page4.png',
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page5.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_05(self):
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
                <a href="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page2.png" alt="View source." title="View source." />
                </a>
            </div>
            <div class="abjad-book-image">
                <a href="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page3.png" alt="View source." title="View source." />
                </a>
            </div>
            <div class="abjad-book-image">
                <a href="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page4.png" alt="View source." title="View source." />
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly',
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page1.png',
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page2.png',
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page3.png',
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page4.png',
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page5.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_06(self):
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
                <a class="table-cell thumbnail" href="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page2.png" alt="View source." title="View source." />
                </a>
                <a class="table-cell thumbnail" href="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page3.png" alt="View source." title="View source." />
                </a>
            </div>
            <div class="table-row">
                <a class="table-cell thumbnail" href="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page4.png" alt="View source." title="View source." />
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly',
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page1.png',
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page2.png',
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page3.png',
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page4.png',
            'lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page5.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_07(self):
        source = r'''
        ..  abjad::
            :hide:
            :no-stylesheet:
            :no-trim:
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
                <a class="table-cell thumbnail" href="../_images/abjadbook/abjadbook/lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a-page2.png" alt="View source." title="View source." />
                </a>
                <a class="table-cell thumbnail" href="../_images/abjadbook/abjadbook/lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a-page3.png" alt="View source." title="View source." />
                </a>
            </div>
            <div class="table-row">
                <a class="table-cell thumbnail" href="../_images/abjadbook/abjadbook/lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a.ly">
                    <img src="../_images/abjadbook/abjadbook/lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a-page4.png" alt="View source." title="View source." />
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a.ly',
            'lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a-page1.png',
            'lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a-page2.png',
            'lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a-page3.png',
            'lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a-page4.png',
            'lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a-page5.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)