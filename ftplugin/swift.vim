setlocal omnifunc=sourcekittendaemon#Complete

let s:hi_id = 0
let s:hi_group_visual = 'Type'
if s:hi_id > 0
    matchdelete(s:hi_id)
endif
let s:hi_id = matchadd(s:hi_group_visual, sourcekittendaemon#place_holder_regex)

vnoremap <cr> :call sourcekittendaemon#RemovePlaceHolderDecoration()<cr>

if exists("g:sourcekittendaemon_jump_placeholder")
    exec "inoremap " . g:sourcekittendaemon_jump_placeholder . " <C-R>=sourcekittendaemon#JumpToPlaceHolder()<cr>"
endif

