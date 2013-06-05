set autoindent
set bg=light
set encoding=utf-8
set expandtab
set fileencodings=utf-8,latin1
set nowrap
set ruler
set showcmd
set showmatch
set showmode
set sw=4
set title
set ts=4

syntax on

filetype plugin on
let g:pydiction_location='/Users/josiah/Documents/Development/abjad/trunk/abjad/etc/autocompletion/complete-dict'
let g:pydiction_menu_height = 20

:map <F5> <Esc>:'a,'bs/^/#/<CR>
:map <F4> <Esc>:'a,'bs/#//<CR>

highlight OverLength ctermbg=red ctermfg=white guibg=#592929
match OverLength /\%81v.\+/

