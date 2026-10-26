# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# This file is based on the tool info from benchexec, but allows loading
# the tool directory from config.yaml and tracking of additional statistics.
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
# SPDX-FileCopyrightText: 2024-2026 Tomas Dacik <idacik@fit.vut.cz>
#
# SPDX-License-Identifier: Apache-2.0


from benchexec import result
from benchexec.tools.template import BaseTool2
from benchexec.tools.sv_benchmarks_util import get_data_model_from_task, ILP32, LP64

from .read_config import get_executable

class Tool(BaseTool2):
    """
    Tool info for RacerF, a data race detection plugin of Frama-C.
    """

    def name(self):
        return "RacerF"

    def project_url(self):
        return "https://github.com/TDacik/RacerF"

    def version(self, executable):
        return self._version_from_tool(executable)

    def executable(self, tool_locator):
        return get_executable(tool_locator, self.name(), "racerf.py")

    def cmdline(self, executable, options, task, rlimits):
        machdep = get_data_model_from_task(
            task, {ILP32: "gcc_x86_32", LP64: "gcc_x86_64"}
        )
        machdep_opt = ["-machdep", machdep] if machdep is not None else []

        return [executable] + machdep_opt + options + list(task.input_files)

    def determine_result(self, run):
        if run.exit_code:
            return result.RESULT_ERROR

        if run.output.any_line_contains("The result may be imprecise"):
            return result.RESULT_UNKNOWN

        if run.output.any_line_contains("Data race (must)"):
            return result.RESULT_FALSE_DATARACE

        if run.output.any_line_contains("Data race (may)"):
            return result.RESULT_UNKNOWN

        if run.output.any_line_contains("No data races found"):
            return result.RESULT_TRUE_PROP

        return result.RESULT_ERROR

    def get_value_from_output(self, output, identifier):
        for line in output:
            if identifier in line:
                [_, val] = line.split(":")
                return int(val.strip())

        return "-"
