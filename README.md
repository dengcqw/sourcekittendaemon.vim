# SourceKittenDaemon.vim

This plugin provides vim integration with [SourceKittenDaemon][sdk].
This means you can have autocomplete for Swift projects in vim.

This plugin uses the normal `'omnifunc'` infrastructure. By default
completion is mapped to `<C-x><C-o>`. See `:help 'omnifunc'` for more
information.

## Limitations

- SourceKittenDaemon doesn't yet provide support for `xcworkspace`s
- This plugin doesn't do anything about completion tokens (meaning you
  can't do `<TAB>` to jump between args as you do in Xcode)
- Currently completion only seems to work after dots
- Currently you cannot configure the port used with SourceKittenDaemon,
  use the default 8081.

## Installation

Install and setup [SourceKittenDaemon][sdk].

If you don't have a preferred plugin installation method, check out
[vim-plug](https://github.com/junegunn/vim-plug).

**NOTE**: This plugin doesn't provide Swift runtime files. If you'd like
those checkout [swift.vim](https://github.com/keith/swift.vim)

[sdk]: https://github.com/terhechte/SourceKittenDaemon

## additional improvement by dengcqw

- complete for "("
- pass string before dot to server for cache
- skip if there are blanks between dot or "(" with cursor
- jump to placeholder, and <CR> to remove patten "<#>"

**Tips**   if set g:ycm_semantic_triggers for swift in vimrc, we can enjoy YCM.  
I also fork [SourceKittenDaemon][https://github.com/terhechte/SourceKittenDaemon] to add cache and sort result
