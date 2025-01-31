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

function mockKubectl() {
  case "$1" in
    'version')
      echo 'non-empty text'
      ;;
    'config')
      case "$2" in
        'view')
          case "$3" in
            '-o=jsonpath={.current-context}')
              echo 'minikube'
              ;;
            '-o=jsonpath={.contexts'*)
              echo ''
              ;;
            *)
              echo "Mock value missed"
              exit 1
              ;;
          esac
          ;;
      esac
      ;;
  esac
}

function mockKubectlOtherNamespace() {
  case "$1" in
    'version')
      echo 'non-empty text'
      ;;
    'config')
      case "$2" in
        'view')
          case "$3" in
            # Get Current Context
            '-o=jsonpath={.current-context}')
              echo 'minikube'
              ;;
            # Get current namespace
            '-o=jsonpath={.contexts'*)
              echo 'kube-system'
              ;;
            *)
              echo "Mock value missed"
              exit 1
              ;;
          esac
          ;;
      esac
      ;;
  esac
}

function testKubeContext() {
  alias kubectl=mockKubectl
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(kubecontext)

  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  assertEquals "%K{004} %F{015}⎈ %F{015}minikube/default %k%F{004}%f " "$(__p9k_build_left_prompt)"

  unalias kubectl
}
function testKubeContextOtherNamespace() {
  alias kubectl=mockKubectlOtherNamespace
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(kubecontext)

  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  assertEquals "%K{004} %F{015}⎈ %F{015}minikube/kube-system %k%F{004}%f " "$(__p9k_build_left_prompt)"

  unalias kubectl
}
function testKubeContextPrintsNothingIfKubectlNotAvailable() {
  alias kubectl=noKubectl
  local P9K_CUSTOM_WORLD='echo world'
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(world::custom kubecontext)

  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  assertEquals "%K{015} %F{000}world %k%F{015}%f " "$(__p9k_build_left_prompt)"

  unalias kubectl
}

source shunit2/shunit2
