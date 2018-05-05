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

            abjad.show(Staff("c'4 d'4 e'4 f'4"))
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
            <a href="../_images/abjadbook/lilypond-4058eb3dfc319740c8cecc269d76c3882aec6088.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-4058eb3dfc319740c8cecc269d76c3882aec6088.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-4058eb3dfc319740c8cecc269d76c3882aec6088.ly',
            'lilypond-4058eb3dfc319740c8cecc269d76c3882aec6088.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_02(self):
        source = r'''
        ..  abjad::
            :hide:
            :no-stylesheet:
            :no-trim:

            abjad.show(Staff("c'4 d'4 e'4 f'4"))
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
            <a href="../_images/abjadbook/lilypond-fb8050d8fe914487cda335bed70d83567b1dc057.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-fb8050d8fe914487cda335bed70d83567b1dc057.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-fb8050d8fe914487cda335bed70d83567b1dc057.ly',
            'lilypond-fb8050d8fe914487cda335bed70d83567b1dc057.png',
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

            abjad.show(Staff("c'4 d'4 e'4 f'4"))
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
            <a href="../_images/abjadbook/lilypond-d75d8e4591211ce47fcb1c83c06ddf84ca4266b8.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-d75d8e4591211ce47fcb1c83c06ddf84ca4266b8.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-d75d8e4591211ce47fcb1c83c06ddf84ca4266b8.ly',
            'lilypond-d75d8e4591211ce47fcb1c83c06ddf84ca4266b8.png',
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

            abjad.show(Staff("c'4 d'4 e'4 f'4"))
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
        assert '../_images/abjadbook/lilypond-d75d8e4591211ce47fcb1c83c06ddf84ca4266b8.png' in self.app.builder.thumbnails
        actual = '\n'.join(self.app.body)
        expected = abjad.String.normalize(r'''
            <a data-lightbox="group-lilypond-d75d8e4591211ce47fcb1c83c06ddf84ca4266b8.ly" href="../_images/abjadbook/lilypond-d75d8e4591211ce47fcb1c83c06ddf84ca4266b8.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-d75d8e4591211ce47fcb1c83c06ddf84ca4266b8-thumbnail.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 3
        for name in (
            'lilypond-d75d8e4591211ce47fcb1c83c06ddf84ca4266b8.ly',
            'lilypond-d75d8e4591211ce47fcb1c83c06ddf84ca4266b8.png',
            'lilypond-d75d8e4591211ce47fcb1c83c06ddf84ca4266b8-thumbnail.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_05(self):
        source = r'''
        ..  abjad::
            :hide:
            :stylesheet: default.ily
            :no-trim:

            abjad.show(Staff("c'4 d'4 e'4 f'4"))
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
            <a href="../_images/abjadbook/lilypond-5929b503d9900d1f22aa1cb08b916d4cc28181c5.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-5929b503d9900d1f22aa1cb08b916d4cc28181c5.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 8
        for name in (
            'default.ily',
            'external-settings-file-1.ily',
            'external-settings-file-2.ily',
            'lilypond-5929b503d9900d1f22aa1cb08b916d4cc28181c5.ly',
            'lilypond-5929b503d9900d1f22aa1cb08b916d4cc28181c5.png',
            'rhythm-maker-docs.ily',
            'text-spanner-id.ily',
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

            abjad.show(staff)
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
            <a href="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page1.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page3.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page4.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page5.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc.ly',
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page1.png',
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page2.png',
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page3.png',
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page4.png',
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page5.png',
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

            abjad.show(staff)
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
            <a href="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page3.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page4.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc.ly',
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page1.png',
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page2.png',
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page3.png',
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page4.png',
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page5.png',
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

            abjad.show(staff)
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
                <a href="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page2.png" alt=""/>
                </a>
                <a href="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page3.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page4.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc.ly',
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page1.png',
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page2.png',
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page3.png',
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page4.png',
            'lilypond-51cd302cf7377dd528854aa8e6eb59d2be0c20cc-page5.png',
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

            abjad.show(staff)
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
                <a href="../_images/abjadbook/lilypond-49b48d1ad1a9f55fcf545837f76109e98c544614.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-49b48d1ad1a9f55fcf545837f76109e98c544614-page2.png" alt=""/>
                </a>
                <a href="../_images/abjadbook/lilypond-49b48d1ad1a9f55fcf545837f76109e98c544614.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-49b48d1ad1a9f55fcf545837f76109e98c544614-page3.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-49b48d1ad1a9f55fcf545837f76109e98c544614.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-49b48d1ad1a9f55fcf545837f76109e98c544614-page4.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-49b48d1ad1a9f55fcf545837f76109e98c544614.ly',
            'lilypond-49b48d1ad1a9f55fcf545837f76109e98c544614-page1.png',
            'lilypond-49b48d1ad1a9f55fcf545837f76109e98c544614-page2.png',
            'lilypond-49b48d1ad1a9f55fcf545837f76109e98c544614-page3.png',
            'lilypond-49b48d1ad1a9f55fcf545837f76109e98c544614-page4.png',
            'lilypond-49b48d1ad1a9f55fcf545837f76109e98c544614-page5.png',
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

            abjad.show(staff)
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
            <a data-lightbox="group-lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b.ly" href="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page1.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page1-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b.ly" href="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page2.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page2-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b.ly" href="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page3.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page3-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b.ly" href="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page4.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page4-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b.ly" href="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page5.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page5-thumbnail.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 11
        for name in (
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b.ly',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page1.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page1-thumbnail.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page2.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page2-thumbnail.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page3.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page3-thumbnail.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page4.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page4-thumbnail.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page5.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page5-thumbnail.png',
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

            abjad.show(staff)
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
                <a data-lightbox="group-lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b.ly" href="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page1.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page1-thumbnail.png" alt=""/>
                </a>
                <a data-lightbox="group-lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b.ly" href="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page2.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page2-thumbnail.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a data-lightbox="group-lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b.ly" href="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page3.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page3-thumbnail.png" alt=""/>
                </a>
                <a data-lightbox="group-lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b.ly" href="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page4.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page4-thumbnail.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a data-lightbox="group-lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b.ly" href="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page5.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page5-thumbnail.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 11
        for name in (
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b.ly',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page1.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page1-thumbnail.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page2.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page2-thumbnail.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page3.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page3-thumbnail.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page4.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page4-thumbnail.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page5.png',
            'lilypond-8a0c69a1ec4fb4f2adfb7b08e8b25a4fe0ffce1b-page5-thumbnail.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)
