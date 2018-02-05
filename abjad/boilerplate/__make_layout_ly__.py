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
            from {layout_module_name} import part_abbreviation
            assert abjad.String(part_abbreviation).is_shout_case()
            document_name = f'{{document_name}}_{{part_abbreviation}}'
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        if buildspace_directory.is_segment():
            string = 'first_measure_number'
            first_measure_number = buildspace_directory.get_metadatum(string)
            assert isinstance(first_measure_number, int)
        else:
            first_measure_number = 1
    except:
        traceback.print_exc()
        sys.exit(1)
        
    try:
        assert abjad.String(document_name).is_shout_case()
        string = 'first_measure_number'
        first_measure_number = buildspace_directory.get_metadatum(string, 1)
        time_signatures = buildspace_directory.get_time_signature_metadata()
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        maker = baca.SegmentMaker(
            breaks=breaks,
            do_not_check_persistence=True,
            final_bar_line=False,
            first_measure_number=first_measure_number,
            score_template=baca.SingleStaffScoreTemplate(),
            spacing=spacing,
            time_signatures=time_signatures,
            )
        lilypond_file = maker.run(remove=abjad.tags.layout_removal_tags())
        context = lilypond_file['GlobalSkips']
        measure_count = len(context)
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
        text = format(score, 'lilypond:strict')
        text = text.replace('GlobalSkips', 'PageLayout')
        text = abjad.LilyPondFormatManager.left_shift_tags(text, realign=89)
        text = f'% measure_count = {{measure_count}}\n\n\n' + text
        layout_ly = layout_module_name.replace('_', '-') + '.ly'
        layout_ly = buildspace_directory(layout_ly)
        layout_ly.write_text(text)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        print(f'Writing BOL measure numbers to metadata ...')
        bol_measure_numbers = []
        prototype = abjad.LilyPondLiteral
        skips = abjad.iterate(score['GlobalSkips']).leaves(abjad.Skip)
        for i, skip in enumerate(skips):
            for literal in abjad.inspect(skip).get_indicators(prototype):
                if literal.argument in (r'\break', r'\pageBreak'):
                    measure_number = first_measure_number + i
                    bol_measure_numbers.append(measure_number)
                    continue
        buildspace_directory.add_buildspace_metadatum(
            'bol_measure_numbers',
            bol_measure_numbers,
            document_name=document_name,
            )
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
