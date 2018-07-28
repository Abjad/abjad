#! /usr/bin/env python
import abjad
import baca
import ide
import os
import pathlib
import sys
import traceback


if __name__ == '__main__':

    layout_module_name = '{layout_module_name}'
    maker = ide.Path(os.path.realpath(__file__))

    try:
        from {layout_module_name} import breaks
        assert isinstance(breaks, baca.BreakMeasureMap), repr(breaks)
    except ImportError:
        print(f'No breaks in {{maker.trim()}} ...')
        sys.exit(1)

    try:
        from {layout_module_name} import spacing
        prototype = baca.HorizontalSpacingSpecifier
        assert isinstance(spacing, prototype), repr(spacing)
    except ImportError:
        spacing = None

    try:
        buildspace_directory = maker.parent
        layout_py = buildspace_directory('{layout_module_name}.py')
        document_name = abjad.String(buildspace_directory.name).to_shout_case()
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        if buildspace_directory.get_metadatum('parts_directory') is True:
            from {layout_module_name} import part_identifier
            assert abjad.String(part_identifier).is_shout_case()
            document_name = f'{{document_name}}_{{part_identifier}}'
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        if buildspace_directory.is_segment():
            string = 'first_measure_number'
            first_measure_number = buildspace_directory.get_metadatum(string)
            if not bool(first_measure_number):
                print('Can not find first measure number ...')
                first_measure_number = False
            assert isinstance(first_measure_number, int)
        else:
            first_measure_number = 1
    except:
        traceback.print_exc()
        sys.exit(1)

    if first_measure_number is False:
        print('Skipping layout ...')
        sys.exit(1)
        
    try:
        assert abjad.String(document_name).is_shout_case()
        string = 'first_measure_number'
        first_measure_number = buildspace_directory.get_metadatum(string, 1)
        time_signatures = buildspace_directory.get_time_signature_metadata()
        if breaks.partial_score is not None:
            time_signatures = time_signatures[:breaks.partial_score]
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        print(' Running segment-maker ...')
        maker = baca.SegmentMaker(
            breaks=breaks,
            do_not_check_persistence=True,
            do_not_include_layout_ly=True,
            final_bar_line=False,
            first_measure_number=first_measure_number,
            score_template=baca.SingleStaffScoreTemplate(),
            spacing=spacing,
            time_signatures=time_signatures,
            )
        lilypond_file = maker.run(remove=abjad.tags.layout_removal_tags())
        context = lilypond_file['GlobalSkips']
        skips = baca.select(context).skips()
        for skip in skips:
            abjad.detach(abjad.TimeSignature, skip)
        score = lilypond_file['Score']
        del(score['MusicContext'])
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        score = lilypond_file['Score']
        text = format(score, 'lilypond')
        text = text.replace('GlobalSkips', 'PageLayout')
        text = abjad.LilyPondFormatManager.left_shift_tags(text, realign=89)
        time_signatures = [str(_) for _ in time_signatures]
        line_1 = f'% time_signatures = {{time_signatures}}\n'
        measure_count = len(time_signatures)
        line_2 = f'% measure_count = {{measure_count}}\n'
        if breaks.partial_score is not None:
            line_3 = f'% partial_score = True'
            text = line_1 + line_2 + line_3 + '\n\n' + text
        else:
            text = line_1 + line_2 + '\n\n' + text
        layout_ly = layout_module_name.replace('_', '-') + '.ly'
        layout_ly = buildspace_directory(layout_ly)
        layout_ly.write_text(text)
        counter = abjad.String('measure').pluralize(measure_count)
        message = f' Writing {{measure_count}} {{counter}}'
        message += f' to {{layout_ly.trim()}} ...'
        print(message)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        bol_measure_numbers = []
        prototype = abjad.LilyPondLiteral
        skips = abjad.iterate(score['GlobalSkips']).leaves(abjad.Skip)
        for i, skip in enumerate(skips):
            for literal in abjad.inspect(skip).indicators(prototype):
                if literal.argument in (r'\break', r'\pageBreak'):
                    measure_number = first_measure_number + i
                    bol_measure_numbers.append(measure_number)
                    continue
        bols = bol_measure_numbers
        count = len(bols)
        numbers = abjad.String('number').pluralize(count)
        if count <= 4:
            items = ', '.join([str(_) for _ in bols])
            print(
                f' Writing BOL measure {{numbers}} {{items}} to metadata ...')
        else:
            print(f' Writing BOL measure {{numbers}} to metadata ...')
            parts = abjad.sequence(bols).partition_by_counts(
                [12],
                cyclic=True,
                overhang=True,
                )
            for part in parts:
                items = ', '.join(str(_) for _ in part)
                print(f'  {{items}} ...')
        buildspace_directory.add_buildspace_metadatum(
            'bol_measure_numbers',
            bol_measure_numbers,
            document_name=document_name,
            )
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
