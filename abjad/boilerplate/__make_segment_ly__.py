import abjad
import ide
import os
import pathlib
import sys
import traceback


if __name__ == '__main__':

    try:
        from definition import maker
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
        segment_directory = pathlib.Path(os.path.realpath(__file__)).parent
        builds_directory = segment_directory.parent.parent / 'builds'
        builds_directory = ide.Path(builds_directory)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        with abjad.Timer() as timer:
            lilypond_file = maker.run(
                metadata=metadata,
                previous_metadata=previous_metadata,
                )
        segment_maker_runtime = int(timer.elapsed_time)
        count = segment_maker_runtime
        counter = abjad.String('second').pluralize(count)
        message = f'Segment-maker runtime {{count}} {{counter}} ...'
        print(message)
        segment_maker_runtime = (count, counter)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        segment = ide.Path(__file__).parent
        segment.write_metadata_py(maker.metadata)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        illustration_ly = segment('illustration.ly')
        result = abjad.persist(lilypond_file).as_ly(illustration_ly, strict=89)
        abjad_format_time = int(result[1])
        count = abjad_format_time
        counter = abjad.String('second').pluralize(count)
        message = f'Abjad format time {{count}} {{counter}} ...'
        print(message)
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
