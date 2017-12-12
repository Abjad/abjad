#! /usr/bin/env python
import abjad
import ide
import sys
import time
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
        with abjad.Timer() as timer:
            lilypond_file = maker.run(
                metadata=metadata,
                previous_metadata=previous_metadata,
                )
        segment_runtime = int(timer.elapsed_time)
        count = segment_runtime
        counter = abjad.String('second').pluralize(count)
        message = f'Segment runtime {{count}} {{counter}} ...'
        print(message)
        segment_runtime = (count, counter)
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
        pdf = segment('illustration.pdf')
        result = abjad.persist(lilypond_file).as_pdf(pdf)
        abjad_runtime = int(result[1])
        lilypond_runtime = int(result[2])
        count = abjad_runtime
        counter = abjad.String('second').pluralize(count)
        message = f'Abjad runtime {{count}} {{counter}} ...'
        print(message)
        abjad_runtime = (count, counter)
        count = lilypond_runtime
        counter = abjad.String('second').pluralize(count)
        message = f'LilyPond runtime {{count}} {{counter}} ...'
        print(message)
        lilypond_runtime = (count, counter)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        history = ide.Path(__file__).parent('.history')
        with history.open(mode='a') as pointer:
            pointer.write('\n')
            line = time.strftime('%Y-%m-%d %H:%M:%S') + '\n'
            pointer.write(line)
            count, counter = segment_runtime
            line = f'Segment runtime: {{count}} {{counter}}\n'
            pointer.write(line)
            count, counter = abjad_runtime
            line = f'Abjad runtime: {{count}} {{counter}}\n'
            pointer.write(line)
            count, counter = lilypond_runtime
            line = f'LilyPond runtime: {{count}} {{counter}}\n'
            pointer.write(line)
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
