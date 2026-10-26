# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# This file is based on the tool info from benchexec, but allows loading
# the tool directory from config.yaml and tracking of additional statistics.
#
# SPDX-FileCopyrightText: 2026 Tomas Dacik <idacik@fit.vut.cz>
#
# SPDX-License-Identifier: Apache-2.0


from benchexec import result
from benchexec.tools.sv_benchmarks_util import ILP32, LP64, get_data_model_from_task
from benchexec.tools.template import BaseTool2


class Tool(BaseTool2):
    """
    Tool info for Moirae, a verifier combining static analysis with dynamic
    analysis based on noise injection to quickly and precisely detect data
    races or prove their absence.
    """

    def name(self):
        return "Moirae"

    def project_url(self):
        return "https://github.com/TDacik/moirae"

    def version(self, executable):
        return self._version_from_tool(executable)

    def executable(self, tool_locator):
        return get_executable(tool_locator, self.name(), "moirae.py")

    def cmdline(self, executable, options, task, rlimits):
        data_model = get_data_model_from_task(task, {ILP32: "ILP32", LP64: "LP64"})
        data_model_opt = ["--data-model", data_model] if data_model is not None else []

        return [executable] + data_model_opt + options + list(task.input_files)

    def determine_result(self, run):
        if run.exit_code:
            if run.output.any_line_contains("RacerF failed"):
                return result.RESULT_ERROR + " (RacerF)"
            if run.output.any_line_contains("Lachesis failed"):
                return result.RESULT_ERROR + " (Lachesis)"
            return result.RESULT_ERROR

        if not run.output:
            return result.RESULT_ERROR + " (no output)"

        verdict = run.output[-1]

        if verdict.startswith("Verification successful"):
            return result.RESULT_TRUE_PROP

        if verdict.startswith("Data race found"):
            return result.RESULT_FALSE_DATARACE

        if verdict.startswith("Verification inconclusive"):
            return result.RESULT_UNKNOWN

        return result.RESULT_ERROR + " (unknown verdict)"
