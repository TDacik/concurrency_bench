#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2026 Tomas Dacik <idacik@fit.vut.cz>
# SPDX-License-Identifier: MIT

set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

# Donwload benchmarks
"$SCRIPT_DIR"/scripts/get_sv_benchmarks.sh

# Install benchexec tool info modules
pip3 install -e analysers/
