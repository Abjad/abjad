# -*- coding: utf-8 -*-
from __future__ import print_function
import abjad
import docutils
import os
import posixpath
import platform
import shutil
import unittest
from abjad.tools import abjadbooktools
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
        source = abjad.String.normalize(source)
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
        expected = abjad.String.normalize(r'''
            <a href="../_images/abjadbook/lilypond-e16d48b9daaa5fc687733330eebf40e142583e58.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-e16d48b9daaa5fc687733330eebf40e142583e58.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-e16d48b9daaa5fc687733330eebf40e142583e58.ly',
            'lilypond-e16d48b9daaa5fc687733330eebf40e142583e58.png',
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
        source = abjad.String.normalize(source)
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
        expected = abjad.String.normalize(r'''
            <a href="../_images/abjadbook/lilypond-9ff77da7bd81f083920be0b350b205fd6b6767a1.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-9ff77da7bd81f083920be0b350b205fd6b6767a1.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-9ff77da7bd81f083920be0b350b205fd6b6767a1.ly',
            'lilypond-9ff77da7bd81f083920be0b350b205fd6b6767a1.png',
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
        source = abjad.String.normalize(source)
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
        expected = abjad.String.normalize(r'''
            <a href="../_images/abjadbook/lilypond-28a967840c6a267316825bff73ccd5418c06ed04.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-28a967840c6a267316825bff73ccd5418c06ed04.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-28a967840c6a267316825bff73ccd5418c06ed04.ly',
            'lilypond-28a967840c6a267316825bff73ccd5418c06ed04.png',
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
        source = abjad.String.normalize(source)
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
        assert '../_images/abjadbook/lilypond-28a967840c6a267316825bff73ccd5418c06ed04.png' in self.app.builder.thumbnails
        actual = '\n'.join(self.app.body)
        expected = abjad.String.normalize(r'''
            <a data-lightbox="group-lilypond-28a967840c6a267316825bff73ccd5418c06ed04.ly" href="../_images/abjadbook/lilypond-28a967840c6a267316825bff73ccd5418c06ed04.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-28a967840c6a267316825bff73ccd5418c06ed04-thumbnail.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 3
        for name in (
            'lilypond-28a967840c6a267316825bff73ccd5418c06ed04.ly',
            'lilypond-28a967840c6a267316825bff73ccd5418c06ed04.png',
            'lilypond-28a967840c6a267316825bff73ccd5418c06ed04-thumbnail.png',
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
        source = abjad.String.normalize(source)
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
        expected = abjad.String.normalize(r'''
            <a href="../_images/abjadbook/lilypond-be904c180d556273c3bd4c6e53c4636e5c7aaf4f.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-be904c180d556273c3bd4c6e53c4636e5c7aaf4f.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 7
        for name in (
            'default.ly',
            'external-settings-file-1.ly',
            'external-settings-file-2.ly',
            'lilypond-be904c180d556273c3bd4c6e53c4636e5c7aaf4f.ly',
            'lilypond-be904c180d556273c3bd4c6e53c4636e5c7aaf4f.png',
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
        source = abjad.String.normalize(source)
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
        expected = abjad.String.normalize(r'''
            <a href="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page1.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page3.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page4.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page5.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5.ly',
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page1.png',
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page2.png',
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page3.png',
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page4.png',
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page5.png',
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
        source = abjad.String.normalize(source)
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
        expected = abjad.String.normalize(r'''
            <a href="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page3.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page4.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5.ly',
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page1.png',
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page2.png',
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page3.png',
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page4.png',
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page5.png',
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
        source = abjad.String.normalize(source)
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
        expected = abjad.String.normalize(r'''
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page2.png" alt=""/>
                </a>
                <a href="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page3.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page4.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5.ly',
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page1.png',
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page2.png',
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page3.png',
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page4.png',
            'lilypond-d8a292fabe1535f5ab562e33bc3c97216675f8a5-page5.png',
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
        source = abjad.String.normalize(source)
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
        expected = abjad.String.normalize(r'''
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-6900efb6ce21bef42b89ef019e69f08e070d7315.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-6900efb6ce21bef42b89ef019e69f08e070d7315-page2.png" alt=""/>
                </a>
                <a href="../_images/abjadbook/lilypond-6900efb6ce21bef42b89ef019e69f08e070d7315.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-6900efb6ce21bef42b89ef019e69f08e070d7315-page3.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-6900efb6ce21bef42b89ef019e69f08e070d7315.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-6900efb6ce21bef42b89ef019e69f08e070d7315-page4.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-6900efb6ce21bef42b89ef019e69f08e070d7315.ly',
            'lilypond-6900efb6ce21bef42b89ef019e69f08e070d7315-page1.png',
            'lilypond-6900efb6ce21bef42b89ef019e69f08e070d7315-page2.png',
            'lilypond-6900efb6ce21bef42b89ef019e69f08e070d7315-page3.png',
            'lilypond-6900efb6ce21bef42b89ef019e69f08e070d7315-page4.png',
            'lilypond-6900efb6ce21bef42b89ef019e69f08e070d7315-page5.png',
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
        source = abjad.String.normalize(source)
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
        expected = abjad.String.normalize(r'''
            <a data-lightbox="group-lilypond-e95e4239a7b2d051083422fe9ff795547273601e.ly" href="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page1.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page1-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-e95e4239a7b2d051083422fe9ff795547273601e.ly" href="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page2.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page2-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-e95e4239a7b2d051083422fe9ff795547273601e.ly" href="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page3.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page3-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-e95e4239a7b2d051083422fe9ff795547273601e.ly" href="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page4.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page4-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-e95e4239a7b2d051083422fe9ff795547273601e.ly" href="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page5.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page5-thumbnail.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 11
        for name in (
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e.ly',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page1.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page1-thumbnail.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page2.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page2-thumbnail.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page3.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page3-thumbnail.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page4.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page4-thumbnail.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page5.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page5-thumbnail.png',
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
        source = abjad.String.normalize(source)
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
        expected = abjad.String.normalize(r'''
            <div class="table-row">
                <a data-lightbox="group-lilypond-e95e4239a7b2d051083422fe9ff795547273601e.ly" href="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page1.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page1-thumbnail.png" alt=""/>
                </a>
                <a data-lightbox="group-lilypond-e95e4239a7b2d051083422fe9ff795547273601e.ly" href="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page2.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page2-thumbnail.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a data-lightbox="group-lilypond-e95e4239a7b2d051083422fe9ff795547273601e.ly" href="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page3.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page3-thumbnail.png" alt=""/>
                </a>
                <a data-lightbox="group-lilypond-e95e4239a7b2d051083422fe9ff795547273601e.ly" href="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page4.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page4-thumbnail.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a data-lightbox="group-lilypond-e95e4239a7b2d051083422fe9ff795547273601e.ly" href="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page5.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page5-thumbnail.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 11
        for name in (
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e.ly',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page1.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page1-thumbnail.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page2.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page2-thumbnail.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page3.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page3-thumbnail.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page4.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page4-thumbnail.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page5.png',
            'lilypond-e95e4239a7b2d051083422fe9ff795547273601e-page5-thumbnail.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)
