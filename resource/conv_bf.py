###########################
#-*- coding: utf-8 -*-
# :h functions
# の関数リストから辞書を構築する
#
# 0) https://raw.githubusercontent.com/vim/vim/master/runtime/doc/eval.txt
# 1) copy the `:h functions` to resource/builtin-func
# 2) do conv_by.py and output to autoload/vimlint/builtin.vim
###########################

# import {{{
import re
# }}}

re1 = re.compile('\).*')
re2 = re.compile('\[.*')
re3 = re.compile('\(.*')
tbl = {}
for line in open('resource/builtin-func', 'r'):
  if line[0] == ' ' or line[0] == '\t':
    continue
  line = line.rstrip('\r\n')
  line = re.sub(re1, ')', line)
  hasdots = (line.count("...") > 0)
  argnum = line.count("{")
  line2 = re.sub(re2, '', line)
  argmin = line2.count("{")
  func = re.sub(re3, '', line2)

  # getreg( [{regname} [, 1]])	String	contents of register
  # => 1 のみを受け付ける.
  #
  # mode( [expr])			String	current editing mode
  # => 好みらしい.
  if func == 'getreg':
    argnum = 3
  if line.count('[expr]') > 0:
    argnum = argnum + 1
  if hasdots:
    argmax = 65535
  else:
    argmax = argnum

  if func in tbl:
    if tbl[func][0] > argmin:
      tbl[func][0] = argmin
    if tbl[func][1] < argmax:
      tbl[func][1] = argmax
  else:
    tbl[func] = [argmin, argmax]
  # bug: argv, char2nr
  # print("let s:builtin_func.%s = {'min' : %d, 'max': %d}" % (func,argmin, argmax))


print('" builtin-functions: generated by resource/conv_bf.py')
print("")
print("let s:save_cpo = &cpo")
print("set cpo&vim")
print("")
print("let s:builtin_func = {}")
print('" {{{')
for f in sorted(tbl.keys()):
  print("let s:builtin_func.%s = {'min' : %d, 'max': %d}" % (f,tbl[f][0],tbl[f][1]))
print('" }}}')
print("")
print('function! vimlint#builtin#get_func_inf(name) "{{{')
print('  return get(s:builtin_func, a:name, {})')
print('endfunction "}}}')
print("")
print('let &cpo = s:save_cpo')
print('unlet s:save_cpo')
print("")
