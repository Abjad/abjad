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
            <a href="../_images/abjadbook/lilypond-0088e89b7def5c05b2a96e22136edef1cd638d75.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-0088e89b7def5c05b2a96e22136edef1cd638d75.png" alt=""/>
            </a>
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
            <a href="../_images/abjadbook/lilypond-32d88a2354ecb601e788a6d43e67625f59dc61d1.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-32d88a2354ecb601e788a6d43e67625f59dc61d1.png" alt=""/>
            </a>
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
            <a href="../_images/abjadbook/lilypond-93ffa240c3eeeb710e929d9d3ccb00128218440e.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-93ffa240c3eeeb710e929d9d3ccb00128218440e.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-93ffa240c3eeeb710e929d9d3ccb00128218440e.ly',
            'lilypond-93ffa240c3eeeb710e929d9d3ccb00128218440e.png',
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
        assert '../_images/abjadbook/lilypond-93ffa240c3eeeb710e929d9d3ccb00128218440e.png' in self.app.builder.thumbnails
        actual = '\n'.join(self.app.body)
        expected = stringtools.normalize(r'''
            <a data-lightbox="group-lilypond-93ffa240c3eeeb710e929d9d3ccb00128218440e.ly" href="../_images/abjadbook/lilypond-93ffa240c3eeeb710e929d9d3ccb00128218440e.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-93ffa240c3eeeb710e929d9d3ccb00128218440e-thumbnail.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 3
        for name in (
            'lilypond-93ffa240c3eeeb710e929d9d3ccb00128218440e.ly',
            'lilypond-93ffa240c3eeeb710e929d9d3ccb00128218440e.png',
            'lilypond-93ffa240c3eeeb710e929d9d3ccb00128218440e-thumbnail.png',
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
            <a href="../_images/abjadbook/lilypond-eabd6888954618b38ced28351cc4a53e950f5a08.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-eabd6888954618b38ced28351cc4a53e950f5a08.png" alt=""/>
            </a>
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
            <a href="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page1.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page3.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page4.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page5.png" alt=""/>
            </a>
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
            <a href="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page3.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page4.png" alt=""/>
            </a>
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
                <a href="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page2.png" alt=""/>
                </a>
                <a href="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page3.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-f75159c51f466ac3f0427cda3f86fba7bb709ae7-page4.png" alt=""/>
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
                <a href="../_images/abjadbook/lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a-page2.png" alt=""/>
                </a>
                <a href="../_images/abjadbook/lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a-page3.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-1113b742beda3b13163bb7fe4bbdd6787edc3c1a-page4.png" alt=""/>
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
            <a data-lightbox="group-lilypond-224663e00b24b652df759bda64c86bca48933457.ly" href="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page1.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page1-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-224663e00b24b652df759bda64c86bca48933457.ly" href="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page2.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page2-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-224663e00b24b652df759bda64c86bca48933457.ly" href="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page3.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page3-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-224663e00b24b652df759bda64c86bca48933457.ly" href="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page4.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page4-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-224663e00b24b652df759bda64c86bca48933457.ly" href="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page5.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page5-thumbnail.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 11
        for name in (
            'lilypond-224663e00b24b652df759bda64c86bca48933457.ly',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page1.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page1-thumbnail.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page2.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page2-thumbnail.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page3.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page3-thumbnail.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page4.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page4-thumbnail.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page5.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page5-thumbnail.png',
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
                <a data-lightbox="group-lilypond-224663e00b24b652df759bda64c86bca48933457.ly" href="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page1.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page1-thumbnail.png" alt=""/>
                </a>
                <a data-lightbox="group-lilypond-224663e00b24b652df759bda64c86bca48933457.ly" href="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page2.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page2-thumbnail.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a data-lightbox="group-lilypond-224663e00b24b652df759bda64c86bca48933457.ly" href="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page3.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page3-thumbnail.png" alt=""/>
                </a>
                <a data-lightbox="group-lilypond-224663e00b24b652df759bda64c86bca48933457.ly" href="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page4.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page4-thumbnail.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a data-lightbox="group-lilypond-224663e00b24b652df759bda64c86bca48933457.ly" href="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page5.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-224663e00b24b652df759bda64c86bca48933457-page5-thumbnail.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 11
        for name in (
            'lilypond-224663e00b24b652df759bda64c86bca48933457.ly',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page1.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page1-thumbnail.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page2.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page2-thumbnail.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page3.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page3-thumbnail.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page4.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page4-thumbnail.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page5.png',
            'lilypond-224663e00b24b652df759bda64c86bca48933457-page5-thumbnail.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)
