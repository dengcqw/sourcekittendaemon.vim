let s:hi_id = 0
let s:hi_group_visual = 'Type'
if s:hi_id > 0
    matchdelete(s:hi_id)
endif
let s:hi_id = matchadd(s:hi_group_visual, sourcekittendaemon#place_holder_regex)

vnoremap <cr> :call sourcekittendaemon#RemovePlaceHolderDecoration()<cr>

if exists("g:sourcekittendaemon_jump_placeholder")
    exec "inoremap " . g:sourcekittendaemon_jump_placeholder . " <Esc>:call sourcekittendaemon#JumpToPlaceHolder()<cr>"
    exec "nnoremap " . g:sourcekittendaemon_jump_placeholder . " :call sourcekittendaemon#JumpToPlaceHolder()<cr>"
endif

let g:sourcekittendaemon_type = 0

setlocal omnifunc=sourcekittendaemon#Complete

