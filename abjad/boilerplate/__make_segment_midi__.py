#! /usr/bin/env python
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
                midi=True,
                previous_metadata=previous_metadata,
                )
        count = int(timer.elapsed_time)
        counter = abjad.String('second').pluralize(count)
        message = f'Abjad runtime {{count}} {{counter}} ...'
        print(message)
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
        segment = ide.Path(__file__).parent
        midi = segment('segment.midi')
        with abjad.Timer() as timer:
            abjad.persist(lilypond_file).as_midi(midi, remove_ly=True)
        count = int(timer.elapsed_time)
        counter = abjad.String('second').pluralize(count)
        message = f'LilyPond runtime {{count}} {{counter}} ...'
        print(message)
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
