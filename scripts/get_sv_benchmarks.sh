#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2026 Tomas Dacik <idacik@fit.vut.cz>
# SPDX-License-Identifier: MIT

# Perform shallow clone of SV-COMP benchmarks, or update it when the repository is already cloned.
#
# Debugging:
#   git rev-parse --is-shallow-repository ... verify that the clone is really shallow

set -euo pipefail

SV_REPO="https://gitlab.com/sosy-lab/benchmarking/sv-benchmarks.git"
SV_LANGUAGE_DIR="c"

BENCHMARKS_DIR=benchmarks
TARGET="$BENCHMARKS_DIR"/sv-comp

# Perform shallow clone of the repository and checkout only C benchmarks
#
# TODO: This saves several GBs, but the content is still large,
#	we could just sparse-checkout contents described in Concurrency.set
clone() {
    git clone --depth=1 --filter=blob:none --sparse --no-tags $SV_REPO $TARGET
    (
    	cd $TARGET
	git sparse-checkout set "$SV_LANGUAGE_DIR"
    )
}

update() {
    (
	cd $TARGET
    	git fetch --quiet --depth=1 --no-tags origin
    	git reset --quiet --keep "@{upstream}"
    )
}

# Create a directory for benchmarks
mkdir -p -- "$BENCHMARKS_DIR"

if [[ -d "$TARGET/.git" ]]; then
    echo "Directory $TARGET exists, updating its content"
    update
elif [[ ! -e "$TARGET" ]] then
    echo "Directory $TARGET doesn't exist, creating it"
    clone
else
    echo "Error: directory $TARGET is not git repository"
    exit 1
fi
