# -*- coding: utf-8 -*-
from __future__ import print_function
import docutils
import os
import posixpath
import platform
import shutil
import unittest
from abjad.tools import abjadbooktools
from abjad.tools import stringtools
from sphinx.util import FilenameUniqDict


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
        self.app.builder.warn = print
        self.app.builder.current_docname = 'test'
        self.app.builder.status_iterator = lambda iterable, x, y, z: iter(iterable)
        self.app.builder.thumbnails = FilenameUniqDict()
        self.app.builder.outdir = os.path.dirname(os.path.abspath(__file__))
        self.app.builder.imagedir = '_images'
        self.app.builder.imgpath = posixpath.join('..', '_images')
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
        source = stringtools.normalize(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        node = document[0]
        try:
            abjadbooktools.SphinxDocumentHandler.visit_abjad_output_block_html(
                self.app, node)
        except docutils.nodes.SkipNode:
            pass
        handler.on_build_finished(self.app, None)
        actual = '\n'.join(self.app.body)
        expected = stringtools.normalize(r'''
            <a href="../_images/abjadbook/lilypond-5277565643d544973acd4092df64f3abb2586994.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-5277565643d544973acd4092df64f3abb2586994.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-5277565643d544973acd4092df64f3abb2586994.ly',
            'lilypond-5277565643d544973acd4092df64f3abb2586994.png',
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
        source = stringtools.normalize(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        node = document[0]
        try:
            abjadbooktools.SphinxDocumentHandler.visit_abjad_output_block_html(
                self.app, node)
        except docutils.nodes.SkipNode:
            pass
        handler.on_build_finished(self.app, None)
        actual = '\n'.join(self.app.body)
        expected = stringtools.normalize(r'''
            <a href="../_images/abjadbook/lilypond-7c082e5b0333af69778f9036846687b8e339e94b.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-7c082e5b0333af69778f9036846687b8e339e94b.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-7c082e5b0333af69778f9036846687b8e339e94b.ly',
            'lilypond-7c082e5b0333af69778f9036846687b8e339e94b.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_03(self):
        source = r'''
        ..  abjad::
            :hide:
            :no-resize:
            :no-stylesheet:
            :no-trim:

            show(Staff("c'4 d'4 e'4 f'4"))
        '''
        source = stringtools.normalize(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        node = document[0]
        try:
            abjadbooktools.SphinxDocumentHandler.visit_abjad_output_block_html(
                self.app, node)
        except docutils.nodes.SkipNode:
            pass
        handler.on_build_finished(self.app, None)
        actual = '\n'.join(self.app.body)
        expected = stringtools.normalize(r'''
            <a href="../_images/abjadbook/lilypond-8a8f45fe58b00dd49561a578f60b7ec69ee75113.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-8a8f45fe58b00dd49561a578f60b7ec69ee75113.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-8a8f45fe58b00dd49561a578f60b7ec69ee75113.ly',
            'lilypond-8a8f45fe58b00dd49561a578f60b7ec69ee75113.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_04(self):
        source = r'''
        ..  abjad::
            :hide:
            :no-resize:
            :no-stylesheet:
            :no-trim:
            :with-thumbnail:

            show(Staff("c'4 d'4 e'4 f'4"))
        '''
        source = stringtools.normalize(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        node = document[0]
        try:
            abjadbooktools.SphinxDocumentHandler.visit_abjad_output_block_html(
                self.app, node)
        except docutils.nodes.SkipNode:
            pass
        handler.on_build_finished(self.app, None)
        assert len(self.app.builder.thumbnails) == 1
        assert '../_images/abjadbook/lilypond-8a8f45fe58b00dd49561a578f60b7ec69ee75113.png' in self.app.builder.thumbnails
        actual = '\n'.join(self.app.body)
        expected = stringtools.normalize(r'''
            <a data-lightbox="group-lilypond-8a8f45fe58b00dd49561a578f60b7ec69ee75113.ly" href="../_images/abjadbook/lilypond-8a8f45fe58b00dd49561a578f60b7ec69ee75113.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-8a8f45fe58b00dd49561a578f60b7ec69ee75113-thumbnail.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 3
        for name in (
            'lilypond-8a8f45fe58b00dd49561a578f60b7ec69ee75113.ly',
            'lilypond-8a8f45fe58b00dd49561a578f60b7ec69ee75113.png',
            'lilypond-8a8f45fe58b00dd49561a578f60b7ec69ee75113-thumbnail.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_05(self):
        source = r'''
        ..  abjad::
            :hide:
            :stylesheet: non-proportional.ly
            :no-trim:

            show(Staff("c'4 d'4 e'4 f'4"))
        '''
        source = stringtools.normalize(source)
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
        handler.on_build_finished(self.app, None)
        actual = '\n'.join(self.app.body)
        expected = stringtools.normalize(r'''
            <a href="../_images/abjadbook/lilypond-7d4a48470c171cd8b46a0bd339cd92e2f9fdfa13.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-7d4a48470c171cd8b46a0bd339cd92e2f9fdfa13.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'default.ly',
            'external-settings-file-1.ly',
            'external-settings-file-2.ly',
            'lilypond-7d4a48470c171cd8b46a0bd339cd92e2f9fdfa13.ly',
            'lilypond-7d4a48470c171cd8b46a0bd339cd92e2f9fdfa13.png',
            'non-proportional.ly',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_06(self):
        source = r'''
        ..  abjad::
            :hide:
            :no-stylesheet:

            staff = Staff("c'1 d'1 e'1 f'1 g'1")
            for note in staff[:-1]:
                attach(indicatortools.PageBreak(), note)

            show(staff)
        '''
        source = stringtools.normalize(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        node = document[0]
        try:
            abjadbooktools.SphinxDocumentHandler.visit_abjad_output_block_html(
                self.app, node)
        except docutils.nodes.SkipNode:
            pass
        handler.on_build_finished(self.app, None)
        actual = '\n'.join(self.app.body)
        expected = stringtools.normalize(r'''
            <a href="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page1.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page3.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page4.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page5.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365.ly',
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page1.png',
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page2.png',
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page3.png',
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page4.png',
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page5.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_07(self):
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
        source = stringtools.normalize(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        node = document[0]
        try:
            abjadbooktools.SphinxDocumentHandler.visit_abjad_output_block_html(
                self.app, node)
        except docutils.nodes.SkipNode:
            pass
        handler.on_build_finished(self.app, None)
        actual = '\n'.join(self.app.body)
        expected = stringtools.normalize(r'''
            <a href="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page3.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page4.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365.ly',
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page1.png',
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page2.png',
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page3.png',
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page4.png',
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page5.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_08(self):
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
        source = stringtools.normalize(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        node = document[0]
        try:
            abjadbooktools.SphinxDocumentHandler.visit_abjad_output_block_html(
                self.app, node)
        except docutils.nodes.SkipNode:
            pass
        handler.on_build_finished(self.app, None)
        actual = '\n'.join(self.app.body)
        expected = stringtools.normalize(r'''
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page2.png" alt=""/>
                </a>
                <a href="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page3.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page4.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365.ly',
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page1.png',
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page2.png',
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page3.png',
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page4.png',
            'lilypond-4b0885a24cb0c0f7d7f825826532e89575af5365-page5.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_09(self):
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
        source = stringtools.normalize(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        node = document[0]
        try:
            abjadbooktools.SphinxDocumentHandler.visit_abjad_output_block_html(
                self.app, node)
        except docutils.nodes.SkipNode:
            pass
        handler.on_build_finished(self.app, None)
        actual = '\n'.join(self.app.body)
        expected = stringtools.normalize(r'''
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-c58647743390ca8f866acf83a0d7efbf9b84d67f.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-c58647743390ca8f866acf83a0d7efbf9b84d67f-page2.png" alt=""/>
                </a>
                <a href="../_images/abjadbook/lilypond-c58647743390ca8f866acf83a0d7efbf9b84d67f.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-c58647743390ca8f866acf83a0d7efbf9b84d67f-page3.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-c58647743390ca8f866acf83a0d7efbf9b84d67f.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-c58647743390ca8f866acf83a0d7efbf9b84d67f-page4.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-c58647743390ca8f866acf83a0d7efbf9b84d67f.ly',
            'lilypond-c58647743390ca8f866acf83a0d7efbf9b84d67f-page1.png',
            'lilypond-c58647743390ca8f866acf83a0d7efbf9b84d67f-page2.png',
            'lilypond-c58647743390ca8f866acf83a0d7efbf9b84d67f-page3.png',
            'lilypond-c58647743390ca8f866acf83a0d7efbf9b84d67f-page4.png',
            'lilypond-c58647743390ca8f866acf83a0d7efbf9b84d67f-page5.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_10(self):
        source = r'''
        ..  abjad::
            :hide:
            :no-resize:
            :no-stylesheet:
            :with-thumbnail:

            staff = Staff("c'1 d'1 e'1 f'1 g'1")
            for note in staff[:-1]:
                attach(indicatortools.PageBreak(), note)

            show(staff)
        '''
        source = stringtools.normalize(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        node = document[0]
        try:
            abjadbooktools.SphinxDocumentHandler.visit_abjad_output_block_html(
                self.app, node)
        except docutils.nodes.SkipNode:
            pass
        handler.on_build_finished(self.app, None)
        actual = '\n'.join(self.app.body)
        expected = stringtools.normalize(r'''
            <a data-lightbox="group-lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a.ly" href="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page1.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page1-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a.ly" href="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page2.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page2-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a.ly" href="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page3.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page3-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a.ly" href="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page4.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page4-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a.ly" href="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page5.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page5-thumbnail.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 11
        for name in (
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a.ly',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page1.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page1-thumbnail.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page2.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page2-thumbnail.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page3.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page3-thumbnail.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page4.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page4-thumbnail.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page5.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page5-thumbnail.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_11(self):
        source = r'''
        ..  abjad::
            :hide:
            :no-resize:
            :no-stylesheet:
            :with-columns: 2
            :with-thumbnail:

            staff = Staff("c'1 d'1 e'1 f'1 g'1")
            for note in staff[:-1]:
                attach(indicatortools.PageBreak(), note)

            show(staff)
        '''
        source = stringtools.normalize(source)
        handler = abjadbooktools.SphinxDocumentHandler()
        document = handler.parse_rst(source)
        handler.on_doctree_read(self.app, document)
        node = document[0]
        try:
            abjadbooktools.SphinxDocumentHandler.visit_abjad_output_block_html(
                self.app, node)
        except docutils.nodes.SkipNode:
            pass
        handler.on_build_finished(self.app, None)
        actual = '\n'.join(self.app.body)
        expected = stringtools.normalize(r'''
            <div class="table-row">
                <a data-lightbox="group-lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a.ly" href="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page1.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page1-thumbnail.png" alt=""/>
                </a>
                <a data-lightbox="group-lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a.ly" href="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page2.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page2-thumbnail.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a data-lightbox="group-lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a.ly" href="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page3.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page3-thumbnail.png" alt=""/>
                </a>
                <a data-lightbox="group-lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a.ly" href="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page4.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page4-thumbnail.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a data-lightbox="group-lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a.ly" href="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page5.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page5-thumbnail.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 11
        for name in (
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a.ly',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page1.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page1-thumbnail.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page2.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page2-thumbnail.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page3.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page3-thumbnail.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page4.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page4-thumbnail.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page5.png',
            'lilypond-de10d0db01d2644c7aea9703f6ed8c78d8dbb89a-page5-thumbnail.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)
