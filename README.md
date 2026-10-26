# Benchmarking scripts for concurrency analysers

## Setup

The only dependencies are [benchexec](https://github.com/sosy-lab/benchexec/blob/main/doc/INSTALL.md#debianubuntu)
and Git >=2.26 (needed for sparse-checkout).

Run the following command to obtain benchmarks and install a Python package with
tool info modules of analysers:

```shellSession
./setup.sh
```

For convenience, paths to executables of analysers may be set in `config.yaml`.
If a path is missing, provided tool info modules will fall back to the method
used by BenchExec to locate executables and you may need to specify them using
the `--tool-directory` argument when running BenchExec.

## Running benchmarks

Run the following command:

```shellSession
benchexec [arguments] benchmark-defs/.../def.xml
```

It may be useful to provide the `-N n` argument to run `n` benchmarks in parallel.
