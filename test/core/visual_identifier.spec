#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  export TERM="xterm-256color"
  local -a P9K_RIGHT_PROMPT_ELEMENTS
  P9K_RIGHT_PROMPT_ELEMENTS=()
  # Load Powerlevel9k
  source powerlevel9k.zsh-theme
  source functions/*
}

function testOverwritingIconsWork() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(world1::custom)
  local P9K_CUSTOM_WORLD1='echo world1'
  local P9K_CUSTOM_WORLD1_ICON='icon-here'

  assertEquals "%K{015} %F{000}icon-here %F{000}world1 %k%F{015}%f " "$(__p9k_build_left_prompt)"
}

function testVisualIdentifierAppearsBeforeSegmentContentOnLeftSegments() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(world1::custom)
  local P9K_CUSTOM_WORLD1='echo world1'
  local P9K_CUSTOM_WORLD1_ICON='icon-here'

  assertEquals "%K{015} %F{000}icon-here %F{000}world1 %k%F{015}%f " "$(__p9k_build_left_prompt)"
}

function testVisualIdentifierAppearsAfterSegmentContentOnRightSegments() {
  local -a P9K_RIGHT_PROMPT_ELEMENTS
  local -a P9K_RIGHT_PROMPT_ELEMENTS
  P9K_RIGHT_PROMPT_ELEMENTS=(world1::custom)
  local P9K_CUSTOM_WORLD1='echo world1'
  local P9K_CUSTOM_WORLD1_ICON='icon-here'

  assertEquals "%F{015}%K{015}%F{000} world1 %F{000}icon-here%f " "$(__p9k_build_right_prompt)"
}

function testVisualIdentifierPrintsNothingIfNotAvailable() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(world1::custom)
  local P9K_CUSTOM_WORLD1='echo world1'

  assertEquals "%K{015} %F{000}world1 %k%F{015}%f " "$(__p9k_build_left_prompt)"
}

function testVisualIdentifierWorksWithUnicodeIcon() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(world1::custom)
  local P9K_CUSTOM_WORLD1='echo world1'
  local P9K_CUSTOM_WORLD1_ICON='\u2714'

  assertEquals "%K{015} %F{000}✔ %F{000}world1 %k%F{015}%f " "$(__p9k_build_left_prompt)"
}

source shunit2/shunit2
