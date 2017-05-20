if !has('python')
  echoerr "SourceKittenDaemon.vim requires Vim compiled with +python"
  finish
endif

let s:plug = expand('<sfile>:p:h:h')
let s:python_version = 'python '
let s:pyfile_version = 'pyfile '
let sourcekittendaemon#place_holder_regex = "<#\[^><].*#>"

augroup sourcekittendaemon_complete
  autocmd!
  autocmd CompleteDone *.swift call s:CompletionFinished(v:completed_item)
augroup END

function! s:LoadPythonScript()
  if exists("s:loaded_sourcekittendaemon_python") && s:loaded_sourcekittendaemon_python
    return
  endif
  let s:loaded_sourcekittendaemon_python = 1

  let l:script = s:plug . "/pythonx/sourcekittendaemon.py"
  execute s:python_version . 'import sys'
  execute s:python_version . 'sys.path.append("' . s:plug . '")'
  execute s:pyfile_version . l:script
  execute s:python_version . 'source_kitten_daemon_vim = SourceKittenDaemonVim()'
endfunction

function! s:GetCompleteCol()
  let [num, pCol] = searchpos("(", "bn", line("."))
  let [num, dotCol] = searchpos("\\.", "bn", line("."))
  let col = dotCol > pCol ? dotCol : pCol
  let [num, spaceCol] = searchpos(" ", "bn", line("."))
  " find space, this is invalid position for comletion
  if spaceCol > col
      return 0
  else
      return col
  endif
endfunction

function! s:GetCompleteOffset()
  let line = line2byte(line("."))
  let col = s:GetCompleteCol()
  if col == 0
      return [0, ""]
  else
      let [num, spaceCol] = searchpos(" ", "bn", line("."))
      let lineString = getline(".")
      let completePart = strpart(lineString, spaceCol, col-spaceCol)
      return [line + col - 1, completePart]
  endif
endfunction

function! s:CompletionFinished(item)
  let word = a:item["word"]
  if word !~ "("
    return
  endif

  call cursor(line("."), 1)
  call sourcekittendaemon#JumpToPlaceHolder()
endfunction

function! sourcekittendaemon#Complete(findstart, base)
  if a:findstart
      return s:GetCompleteCol()
  endif

  update

  let [col, completePart] = s:GetCompleteOffset()
  call s:LoadPythonScript()
  execute "python source_kitten_daemon_vim.complete(prefix = '" . a:base
        \ . "', path = '" . expand("%:p")
        \ . "', completePart = '" . completePart
        \ . "', offset = " . col . ")"
  return s:result
endfunction

function! sourcekittendaemon#JumpToPlaceHolder()
    let [num, col] = searchpos("<#\[^><].*#>", "", line("."))
    " l : is noamal model move cursor left, for exit insert model, cursor is outside of place holder
    " va> : select all <> place holder
    call feedkeys("\<Esc>lva>")
    return ''
endfunction

function! sourcekittendaemon#RemovePlaceHolderDecoration()
    let pos_1 = getpos("'<")
    let pos_2 = getpos("'>")
    if pos_1[1] != pos_2[1]
        " not process for multi-line
        call feedkeys("\<CR>", "n")
        return
    endif

    let line = getline(".")
    let placeholder = line[pos_1[2]-1:pos_2[2]-1]

    let newString = substitute(placeholder, "<#T##\\|#>\\|#", "", "g")

    if newString == placeholder
        call feedkeys("\<CR>", "n")
    else
        " Fixed: directly replace with new string
        let newline = substitute(line, placeholder, newString, '')
        call setline(line("."), newline)

        let pos_1 = getpos("'<")
        let col = pos_1[2]
        "or call feedkeys(":'<,'>s/<#T##\\|#>\\|#//g\<CR>", "n")
        call cursor(line("."), col)
    endif
endfunction

