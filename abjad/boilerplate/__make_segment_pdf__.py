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
        scores_directory = segment_directory.parent.parent.parent.parent
        segment_directory = ide.Path(
            segment_directory,
            scores=scores_directory,
            )
        assert segment_directory.is_score_package_path(), repr(segment_directory)
        illustration_ly = segment_directory('illustration.ly')
        print(' Running segment-maker ...')
        with abjad.Timer() as timer:
            lilypond_file = maker.run(
                metadata=metadata,
                previous_metadata=previous_metadata,
                segment_directory=segment_directory,
                )
        segment_maker_runtime = int(timer.elapsed_time)
        count = segment_maker_runtime
        counter = abjad.String('second').pluralize(count)
        message = f' Segment-maker runtime {{count}} {{counter}} ...'
        print(message)
        segment_maker_runtime = (count, counter)
        segment_directory.write_metadata_py(maker.metadata)
        result = abjad.persist(lilypond_file).as_ly(illustration_ly, strict=89)
        abjad_format_time = int(result[1])
        count = abjad_format_time
        counter = abjad.String('second').pluralize(count)
        message = f' Abjad format time {{count}} {{counter}} ...'
        print(message)
        abjad_format_time = (count, counter)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        if 'GlobalSkips' in lilypond_file:
            context = lilypond_file['GlobalSkips']
            measure_count = len(context)
            counter = abjad.String('measure').pluralize(measure_count)
            message = f' Wrote {{measure_count}} {{counter}}'
            message += f' to {{illustration_ly.trim()}} ...'
            print(message)
            time_signatures = []
            prototype = abjad.TimeSignature
            for skip in context:
                time_signature = abjad.inspect(skip).effective(prototype)
                assert isinstance(time_signature, prototype)
                time_signatures.append(str(time_signature))
        else:
            measure_count = None
            time_signatures = None
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        text = illustration_ly.read_text()
        text = abjad.LilyPondFormatManager.left_shift_tags(text, realign=99)
        illustration_ly.write_text(text)
        for job in [
            abjad.Job.handle_edition_tags(illustration_ly),
            abjad.Job.show_music_annotations(illustration_ly, undo=True),
            abjad.Job.handle_fermata_bar_lines(segment_directory),
            abjad.Job.handle_shifted_clefs(segment_directory),
            ]:
            for message in job():
                print(' ' + message)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        layout_py = segment_directory('layout.py')
        if not layout_py.exists():
            print(' Writing stub layout.py ...')
            layout_py.write_text('')
        layout_ly = segment_directory('layout.ly')
        if not layout_ly.exists():
            print(' Writing stub layout.ly ...')
            layout_ly.write_text('')
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        if layout_py.read_text() == '':
            empty_layout = True
        else:
            empty_layout = False
        if empty_layout:
            print(f' Ignoring empty {{layout_py.trim()}} ...')
        else:
            layout_time_signatures = layout_ly.get_preamble_time_signatures()
            if layout_time_signatures is not None:
                assert isinstance(layout_time_signatures, list)
                layout_measure_count = len(layout_time_signatures)
                counter = abjad.String('measure').pluralize(
                    layout_measure_count)
                message = f' Found {{layout_measure_count}} {{counter}}'
                message += f' in {{layout_ly.trim()}} ...'
                print(message)
                if layout_time_signatures == time_signatures:
                    message = ' Music time signatures match'
                    message += ' layout time signatures ...'
                    print(message)
                else:
                    message = 'Music time signatures do not match'
                    message += ' layout time signatures ...'
                    print(message)
                    print(f' Remaking {{layout_ly.trim()}} ...')
                    ide = ide.AbjadIDE()
                    ide._make_layout_ly(layout_py)
                    counter = abjad.String('measure').pluralize(measure_count)
                    message = f' Found {{measure_count}} {{counter}}'
                    message += f' in {{illustration_ly.trim()}} ...'
                    print(message)
                    layout_time_signatures = \
                        layout_ly.get_preamble_time_signatures()
                    layout_measure_count = len(layout_time_signatures)
                    counter = abjad.String('measure').pluralize(
                        layout_measure_count
                        )
                    message = f' Found {{layout_measure_count}} {{counter}}'
                    message += f' in {{layout_ly.trim()}} ...'
                    print(message)
                    if layout_time_signatures != time_signatures:
                        message = ' Music time signatures still do not match'
                        message += ' layout time signatures ...'
                        print(message)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        if getattr(maker, 'do_not_externalize', False) is not True:
            illustration_ly.extern()
            illustration_ily = illustration_ly.with_suffix('.ily')
            assert illustration_ily.is_file()
        with abjad.Timer() as timer:
            print(' Running LilyPond ...')
            abjad.IOManager.run_lilypond(illustration_ly)
        lilypond_runtime = int(timer.elapsed_time)
        count = lilypond_runtime
        counter = abjad.String('second').pluralize(count)
        message = f' LilyPond runtime {{count}} {{counter}} ...'
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
            line = f' Segment-maker runtime: {{count}} {{counter}}\n'
            pointer.write(line)
            count, counter = abjad_format_time
            line = f' Abjad format time: {{count}} {{counter}}\n'
            pointer.write(line)
            count, counter = lilypond_runtime
            line = f' LilyPond runtime: {{count}} {{counter}}\n'
            pointer.write(line)
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
