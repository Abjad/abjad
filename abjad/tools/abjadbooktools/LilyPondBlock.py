from abjad.tools import abctools


class LilyPondBlock(abctools.AbjadValueObject):
    r'''A LilyPond block.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Internals'

    ### CLASS VARIABLES ###

    __slots__ = (
        '_image_layout_specifier',
        '_image_render_specifier',
        '_output_proxies',
        '_options',
        '_source_lines',
        '_starting_line_number',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        input_file_contents,
        image_layout_specifier=None,
        image_render_specifier=None,
        starting_line_number=None,
        **options
        ):
        from abjad.tools import abjadbooktools
        self._image_layout_specifier = image_layout_specifier
        self._image_render_specifier = image_render_specifier
        self._source_lines = tuple(input_file_contents)
        self._starting_line_number = starting_line_number
        self._output_proxies = [
            abjadbooktools.RawLilyPondOutputProxy(
                payload='\n'.join(input_file_contents),
                image_layout_specifier=image_layout_specifier,
                image_render_specifier=image_render_specifier,
                **options
                ),
            ]
        self._options = options

    ### PUBLIC METHODS ###

    def as_latex(
        self,
        configuration=None,
        output_directory=None,
        relative_output_directory=None,
        ):
        from abjad.tools import abjadbooktools
        result = []
        configuration = configuration or {}
        latex_configuration = configuration.get('latex', {})
        output_start_delimiter = latex_configuration.get(
            'output-start-delimiter',
            ('%%% ABJADBOOK START %%%',),
            )
        output_stop_delimiter = latex_configuration.get(
            'output-stop-delimiter',
            ('%%% ABJADBOOK END %%%',),
            )
        if self.output_proxies:
            result.extend(output_start_delimiter)
            before = latex_configuration.get('before-code-block', ())
            result.extend(before)
            for i, output_proxy in enumerate(self.output_proxies):
                lines = output_proxy.as_latex(
                    configuration=configuration,
                    output_directory=output_directory,
                    relative_output_directory=relative_output_directory,
                    )
                string = '\n'.join(lines)
                if isinstance(output_proxy, abjadbooktools.ImageOutputProxy):
                    if i < len(self.output_proxies) - 1:
                        next_proxy = self.output_proxies[i + 1]
                        if isinstance(next_proxy, abjadbooktools.ImageOutputProxy):
                            string += r'\\'
                result.append(string)
            after = latex_configuration.get('after-code-block', ())
            result.extend(after)
            result.extend(output_stop_delimiter)
            result = '\n'.join(result)
            result = [result]
        return result

    @classmethod
    def from_latex_lilypond_block(
        cls,
        input_file_contents,
        starting_line_number=None,
        **options
        ):
        from abjad.tools import abjadbooktools
        cleaned_options = {}
        for key, value in options.items():
            key = key.replace('-', '_')
            cleaned_options[key] = value
        image_layout_specifier, cleaned_options = abjadbooktools.ImageLayoutSpecifier.from_options(
            **cleaned_options)
        image_render_specifier, cleaned_options = abjadbooktools.ImageRenderSpecifier.from_options(
            **cleaned_options)
        code_block = cls(
            image_layout_specifier=image_layout_specifier,
            image_render_specifier=image_render_specifier,
            input_file_contents=input_file_contents,
            starting_line_number=starting_line_number,
            **cleaned_options
            )
        return code_block

    def interpret(self, console):
        """
        No-op.
        """
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def image_layout_specifier(self):
        return self._image_layout_specifier

    @property
    def image_render_specifier(self):
        return self._image_render_specifier

    @property
    def input_file_contents(self):
        return self._source_lines

    @property
    def options(self):
        return self._options

    @property
    def output_proxies(self):
        return self._output_proxies

    @property
    def starting_line_number(self):
        return self._starting_line_number
