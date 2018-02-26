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
        from __metadata__ import metadata as metadata
        {previous_segment_metadata_import_statement}
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        segment_directory = ide.Path(os.path.realpath(__file__)).parent
        illustration_ly = segment_directory('illustration.ly')
        with abjad.Timer() as timer:
            lilypond_file = maker.run(
                metadata=metadata,
                previous_metadata=previous_metadata,
                segment_directory=segment_directory,
                )
        segment_maker_runtime = int(timer.elapsed_time)
        count = segment_maker_runtime
        counter = abjad.String('second').pluralize(count)
        message = f'Segment-maker runtime {{count}} {{counter}} ...'
        print(message)
        segment_maker_runtime = (count, counter)
        segment_directory.write_metadata_py(maker.metadata)
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
        text = illustration_ly.read_text()
        text = abjad.LilyPondFormatManager.left_shift_tags(text, realign=89)
        illustration_ly.write_text(text)
        for job in [
            abjad.Job.edition_specific_job(illustration_ly),
            abjad.Job.music_annotation_job(illustration_ly, undo=True),
            abjad.Job.fermata_bar_line_job(segment_directory),
            abjad.Job.shifted_clef_job(segment_directory),
            ]:
            for message in job():
                print(message)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        layout_py = segment_directory('layout.py')
        if not layout_py.exists():
            print('Writing stub layout.py ...')
            layout_py.write_text('')
        layout_ly = segment_directory('layout.ly')
        if not layout_ly.exists():
            print('Writing stub layout.ly ...')
            layout_ly.write_text('')
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        if getattr(maker, 'do_not_externalize', False) is not True:
            illustration_ly.extern()
            illustration_ily = illustration_ly.with_suffix('.ily')
            assert illustration_ily.is_file()
        with abjad.Timer() as timer:
            abjad.IOManager.run_lilypond(illustration_ly)
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
        history = segment_directory('.history')
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
