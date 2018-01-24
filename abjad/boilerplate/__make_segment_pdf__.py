#! /usr/bin/env python
import abjad
import ide
import os
import pathlib
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
        segment = ide.Path(os.path.realpath(__file__)).parent
        ly = segment('illustration.ly')
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
        abjad_format_time = (count, counter)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        text = ly.read_text()
        text = abjad.LilyPondFormatManager.left_shift_tags(text, realign=89)
        ly.write_text(text)
        result = ly.activate('+SEGMENT')
        for message in result[-1]:
            print(message)
        result = ly.deactivate('-SEGMENT')
        for message in result[-1]:
            print(message)
        tags_ = abjad.tags.all_score_annotation_tags()
        match = lambda tags: bool(set(tags) & set(tags_))
        result = ly.deactivate(match, name='score annotation')
        for message in result[-1]:
            print(message)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        result = segment._deactivate_bar_line_adjustment()
        for message in result[-1]:
            print(message)
        result = segment._deactivate_shifted_clef_at_bol()
        for message in result[-1]:
            print(message)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        layout_py = segment('layout.py')
        if not layout_py.exists():
            print('Writing stub layout.py ...')
            layout_py.write_text('')
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        layout_ly = segment('layout.ly')
        if not layout_ly.exists():
            print('Writing stub layout.ly ...')
            layout_ly.write_text('')
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        with abjad.Timer() as timer:
            abjad.IOManager.run_lilypond(ly)
        lilypond_runtime = int(timer.elapsed_time)
        count = lilypond_runtime
        counter = abjad.String('second').pluralize(count)
        message = f'LilyPond runtime {{count}} {{counter}} ...'
        print(message)
        lilypond_runtime = (count, counter)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        history = segment('.history')
        with history.open(mode='a') as pointer:
            pointer.write('\n')
            line = time.strftime('%Y-%m-%d %H:%M:%S') + '\n'
            pointer.write(line)
            count, counter = segment_maker_runtime
            line = f'Segment-maker runtime: {{count}} {{counter}}\n'
            pointer.write(line)
            count, counter = abjad_format_time
            line = f'Abjad format time: {{count}} {{counter}}\n'
            pointer.write(line)
            count, counter = lilypond_runtime
            line = f'LilyPond runtime: {{count}} {{counter}}\n'
            pointer.write(line)
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
