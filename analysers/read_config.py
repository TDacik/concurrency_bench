# Read path of analyser's executable from the config file
#
# SPDX-FileCopyrightText: 2026 Tomas Dacik <idacik@fit.vut.cz>
# SPDX-License-Identifier: MIT

import yaml

from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"

def get_executable(tool_locator, analyser_name, exe_name):
    with CONFIG_PATH.open("r") as f:
        config = yaml.safe_load(f) or {}
    
    path_str = config.get(analyser_name.lower())

    # If there is no entry in config, we fall back to Benchexec's tool locator
    if not path_str:
        return tool_locator.find_executable(exe_name)

    path = Path(path_str)
    if not path.is_absolute():
        path = (CONFIG_PATH.parent / path).resolve()
    
    return str(path / exe_name)
