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

    try:
        from {layout_module_name} import breaks
        assert isinstance(breaks, baca.BreakMeasureMap), repr(breaks)
    except ImportError:
        print('Can not import breaks ...')
        sys.exit(1)

    try:
        from {layout_module_name} import spacing
        prototype = baca.HorizontalSpacingSpecifier
        assert isinstance(spacing, prototype), repr(spacing)
    except ImportError:
        spacing = None

    try:
        file_ = pathlib.Path(os.path.realpath(__file__))
        buildspace_directory = file_.parent
        buildspace_directory = ide.Path(buildspace_directory)
        document_name = abjad.tags.document(buildspace_directory.name)
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
        if buildspace_directory.is_segment():
            string = 'time_signatures'
            time_signatures = buildspace_directory.get_metadatum(string)
            assert isinstance(time_signatures, list)
            time_signatures = [
                abjad.TimeSignature.from_string(_)
                for _ in time_signatures
                ]
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        if not buildspace_directory.is_segment():
            builds_directory = buildspace_directory.parent
            score_name = builds_directory.parent.name
            score_path = ide.Path(score_name)
            time_signatures = score_path.get_metadatum('time_signatures')
            prototype = abjad.TypedOrderedDict
            assert isinstance(time_signatures, prototype), repr(
                time_signatures)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        if not buildspace_directory.is_segment():
            time_signatures_ = []
            for segment_name, strings in time_signatures.items():
                for string in strings:
                    time_signature = abjad.TimeSignature.from_string(string)
                    time_signatures_.append(time_signature)
            time_signatures = time_signatures_
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        maker = baca.SegmentMaker(
            breaks=breaks,
            final_bar_line=False,
            first_measure_number=first_measure_number,
            score_template=baca.SingleStaffScoreTemplate(),
            spacing_specifier=spacing,
            time_signatures=time_signatures,
            )
        remove = (
            abjad.tags.EMPTY_START_BAR,
            abjad.tags.MEASURE_NUMBER_MARKUP,
            abjad.tags.STAGE_NUMBER_MARKUP,
            baca.tags.EXPLICIT_TIME_SIGNATURE_COLOR,
            baca.tags.REDUNDANT_TIME_SIGNATURE_COLOR,
            'SM29',
            )
        lilypond_file = maker.run(remove=remove)
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
        text = format(score, 'lilypond:strict')
        text = text.replace('GlobalSkips', 'PageLayout')
        text = abjad.LilyPondFormatManager.left_shift_tags(text, realign=89)
        layout_ly = layout_module_name.replace('_', '-') + '.ly'
        layout_ly = buildspace_directory / layout_ly
        layout_ly.write_text(text)
        print(f'Writing {{layout_ly.trim()}} ...')
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        bol_measure_numbers = []
        prototype = abjad.LilyPondLiteral
        skips = abjad.iterate(score['GlobalSkips']).leaves(abjad.Skip)
        for i, skip in enumerate(skips):
            for literal in abjad.inspect(skip).get_indicators(prototype):
                if literal.argument in (r'\break', r'\pageBreak'):
                    measure_number = first_measure_number + i
                    bol_measure_numbers.append(measure_number)
                    continue
        if buildspace_directory.is_parts():
            part_dictionary = buildspace_directory.get_metadatum(
                document_name,
                abjad.TypedOrderedDict(),
                )
            part_dictionary['bol_measure_numbers'] = bol_measure_numbers
            buildspace_directory.add_metadatum(document_name, part_dictionary)
        else:
            buildspace_directory.add_metadatum(
                'bol_measure_numbers',
                bol_measure_numbers,
                )
        print(f'Writing BOL measure numbers to metadata ...')
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
