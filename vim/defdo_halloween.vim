" defdo halloween — generated from palette.json (defdo theme family)
" vim: use in ~/.vim/colors/  ·  nvim: use in ~/.config/nvim/colors/
set background=dark
hi clear
if exists('syntax_on')
  syntax reset
endif
let g:colors_name = "defdo_halloween"

let s:ansi = {"0": "#131c21", "1": "#e24f4f", "2": "#0dbc79", "3": "#f9bc02", "4": "#006ee8", "5": "#8954ac", "6": "#11a8cd", "7": "#e5e5e5", "8": "#666666", "9": "#f65757", "10": "#23d18b", "11": "#f9e802", "12": "#3b8eea", "13": "#a870d6", "14": "#29b8db", "15": "#fffefe"}
for s:i in range(16)
  execute 'let g:terminal_' . s:i . '_color = "' + s:ansi[string(s:i)] + '"'
endfor
let g:terminal_ansi_colors = map(range(16), {i -> s:ansi[string(i)]})

hi! Normal guifg=#eeffff ctermfg=231 guibg=#140021 ctermbg=233
hi! NonText guifg=#554c64 ctermfg=240 guibg=NONE ctermbg=NONE
hi! EndOfBuffer guifg=#554c64 ctermfg=240 guibg=NONE ctermbg=NONE
hi! LineNr guifg=#554c64 ctermfg=240 guibg=#180525 ctermbg=233
hi! CursorLineNr guifg=#afa6f6 ctermfg=147 guibg=#180525 ctermbg=233 gui=bold cterm=bold
hi! CursorLine guifg=NONE ctermfg=NONE guibg=#210f2e ctermbg=234
hi! ColorColumn guifg=NONE ctermfg=NONE guibg=#210f2e ctermbg=234
hi! Visual guifg=NONE ctermfg=NONE guibg=#afa6f6 ctermbg=147
hi! MatchParen guifg=#140021 ctermfg=233 guibg=#afa6f6 ctermbg=147 gui=bold cterm=bold
hi! StatusLine guifg=#eeffff ctermfg=231 guibg=#1d0a2a ctermbg=234
hi! StatusLineNC guifg=#554c64 ctermfg=240 guibg=#180525 ctermbg=233
hi! WinSeparator guifg=#554c64 ctermfg=240 guibg=NONE ctermbg=NONE
hi! VertSplit guifg=#554c64 ctermfg=240 guibg=#180525 ctermbg=233
hi! Directory guifg=#afa6f6 ctermfg=147 guibg=NONE ctermbg=NONE gui=bold cterm=bold
hi! Search guifg=#140021 ctermfg=233 guibg=#afa6f6 ctermbg=147
hi! IncSearch guifg=#140021 ctermfg=233 guibg=#a6c27b ctermbg=144
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
hi! Error guifg=#fd4d6a ctermfg=203 guibg=#370c2c ctermbg=235

hi! DiffAdd guifg=#a6c27b ctermfg=144 guibg=#26172c ctermbg=235
hi! DiffChange guifg=#f9bc02 ctermfg=214 guibg=#2f171d ctermbg=234
hi! DiffDelete guifg=#fd4d6a ctermfg=203 guibg=#30092a ctermbg=234
hi! DiffText guifg=#0291f7 ctermfg=33 guibg=#111641 ctermbg=235

hi! Pmenu guifg=#eeffff ctermfg=231 guibg=#1d0a2a ctermbg=234
hi! PmenuSel guifg=#140021 ctermfg=233 guibg=#afa6f6 ctermbg=147
hi! PmenuSbar guifg=NONE ctermfg=NONE guibg=#180525 ctermbg=233
hi! PmenuThumb guifg=NONE ctermfg=NONE guibg=#554c64 ctermbg=240
hi! TabLine guifg=#554c64 ctermfg=240 guibg=#180525 ctermbg=233
hi! TabLineSel guifg=#eeffff ctermfg=231 guibg=#1d0a2a ctermbg=234 gui=bold cterm=bold
hi! TabLineFill guifg=NONE ctermfg=NONE guibg=#180525 ctermbg=233
hi! Folded guifg=#554c64 ctermfg=240 guibg=#1d0a2a ctermbg=234
hi! FoldColumn guifg=#554c64 ctermfg=240 guibg=#180525 ctermbg=233
hi! SignColumn guifg=#554c64 ctermfg=240 guibg=#180525 ctermbg=233

