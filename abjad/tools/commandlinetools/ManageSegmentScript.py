# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import traceback
from abjad.tools import stringtools
from abjad.tools import systemtools
from abjad.tools.commandlinetools.ScorePackageScript import ScorePackageScript


class ManageSegmentScript(ScorePackageScript):
    '''
    Manages score package segments.

    ..  shell::

        ajv segment --help

    '''

    ### CLASS VARIABLES ###

    alias = 'segment'
    short_description = 'Manage score package segments.'

    ### PRIVATE METHODS ###

    def _collect_matching_paths(self, names, include_unstaged):
        valid_paths = self._list_segment_subpackages()
        staged_names = self._read_segments_list_json()
        staged_matching_paths, unstaged_matching_paths = [], []
        for name in names:
            if name.startswith('+'):
                name = '*{}*'.format('*'.join(name[1:]))
            for path in sorted(self._segments_path.glob(name)):
                if path not in valid_paths:
                    continue
                elif (
                    path in staged_matching_paths or
                    path in unstaged_matching_paths
                    ):
                    continue
                if path.name not in staged_names:
                    if include_unstaged:
                        unstaged_matching_paths.append(path)
                else:
                    staged_matching_paths.append(path)
        matching_paths = []
        matching_paths.extend(sorted(staged_matching_paths,
            key=lambda path: staged_names.index(path.name)))
        matching_paths.extend(sorted(unstaged_matching_paths))
        return matching_paths

    def _create_staging_contents(self, all_names, staged_names):
        names_list = list(staged_names)
        for name in all_names:
            if name not in staged_names:
                names_list.append('# {}'.format(name))
        names_list = '\n'.join(names_list)
        contents = stringtools.normalize('''
        {}

        # Instructions:
        #
        # Reorder, comment or uncomment the segment names
        # above to stage those segments for illustration.
        #
        # Lines beginning with "#" will be unstaged.
        # Duplicates will be ignored.
        # Unknown names will be ignored.
        ''').format(names_list)
        return contents

    def _handle_collect(self):
        print('Collecting segments:')
        collected_names = []
        for segment_path in self._list_segment_subpackages(
            self._score_package_path):
            source_path = segment_path.joinpath('illustration.ly')
            if not source_path.is_file():
                continue
            collected_names.append(segment_path.name)
            target_path = self._build_path.joinpath(
                'segments',
                stringtools.to_dash_case(segment_path.name) + '.ily'
                )
            contents = self._process_illustration_contents(source_path)
            with open(str(target_path), 'w') as file_pointer:
                file_pointer.write(contents)
            message = '    {!s} --> {!s}'.format(
                source_path.relative_to(self._score_package_path),
                target_path.relative_to(self._score_package_path),
                )
            print(message)
        staged_names = self._read_segments_list_json(self._score_package_path)
        segments_ily_path = self._build_path.joinpath('segments.ily')
        include_template = '    \\include "..{sep}segments{sep}{name}.ily"\n'
        with open(str(segments_ily_path), 'w') as file_pointer:
            file_pointer.write('{\n')
            for name in staged_names:
                if name not in collected_names:
                    continue
                name = stringtools.to_dash_case(name)
                file_pointer.write(include_template.format(
                    name=name,
                    sep=os.path.sep))
            file_pointer.write('}\n')

    def _handle_create(self, segment_name, force):
        print('Creating segment subpackage {!r} ...'.format(segment_name))
        segment_path = self._name_to_score_subdirectory_path(
            segment_name, 'segments', self._score_package_path)
        if segment_path.exists() and not force:
            print('    Path exists: {}'.format(
                segment_path.relative_to(self._score_package_path.parent)))
            sys.exit(1)
        segment_name = segment_path.name
        metadata = self._read_score_metadata_json()
        metadata['score_package_name'] = self._score_package_path.name
        source_name = 'example_segment'
        source_path = self._get_boilerplate_path().joinpath(source_name)
        suffixes = ('.py', '.tex', '.ly', '.ily')
        for path in self._copy_tree(source_path, segment_path):
            if path.is_file() and path.suffix in suffixes:
                self._template_file(path, **metadata)
        segment_names = self._read_segments_list_json()
        if segment_name not in segment_names:
            segment_names.append(segment_name)
            self._write_segments_list_json(segment_names)
        print('    Created {path!s}{sep}'.format(
            path=segment_path.relative_to(self._score_package_path.parent),
            sep=os.path.sep,
            ))

    def _handle_edit(self, segment_name):
        from abjad import abjad_configuration
        segment_name = segment_name or '*'
        globbable_names = self._collect_globbable_names(segment_name)
        print('Edit candidates: {!r} ...'.format(
            ' '.join(globbable_names)))
        matching_paths = self._collect_matching_paths(
            globbable_names,
            include_unstaged=True,
            )
        if not matching_paths:
            print('    No matching segments.')
            self._handle_list()
        command = [abjad_configuration.get_text_editor()]
        for path in matching_paths:
            command.append(str(path.joinpath('definition.py')))
        command = ' '.join(command)
        exit_code = self._call_subprocess(command)
        if exit_code:
            sys.exit(exit_code)

    def _handle_illustrate(self, segment_name, unstaged=False):
        globbable_names = self._collect_globbable_names(segment_name)
        print('Illustration candidates: {!r} ...'.format(
            ' '.join(globbable_names)))
        matching_paths = self._collect_matching_paths(
            globbable_names,
            include_unstaged=unstaged,
            )
        if not matching_paths:
            print('    No matching segments.')
            self._handle_list()
        for path in matching_paths:
            self._illustrate_one_segment(segment_directory_path=path)
            print('    Illustrated {path!s}{sep}'.format(
                path=path.relative_to(self._score_package_path.parent),
                sep=os.path.sep))
        for path in matching_paths:
            pdf_path = path.joinpath('illustration.pdf')
            systemtools.IOManager.open_file(str(pdf_path))

    def _handle_list(self):
        print('Available segments:')
        valid_paths = self._list_segment_subpackages(self._score_package_path)
        valid_names = [_.name for _ in valid_paths]
        staged_names = [_ for _ in self._read_segments_list_json()
            if _ in valid_names]
        unstaged_names = [_ for _ in valid_names if _ not in staged_names]
        if staged_names:
            max_length = max(len(_) for _ in staged_names)
            for i, name in enumerate(staged_names, 1):
                spacing = ' ' * (max_length - len(name))
                print('    {}{} [{}]'.format(name, spacing, i))
        for name in unstaged_names:
            print('    {}'.format(name))
        if not staged_names and not unstaged_names:
            print('    No segments available.')
        sys.exit(2)

    def _handle_render(self, segment_name, unstaged=False):
        globbable_names = self._collect_globbable_names(segment_name)
        print('Rendering candidates: {!r} ...'.format(
            ' '.join(globbable_names)))
        matching_paths = self._collect_matching_paths(
            globbable_names,
            unstaged,
            )
        if not matching_paths:
            print('    No matching segments.')
            self._handle_list()
        for path in matching_paths:
            self._render_one_segment(segment_directory_path=path)
            print('    Rendered {path!s}{sep}'.format(
                path=path.relative_to(self._score_package_path.parent),
                sep=os.path.sep))
        for path in matching_paths:
            pdf_path = path.joinpath('illustration.pdf')
            systemtools.IOManager.open_file(str(pdf_path))

    def _handle_stage(self):
        from abjad import abjad_configuration
        print('Staging segments:')
        all_names = [
            path.name for path in
            self._list_segment_subpackages(self._score_package_path)
            ]
        old_staged_names = self._read_segments_list_json()
        contents = self._create_staging_contents(all_names, old_staged_names)
        with systemtools.TemporaryDirectory() as directory_path:
            with systemtools.TemporaryDirectoryChange(directory_path):
                file_path = 'segments.txt'
                with open(file_path, 'w') as file_pointer:
                    file_pointer.write(contents)
                command = '{} {}'.format(
                    abjad_configuration.get_text_editor(),
                    file_path,
                    )
                self._call_subprocess(command)
                with open(file_path, 'r') as file_pointer:
                    contents = file_pointer.read()
        lines = (line.strip() for line in contents.splitlines())
        lines = (line for line in lines if not line.startswith('#'))
        lines = (line for line in lines if line in all_names)
        new_staged_names = list(lines)
        if new_staged_names != old_staged_names:
            self._write_segments_list_json(new_staged_names)
        print('Staged:')
        for name in new_staged_names:
            print('    {}'.format(name))

    def _illustrate_one_segment(self, segment_directory_path):
        print('Illustrating {path!s}{sep}'.format(
            path=segment_directory_path.relative_to(self._score_package_path.parent),
            sep=os.path.sep))
        segment_name = segment_directory_path.name
        segment_names = self._read_segments_list_json()
        previous_segment_name = None
        index = None
        if segment_name in segment_names:
            index = segment_names.index(segment_name)
            if 0 < index:
                previous_segment_name = segment_names[index - 1]
            index += 1
        previous_segment_metadata = {}
        if previous_segment_name:
            previous_segment_metadata_path = self._segments_path.joinpath(
                previous_segment_name,
                'metadata.json',
                )
            previous_segment_metadata = self._read_json(
                previous_segment_metadata_path)
        segment_metadata_path = segment_directory_path.joinpath('metadata.json')
        segment_metadata = self._read_json(segment_metadata_path)
        segment_metadata['segment_count'] = len(segment_names)
        segment_metadata['segment_number'] = index
        segment_metadata['first_bar_number'] = (
            previous_segment_metadata.get('measure_count', 0) +
            previous_segment_metadata.get('first_bar_number', 1)
            )
        segment_package_path = self._path_to_packagesystem_path(
            segment_directory_path)
        definition_import_path = segment_package_path + '.definition'
        try:
            module = self._import_path(
                definition_import_path,
                self._score_repository_path,
                )
            segment_maker = getattr(module, 'segment_maker')
        except (ImportError, AttributeError):
            traceback.print_exc()
            sys.exit(1)
        with systemtools.Timer() as timer:
            try:
                lilypond_file, segment_metadata = segment_maker(
                    segment_metadata=segment_metadata,
                    previous_segment_metadata=previous_segment_metadata,
                    )
            except:
                traceback.print_exc()
                sys.exit(1)
            self._write_json(segment_metadata, segment_metadata_path)
        self._report_time(timer, prefix='Abjad runtime')
        ly_path = self._write_lilypond_ly(
            lilypond_file,
            output_directory_path=segment_directory_path,
            )
        self._write_lilypond_pdf(
            ly_path=ly_path,
            output_directory_path=segment_directory_path,
            )

    def _process_args(self, args):
        self._setup_paths(args.score_path)
        if args.collect:
            self._handle_collect()
        if args.edit is not None:
            self._handle_edit(segment_name=args.edit)
        if args.illustrate is not None:
            self._handle_illustrate(
                segment_name=args.illustrate,
                unstaged=args.unstaged,
                )
        if args.list_:
            self._handle_list()
        if args.new:
            self._handle_create(force=args.force, segment_name=args.new)
        if args.render is not None:
            self._handle_render(
                segment_name=args.render,
                unstaged=args.unstaged,
                )
        if args.stage:
            self._handle_stage()

    def _process_illustration_contents(self, ly_path):
        with open(str(ly_path), 'r') as file_pointer:
            contents = file_pointer.read().splitlines()
        while contents and contents[0] != r'\score {':
            contents.pop(0)
        contents.pop(0)
        for i in range(len(contents)):
            if contents[i] == '}':
                contents = contents[:i]
                break
        contents = '\n'.join(contents)
        return contents

    def _render_one_segment(self, segment_directory_path):
        print('Rendering {path!s}{sep}'.format(
            path=segment_directory_path.relative_to(self._score_package_path.parent),
            sep=os.path.sep))
        ly_path = segment_directory_path.joinpath('illustration.ly')
        if not ly_path.is_file():
            print('    illustration.ly is missing or malformed.')
            sys.exit(1)
        self._write_lilypond_pdf(
            ly_path=ly_path,
            output_directory_path=segment_directory_path,
            )

    def _setup_argument_parser(self, parser):
        action_group = parser.add_argument_group('actions')
        action_group = action_group.add_mutually_exclusive_group(required=True)
        action_group.add_argument(
            '--new', '-N',
            help='create a new segment',
            metavar='NAME',
            )
        action_group.add_argument(
            '--edit', '-E',
            help='edit segments',
            metavar='PATTERN',
            nargs='*',
            )
        action_group.add_argument(
            '--illustrate', '-I',
            help='illustrate segments',
            metavar='PATTERN',
            nargs='+',
            )
        action_group.add_argument(
            '--render', '-R',
            help='render segment illustrations',
            metavar='PATTERN',
            nargs='+',
            )
        action_group.add_argument(
            '--collect', '-C',
            help='collect segment illustrations',
            action='store_true',
            )
        action_group.add_argument(
            '--stage', '-T',
            help='stage segments for illustration',
            action='store_true',
            )
        action_group.add_argument(
            '--list', '-L',
            dest='list_',
            help='list segments',
            action='store_true',
            )
#        action_group.add_argument(
#            '--copy', '-Y',
#            help='copy segment',
#            metavar=('SOURCE', 'TARGET'),
#            nargs=2,
#            )
#        action_group.add_argument(
#            '--rename', '-M',
#            help='rename segment',
#            metavar=('SOURCE', 'TARGET'),
#            nargs=2,
#            )
#        action_group.add_argument(
#            '--delete', '-D',
#            help='delete segment',
#            metavar='NAME',
#            )
        common_group = parser.add_argument_group('common options')
        common_group.add_argument(
            '--score-path', '-s',
            metavar='SCORE',
            help='score path or package name',
            default=os.path.curdir,
            )
        common_group.add_argument(
            '--force', '-f',
            action='store_true',
            help='force overwriting',
            )
        common_group.add_argument(
            '-u', '--unstaged',
            help='Include segments not staged in segments{sep}metadata.json'.format(sep=os.path.sep),
            action='store_true',
            )
