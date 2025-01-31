#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  export TERM="xterm-256color"
  local -a P9K_RIGHT_PROMPT_ELEMENTS
  P9K_RIGHT_PROMPT_ELEMENTS=()
  source test/helper/build_prompt_wrapper.sh
}

function testCommandExecutionTimeIsNotShownIfTimeIsBelowThreshold() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(world::custom command_execution_time)
  P9K_CUSTOM_WORLD='echo world'

  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  local _P9K_COMMAND_DURATION=2
  assertEquals "%K{015} %F{000}world %k%F{015}%f " "$(__p9k_build_left_prompt)"
}

function testCommandExecutionTimeThresholdCouldBeChanged() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(command_execution_time)
  local P9K_COMMAND_EXECUTION_TIME_THRESHOLD=1

  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  local _P9K_COMMAND_DURATION=2.03
  assertEquals "%K{001} %F{226}Dur %F{226}2.03s %k%F{001}%f " "$(__p9k_build_left_prompt)"
}

function testCommandExecutionTimeThresholdCouldBeSetToZero() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(command_execution_time)
  local P9K_COMMAND_EXECUTION_TIME_THRESHOLD=0

  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  local _P9K_COMMAND_DURATION=0.03
  assertEquals "%K{001} %F{226}Dur %F{226}0.03s %k%F{001}%f " "$(__p9k_build_left_prompt)"
}

function testCommandExecutionTimePrecisionCouldBeChanged() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(command_execution_time)
  local P9K_COMMAND_EXECUTION_TIME_THRESHOLD=0
  local P9K_COMMAND_EXECUTION_TIME_PRECISION=4

  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  local _P9K_COMMAND_DURATION=0.0001
  assertEquals "%K{001} %F{226}Dur %F{226}0.0001s %k%F{001}%f " "$(__p9k_build_left_prompt)"
}

function testCommandExecutionTimePrecisionCouldBeSetToZero() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(command_execution_time)
  local P9K_COMMAND_EXECUTION_TIME_PRECISION=0

  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  local _P9K_COMMAND_DURATION=23.5001
  assertEquals "%K{001} %F{226}Dur %F{226}23s %k%F{001}%f " "$(__p9k_build_left_prompt)"
}

function testCommandExecutionTimeIsFormattedHumandReadbleForMinuteLongCommand() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(command_execution_time)

  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  local _P9K_COMMAND_DURATION=180
  assertEquals "%K{001} %F{226}Dur %F{226}03:00 %k%F{001}%f " "$(__p9k_build_left_prompt)"
}

function testCommandExecutionTimeIsFormattedHumandReadbleForHourLongCommand() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(command_execution_time)

  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  local _P9K_COMMAND_DURATION=7200
  assertEquals "%K{001} %F{226}Dur %F{226}02:00:00 %k%F{001}%f " "$(__p9k_build_left_prompt)"
}

source shunit2/shunit2
