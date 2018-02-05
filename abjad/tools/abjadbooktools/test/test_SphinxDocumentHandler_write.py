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
            <a href="../_images/abjadbook/lilypond-9fc2c4855204dd276ff878a261ad36d4a358c63d.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-9fc2c4855204dd276ff878a261ad36d4a358c63d.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-9fc2c4855204dd276ff878a261ad36d4a358c63d.ly',
            'lilypond-9fc2c4855204dd276ff878a261ad36d4a358c63d.png',
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
            <a href="../_images/abjadbook/lilypond-1d6adce9cf45520580076ea56583302a683b8a68.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-1d6adce9cf45520580076ea56583302a683b8a68.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-1d6adce9cf45520580076ea56583302a683b8a68.ly',
            'lilypond-1d6adce9cf45520580076ea56583302a683b8a68.png',
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
            <a href="../_images/abjadbook/lilypond-b70ff76f6d891a8b5ffa889dfb989dd31d659911.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-b70ff76f6d891a8b5ffa889dfb989dd31d659911.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-b70ff76f6d891a8b5ffa889dfb989dd31d659911.ly',
            'lilypond-b70ff76f6d891a8b5ffa889dfb989dd31d659911.png',
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
        assert '../_images/abjadbook/lilypond-b70ff76f6d891a8b5ffa889dfb989dd31d659911.png' in self.app.builder.thumbnails
        actual = '\n'.join(self.app.body)
        expected = abjad.String.normalize(r'''
            <a data-lightbox="group-lilypond-b70ff76f6d891a8b5ffa889dfb989dd31d659911.ly" href="../_images/abjadbook/lilypond-b70ff76f6d891a8b5ffa889dfb989dd31d659911.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-b70ff76f6d891a8b5ffa889dfb989dd31d659911-thumbnail.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 3
        for name in (
            'lilypond-b70ff76f6d891a8b5ffa889dfb989dd31d659911.ly',
            'lilypond-b70ff76f6d891a8b5ffa889dfb989dd31d659911.png',
            'lilypond-b70ff76f6d891a8b5ffa889dfb989dd31d659911-thumbnail.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

    def test_05(self):
        source = r'''
        ..  abjad::
            :hide:
            :stylesheet: non-proportional.ly
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
            <a href="../_images/abjadbook/lilypond-0b7a2a64005bc82bc16303c2f194f4497ea94e15.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-0b7a2a64005bc82bc16303c2f194f4497ea94e15.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 7
        for name in (
            'default.ly',
            'external-settings-file-1.ly',
            'external-settings-file-2.ly',
            'lilypond-0b7a2a64005bc82bc16303c2f194f4497ea94e15.ly',
            'lilypond-0b7a2a64005bc82bc16303c2f194f4497ea94e15.png',
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
            <a href="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page1.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page3.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page4.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page5.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968.ly',
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page1.png',
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page2.png',
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page3.png',
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page4.png',
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page5.png',
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
            <a href="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page3.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page4.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968.ly',
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page1.png',
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page2.png',
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page3.png',
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page4.png',
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page5.png',
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
                <a href="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page2.png" alt=""/>
                </a>
                <a href="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page3.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page4.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968.ly',
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page1.png',
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page2.png',
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page3.png',
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page4.png',
            'lilypond-ebfcef165988df8b00f79d283de3019c96f17968-page5.png',
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
                <a href="../_images/abjadbook/lilypond-3455132ce86f419c903206441de9049369a1c8fa.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-3455132ce86f419c903206441de9049369a1c8fa-page2.png" alt=""/>
                </a>
                <a href="../_images/abjadbook/lilypond-3455132ce86f419c903206441de9049369a1c8fa.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-3455132ce86f419c903206441de9049369a1c8fa-page3.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-3455132ce86f419c903206441de9049369a1c8fa.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-3455132ce86f419c903206441de9049369a1c8fa-page4.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-3455132ce86f419c903206441de9049369a1c8fa.ly',
            'lilypond-3455132ce86f419c903206441de9049369a1c8fa-page1.png',
            'lilypond-3455132ce86f419c903206441de9049369a1c8fa-page2.png',
            'lilypond-3455132ce86f419c903206441de9049369a1c8fa-page3.png',
            'lilypond-3455132ce86f419c903206441de9049369a1c8fa-page4.png',
            'lilypond-3455132ce86f419c903206441de9049369a1c8fa-page5.png',
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
            <a data-lightbox="group-lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623.ly" href="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page1.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page1-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623.ly" href="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page2.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page2-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623.ly" href="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page3.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page3-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623.ly" href="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page4.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page4-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623.ly" href="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page5.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page5-thumbnail.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 11
        for name in (
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623.ly',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page1.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page1-thumbnail.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page2.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page2-thumbnail.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page3.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page3-thumbnail.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page4.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page4-thumbnail.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page5.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page5-thumbnail.png',
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
                <a data-lightbox="group-lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623.ly" href="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page1.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page1-thumbnail.png" alt=""/>
                </a>
                <a data-lightbox="group-lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623.ly" href="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page2.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page2-thumbnail.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a data-lightbox="group-lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623.ly" href="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page3.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page3-thumbnail.png" alt=""/>
                </a>
                <a data-lightbox="group-lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623.ly" href="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page4.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page4-thumbnail.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a data-lightbox="group-lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623.ly" href="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page5.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page5-thumbnail.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 11
        for name in (
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623.ly',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page1.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page1-thumbnail.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page2.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page2-thumbnail.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page3.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page3-thumbnail.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page4.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page4-thumbnail.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page5.png',
            'lilypond-0aa2622a00db4f1eb5e873ef7e6a7f14fa465623-page5-thumbnail.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)
