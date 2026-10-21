import abjad
import pytest


def _score_file(*, tagged=False):
    note = abjad.Note("c'4")
    if tagged:
        literal = abjad.LilyPondLiteral(r"\fermata", site="before")
        abjad.attach(literal, note, tag=abjad.Tag("SYNTHETIC"))
    score = abjad.Score([abjad.Staff([note])])
    block = abjad.Block("score", items=[score])
    return abjad.LilyPondFile(
        [block],
        lilypond_language_token=False,
        lilypond_version_token=False,
    )


def test_as_ly_uses_keep_tags_and_illustrate_keywords(tmp_path):
    illustrated_keywords = {}

    def illustrate(**keywords):
        illustrated_keywords.update(keywords)
        return _score_file()

    ly_path = tmp_path / "score.ly"
    formatting_time = abjad.persist.as_ly(
        object(),
        ly_path,
        illustrate_function=illustrate,
        keep_tags=True,
        synthetic_option="value",
    )

    assert isinstance(formatting_time, float)
    assert ly_path.is_file()
    assert illustrated_keywords == {"synthetic_option": "value"}


def test_as_ly_can_preserve_score_tags(tmp_path):
    ly_path = tmp_path / "tagged-score.ly"
    formatting_time = abjad.persist.as_ly(
        _score_file(tagged=True), ly_path, keep_tags=True
    )

    assert isinstance(formatting_time, float)
    assert "%! SYNTHETIC" in ly_path.read_text(encoding="utf-8")


def test_as_midi_returns_times_and_exit_code_and_forwards_keywords(
    monkeypatch, tmp_path
):
    illustrated_keywords = []
    render_calls = []

    def illustrate(argument, **keywords):
        illustrated_keywords.append(keywords)
        return _score_file()

    def run_lilypond(ly_path, *, flags):
        render_calls.append((ly_path, flags))
        return 23

    monkeypatch.setattr(abjad.persist._illustrators, "illustrate", illustrate)
    monkeypatch.setattr(abjad.persist._io, "run_lilypond", run_lilypond)
    result = abjad.persist.as_midi(
        object(),
        tmp_path / "score.midi",
        lilypond_flags="--synthetic-midi",
        synthetic_option="value",
    )

    assert len(result) == 3
    assert isinstance(result[0], float)
    assert isinstance(result[1], float)
    assert result[2] == 23
    assert illustrated_keywords == [
        {"synthetic_option": "value"},
        {"synthetic_option": "value"},
    ]
    assert render_calls[0][0] == str(tmp_path / "score.ly")
    assert render_calls[0][1] == "--synthetic-midi"


def test_as_pdf_requires_pdf_extension(tmp_path):
    with pytest.raises(ValueError, match=".pdf"):
        abjad.persist.as_pdf(_score_file(), tmp_path / "score")

    assert not (tmp_path / "score.ly").exists()


def test_as_pdf_returns_times_and_exit_code_and_forwards_keywords(
    monkeypatch, tmp_path
):
    illustrated_keywords = {}
    render_calls = []

    def illustrate(**keywords):
        illustrated_keywords.update(keywords)
        return _score_file(tagged=True)

    def run_lilypond(ly_path, *, flags):
        render_calls.append((ly_path, flags))
        return 17

    monkeypatch.setattr(abjad.persist._io, "run_lilypond", run_lilypond)
    result = abjad.persist.as_pdf(
        object(),
        tmp_path / "score.pdf",
        lilypond_flags="--synthetic-pdf",
        illustrate_function=illustrate,
        keep_tags=True,
        synthetic_option="value",
    )

    assert len(result) == 3
    assert isinstance(result[0], float)
    assert isinstance(result[1], float)
    assert result[2] == 17
    assert illustrated_keywords == {"synthetic_option": "value"}
    assert render_calls == [(str(tmp_path / "score.ly"), "--synthetic-pdf")]
    assert "%! SYNTHETIC" in (tmp_path / "score.ly").read_text(encoding="utf-8")


def test_as_png_uses_new_keyword_names_and_task_local_temporary_files(
    monkeypatch, tmp_path
):
    illustrated_keywords = {}
    render_calls = []
    temporary_directory = tmp_path / "png-render"

    def illustrate(**keywords):
        illustrated_keywords.update(keywords)
        return _score_file(tagged=True)

    def make_temporary_directory():
        temporary_directory.mkdir()
        return str(temporary_directory)

    def run_lilypond(ly_path, *, flags):
        render_calls.append((ly_path, flags))
        return 11

    monkeypatch.setattr(abjad.persist.tempfile, "mkdtemp", make_temporary_directory)
    monkeypatch.setattr(abjad.persist._io, "run_lilypond", run_lilypond)
    result = abjad.persist.as_png(
        object(),
        tmp_path / "score.png",
        lilypond_flags="--png",
        illustrate_function=illustrate,
        preview=True,
        resolution=144,
        keep_tags=True,
        synthetic_option="value",
    )

    assert result[0] == ()
    assert isinstance(result[1], float)
    assert isinstance(result[2], float)
    assert result[3] == 11
    assert illustrated_keywords == {"synthetic_option": "value"}
    assert render_calls[0][0].startswith(str(temporary_directory))
    assert render_calls[0][1] == "--png -dpreview -dresolution=144"
    assert not temporary_directory.exists()
    assert "%! SYNTHETIC" in (tmp_path / "score.ly").read_text(encoding="utf-8")


def test_lilypond_uses_keep_keyword_names():
    note = abjad.Note("c'4")
    literal = abjad.LilyPondLiteral(r"\fermata", site="before")
    abjad.attach(literal, note, tag=abjad.Tag("SYNTHETIC"))

    lilypond = abjad.lilypond(note, keep_site_comments=True, keep_tags=True)

    assert "%! SYNTHETIC" in lilypond
