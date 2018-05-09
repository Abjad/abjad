import abjad.book
import docutils
import os
import posixpath
import pytest
import shutil
import types
from uqbar.strings import normalize
from sphinx.util import FilenameUniqDict


@pytest.fixture
def app():
    app = types.SimpleNamespace()
    app.config = types.SimpleNamespace()
    app.config.abjadbook_ignored_documents = ()
    app.builder = types.SimpleNamespace()
    app.builder.warn = print
    app.builder.current_docname = 'test'
    app.builder.status_iterator = lambda iterable, x, y, z: iter(iterable)
    app.builder.thumbnails = FilenameUniqDict()
    app.builder.outdir = os.path.dirname(os.path.abspath(__file__))
    app.builder.imagedir = '_images'
    app.builder.imgpath = posixpath.join('..', '_images')
    app.builder.srcdir = os.path.join(
        abjad.__path__[0],
        'docs',
        'source',
        )
    app.body = []
    return app


@pytest.fixture
def paths(app):
    paths = types.SimpleNamespace()
    paths.images_directory = os.path.join(
        app.builder.outdir,
        app.builder.imagedir,
        )
    paths.abjadbook_images_directory = os.path.join(
        paths.images_directory,
        'abjadbook',
        )
    if os.path.exists(paths.images_directory):
        shutil.rmtree(paths.images_directory)
    yield paths
    if os.path.exists(paths.images_directory):
        shutil.rmtree(paths.images_directory)


