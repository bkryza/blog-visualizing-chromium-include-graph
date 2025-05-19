#!/usr/bin/env bash
set -euo pipefail

# Remember where we started
ROOT_DIR="$(pwd)"
CLANG_INCLUDE_GRAPH_BIN=/usr/bin/clang-include-graph

fetch_sources() {
  echo "=== Fetching Chromium sources ==="

  pushd "$ROOT_DIR" >/dev/null

  rm -rf depot_tools
  git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git

  mkdir -p chromium
  cd chromium
  # PATH should already contain path to depot_tools
  fetch --nohooks --no-history chromium
  gclient runhooks

  popd >/dev/null
}

build_chromium() {
  echo "=== Building Chromium ==="

  pushd "$ROOT_DIR/chromium/src" >/dev/null

  gn gen out/Default
  tools/clang/scripts/generate_compdb.py -p out/Default > compile_commands.json
  ninja -C out/Default chrome unit_tests browser_tests

  # Remove .o files to reduce volume size - we only need sources and compile_commands.json
  find . -type f -name '*.o' -exec rm -- '{}' \;

  popd >/dev/null
}

call_clang_include_graph() {
  local output_type=$1
  echo "=== Generating $output_type ==="

  pushd /build/chromium/src/out/Default >/dev/null

  $CLANG_INCLUDE_GRAPH_BIN \
    -d /build/chromium/src -v 1 --$output_type \
    --relative-to /build/chromium/src --relative-only \
    --remove-compile-flag "-fextend-variable-liveness=none" \
    --remove-compile-flag -Wno-nontrivial-memcall \
    --add-compile-flag -Wno-unknown-pragmas \
    --remove-compile-flag -fcomplete-member-pointers \
    --remove-compile-flag -MMD --jobs 32 \
    --add-compile-flag -fsyntax-only \
    -o $ROOT_DIR/chromium_include_graph_full.$output_type

  popd >/dev/null
}

generate_graphml() {
  call_clang_include_graph "graphml"
}

generate_graphviz() {
  call_clang_include_graph "graphviz"
}

generate_json() {
  call_clang_include_graph "json"
}

calculate_statistics() {
  echo "=== Calculate include graph statistics ==="

  pushd /build >/dev/null

  /calculate_statistics.py chromium_include_graph.graphml

  popd >/dev/null
}

# ================
# Usage / Dispatch
# ================

usage() {
  cat <<EOF
Usage: $(basename "$0") <step>

Steps:
  fetch     Fetch Chromium sources
  build     Build Chromium
  graphml   Generate the include graph in GraphML format
  graphviz  Generate the include graph in Graphviz format
  json      Generate the include graph in JSON format
  stats     Calculate include graph statistics
  all       Run all steps in order (default)

Example:
  $(basename "$0") fetch
  $(basename "$0") build
  $(basename "$0") graphml
  $(basename "$0") graphviz
  $(basename "$0") json
  $(basename "$0") stats
  $(basename "$0") all
EOF
  exit 1
}

# If no argument given, default to "all"
step="${1:-all}"

case "$step" in
  fetch)    fetch_sources;;
  build)    build_chromium;;
  graphml)  generate_graphml;;
  graphviz) generate_graphviz;;
  json)     generate_json;;
  stats)    calculate_statistics;;
  all)
    fetch_sources
    build_chromium
    generate_graphml
    calculate_statistics
    ;;
  *) usage;;
esac

