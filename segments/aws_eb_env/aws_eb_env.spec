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

function testAwsEbEnvSegmentPrintsNothingIfNoElasticBeanstalkEnvironmentIsSet() {
  local P9K_CUSTOM_WORLD='echo world'
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(aws_eb_env world::custom)

  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  assertEquals "%K{015} %F{000}world %k%F{015}%f " "$(__p9k_build_left_prompt)"
}

function testAwsEbEnvSegmentWorksIfElasticBeanstalkEnvironmentIsSet() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(aws_eb_env)

  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  mkdir -p /tmp/powerlevel9k-test/.elasticbeanstalk
  echo "test:\n    environment: test" > /tmp/powerlevel9k-test/.elasticbeanstalk/config.yml
  cd /tmp/powerlevel9k-test

  assertEquals "%K{000} %F{002}🌱  %F{002}test %k%F{000}%f " "$(__p9k_build_left_prompt)"

  rm -fr /tmp/powerlevel9k-test
  cd -
}

function testAwsEbEnvSegmentWorksIfElasticBeanstalkEnvironmentIsSetInParentDirectory() {
  # Skip test, because currently we cannot detect
  # if the configuration is in a parent directory
  startSkipping # Skip test
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(aws_eb_env)

  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  mkdir -p /tmp/powerlevel9k-test/.elasticbeanstalk
  mkdir -p /tmp/powerlevel9k-test/1/12/123/1234/12345
  echo "test:\n    environment: test" > /tmp/powerlevel9k-test/.elasticbeanstalk/config.yml
  cd /tmp/powerlevel9k-test/1/12/123/1234/12345

  assertEquals "%K{000} %F{002}🌱  %F{002}test %k%F{000}%f " "$(__p9k_build_left_prompt)"

  rm -fr /tmp/powerlevel9k-test
  cd -
}

source shunit2/shunit2
