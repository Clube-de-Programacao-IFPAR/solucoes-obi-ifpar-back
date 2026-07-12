import json
import os
import pathlib
import shutil
import subprocess
import tempfile

from services.execution_utils import (
    compile_code,
    validate_subtask,
)

USE_DOCKER = (
    os.getenv("USE_DOCKER_SANDBOX", "false").lower() == "true"
)

DOCKER_IMAGE = os.getenv(
    "DOCKER_RUNNER_IMAGE",
    "obi-judge-runner",
)

def execute_submission(
    filename: str,
    source_code: str,
    subtasks: list[pathlib.Path],
):
    if USE_DOCKER:
        return execute_with_docker(
            filename,
            source_code,
            subtasks,
        )

    return execute_locally(
        filename,
        source_code,
        subtasks,
    )

def execute_locally(
    filename: str,
    source_code: str,
    subtasks: list[pathlib.Path],
):
    result = compile_code(
        pathlib.Path(filename),
        source_code,
    )

    if result is None or result[0] is None:
        raise RuntimeError("Erro ao preparar execução.")

    command, cleanup = result

    try:
        response = {
            "subtasks": []
        }

        for subtask in subtasks:
            response["subtasks"].append(
                validate_subtask(
                    subtask,
                    command,
                )
            )

        response["max_time"] = max(
            test["time"]
            for sub in response["subtasks"]
            for test in sub["tests"]
        )

        response["max_memory"] = max(
            test["memory"]
            for sub in response["subtasks"]
            for test in sub["tests"]
        )

        return response

    finally:
        for item in cleanup:
            if callable(item):
                item()
            else:
                subprocess.call(item)


def execute_with_docker(
    filename: str,
    source_code: str,
    subtasks: list[pathlib.Path],
):
    tempdir = pathlib.Path(
        tempfile.mkdtemp()
    )

    try:

        (tempdir / filename).write_text(
            source_code,
            encoding="utf-8",
        )

        tests_root = tempdir / "tests"
        tests_root.mkdir()

        for i, subtask in enumerate(subtasks, start=1):

            dst = tests_root / str(i)
            dst.mkdir()

            for file in subtask.iterdir():

                if file.is_file():

                    shutil.copy2(
                        file,
                        dst / file.name,
                    )

        subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "--network",
                "none",
                "--memory=512m",
                "--cpus=1",
                "--pids-limit=64",
                "-v",
                f"{tempdir.resolve()}:/workspace",
                DOCKER_IMAGE,
            ],
            check=True,
        )

        result_path = tempdir / "result.json"

        if not result_path.exists():
            raise RuntimeError(
                "runner.py não gerou result.json"
            )

        with result_path.open(
            encoding="utf-8",
        ) as f:

            return json.load(f)

    finally:

        shutil.rmtree(
            tempdir,
            ignore_errors=True,
        )
