" defdo solid-gray — generated from palette.json (defdo theme family)
" vim: use in ~/.vim/colors/  ·  nvim: use in ~/.config/nvim/colors/
set background=dark
hi clear
if exists('syntax_on')
  syntax reset
endif
let g:colors_name = "defdo_solid_gray"

let s:ansi = {"0": "#131c21", "1": "#e24f4f", "2": "#0dbc79", "3": "#f9bc02", "4": "#006ee8", "5": "#8954ac", "6": "#11a8cd", "7": "#e5e5e5", "8": "#666666", "9": "#f65757", "10": "#23d18b", "11": "#f9e802", "12": "#3b8eea", "13": "#a870d6", "14": "#29b8db", "15": "#fffefe"}
for s:i in range(16)
  execute 'let g:terminal_' . s:i . '_color = "' + s:ansi[string(s:i)] + '"'
endfor
let g:terminal_ansi_colors = map(range(16), {i -> s:ansi[string(i)]})

hi! Normal guifg=#eeffff ctermfg=231 guibg=#303841 ctermbg=237
hi! NonText guifg=#69747a ctermfg=243 guibg=NONE ctermbg=NONE
hi! EndOfBuffer guifg=#69747a ctermfg=243 guibg=NONE ctermbg=NONE
hi! LineNr guifg=#69747a ctermfg=243 guibg=#343c45 ctermbg=237
hi! CursorLineNr guifg=#bebc2e ctermfg=142 guibg=#343c45 ctermbg=237 gui=bold cterm=bold
hi! CursorLine guifg=NONE ctermfg=NONE guibg=#3b444c ctermbg=238
hi! ColorColumn guifg=NONE ctermfg=NONE guibg=#3b444c ctermbg=238
hi! Visual guifg=NONE ctermfg=NONE guibg=#bebc2e ctermbg=142
hi! MatchParen guifg=#303841 ctermfg=237 guibg=#bebc2e ctermbg=142 gui=bold cterm=bold
hi! StatusLine guifg=#eeffff ctermfg=231 guibg=#384049 ctermbg=238
hi! StatusLineNC guifg=#69747a ctermfg=243 guibg=#343c45 ctermbg=237
hi! WinSeparator guifg=#69747a ctermfg=243 guibg=NONE ctermbg=NONE
hi! VertSplit guifg=#69747a ctermfg=243 guibg=#343c45 ctermbg=237
hi! Directory guifg=#bebc2e ctermfg=142 guibg=NONE ctermbg=NONE gui=bold cterm=bold
hi! Search guifg=#303841 ctermfg=237 guibg=#bebc2e ctermbg=142
hi! IncSearch guifg=#303841 ctermfg=237 guibg=#a6c27b ctermbg=144
hi! Cursor guifg=NONE ctermfg=NONE guibg=NONE ctermbg=NONE gui=reverse cterm=reverse
hi! lCursor guifg=NONE ctermfg=NONE guibg=NONE ctermbg=NONE gui=reverse cterm=reverse

