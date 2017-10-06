import abjad
import ide
import pathlib
import sys
import traceback


if __name__ == '__main__':

    try:
        from definition import segment_maker
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        from __metadata__ import metadata as metadata
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        {previous_segment_metadata_import_statement}
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        with abjad.Timer() as timer:
            result = segment_maker.run(
                metadata=metadata,
                previous_metadata=previous_metadata,
                )
            lilypond_file, metadata = result
        total_time = int(timer.elapsed_time)
        identifier = abjad.String('second').pluralize(total_time)
        message = f'Abjad runtime {{total_time}} {{identifier}} ...'
        print(message)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        directory = pathlib.Path(__file__).parent
        directory = ide.Path(directory)
        directory._write_metadata_py(metadata)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        directory = pathlib.Path(__file__).parent
        directory = ide.Path(directory)
        target = directory('illustration.ly')
        with abjad.Timer() as timer:
            abjad.persist(lilypond_file).as_ly(target)
        total_time = int(timer.elapsed_time)
        identifier = abjad.String('second').pluralize(total_time)
        message = f'LilyPond runtime {{total_time}} {{identifier}} ...'
        print(message)
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
