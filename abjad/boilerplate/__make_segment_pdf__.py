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
        segment = ide.Path(__file__).parent
        ly = segment('illustration.ly')
        result = abjad.persist(lilypond_file).as_ly(ly, strict=89)
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
        segment = ide.Path(__file__).parent
        ly = segment('illustration.ly')
        text = ly.read_text()
        text = abjad.LilyPondFormatManager.left_shift_tags(text, realign=89)
        ly.write_text(text)
        tag = f'+{{abjad.tags.SEGMENT}}'
        text, count = ly.activate_tag(tag)
        messages = ide.AbjadIDE._message_activate(None, tag, count)
        for message in messages:
            print(abjad.String(message).capitalize_start())
        ly.write_text(text)
        tag = f'-{{abjad.tags.SEGMENT}}'
        text, count = ly.deactivate_tag(tag)
        messages = ide.AbjadIDE._message_deactivate(None, tag, count)
        for message in messages:
            print(abjad.String(message).capitalize_start())
        ly.write_text(text)
        text, count = ly.deactivate_tag(
            lambda tags: bool(set(tags) & set(abjad.tags.markup_tags)),
            )
        messages = ide.AbjadIDE._message_deactivate(
            None,
            tag,
            count,
            name='markup',
            )
        for message in messages:
            print(abjad.String(message).capitalize_start())
        ly.write_text(text)
    except:
        traceback.print_exc()
        sys.exit(1)

    # deactivate bar line adjustments after non-EOL fermata measures:
    try:
        bol_measure_numbers = segment.get_metadatum('bol_measure_numbers')
        if bol_measure_numbers is not None:
            eol_measure_numbers = [_ - 1 for _ in bol_measure_numbers[1:]]
            last_measure_number = segment.get_metadatum('last_measure_number')
            eol_measure_numbers.append(last_measure_number)
            eol_measure_numbers = [
                f'MEASURE_{{_}}' for _ in eol_measure_numbers
                ]
            tag = abjad.tags.BAR_LINE_ADJUSTMENT_AFTER_EOL_FERMATA
            def match(tags):
                if tag not in tags:
                    return False
                if any(_ in tags for _ in eol_measure_numbers):
                    return False
                return True
            text, count = ly.deactivate_tag(match)
            name = abjad.tags.BAR_LINE_ADJUSTMENT_AFTER_EOL_FERMATA
            messages = ide.AbjadIDE._message_deactivate(
                None,
                tag,
                count,
                name=name,
                )
            for message in messages:
                print(abjad.String(message).capitalize_start())
            ly.write_text(text)
    except:
        traceback.print_exc()
        sys.exit(1)

    # deactivate shifted clefs at BOL measures:
    try:
        bol_measure_numbers = segment.get_metadatum('bol_measure_numbers')
        if bol_measure_numbers is not None:
            bol_measure_numbers = [
                f'MEASURE_{{_}}' for _ in bol_measure_numbers
                ]
            def match(tags):
                if abjad.tags.SHIFTED_CLEF not in tags:
                    return False
                if any(_ in tags for _ in bol_measure_numbers):
                    return True
                return False
            text, count = ly.deactivate_tag(match)
            name = abjad.tags.SHIFTED_CLEF
            messages = ide.AbjadIDE._message_deactivate(
                None,
                tag,
                count,
                name=name,
                )
            for message in messages:
                print(abjad.String(message).capitalize_start())
            ly.write_text(text)
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
        segment = ide.Path(__file__).parent
        ly = segment('illustration.ly')
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
        history = ide.Path(__file__).parent('.history')
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