def test_01(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :no-stylesheet:

        abjad.show(Staff("c'4 d'4 e'4 f'4"))
    '''
    source = normalize(source)
    handler = abjad.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjad.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a href="../_images/abjadbook/lilypond-45bfa031a0601d63a5d8a63a90975a50bfe09a4b.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-45bfa031a0601d63a5d8a63a90975a50bfe09a4b.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 2
    for name in (
        'lilypond-45bfa031a0601d63a5d8a63a90975a50bfe09a4b.ly',
        'lilypond-45bfa031a0601d63a5d8a63a90975a50bfe09a4b.png',
        ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_02(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :no-stylesheet:
        :no-trim:

        abjad.show(Staff("c'4 d'4 e'4 f'4"))
    '''
    source = normalize(source)
    handler = abjad.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjad.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a href="../_images/abjadbook/lilypond-c33d221e64c923a2644f695ea69827db3dcc9c35.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-c33d221e64c923a2644f695ea69827db3dcc9c35.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 2
    for name in (
        'lilypond-c33d221e64c923a2644f695ea69827db3dcc9c35.ly',
        'lilypond-c33d221e64c923a2644f695ea69827db3dcc9c35.png',
        ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_03(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :no-resize:
        :no-stylesheet:
        :no-trim:

        abjad.show(Staff("c'4 d'4 e'4 f'4"))
    '''
    source = normalize(source)
    handler = abjad.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjad.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a href="../_images/abjadbook/lilypond-ab9aee33cea9a52139c015a2d0e87a4c40b35bc6.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-ab9aee33cea9a52139c015a2d0e87a4c40b35bc6.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 2
    for name in (
        'lilypond-ab9aee33cea9a52139c015a2d0e87a4c40b35bc6.ly',
        'lilypond-ab9aee33cea9a52139c015a2d0e87a4c40b35bc6.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_04(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :no-resize:
        :no-stylesheet:
        :no-trim:
        :with-thumbnail:

        abjad.show(Staff("c'4 d'4 e'4 f'4"))
    '''
    source = normalize(source)
    handler = abjad.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjad.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    assert len(app.builder.thumbnails) == 1
    assert '../_images/abjadbook/lilypond-ab9aee33cea9a52139c015a2d0e87a4c40b35bc6.png' in app.builder.thumbnails
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a data-lightbox="group-lilypond-ab9aee33cea9a52139c015a2d0e87a4c40b35bc6.ly" href="../_images/abjadbook/lilypond-ab9aee33cea9a52139c015a2d0e87a4c40b35bc6.png" title="" data-title="" class="abjadbook thumbnail">
            <img src="../_images/abjadbook/lilypond-ab9aee33cea9a52139c015a2d0e87a4c40b35bc6-thumbnail.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 3
    for name in (
        'lilypond-ab9aee33cea9a52139c015a2d0e87a4c40b35bc6.ly',
        'lilypond-ab9aee33cea9a52139c015a2d0e87a4c40b35bc6.png',
        'lilypond-ab9aee33cea9a52139c015a2d0e87a4c40b35bc6-thumbnail.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_05(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :stylesheet: default.ily
        :no-trim:

        abjad.show(Staff("c'4 d'4 e'4 f'4"))
    '''
    source = normalize(source)
    handler = abjad.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    abjad.book.SphinxDocumentHandler.on_builder_inited(app)
    node = document[0]
    try:
        abjad.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a href="../_images/abjadbook/lilypond-c2d3520ee8bb7c6716a50142bf0c3bcdde2c89bd.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-c2d3520ee8bb7c6716a50142bf0c3bcdde2c89bd.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 8
    for name in (
        'default.ily',
        'external-settings-file-1.ily',
        'external-settings-file-2.ily',
        'lilypond-c2d3520ee8bb7c6716a50142bf0c3bcdde2c89bd.ly',
        'lilypond-c2d3520ee8bb7c6716a50142bf0c3bcdde2c89bd.png',
        'rhythm-maker-docs.ily',
        'text-spanner-id.ily',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_06(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :no-stylesheet:

        staff = Staff("c'1 d'1 e'1 f'1 g'1")
        for note in staff[:-1]:
            attach(indicatortools.PageBreak(), note)

        abjad.show(staff)
    '''
    source = normalize(source)
    handler = abjad.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjad.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a href="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e-page1.png" alt=""/>
        </a>
        <a href="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e-page2.png" alt=""/>
        </a>
        <a href="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e-page3.png" alt=""/>
        </a>
        <a href="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e-page4.png" alt=""/>
        </a>
        <a href="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e-page5.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 6
    for name in (
        'lilypond-041ad924d923b74ec406310887d4a8609350791e.ly',
        'lilypond-041ad924d923b74ec406310887d4a8609350791e-page1.png',
        'lilypond-041ad924d923b74ec406310887d4a8609350791e-page2.png',
        'lilypond-041ad924d923b74ec406310887d4a8609350791e-page3.png',
        'lilypond-041ad924d923b74ec406310887d4a8609350791e-page4.png',
        'lilypond-041ad924d923b74ec406310887d4a8609350791e-page5.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_07(app, paths):
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
    source = normalize(source)
    handler = abjad.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjad.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a href="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e-page2.png" alt=""/>
        </a>
        <a href="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e-page3.png" alt=""/>
        </a>
        <a href="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e-page4.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 6
    for name in (
        'lilypond-041ad924d923b74ec406310887d4a8609350791e.ly',
        'lilypond-041ad924d923b74ec406310887d4a8609350791e-page1.png',
        'lilypond-041ad924d923b74ec406310887d4a8609350791e-page2.png',
        'lilypond-041ad924d923b74ec406310887d4a8609350791e-page3.png',
        'lilypond-041ad924d923b74ec406310887d4a8609350791e-page4.png',
        'lilypond-041ad924d923b74ec406310887d4a8609350791e-page5.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_08(app, paths):
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
    source = normalize(source)
    handler = abjad.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjad.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <div class="table-row">
            <a href="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e.ly" title="" class="table-cell">
                <img src="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e.ly" title="" class="table-cell">
                <img src="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e-page3.png" alt=""/>
            </a>
        </div>
        <div class="table-row">
            <a href="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e.ly" title="" class="table-cell">
                <img src="../_images/abjadbook/lilypond-041ad924d923b74ec406310887d4a8609350791e-page4.png" alt=""/>
            </a>
        </div>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 6
    for name in (
        'lilypond-041ad924d923b74ec406310887d4a8609350791e.ly',
        'lilypond-041ad924d923b74ec406310887d4a8609350791e-page1.png',
        'lilypond-041ad924d923b74ec406310887d4a8609350791e-page2.png',
        'lilypond-041ad924d923b74ec406310887d4a8609350791e-page3.png',
        'lilypond-041ad924d923b74ec406310887d4a8609350791e-page4.png',
        'lilypond-041ad924d923b74ec406310887d4a8609350791e-page5.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_09(app, paths):
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
    source = normalize(source)
    handler = abjad.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjad.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <div class="table-row">
            <a href="../_images/abjadbook/lilypond-33d15a8a1af45ee088546508b41684b2c0768e21.ly" title="" class="table-cell">
                <img src="../_images/abjadbook/lilypond-33d15a8a1af45ee088546508b41684b2c0768e21-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-33d15a8a1af45ee088546508b41684b2c0768e21.ly" title="" class="table-cell">
                <img src="../_images/abjadbook/lilypond-33d15a8a1af45ee088546508b41684b2c0768e21-page3.png" alt=""/>
            </a>
        </div>
        <div class="table-row">
            <a href="../_images/abjadbook/lilypond-33d15a8a1af45ee088546508b41684b2c0768e21.ly" title="" class="table-cell">
                <img src="../_images/abjadbook/lilypond-33d15a8a1af45ee088546508b41684b2c0768e21-page4.png" alt=""/>
            </a>
        </div>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 6
    for name in (
        'lilypond-33d15a8a1af45ee088546508b41684b2c0768e21.ly',
        'lilypond-33d15a8a1af45ee088546508b41684b2c0768e21-page1.png',
        'lilypond-33d15a8a1af45ee088546508b41684b2c0768e21-page2.png',
        'lilypond-33d15a8a1af45ee088546508b41684b2c0768e21-page3.png',
        'lilypond-33d15a8a1af45ee088546508b41684b2c0768e21-page4.png',
        'lilypond-33d15a8a1af45ee088546508b41684b2c0768e21-page5.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_10(app, paths):
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
    source = normalize(source)
    handler = abjad.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjad.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a data-lightbox="group-lilypond-ca6b22f15b089a977dd33af90e7930623c29371e.ly" href="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page1.png" title="" data-title="" class="abjadbook thumbnail">
            <img src="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page1-thumbnail.png" alt=""/>
        </a>
        <a data-lightbox="group-lilypond-ca6b22f15b089a977dd33af90e7930623c29371e.ly" href="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page2.png" title="" data-title="" class="abjadbook thumbnail">
            <img src="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page2-thumbnail.png" alt=""/>
        </a>
        <a data-lightbox="group-lilypond-ca6b22f15b089a977dd33af90e7930623c29371e.ly" href="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page3.png" title="" data-title="" class="abjadbook thumbnail">
            <img src="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page3-thumbnail.png" alt=""/>
        </a>
        <a data-lightbox="group-lilypond-ca6b22f15b089a977dd33af90e7930623c29371e.ly" href="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page4.png" title="" data-title="" class="abjadbook thumbnail">
            <img src="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page4-thumbnail.png" alt=""/>
        </a>
        <a data-lightbox="group-lilypond-ca6b22f15b089a977dd33af90e7930623c29371e.ly" href="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page5.png" title="" data-title="" class="abjadbook thumbnail">
            <img src="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page5-thumbnail.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 11
    for name in (
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e.ly',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page1.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page1-thumbnail.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page2.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page2-thumbnail.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page3.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page3-thumbnail.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page4.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page4-thumbnail.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page5.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page5-thumbnail.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_11(app, paths):
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
    source = normalize(source)
    handler = abjad.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjad.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <div class="table-row">
            <a data-lightbox="group-lilypond-ca6b22f15b089a977dd33af90e7930623c29371e.ly" href="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page1.png" title="" data-title="" class="table-cell thumbnail">
                <img src="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page1-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-ca6b22f15b089a977dd33af90e7930623c29371e.ly" href="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page2.png" title="" data-title="" class="table-cell thumbnail">
                <img src="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page2-thumbnail.png" alt=""/>
            </a>
        </div>
        <div class="table-row">
            <a data-lightbox="group-lilypond-ca6b22f15b089a977dd33af90e7930623c29371e.ly" href="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page3.png" title="" data-title="" class="table-cell thumbnail">
                <img src="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page3-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-ca6b22f15b089a977dd33af90e7930623c29371e.ly" href="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page4.png" title="" data-title="" class="table-cell thumbnail">
                <img src="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page4-thumbnail.png" alt=""/>
            </a>
        </div>
        <div class="table-row">
            <a data-lightbox="group-lilypond-ca6b22f15b089a977dd33af90e7930623c29371e.ly" href="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page5.png" title="" data-title="" class="table-cell thumbnail">
                <img src="../_images/abjadbook/lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page5-thumbnail.png" alt=""/>
            </a>
        </div>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 11
    for name in (
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e.ly',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page1.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page1-thumbnail.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page2.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page2-thumbnail.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page3.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page3-thumbnail.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page4.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page4-thumbnail.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page5.png',
        'lilypond-ca6b22f15b089a977dd33af90e7930623c29371e-page5-thumbnail.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)