hi! Comment guifg=#546e7a ctermfg=60 guibg=NONE ctermbg=NONE gui=italic cterm=italic
hi! Todo guifg=#f78c6c ctermfg=209 guibg=NONE ctermbg=NONE gui=bold,italic cterm=bold,italic
hi! Constant guifg=#f78c6c ctermfg=209 guibg=NONE ctermbg=NONE
hi! String guifg=#a6c27b ctermfg=144 guibg=NONE ctermbg=NONE
hi! Character guifg=#a6c27b ctermfg=144 guibg=NONE ctermbg=NONE
hi! Number guifg=#f78c6c ctermfg=209 guibg=NONE ctermbg=NONE
hi! Boolean guifg=#f78c6c ctermfg=209 guibg=NONE ctermbg=NONE
hi! Float guifg=#f78c6c ctermfg=209 guibg=NONE ctermbg=NONE
hi! Identifier guifg=#eeffff ctermfg=231 guibg=NONE ctermbg=NONE
hi! Function guifg=#0291f7 ctermfg=33 guibg=NONE ctermbg=NONE
hi! Statement guifg=#bfa6f1 ctermfg=147 guibg=NONE ctermbg=NONE
hi! Keyword guifg=#bfa6f1 ctermfg=147 guibg=NONE ctermbg=NONE
hi! Conditional guifg=#bfa6f1 ctermfg=147 guibg=NONE ctermbg=NONE
hi! Repeat guifg=#bfa6f1 ctermfg=147 guibg=NONE ctermbg=NONE
hi! Label guifg=#bfa6f1 ctermfg=147 guibg=NONE ctermbg=NONE
hi! Operator guifg=#89c6df ctermfg=116 guibg=NONE ctermbg=NONE
hi! Exception guifg=#bfa6f1 ctermfg=147 guibg=NONE ctermbg=NONE
hi! PreProc guifg=#f07178 ctermfg=204 guibg=NONE ctermbg=NONE
hi! Include guifg=#bfa6f1 ctermfg=147 guibg=NONE ctermbg=NONE
hi! Define guifg=#f07178 ctermfg=204 guibg=NONE ctermbg=NONE
hi! Macro guifg=#f07178 ctermfg=204 guibg=NONE ctermbg=NONE
hi! Type guifg=#f9bc02 ctermfg=214 guibg=NONE ctermbg=NONE
hi! StorageClass guifg=#bfa6f1 ctermfg=147 guibg=NONE ctermbg=NONE
hi! Structure guifg=#f9bc02 ctermfg=214 guibg=NONE ctermbg=NONE
hi! Typedef guifg=#f9bc02 ctermfg=214 guibg=NONE ctermbg=NONE
hi! Special guifg=#f9bc02 ctermfg=214 guibg=NONE ctermbg=NONE
hi! SpecialComment guifg=#546e7a ctermfg=60 guibg=NONE ctermbg=NONE gui=italic cterm=italic
hi! Delimiter guifg=#89c6df ctermfg=116 guibg=NONE ctermbg=NONE
hi! SpecialKey guifg=#89c6df ctermfg=116 guibg=NONE ctermbg=NONE
hi! Tag guifg=#f9bc02 ctermfg=214 guibg=NONE ctermbg=NONE
hi! Error guifg=#fd4d6a ctermfg=203 guibg=#4f3b47 ctermbg=238

hi! DiffAdd guifg=#a6c27b ctermfg=144 guibg=#3e4948 ctermbg=238
hi! DiffChange guifg=#f9bc02 ctermfg=214 guibg=#484839 ctermbg=238
hi! DiffDelete guifg=#fd4d6a ctermfg=203 guibg=#493b46 ctermbg=238
hi! DiffText guifg=#0291f7 ctermfg=33 guibg=#29455c ctermbg=238

hi! Pmenu guifg=#eeffff ctermfg=231 guibg=#384049 ctermbg=238
hi! PmenuSel guifg=#303841 ctermfg=237 guibg=#bebc2e ctermbg=142
hi! PmenuSbar guifg=NONE ctermfg=NONE guibg=#343c45 ctermbg=237
hi! PmenuThumb guifg=NONE ctermfg=NONE guibg=#69747a ctermbg=243
hi! TabLine guifg=#69747a ctermfg=243 guibg=#343c45 ctermbg=237
hi! TabLineSel guifg=#eeffff ctermfg=231 guibg=#384049 ctermbg=238 gui=bold cterm=bold
hi! TabLineFill guifg=NONE ctermfg=NONE guibg=#343c45 ctermbg=237
hi! Folded guifg=#69747a ctermfg=243 guibg=#384049 ctermbg=238
hi! FoldColumn guifg=#69747a ctermfg=243 guibg=#343c45 ctermbg=237
hi! SignColumn guifg=#69747a ctermfg=243 guibg=#343c45 ctermbg=237

