import os
import pathlib
import shutil


class Path(pathlib.PosixPath):
    r'''Path (of an Abjad score package).

    ..  container:: example

        >>> path = abjad.Path(
        ...     '/path/to/scores/my_score/my_score',
        ...     scores='/path/to/scores',
        ...     )

        >>> path.materials
        Path*('/path/to/scores/my_score/my_score/materials')

        >>> path.materials('instruments')
        Path*('/path/to/scores/my_score/my_score/materials/instruments')

        >>> path.materials('instruments').is_material()
        True

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segment-makers'

    _known_directories = (
        '_segments',
        'builds',
        'distribution',
        'etc',
        'materials',
        'segments',
        'stylesheets',
        'test',
        'tools',
        )

    _secondary_names = (
        '__init__.py',
        '__make_pdf__.py',
        '__make_midi__.py',
        '__metadata__.py',
        '_segments',
        )

    ### CONSTRUCTOR ###

    def __new__(class_, *arguments, scores=None):
        import abjad
        configuration = abjad.abjad_configuration
        if not arguments:
            raise Exception('must provide at least one argument.')
        argument = arguments[0]
        _arguments = arguments[1:]
        if isinstance(argument, pathlib.Path) or os.sep in argument:
            self = pathlib.Path.__new__(class_, argument)
        else:
            arguments = []
            if argument == 'boilerplate':
                arguments.append(configuration.boilerplate_directory)
            elif scores is not None:
                arguments.append(scores)
                arguments.extend(2 * [argument])
            else:
                arguments.append(configuration.composer_scores_directory)
                arguments.extend(2 * [argument])
            arguments.extend(_arguments)
            self = pathlib.Path.__new__(class_, *arguments)
        if scores is not None:
            scores = type(self)(scores)
        self._scores = scores
        return self

    ### SPECIAL METHODS ###

    def __call__(self, *names):
        r'''Calls path on `names`.

        Returns new path.
        '''
        path = self
        for name in names:
            path /= name
        return path

    def __repr__(self):
        r'''Gets interpreter representation of path.

        Returns string.
        '''
        if bool(getattr(self, '_scores', None)):
            return "Path*('{}')".format(self)
        else:
            return "Path('{}')".format(self)

    def __rtruediv__(self, argument):
        r'''Joins path to `argument`.

        Returns new path.
        '''
        result = super(Path, self).__rtruediv__(argument)
        result._scores = getattr(self, '_scores', None)
        return result

    def __truediv__(self, argument):
        r'''Joins `argument` to path.

        Returns new path.
        '''
        result = super(Path, self).__truediv__(argument)
        result._scores = getattr(self, '_scores', None)
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def _segments(self):
        '''Gets _segments directory.

        Returns path.
        '''
        if self.builds:
            return self.builds('_segments')

    ### PRIVATE METHODS ###

    def _filter_by_view(self, paths):
        view = self.get_metadatum('view')
        if view is None:
            return paths
        filtered_paths = []
        for pattern in view:
            if ':ds:' in pattern:
                for path in paths:
                    if path._match_identifier_pattern(pattern):
                        filtered_paths.append(path)
            elif 'md:' in pattern:
                pairs = []
                for path in paths:
                    metadatum = path._match_metadata_pattern(pattern)
                    if metadatum is not None:
                        pairs.append((metadatum, path))
                pairs.sort(key=lambda _: _[0])
                pairs.reverse()
                filtered_paths_ = [_[-1] for _ in pairs]
                filtered_paths.extend(filtered_paths_)
            elif ':path:' in pattern:
                for path in paths:
                    if path._match_path_pattern(pattern):
                        filtered_paths.append(path)
            else:
                for path in paths:
                    if pattern == path.get_identifier():
                        filtered_paths.append(path)
        return filtered_paths

    def _find_empty_wrapper(self):
        if not self.scores:
            return
        for path in self.scores.iterdir():
            if not path.name[0].isalpha():
                continue
            if not path.name[0].islower():
                continue
            if not path.is_dir():
                continue
            has_contents = False
            if all(_.name.startswith('.') for _ in path.iterdir()):
                return type(self)(path)

    def _get_file_path_ending_with(self, string):
        if not self.is_dir():
            return
        glob = '*{}'.format(string)
        for path in sorted(self.glob(glob)):
            if path.is_file():
                return path

    def _get_score_pdf(self):
        path = self.distribution._get_file_path_ending_with('score.pdf')
        if not path:
            path = self.builds._get_file_path_ending_with('score.pdf')
        return path

    def _list_paths(self):
        import abjad
        paths = []
        if not self.exists():
            return paths
        predicate = self.get_name_predicate()
        is_external = self.is_external()
        is_scores = self.is_scores()
        is_segments = self.is_segments()
        for name in sorted([_.name for _ in self.iterdir()]):
            name = abjad.String(name)
            if name.startswith('_') and not (is_external or is_segments):
                continue
            if name in ('.DS_Store', '.cache', '.git', '.gitmodules'):
                continue
            if name in ('__init__.py', '__pycache__'):
                continue
            if name == '.gitignore' and not self.is_wrapper():
                continue
            if (predicate is not None and
                not predicate(name) and
                name != '_segments'):
                continue
            path = self(name)
            try:
                path.relative_to(self)
            except ValueError:
                continue
            if path.name == '_' and path.parent.name == 'segments':
                paths.insert(0, path)
            else:
                paths.append(path)
        return paths

    def _match_identifier_pattern(self, pattern):
        token = ':ds:'
        assert token in pattern, repr(pattern)
        identifier = self.get_identifier()
        pattern = pattern.replace(token, repr(identifier))
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            result = False
        return result

    def _match_metadata_pattern(self, pattern):
        count = pattern.count('md:')
        for _ in range(count + 1):
            parts = pattern.split()
            for part in parts:
                if part.startswith('md:'):
                    metadatum_name = part[3:]
                    metadatum = self.get_metadatum(metadatum_name)
                    metadatum = repr(metadatum)
                    pattern = pattern.replace(part, metadatum)
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            return False
        return result

    def _match_path_pattern(self, pattern):
        token = ':path:'
        assert token in pattern, repr(pattern)
        pattern = pattern.replace(token, repr(self))
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            return False
        return result

    @staticmethod
    def _sort_by_identifier(paths):
        import abjad
        pairs = []
        for path in paths:
            identifier = abjad.String(path.get_identifier())
            identifier = identifier.strip_diacritics().replace("'", '')
            pairs.append((identifier, path))
        pairs.sort(key=lambda _: _[0])
        paths = [_[-1] for _ in pairs]
        return paths

    ### PUBLIC PROPERTIES ###

    @property
    def builds(self):
        r'''Gets builds directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.builds
            Path*('/path/to/scores/my_score/my_score/builds')
            >>> path.builds('letter')
            Path*('/path/to/scores/my_score/my_score/builds/letter')

        Returns path.
        '''
        if self.contents:
            return self.contents('builds')

    @property
    def contents(self):
        r'''Gets contents directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.contents
            Path*('/path/to/scores/my_score/my_score')
            >>> path.contents('etc', 'notes.txt')
            Path*('/path/to/scores/my_score/my_score/etc/notes.txt')

        Returns path.
        '''
        scores = self.scores
        if not scores:
            return
        parts = self.relative_to(scores).parts
        if not parts:
            return
        result = scores(parts[0], parts[0])
        result._scores = getattr(self, '_scores', None)
        return result

    @property
    def distribution(self):
        r'''Gets distribution directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.distribution
            Path*('/path/to/scores/my_score/my_score/distribution')
            >>> path.distribution('score.pdf')
            Path*('/path/to/scores/my_score/my_score/distribution/score.pdf')

        Returns path.
        '''
        if self.contents:
            return self.contents('distribution')

    @property
    def etc(self):
        r'''Gets etc directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.etc
            Path*('/path/to/scores/my_score/my_score/etc')
            >>> path.etc('notes.txt')
            Path*('/path/to/scores/my_score/my_score/etc/notes.txt')

        Returns path.
        '''
        if self.contents:
            return self.contents('etc')

    @property
    def materials(self):
        r'''Gets materials directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.materials
            Path*('/path/to/scores/my_score/my_score/materials')
            >>> path.materials('instruments')
            Path*('/path/to/scores/my_score/my_score/materials/instruments')

        Returns path.
        '''
        if self.contents:
            return self.contents('materials')

    @property
    def scores(self):
        r'''Gets scores directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.scores
            Path*('/path/to/scores')
            >>> path.scores('red_score', 'red_score')
            Path*('/path/to/scores/red_score/red_score')

        Returns path or none.
        '''
        import abjad
        configuration = abjad.abjad_configuration
        if getattr(self, '_scores', None) is not None:
            result = self._scores
            result._scores = self._scores
            return result
        directory = configuration.composer_scores_directory
        if str(self).startswith(str(directory)):
            return type(self)(directory)

    @property
    def segments(self):
        r'''Gets segments directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.segments
            Path*('/path/to/scores/my_score/my_score/segments')
            >>> path.segments('segment_01')
            Path*('/path/to/scores/my_score/my_score/segments/segment_01')

        Returns path.
        '''
        if self.contents:
            return self.contents('segments')

    @property
    def stylesheets(self):
        r'''Gets stylesheets directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.stylesheets
            Path*('/path/to/scores/my_score/my_score/stylesheets')
            >>> path.stylesheets('stylesheet.ily')
            Path*('/path/to/scores/my_score/my_score/stylesheets/stylesheet.ily')

        Returns path.
        '''
        if self.contents:
            return self.contents('stylesheets')

    @property
    def test(self):
        r'''Gets test directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.test
            Path*('/path/to/scores/my_score/my_score/test')
            >>> path.test('test_materials.py')
            Path*('/path/to/scores/my_score/my_score/test/test_materials.py')

        Returns path.
        '''
        if self.contents:
            return self.contents('test')

    @property
    def tools(self):
        r'''Gets tools directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.tools
            Path*('/path/to/scores/my_score/my_score/tools')
            >>> path.tools('SegmentMaker.py')
            Path*('/path/to/scores/my_score/my_score/tools/SegmentMaker.py')

        Returns path.
        '''
        if self.contents:
            return self.contents('tools')

    @property
    def wrapper(self):
        r'''Gets wrapper directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.wrapper
            Path*('/path/to/scores/my_score')
            >>> path.wrapper('my_score', 'etc')
            Path*('/path/to/scores/my_score/my_score/etc')

        Returns path.
        '''
        if self.contents:
            result = type(self)(self.contents()).parent
            result._scores = getattr(self, '_scores', None)
            return result
            return result

    ### PUBLIC METHODS ###

    def add_metadatum(self, name, value):
        r'''Adds metadatum.

        Returns none.
        '''
        assert ' ' not in name, repr(name)
        metadata = self.get_metadata()
        metadata[name] = value
        self.write_metadata_py(metadata)

    def coerce(self, name, suffix=None):
        r'''Coerces asset `name`.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

        ..  container:: example

            In build directory:

            >>> path.builds('letter').coerce('back cover.tex')
            'back cover.tex'
            >>> path.builds('letter').coerce('Back Cover.tex')
            'Back Cover.tex'
            >>> path.builds('letter').coerce('BACK_COVER.tex')
            'BACK_COVER.tex'

            >>> path.builds('letter').coerce('new music.ly')
            'new music.ly'
            >>> path.builds('letter').coerce('New Music.ly')
            'New Music.ly'
            >>> path.builds('letter').coerce('NEW_MUSIC.ly')
            'NEW_MUSIC.ly'

            >>> path.builds('letter').coerce('page_layout.py')
            'page_layout.py'
            >>> path.builds('letter').coerce('Page Layout.py')
            'Page Layout.py'
            >>> path.builds('letter').coerce('PAGE_LAYOUT.py')
            'PAGE_LAYOUT.py'

        ..  container:: example

            In builds directory:

            >>> path.builds.coerce('letter_landscape')
            'letter-landscape'
            >>> path.builds.coerce('letter landscape')
            'letter-landscape'
            >>> path.builds.coerce('Letter Landscape')
            'letter-landscape'

        ..  container:: example

            In contents directory:

            >>> path.contents.coerce('ETC')
            'etc'

        ..  container:: example

            In distribution directory:

            >>> path.distribution.coerce('program notes.txt')
            'program-notes.txt'
            >>> path.distribution.coerce('Program Notes.txt')
            'program-notes.txt'
            >>> path.distribution.coerce('PROGRAM_NOTES.txt')
            'program-notes.txt'

        ..  container:: example

            In etc directory:

            >>> path.etc.coerce('material sketches.md')
            'material-sketches.md'
            >>> path.etc.coerce('Material Sketches.md')
            'material-sketches.md'
            >>> path.etc.coerce('MATERIAL_SKETCHES.md')
            'material-sketches.md'

        ..  container:: example

            In scores directory:

            >>> path.scores.coerce('Green Score')
            'green_score'

        ..  container:: example

            In segment directory:

            >>> path.segments.coerce('_')
            '_'
            >>> path.segments.coerce('A')
            'A'
            >>> path.segments.coerce('A1')
            'A1'
            >>> path.segments.coerce('A99')
            'A99'

            >>> path.segments.coerce('segment_01')
            'segment_01'
            >>> path.segments.coerce('segment 01')
            'segment_01'
            >>> path.segments.coerce('Segment 01')
            'segment_01'
            >>> path.segments.coerce('SEGMENT 01')
            'segment_01'

        ..  container:: example

            In stylesheets directory:

            >>> path.stylesheets.coerce('segment stylesheet')
            'segment-stylesheet.ily'
            >>> path.stylesheets.coerce('Segment Stylesheet')
            'segment-stylesheet.ily'
            >>> path.stylesheets.coerce('SEGMENT_STYLESHEET')
            'segment-stylesheet.ily'

        Returns string.
        '''
        import abjad
        name = abjad.String(name).strip_diacritics()
        assert os.path.sep not in name, repr(name)
        suffix = suffix or type(self)(name).suffix
        stem = abjad.String(type(self)(name).stem)
        if self.is_scores():
            name = stem.to_snake_case()
        elif self.is_external():
            pass
        elif self.is__segments():
            pass
        elif self.is_build():
            pass
        elif self.is_builds():
            name = stem.to_dash_case()
        elif self.is_contents():
            name = stem.to_snake_case()
        elif self.is_distribution():
            name = stem.to_dash_case() + suffix
        elif self.is_etc():
            name = stem.to_dash_case() + suffix
        elif self.is_material():
            name = stem.to_snake_case() + '.py'
        elif self.is_materials():
            name = stem.to_snake_case()
        elif self.is_segment():
            name = stem.to_snake_case() + '.py'
        elif self.is_segments():
            if stem.is_segment_name():
                name = stem
            else:
                name = stem.to_snake_case()
        elif self.is_stylesheets():
            name = stem.to_dash_case() + '.ily'
        elif self.is_test():
            name = stem.to_snake_case() + '.py'
        elif self.is_tools() and name[0].isupper():
            name = stem.to_upper_camel_case() + '.py'
        elif self.is_tools() and name[0].islower():
            name = stem.to_snake_case() + '.py'
        elif self.is_wrapper():
            pass
        elif self.is_external():
            pass
        else:
            raise ValueError(self)
        return name

    def comment_out_tag(self, tag, greedy=False):
        r'''Comments out `tag` in LilyPond file.

        Returns text, count, skipped triple.

        Text gives processed file contents ready to be written.

        Count gives the number of tags commented out.

        Skipped gives number of tags already commented out (and therefore
        skipped).

        Matches all of `tag` when `greedy` is false; matches `tag` anywhere in
        tag when `greedy` is true.
        '''
        assert self.is_file()
        lines, count, skipped = [], 0, 0
        current_tag_number = None
        tag_parts = tag.split(':')
        with self.open() as file_pointer:
            for line in file_pointer.readlines():
                if ((greedy is True and tag not in line) or
                    (greedy is not True and
                    any(_ not in line for _ in tag_parts))):
                    current_tag_number = None
                    lines.append(line)
                    continue
                start = line.rfind(':') + 1
                tag_number = int(line[start:])
                first_nonwhitespace_index = len(line) - len(line.lstrip())
                index = first_nonwhitespace_index
                if line[index] != '%':
                    line = list(line)
                    line[index:index] = '%%% '
                    line = ''.join(line)
                    if tag_number != current_tag_number:
                        current_tag_number = tag_number
                        count += 1
                else:
                    if tag_number != current_tag_number:
                        current_tag_number = tag_number
                        skipped += 1
                lines.append(line)
        lines = ''.join(lines)
        return lines, count, skipped

    def get_asset_type(self):
        r'''Gets asset identifier.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.builds.get_asset_type()
            'directory'

            >>> path.contents.get_asset_type()
            'directory'

            >>> path.distribution.get_asset_type()
            'file'

            >>> path.etc.get_asset_type()
            'file'

            >>> path.materials.get_asset_type()
            'package'

            >>> path.scores.get_asset_type()
            'package'

            >>> path.segments.get_asset_type()
            'package'

            >>> path.stylesheets.get_asset_type()
            'file'

            >>> path.test.get_asset_type()
            'file'

            >>> path.tools.get_asset_type()
            'file'

            >>> path.wrapper.get_asset_type()
            'asset'

        ..  container:: example

            With external path:

            >>> abjad.Path('/path/to/external').get_asset_type()
            'asset'

        Returns string.
        '''
        if self.is_scores():
            return 'package'
        elif self.is_wrapper():
            return 'asset'
        elif self.is_contents():
            return 'directory'
        elif self.is_builds():
            return 'directory'
        elif self.is_materials_or_segments():
            return 'package'
        elif self.is_score_package_path((
            '_segments',
            'build',
            'distribution',
            'etc',
            'tools',
            'material',
            'segment',
            'stylesheets',
            'test',
            )):
            return 'file'
        else:
            return 'asset'

    def get_identifier(self):
        r'''Gets identifier.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.contents.get_identifier()
            '(untitled score)'

            >>> path.materials('tempi').get_identifier()
            'tempi'

            >>> path.materials().get_identifier()
            'materials'

            >>> path.segments('segment_01').get_identifier()
            'segment_01'

            >>> path.segments().get_identifier()
            'segments'

            >>> path.wrapper().get_identifier()
            '(untitled score)'

        Returns title when path is contents directory.

        Returns name metadatum when name metadatum exists.

        Returns path name otherwise.
        '''
        import abjad
        if self.is_wrapper():
            result = self.contents().get_title()
        elif self.is_contents():
            result = self.get_title()
        elif self.is_dir():
            result = self.get_metadatum('name', self.name)
        else:
            result = self.name
        return abjad.String(result)

    def get_metadata(self):
        r'''Gets __metadata__.py file in path.

        Returns ordered dictionary.
        '''
        import abjad
        metadata_py_path = self('__metadata__.py')
        metadata = None
        if metadata_py_path.is_file():
            file_contents_string = metadata_py_path.read_text()
            try:
                result = abjad.IOManager.execute_string(
                    file_contents_string,
                    attribute_names=('metadata',),
                    )
            except NameError as e:
                raise Exception(repr(metadata_py_path), e)
            if result:
                metadata = result[0]
            else:
                metadata = None
        return abjad.TypedOrderedDict(metadata)

    def get_metadatum(self, metadatum_name, default=None):
        r'''Gets metadatum.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.contents.get_metadatum('foo') is None
            True

        Returns object.
        '''
        metadata = self.get_metadata()
        metadatum = metadata.get(metadatum_name)
        if not metadatum:
            metadatum = default
        return metadatum

    def get_name_predicate(self):
        r'''Gets name predicate.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path._segments.get_name_predicate() is None
            True

            >>> path.builds.get_name_predicate()
            <function String.is_build_directory_name at ...>

            >>> path.contents.get_name_predicate()
            <function String.is_package_name at ...>

            >>> path.materials.get_name_predicate()
            <function String.is_package_name at ...>

            >>> path.materials('tempi').get_name_predicate()
            <function String.is_lowercase_file_name at ...>

            >>> path.scores.get_name_predicate()
            <function String.is_package_name at ...>

            >>> path.segments.get_name_predicate()
            <function String.is_segment_name at ...>

            >>> path.segments('segment_01').get_name_predicate()
            <function String.is_lowercase_file_name at ...>

            >>> path.wrapper.get_name_predicate() is None
            True

        Returns function.
        '''
        import abjad
        if self.is_scores():
            return abjad.String.is_package_name
        elif self.is_external():
            return
        elif self.is_wrapper():
            return
        elif self.is_build():
            return
        elif self.is_builds():
            return abjad.String.is_build_directory_name
        elif self.is_builds_segments():
            return
        elif self.is_contents():
            return abjad.String.is_package_name
        elif self.is_distribution():
            return abjad.String.is_dash_case_file_name
        elif self.is_etc():
            return abjad.String.is_dash_case_file_name
        elif self.is_material():
            return abjad.String.is_lowercase_file_name
        elif self.is_materials():
            return abjad.String.is_package_name
        elif self.is_scores():
            return abjad.String.is_package_name
        elif self.is_segment():
            return abjad.String.is_lowercase_file_name
        elif self.is_segments():
            return abjad.String.is_segment_name
        elif self.is_tools():
            return abjad.String.is_tools_file_name
        elif self.is_stylesheets():
            return abjad.String.is_stylesheet_name
        elif self.is_test():
            return abjad.String.is_module_file_name
        elif self.is_wrapper():
            return
        else:
            return

    def get_next_package(self, cyclic=False):
        r'''Gets next package.

        ..  container:: example

                >>> path = abjad.Path(
                ...     '/path/to/scores/my_score/my_score',
                ...     scores='/path/to/scores',
                ...     )

            >>> path.get_next_package() is None
            True

        Returns path or none.
        '''
        import abjad
        if not self.is_dir():
            return
        if self.is_material():
            paths = self.materials().list_paths()
            if self == paths[-1] and not cyclic:
                path = self
            else:
                index = paths.index(self)
                paths = abjad.CyclicTuple(paths)
                path = paths[index + 1]
        elif self.is_materials():
            paths = self.list_paths()
            path = paths[0]
        elif self.is_segment():
            paths = self.segments().list_paths()
            if self == paths[-1] and not cyclic:
                path = None
            else:
                index = paths.index(self)
                paths = abjad.CyclicTuple(paths)
                path = paths[index + 1]
        elif self.is_segments():
            paths = self.list_paths()
            path = paths[0]
        else:
            raise ValueError(self)
        return path

    def get_next_score(self, cyclic=False):
        r'''Gets next score.

        ..  container:: example

                >>> path = abjad.Path(
                ...     '/path/to/scores/my_score/my_score',
                ...     scores='/path/to/scores',
                ...     )

            >>> path.get_next_score() is None
            True

        Returns path or none.
        '''
        import abjad
        if not self.is_dir():
            return
        if not (self.is_score_package_path() or self.is_scores()):
            return
        if self.is_scores():
            wrappers = self.list_paths()
            if wrappers:
                return wrappers[0]
        wrappers = self.scores.list_paths()
        if not wrappers:
            return
        wrapper = self.wrapper()
        if wrapper == wrappers[-1] and not cyclic:
            return
        index = wrappers.index(wrapper)
        wrappers = abjad.CyclicTuple(wrappers)
        return wrappers[index + 1]

    def get_previous_package(self, cyclic=False):
        r'''Gets previous package.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.get_previous_package() is None
            True

        Returns path or none.
        '''
        import abjad
        if not self.is_dir():
            return
        if self.is_material():
            paths = self.materials().list_paths()
            if self == paths[0] and not cyclic:
                path = None
            else:
                index = paths.index(self)
                paths = abjad.CyclicTuple(paths)
                path = paths[index - 1]
        elif self.is_materials():
            paths = self.list_paths()
            path = paths[-1]
        elif self.is_segment():
            paths = self.segments().list_paths()
            if self == paths[0] and not cyclic:
                path = None
            else:
                index = paths.index(self)
                paths = abjad.CyclicTuple(paths)
                path = paths[index - 1]
        elif self.is_segments():
            paths = self.list_paths()
            path = paths[-1]
        else:
            raise ValueError(self)
        return path

    def get_previous_score(self, cyclic=False):
        r'''Gets previous score.

        ..  container:: example

                >>> path = abjad.Path(
                ...     '/path/to/scores/my_score/my_score',
                ...     scores='/path/to/scores',
                ...     )

            >>> path.get_previous_score() is None
            True

        Returns path or none.
        '''
        import abjad
        if not self.is_dir():
            return
        if not (self.is_score_package_path() or self.is_scores()):
            return
        if self.is_scores():
            wrappers = self.list_paths()
            if wrappers:
                return wrappers[-1]
        wrappers = self.scores.list_paths()
        if not wrappers:
            return
        wrapper = self.wrapper()
        if wrapper == wrappers[0] and not cyclic:
            return
        index = wrappers.index(wrapper)
        wrappers = abjad.CyclicTuple(wrappers)
        return wrappers[index - 1]

    def get_title(self, year=True):
        r'''Gets score title.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.get_title()
            '(untitled score)'
        
        Returns string.
        '''
        if year and self.get_metadatum('year'):
            title = self.get_title(year=False)
            year = self.get_metadatum('year')
            result = '{} ({})'.format(title, year)
            return result
        else:
            result = self.get_metadatum('title')
            result = result or '(untitled score)'
            return result

    def is__segments(self):
        r'''Is true when path is _segments directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path._segments.is__segments()
            True

        Returns true or false.
        '''
        return self.name == '_segments'

    def is_build(self):
        '''Is true when path is build directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.builds('letter').is_build()
            True

        Returns true or false.
        '''
        return self.parent.name == 'builds' and self.name != '_segments'

    def is_builds(self):
        r'''Is true when path is builds directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.builds.is_builds()
            True

        Returns true or false.
        '''
        return self.name == 'builds'

    def is_builds_segments(self):
        r'''Is true when path is builds _segments directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path._segments.is_builds_segments()
            True

        '''
        if self.parent.is_builds() and self.name == '_segments':
            return True

    def is_contents(self):
        r'''Is true when path is contents directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.contents.is_contents()
            True

        Returns true or false.
        '''
        return self.scores and self.scores(self.name, self.name) == self

    def is_distribution(self):
        r'''Is true when path is distribution directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.distribution.is_distribution()
            True

        Returns true or false.
        '''
        return self.name == 'distribution'

    def is_etc(self):
        r'''Is true when path is etc directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.etc.is_etc()
            True

        Returns true or false.
        '''
        return self.name == 'etc'

    def is_external(self):
        r'''Is true when path is not a score package path.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.builds.is_external()
            False
            >>> path.contents.is_external()
            False
            >>> path.wrapper.is_external()
            False

            >>> path.scores.is_external()
            True

        ..  container:: example

            >>> abjad.Path('/path/to/location').is_external()
            True

        Returns true or false.
        '''
        import abjad
        configuration = abjad.abjad_configuration
        directory = configuration.composer_scores_directory
        if str(self) == str(directory):
            return True
        if (not self.name[0].isalpha() and
            not self.name == '_segments' and
            not self.parent.name == 'segments'):
            return True
        if str(self).startswith(str(directory)):
            return False
        directory = getattr(self, '_scores', None)
        if str(self) == str(directory):
            return True
        if directory and str(self).startswith(str(directory)):
            return False
        return True

    def is_library(self):
        r'''Is true when path is composer library tools directory.

        Returns true or false.
        '''
        import abjad
        configuration = abjad.abjad_configuration
        if configuration.composer_library_tools:
            return str(self) == configuration.composer_library_tools
        return False

    def is_material(self):
        r'''Is true when path is material directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.materials('tempi').is_material()
            True

        Returns true or false.
        '''
        return self.parent.name == 'materials'

    def is_material_or_segment(self):
        r'''Is true when path is material directory or segment directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.materials.is_material_or_segment()
            False

            >>> path.materials('tempi').is_material_or_segment()
            True

            >>> path.segments.is_material_or_segment()
            False

            >>> path.segments('A').is_material_or_segment()
            True

        Returns true or false.
        '''
        return self.parent.name in ('materials', 'segments')

    def is_materials(self):
        r'''Is true when path is materials directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.materials.is_materials()
            True

        Returns true or false.
        '''
        return self.name == 'materials'

    def is_materials_or_segments(self):
        r'''Is true when path is materials directory or segments directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.materials.is_materials_or_segments()
            True

            >>> path.materials('tempi').is_materials_or_segments()
            False

            >>> path.segments.is_materials_or_segments()
            True

            >>> path.segments('A').is_materials_or_segments()
            False

        Returns true or false.
        '''
        return self.name in ('materials', 'segments')

    def is_score_package_path(self, prototype=()):
        r'''Is true when path is package path.

        ..  container:: example

            External path returns false:

            >>> abjad.Path('/path/to/location').is_score_package_path()
            False

        ..  container:: example

            Scores directory returns false:

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.scores.is_score_package_path()
            False

        ..  container:: example

            Package paths return true:

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.wrapper.is_score_package_path()
            True

            >>> path.contents.is_score_package_path()
            True

            >>> path.stylesheets.is_score_package_path()
            True

            >>> path._segments.is_score_package_path()
            True

        Returns true or false.
        '''
        if self.is_external():
            return False
        if self.is_scores():
            return False
        if not self.scores:
            return False
        if (not self.name[0].isalpha() and
            not (self.is_builds_segments() or self.is_segment())):
            return False
        if not prototype:
            return True
        if isinstance(prototype, str):
            prototype = (prototype,)
        assert isinstance(prototype, tuple), repr(prototype)
        assert all(isinstance(_, str) for _ in prototype)
        if 'scores' in prototype:
            raise Exception(self, prototype)
        if self.name in prototype:
            return True
        if 'build' in prototype and self.is_build():
            return True
        if 'contents' in prototype and self.is_contents():
            return True
        if 'material' in prototype and self.is_material():
            return True
        if 'segment' in prototype and self.is_segment():
            return True
        if 'wrapper' in prototype and self.is_wrapper():
            return True
        return False

    def is_scores(self):
        r'''Is true when path is scores directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.scores.is_scores()
            True

        Returns true or false.
        '''
        return self == self.scores

    def is_segment(self):
        r'''Is true when path is segment directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.segments('segment_01').is_segment()
            True

        Returns true or false.
        '''
        return self.parent.name == 'segments'

    def is_segments(self):
        r'''Is true when path is segments directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.segments.is_segments()
            True

        Returns true or false.
        '''
        return self.name == 'segments'

    def is_stylesheets(self):
        r'''Is true when path is stylesheets directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.stylesheets.is_stylesheets()
            True

        Returns true or false.
        '''
        return self.name == 'stylesheets'

    def is_test(self):
        r'''Is true when path is test directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.test.is_test()
            True

        Returns true or false.
        '''
        return self.name == 'test'

    def is_tools(self):
        r'''Is true when path is tools directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.tools.is_tools()
            True

        Returns true or false.
        '''
        return self.name == 'tools'

    def is_wrapper(self):
        r'''Is true when path is wrapper directory

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.wrapper.is_wrapper()
            True

        Returns true or false.
        '''
        return self.scores and self.scores(self.name) == self

    def list_paths(self):
        r'''Lists paths ordered by view (if any).

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.list_paths()
            []

        Returns list.
        '''
        paths = self._list_paths()
        paths = self._filter_by_view(paths)
        if self.is_scores() and self.get_metadatum('view') is None:
            paths = self._sort_by_identifier(paths)
        return paths

    def list_secondary_paths(self):
        r'''Lists secondary paths.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.list_secondary_paths()
            []

        Returns list.
        '''
        paths = []
        for path in sorted(self.glob('*')):
            if path.name in sorted(self._secondary_names):
                paths.append(path)
        return paths

    def remove(self):
        r'''Removes path if it exists.

        Returns none.
        '''
        if self.is_file():
            self.unlink()
        elif self.is_dir():
            shutil.rmtree(str(self))

    def remove_metadatum(self, name):
        r'''Removes metadatum.

        Returns none.
        '''
        assert ' ' not in name, repr(name)
        metadata = self.get_metadata()
        try:
            metadata.pop(name)
        except KeyError:
            pass
        self.write_metadata_py(metadata)

    def segment_number_to_path(self, number):
        r'''Changes segment number to path.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.segment_number_to_path(1)

        Returns path.
        '''
        for path in sorted(self.segments().glob('*')):
            if not path.is_dir():
                continue
            if not path.name.startswith('segment_'):
                continue
            body = path.name[8:]
            try:
                body = int(body)
            except ValueError:
                continue
            if body == number:
                return path

    def trim(self):
        r'''Trims path.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.contents.trim()
            '/path/to/scores/my_score/my_score'

            >>> path.segments.trim()
            'my_score/segments'

            >>> path.segments('segment_01').trim()
            'my_score/segments/segment_01'

            >>> path.materials.trim()
            'my_score/materials'

            >>> path.materials('tempi').trim()
            'my_score/materials/tempi'

        Returns string.
        '''
        import abjad
        configuration = abjad.abjad_configuration
        if self.scores is None or self.is_wrapper() or self.is_contents():
            home_directory = Path(configuration.home_directory)
            if str(self).startswith(str(home_directory)):
                return '../' + str(self.relative_to(home_directory))
            return str(self)
        count = len(self.scores.parts) + 1
        parts = self.parts
        parts = parts[count:]
        path = pathlib.Path(*parts)
        if str(path) == '.':
            return str(self)
        return str(path)

    def uncomment_tag(self, tag, greedy=False):
        r'''Uncomments `tag` in LilyPond file.

        Returns text, count, skipped triple.

        Text gives the processed file.

        Count gives the number of tags uncommented.

        Skipped gives the number of tags already uncommented (and therefore
        skipped).

        Matches all of `tag` when `greedy` is false; matches `tag` anywhere in
        tag when `greedy` is true.
        '''
        assert self.is_file()
        lines, count, skipped = [], 0, 0
        current_tag_number = None
        tag_parts = tag.split(':')
        with self.open() as file_pointer:
            for line in file_pointer.readlines():
                if ((greedy is True and tag not in line) or
                    (greedy is not True and
                    any(_ not in line for _ in tag_parts))):
                    current_tag_number = None
                    lines.append(line)
                    continue
                start = line.rfind(':') + 1
                tag_number = int(line[start:])
                first_nonwhitespace_index = len(line) - len(line.lstrip())
                index = first_nonwhitespace_index
                if line[index:index+4] == '%%% ':
                    line = list(line)
                    line[index:index+4] = []
                    line = ''.join(line)
                    if tag_number != current_tag_number:
                        current_tag_number = tag_number
                        count += 1
                else:
                    if tag_number != current_tag_number:
                        current_tag_number = tag_number
                        skipped += 1
                lines.append(line)
        text = ''.join(lines)
        return text, count, skipped

    def update_order_dependent_segment_metadata(self):
        r'''Updates order-dependent segment metadata.

        Returns none.
        '''
        paths = self.segments().list_paths()
        if not paths:
            return
        segment_count = len(paths)
        for segment_index, path in enumerate(paths):
            segment_number = segment_index + 1
            path.add_metadatum('segment_number', segment_number)
            path.add_metadatum('segment_count', segment_count)
        path = paths[0]
        first_bar_number = 1
        path.add_metadatum('first_bar_number', first_bar_number)
        measure_count = path.get_metadatum('measure_count')
        if not measure_count:
            return
        next_bar_number = first_bar_number + measure_count
        for path in paths[1:]:
            first_bar_number = next_bar_number
            path.add_metadatum('first_bar_number', next_bar_number)
            measure_count = path.get_metadatum('measure_count')
            if not measure_count:
                return
            next_bar_number = first_bar_number + measure_count

    def with_name(self, name):
        '''Gets path with `name`.

        Returns path.
        '''
        return self.parent / name

    def with_parent(self, name):
        '''Gets path with parent `name`.

        Returns path.
        '''
        return self.parent.parent / name / self.name

    def with_score(self, name):
        '''Gets path with score `name`.

        Returns path.
        '''
        if not self.is_score_package_path():
            return
        if self.is_wrapper():
            return self.with_name(name)
        if self.is_contents():
            return self.scores(name, name)
        path = self.scores(name, name)
        for part in self.parts[len(self.scores.parts) + 2:]:
            path /= part
        return path

    def write_metadata_py(self, metadata):
        r'''Writes `metadata` to `__metadata__.py` in current directory.

        Returns none.
        '''
        import abjad
        metadata_py_path = self('__metadata__.py')
        lines = []
        lines.append('import abjad')
        lines.append('')
        lines.append('')
        metadata = abjad.TypedOrderedDict(metadata)
        items = list(metadata.items())
        items.sort()
        metadata = abjad.TypedOrderedDict(items)
        if metadata:
            line = format(metadata, 'storage')
            line = 'metadata = {}'.format(line)
            lines.append(line)
        else:
            lines.append('metadata = abjad.TypedOrderedDict()')
        lines.append('')
        text = '\n'.join(lines)
        metadata_py_path.write_text(text)
