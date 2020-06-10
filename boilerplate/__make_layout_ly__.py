#! /usr/bin/env python
import os
import pathlib
import pprint
import sys
import traceback

import abjad
import baca

if __name__ == '__main__':

    layout_module_name = '{layout_module_name}'
    maker = abjad.Path(os.path.realpath(__file__))

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
        layout_py = buildspace_directory / '{layout_module_name}.py'
        document_name = abjad.String(buildspace_directory.name).to_shout_case()
    except Exception:
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
    except Exception:
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
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    try:
        maker = baca.SegmentMaker(
            breaks=breaks,
            do_not_check_persistence=True,
            do_not_include_layout_ly=True,
            first_measure_number=first_measure_number,
            score_template=baca.SingleStaffScoreTemplate(),
            spacing=spacing,
            time_signatures=time_signatures,
            )
        lilypond_file = maker.run(
            do_not_print_timing=True,
            environment='layout',
            remove=abjad.tags.layout_removal_tags(),
            )
        context = lilypond_file['Global_Skips']
        context.lilypond_type = 'PageLayout'
        context.name = 'Page_Layout'
        skips = baca.select(context).skips()
        for skip in skips:
            abjad.detach(abjad.TimeSignature, skip)
        score = lilypond_file['Score']
        del(score['Music_Context'])
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    try:
        score = lilypond_file['Score']
        text = format(score, 'lilypond')
        text = text.replace('Global_Skips', 'Page_Layout')
        text = abjad.LilyPondFormatManager.left_shift_tags(text, realign=79)
        layout_ly = layout_module_name.replace('_', '-') + '.ly'
        layout_ly = buildspace_directory / layout_ly
        lines = []
        if breaks.partial_score is not None:
            lines.append(f'% partial_score = True')
        if buildspace_directory.is_segment():
            first_segment = buildspace_directory.segments.get_next_package()
            if buildspace_directory.name != first_segment.name:
                previous_segment = buildspace_directory.get_previous_package()
                previous_layout_ly = previous_segment / 'layout.ly'
                result = previous_layout_ly.get_preamble_page_count_overview()
                if result is not None:
                    _, _, final_page_number = result
                    first_page_number = final_page_number + 1
                    line = f'% first_page_number = {{first_page_number}}'
                    lines.append(line)
        page_count = breaks.page_count
        lines.append(f'% page_count = {{page_count}}')
        time_signatures = [str(_) for _ in time_signatures]
        measure_count = len(time_signatures)
        lines.append(f'% measure_count = {{measure_count}} + 1')
        string = pprint.pformat(time_signatures, compact=True, width=80 - 3)
        lines_ = string.split('\n')
        lines_ = [_.strip('[').strip(']') for _ in lines_]
        lines_ = ['% ' + _ for _ in lines_]
        lines_.insert(0, '% time_signatures = [')
        lines_.append('%  ]')
        lines.extend(lines_)
        header = '\n'.join(lines) + '\n\n'
        layout_ly.write_text(header + text)
        counter = abjad.String('measure').pluralize(measure_count)
        message = f' Writing {{measure_count}} + 1 {{counter}}'
        message += f' to {{layout_ly.trim()}} ...'
        print(message)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    try:
        bol_measure_numbers = []
        prototype = abjad.LilyPondLiteral
        skips = abjad.iterate(score['Page_Layout']).leaves(abjad.Skip)
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
            string = pprint.pformat(bols, compact=True, width=80 - 3)
            lines = string.split('\n')
            lines = ['  ' + _.strip('[').strip(']').strip() for _ in lines]
            lines[-1] = lines[-1] + ' ...'
            for line in lines:
                print(line)
        buildspace_directory.add_buildspace_metadatum(
            'bol_measure_numbers',
            bol_measure_numbers,
            document_name=document_name,
            )
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
