import pathlib
import re
import shutil

import pytest
from uqbar.strings import normalize


@pytest.fixture
def rm_dirs(app):
    path = pathlib.Path(app.doctreedir)
    shutil.rmtree(path)
    yield


@pytest.mark.sphinx("html", testroot="ext-sphinx")
def test_ext_sphinx_01(app, status, warning, rm_dirs):
    app.build()
    assert not warning.getvalue().strip()
    images_path = pathlib.Path(app.outdir) / "_images"
    assert sorted(path.name for path in images_path.iterdir()) == [
        "lilypond-3783b6e7181254e55e3b7d08e13d0d33e6c38f876cfd5940ccb4463d330038c9.cropped.svg",
        "lilypond-3783b6e7181254e55e3b7d08e13d0d33e6c38f876cfd5940ccb4463d330038c9.ly",
        "lilypond-3783b6e7181254e55e3b7d08e13d0d33e6c38f876cfd5940ccb4463d330038c9.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-1.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-2.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-3.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-4.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6.cropped.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6.ly",
    ]

    index_path = pathlib.Path(app.srcdir) / "_build" / "html" / "index.html"
    index_source = index_path.read_text()
    assert re.findall(r"lilypond-\w{64}(?:-\d+|.cropped)?\.svg", index_source) == [
        "lilypond-3783b6e7181254e55e3b7d08e13d0d33e6c38f876cfd5940ccb4463d330038c9.cropped.svg",
        "lilypond-3783b6e7181254e55e3b7d08e13d0d33e6c38f876cfd5940ccb4463d330038c9.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6.cropped.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-1.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-2.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-3.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-4.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-2.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-3.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-1.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-1.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-1.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-2.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-2.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-3.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-3.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-4.svg",
        "lilypond-ae85543c2c6b55401c314d48f1cbccc7cb9b73226151a6a2d3453333945d0be6-4.svg",
    ]


@pytest.mark.sphinx("text", testroot="ext-sphinx")
def test_ext_sphinx_02(app, status, warning, rm_dirs):
    app.build()
    assert not warning.getvalue().strip()
    index_path = pathlib.Path(app.srcdir) / "_build" / "text" / "index.txt"
    assert normalize(index_path.read_text()) == normalize(
        r"""
        Fake Docs
        *********

        This will show the cropped version of the staff:

           >>> staff = abjad.Staff("c' d' e' f'")
           >>> abjad.show(staff)

           \version "2.19.83"
           \language "english"
           #(ly:set-option 'relative-includes #t)
           \include "default.ily"

           \score {
               \new Staff
               {
                   c'4
                   d'4
                   e'4
                   f'4
               }
           }

        This will show the uncropped version of the staff:

           >>> abjad.show(staff)

           \version "2.19.83"
           \language "english"
           #(ly:set-option 'relative-includes #t)
           \include "default.ily"

           \score {
               \new Staff
               {
                   c'4
                   d'4
                   e'4
                   f'4
               }
           }

        This will show the single-SVG cropped version of the 4-page staff:

           >>> multipage_staff = abjad.Staff("c'1 d'1 e'1 f'1")
           >>> for note in multipage_staff:
           ...     page_break = abjad.LilyPondLiteral(r"\pageBreak", format_slot="after")
           ...     abjad.attach(page_break, note)
           ...
           >>> abjad.show(multipage_staff)

           \version "2.19.83"
           \language "english"
           #(ly:set-option 'relative-includes #t)
           \include "default.ily"

           \score {
               \new Staff
               {
                   c'1
                   \pageBreak
                   d'1
                   \pageBreak
                   e'1
                   \pageBreak
                   f'1
                   \pageBreak
               }
           }

        This will show four individual pages, because there is no single SVG
        for uncropped output for the 4-page staff:

           >>> abjad.show(multipage_staff)

           \version "2.19.83"
           \language "english"
           #(ly:set-option 'relative-includes #t)
           \include "default.ily"

           \score {
               \new Staff
               {
                   c'1
                   \pageBreak
                   d'1
                   \pageBreak
                   e'1
                   \pageBreak
                   f'1
                   \pageBreak
               }
           }

        This will show pages 2, 3 and 1 of the 4-page staff:

           >>> abjad.show(multipage_staff)

           \version "2.19.83"
           \language "english"
           #(ly:set-option 'relative-includes #t)
           \include "default.ily"

           \score {
               \new Staff
               {
                   c'1
                   \pageBreak
                   d'1
                   \pageBreak
                   e'1
                   \pageBreak
                   f'1
                   \pageBreak
               }
           }

        This will show all four pages, in a 2x2 grid:

           >>> abjad.show(multipage_staff)

           \version "2.19.83"
           \language "english"
           #(ly:set-option 'relative-includes #t)
           \include "default.ily"

           \score {
               \new Staff
               {
                   c'1
                   \pageBreak
                   d'1
                   \pageBreak
                   e'1
                   \pageBreak
                   f'1
                   \pageBreak
               }
           }
        """
    )
