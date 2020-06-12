#! /usr/bin/env python
import os
import pathlib
import sys
import traceback

import abjad

if __name__ == "__main__":

    try:
        from definition import maker
        from __metadata__ import metadata as metadata

        {previous_segment_metadata_import_statement}
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        segment_directory = abjad.Path(os.path.realpath(__file__)).parent
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    try:
        with abjad.Timer() as timer:
            lilypond_file = maker.run(
                metadata=metadata,
                midi=True,
                previous_metadata=previous_metadata,
                # include segment directory to write segment name metadata after run
                segment_directory=segment_directory,
            )
        count = int(timer.elapsed_time)
        counter = abjad.String("second").pluralize(count)
        message = f"Abjad runtime {{count}} {{counter}} ..."
        print(message)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    try:
        segment = abjad.Path(__file__).parent
        segment.write_metadata_py(maker.metadata)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    try:
        segment = abjad.Path(__file__).parent
        midi = segment / "segment.midi"
        with abjad.Timer() as timer:
            abjad.persist(lilypond_file).as_midi(midi, remove_ly=True)
        count = int(timer.elapsed_time)
        counter = abjad.String("second").pluralize(count)
        message = f"LilyPond runtime {{count}} {{counter}} ..."
        print(message)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
