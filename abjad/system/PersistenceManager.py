import os
import re
import shutil
import tempfile

from .IOManager import IOManager
from .StorageFormatManager import StorageFormatManager
from .Timer import Timer


class PersistenceManager(object):
    """
    Persistence manager.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.persist(staff)
        PersistenceManager(client=Staff("c'4 e'4 d'4 f'4"))

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_client",)

    _png_page_pattern = re.compile(r".+page(\d+)\.png")

    ### INITIALIZER ###

    def __init__(self, client=None):
        self._client = client

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        """
        Client of persistence manager.

        Returns component or selection.
        """
        return self._client

    ### PUBLIC METHODS ###

    def as_ly(
        self, ly_file_path=None, illustrate_function=None, strict=None, **keywords,
    ):
        """
        Persists client as LilyPond file.

        Autogenerates file path when ``ly_file_path`` is none.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
            >>> for x in abjad.persist(staff).as_ly('~/example.ly'): # doctest: +SKIP
            ...     x
            ...
            '/Users/josiah/Desktop/example.ly'
            0.04491996765136719

        Returns output path and elapsed formatting time when LilyPond output is
        written.
        """
        import abjad

        if strict is not None:
            assert isinstance(strict, int), repr(strict)
        if illustrate_function is None:
            assert hasattr(self._client, "__illustrate__")
            illustrate_function = self._client.__illustrate__
        lilypond_file = illustrate_function(**keywords)
        if ly_file_path is None:
            ly_file_name = abjad.IOManager.get_next_output_file_name()
            ly_file_path = os.path.join(
                abjad.abjad_configuration.abjad_output_directory, ly_file_name
            )
        else:
            ly_file_path = str(ly_file_path)
            ly_file_path = os.path.expanduser(ly_file_path)
        assert ly_file_path.endswith(".ly"), ly_file_path
        timer = abjad.Timer()
        with timer:
            string = lilypond_file.__format__(format_specification="lilypond")
            if isinstance(strict, int):
                string = abjad.LilyPondFormatManager.align_tags(string, strict)
        abjad_formatting_time = timer.elapsed_time
        directory = os.path.dirname(ly_file_path)
        abjad.IOManager._ensure_directory_existence(directory)
        with open(ly_file_path, "w") as file_pointer:
            file_pointer.write(string)
        return ly_file_path, abjad_formatting_time

    def as_midi(self, midi_file_path=None, remove_ly=False, **keywords):
        """
        Persists client as MIDI file.

        Autogenerates file path when ``midi_file_path`` is none.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
            >>> for x in abjad.persist(staff).as_midi(): # doctest: +SKIP
            ...     x
            ...
            '/Users/josiah/.abjad/output/1415.midi'
            0.07831692695617676
            1.0882699489593506

        Returns 4-tuple of output MIDI path, Abjad formatting time, LilyPond
        rendering time and success boolean.
        """
        assert hasattr(self._client, "__illustrate__")
        lilypond_file = self._client.__illustrate__(**keywords)
        assert hasattr(lilypond_file, "score_block")
        if midi_file_path is not None:
            midi_file_path = os.path.expanduser(midi_file_path)
            without_extension = os.path.splitext(midi_file_path)[0]
            ly_file_path = f"{without_extension}.ly"
        else:
            ly_file_path = None
        result = type(self)(lilypond_file).as_ly(ly_file_path, **keywords)
        ly_file_path, abjad_formatting_time = result
        timer = Timer()
        with timer:
            success = IOManager.run_lilypond(ly_file_path)
        lilypond_rendering_time = timer.elapsed_time
        if remove_ly:
            os.remove(ly_file_path)
        if os.name == "nt":
            extension = "mid"
        else:
            extension = "midi"
        path = os.path.splitext(ly_file_path)[0]
        pdf_file_path = f"{path}.pdf"
        os.remove(pdf_file_path)
        midi_file_path = f"{path}.{extension}"
        return (
            midi_file_path,
            abjad_formatting_time,
            lilypond_rendering_time,
            success,
        )

    def as_pdf(
        self,
        pdf_file_path=None,
        illustrate_function=None,
        remove_ly=False,
        strict=None,
        **keywords,
    ):
        """
        Persists client as PDF.

        Autogenerates file path when ``pdf_file_path`` is none.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
            >>> for x in abjad.persist(staff).as_pdf(): # doctest: +SKIP
            ...     x
            ...
            '/Users/josiah/.abjad/output/1416.pdf'
            0.047142982482910156
            0.7839350700378418

        Returns output path, elapsed formatting time and elapsed rendering
        time when PDF output is written.
        """
        import abjad

        if strict is not None:
            assert isinstance(strict, int), repr(strict)
        if illustrate_function is None:
            assert hasattr(self._client, "__illustrate__"), repr(self._client)
        if pdf_file_path is not None:
            pdf_file_path = str(pdf_file_path)
            pdf_file_path = os.path.expanduser(pdf_file_path)
            without_extension = os.path.splitext(pdf_file_path)[0]
            ly_file_path = "{}.ly".format(without_extension)
        else:
            ly_file_path = None
        result = self.as_ly(
            ly_file_path,
            illustrate_function=illustrate_function,
            strict=strict,
            **keywords,
        )
        ly_file_path, abjad_formatting_time = result
        without_extension = os.path.splitext(ly_file_path)[0]
        pdf_file_path = "{}.pdf".format(without_extension)
        timer = abjad.Timer()
        with timer:
            success = abjad.IOManager.run_lilypond(ly_file_path)
        lilypond_rendering_time = timer.elapsed_time
        if remove_ly:
            os.remove(ly_file_path)
        return (
            pdf_file_path,
            abjad_formatting_time,
            lilypond_rendering_time,
            success,
        )

    def as_png(
        self,
        flags="--png",
        illustrate_function=None,
        png_file_path=None,
        preview=False,
        remove_ly=False,
        resolution=False,
        **keywords,
    ):
        """
        Persists client as PNG.

        ..  container:: example

            >>> staff = abjad.Staff()
            >>> container = abjad.Container("c'4 d'4 e'4 f'4")
            >>> command = abjad.LilyPondLiteral(r'\break', 'after')
            >>> abjad.attach(command, container[-1])
            >>> staff.extend(200 * container)

            >>> result = abjad.persist(staff).as_png() # doctest: +SKIP
            >>> for x in result[0]: # doctest: +SKIP
            ...     x
            ...
            '/Users/josiah/Desktop/test-page1.png'
            '/Users/josiah/Desktop/test-page2.png'
            '/Users/josiah/Desktop/test-page3.png'
            '/Users/josiah/Desktop/test-page4.png'
            '/Users/josiah/Desktop/test-page5.png'
            '/Users/josiah/Desktop/test-page6.png'
            '/Users/josiah/Desktop/test-page7.png'
            '/Users/josiah/Desktop/test-page8.png'
            '/Users/josiah/Desktop/test-page9.png'
            '/Users/josiah/Desktop/test-page10.png'
            '/Users/josiah/Desktop/test-page11.png'
            '/Users/josiah/Desktop/test-page12.png'
            '/Users/josiah/Desktop/test-page13.png'
            '/Users/josiah/Desktop/test-page14.png'
            '/Users/josiah/Desktop/test-page15.png'

        Autogenerates file path when ``png_file_path`` is none.

        Returns output path(s), elapsed formatting time and elapsed rendering
        time.
        """
        import abjad

        if illustrate_function is None:
            assert hasattr(self._client, "__illustrate__")
        if png_file_path is not None:
            png_file_path = os.path.expanduser(png_file_path)
            without_extension = os.path.splitext(png_file_path)[0]
            ly_file_path = "{}.ly".format(without_extension)
        else:
            ly_file_path = None
        result = self.as_ly(
            ly_file_path, illustrate_function=illustrate_function, **keywords
        )

        ly_file_path, abjad_formatting_time = result

        original_directory = os.path.split(ly_file_path)[0]
        original_ly_file_path = ly_file_path
        temporary_directory = tempfile.mkdtemp()
        temporary_ly_file_path = os.path.join(
            temporary_directory, os.path.split(ly_file_path)[1]
        )
        shutil.copy(original_ly_file_path, temporary_ly_file_path)

        # render lilypond flags
        if preview:
            flags = "-dpreview"
        if resolution and isinstance(resolution, int):
            flags += " -dresolution={}".format(resolution)

        timer = abjad.Timer()
        with timer:
            success = abjad.IOManager.run_lilypond(temporary_ly_file_path, flags=flags)
        lilypond_rendering_time = timer.elapsed_time

        png_file_paths = []
        for file_name in os.listdir(temporary_directory):
            if not file_name.endswith(".png"):
                continue
            source_png_file_path = os.path.join(temporary_directory, file_name)
            target_png_file_path = os.path.join(original_directory, file_name)
            shutil.move(source_png_file_path, target_png_file_path)
            png_file_paths.append(target_png_file_path)
        shutil.rmtree(temporary_directory)

        if remove_ly:
            os.remove(ly_file_path)

        if 1 < len(png_file_paths):
            png_file_paths.sort(
                key=lambda x: int(self._png_page_pattern.match(x).groups()[0])
            )

        return (
            tuple(png_file_paths),
            abjad_formatting_time,
            lilypond_rendering_time,
            success,
        )
