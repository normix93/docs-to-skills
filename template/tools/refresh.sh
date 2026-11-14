#!/usr/bin/env bash
# Fetch the public sources (shallow, sparse) and rebuild every GENERATED file.
#   tools/refresh.sh [workdir]      default /tmp/__PREFIX__-src
# No credentials: only public repositories.
set -euo pipefail
cd "$(dirname "$0")/.."
W="${1:-/tmp/__PREFIX__-src}"
mkdir -p "$W"

sparse_clone() {  # repo branch dir paths...
  local repo=$1 branch=$2 dir=$3; shift 3
  if [ ! -d "$dir/.git" ]; then
    git clone -q --depth 1 --filter=blob:none --sparse -b "$branch" "https://github.com/$repo.git" "$dir"
  else
    git -C "$dir" fetch -q --depth 1 origin "$branch" && git -C "$dir" reset -q --hard FETCH_HEAD
  fi
  git -C "$dir" sparse-checkout set --no-cone "$@"
}

# Replace with the official repository and the paths you read:
# sparse_clone <owner>/<repo> main "$W/source" /LICENSE* /docs/ /spec/
mkdir -p "$W/source"

python3 tools/build_references.py --source "$W/source"
echo "Rebuilt. Now: python3 -m unittest discover -s tests"
