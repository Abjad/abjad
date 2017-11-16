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
            <a href="../_images/abjadbook/lilypond-7803f52afedde4eb2ade80aa92cfa82c1e7cc36b.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-7803f52afedde4eb2ade80aa92cfa82c1e7cc36b.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-7803f52afedde4eb2ade80aa92cfa82c1e7cc36b.ly',
            'lilypond-7803f52afedde4eb2ade80aa92cfa82c1e7cc36b.png',
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
            <a href="../_images/abjadbook/lilypond-4da9e9fdacc548126c08ef963af14d1b25cad4a9.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-4da9e9fdacc548126c08ef963af14d1b25cad4a9.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-4da9e9fdacc548126c08ef963af14d1b25cad4a9.ly',
            'lilypond-4da9e9fdacc548126c08ef963af14d1b25cad4a9.png',
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
            <a href="../_images/abjadbook/lilypond-6868d59d5934f664a4e11b137839de0f9bcfd373.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-6868d59d5934f664a4e11b137839de0f9bcfd373.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 2
        for name in (
            'lilypond-6868d59d5934f664a4e11b137839de0f9bcfd373.ly',
            'lilypond-6868d59d5934f664a4e11b137839de0f9bcfd373.png',
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
        assert '../_images/abjadbook/lilypond-6868d59d5934f664a4e11b137839de0f9bcfd373.png' in self.app.builder.thumbnails
        actual = '\n'.join(self.app.body)
        expected = abjad.String.normalize(r'''
            <a data-lightbox="group-lilypond-6868d59d5934f664a4e11b137839de0f9bcfd373.ly" href="../_images/abjadbook/lilypond-6868d59d5934f664a4e11b137839de0f9bcfd373.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-6868d59d5934f664a4e11b137839de0f9bcfd373-thumbnail.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 3
        for name in (
            'lilypond-6868d59d5934f664a4e11b137839de0f9bcfd373.ly',
            'lilypond-6868d59d5934f664a4e11b137839de0f9bcfd373.png',
            'lilypond-6868d59d5934f664a4e11b137839de0f9bcfd373-thumbnail.png',
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
            <a href="../_images/abjadbook/lilypond-c6c477783474a7d258cef8c73fe6f086e11e4280.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-c6c477783474a7d258cef8c73fe6f086e11e4280.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 7
        for name in (
            'default.ly',
            'external-settings-file-1.ly',
            'external-settings-file-2.ly',
            'lilypond-c6c477783474a7d258cef8c73fe6f086e11e4280.ly',
            'lilypond-c6c477783474a7d258cef8c73fe6f086e11e4280.png',
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
            <a href="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page1.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page3.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page4.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page5.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1.ly',
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page1.png',
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page2.png',
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page3.png',
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page4.png',
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page5.png',
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
            <a href="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page3.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1.ly" title="" class="abjadbook">
                <img src="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page4.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1.ly',
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page1.png',
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page2.png',
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page3.png',
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page4.png',
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page5.png',
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
                <a href="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page2.png" alt=""/>
                </a>
                <a href="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page3.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page4.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1.ly',
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page1.png',
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page2.png',
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page3.png',
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page4.png',
            'lilypond-961ede3dfbd0b5c408f4c705ff62e4939fd859a1-page5.png',
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
                <a href="../_images/abjadbook/lilypond-19c0fcbf7e06c54c75e38181eb11da94ce50d35b.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-19c0fcbf7e06c54c75e38181eb11da94ce50d35b-page2.png" alt=""/>
                </a>
                <a href="../_images/abjadbook/lilypond-19c0fcbf7e06c54c75e38181eb11da94ce50d35b.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-19c0fcbf7e06c54c75e38181eb11da94ce50d35b-page3.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a href="../_images/abjadbook/lilypond-19c0fcbf7e06c54c75e38181eb11da94ce50d35b.ly" title="" class="table-cell">
                    <img src="../_images/abjadbook/lilypond-19c0fcbf7e06c54c75e38181eb11da94ce50d35b-page4.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 6
        for name in (
            'lilypond-19c0fcbf7e06c54c75e38181eb11da94ce50d35b.ly',
            'lilypond-19c0fcbf7e06c54c75e38181eb11da94ce50d35b-page1.png',
            'lilypond-19c0fcbf7e06c54c75e38181eb11da94ce50d35b-page2.png',
            'lilypond-19c0fcbf7e06c54c75e38181eb11da94ce50d35b-page3.png',
            'lilypond-19c0fcbf7e06c54c75e38181eb11da94ce50d35b-page4.png',
            'lilypond-19c0fcbf7e06c54c75e38181eb11da94ce50d35b-page5.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)

#    @unittest.skipIf(
#        True,
#        'macOS High Sierra introduces glob(*) alphabetization bug.',
#        )
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
            <a data-lightbox="group-lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208.ly" href="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page1.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page1-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208.ly" href="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page2.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page2-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208.ly" href="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page3.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page3-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208.ly" href="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page4.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page4-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208.ly" href="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page5.png" title="" data-title="" class="abjadbook thumbnail">
                <img src="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page5-thumbnail.png" alt=""/>
            </a>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 11
        for name in (
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208.ly',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page1.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page1-thumbnail.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page2.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page2-thumbnail.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page3.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page3-thumbnail.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page4.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page4-thumbnail.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page5.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page5-thumbnail.png',
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
                <a data-lightbox="group-lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208.ly" href="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page1.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page1-thumbnail.png" alt=""/>
                </a>
                <a data-lightbox="group-lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208.ly" href="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page2.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page2-thumbnail.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a data-lightbox="group-lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208.ly" href="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page3.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page3-thumbnail.png" alt=""/>
                </a>
                <a data-lightbox="group-lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208.ly" href="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page4.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page4-thumbnail.png" alt=""/>
                </a>
            </div>
            <div class="table-row">
                <a data-lightbox="group-lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208.ly" href="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page5.png" title="" data-title="" class="table-cell thumbnail">
                    <img src="../_images/abjadbook/lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page5-thumbnail.png" alt=""/>
                </a>
            </div>
            ''')
        self.assertEqual(actual, expected)
        assert len(os.listdir(self.abjadbook_images_directory)) == 11
        for name in (
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208.ly',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page1.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page1-thumbnail.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page2.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page2-thumbnail.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page3.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page3-thumbnail.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page4.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page4-thumbnail.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page5.png',
            'lilypond-73b5c6d2d76fa211ae38dd0081a86219dbfe6208-page5-thumbnail.png',
            ):
            path = os.path.join(self.images_directory, 'abjadbook', name)
            assert os.path.exists(path)
