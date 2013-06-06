" General commands
set autoindent
set bg=light
set encoding=utf-8
set fileencodings=utf-8,latin1
set ruler
set showcmd
set showmatch
set showmode
set title


" Showing line numbers and length
set number  " show line numbers
set tw=79   " width of document (used by gd)
set nowrap  " don't automatically wrap on load
set fo-=t   " don't automatically wrap text when typing
set colorcolumn=80


" Don't use TABs but spaces
set tabstop=4
set softtabstop=4
set shiftwidth=4
set shiftround
set expandtab


" Syntax highlighting
syntax on


" Remap <Leader> key to comma
let mapleader = ","


" Paragraph wrapping up to ``tw``
vmap Q gq
nmap Q gqap


" Sticky indentation in visual mode
vnoremap < <gv
vnoremap > >gv


" Comment out blocks
:map <F5> <Esc>:'a,'bs/^/#/<CR>
:map <F4> <Esc>:'a,'bs/#//<CR>


" Highlight parts of lines longer than ``tw`` characters
highlight OverLength ctermbg=red ctermfg=white guibg=#592929
match OverLength /\%81v.\+/


" Reload .vimrc on save
autocmd! bufwritepost .vimrc source %


" (plugin) pydiction
" https://github.com/vim-scripts/Pydiction
filetype plugin on
let g:pydiction_location='/Users/josiah/Documents/Development/abjad/trunk/abjad/etc/autocompletion/complete-dict'
let g:pydiction_menu_height = 20


" (plugin) vim-powerline
" cd ~/.vim/bundle
" git clone git://github.com/Lokaltog/vim-powerline.git
" set laststatus=2


" (plugin) Python folding
" mkdir -p ~/.vim/ftplugin
" wget -O ~/.vim/ftplugin/python_editing.vim http://www.vim.org/scripts/download_script.php?src_id=5492
" set nofoldenable
