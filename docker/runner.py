# "docker build -t obi-judge-runner -f docker/Dockerfile ." (para gerar a imagem)
# "docker images" (para verificar se foi criada)
# garanta que tenha "USE_DOCKER_SANDBOX=true" no .env para usar o docker

import json
import subprocess
import time
from pathlib import Path

workspace = Path("/workspace")
tests_root = workspace / "tests"

# ----------------------------------------------------------------------
# Descobre o arquivo fonte
# ----------------------------------------------------------------------

source = None

for file in workspace.iterdir():
    if file.is_file() and file.suffix in {
        ".py",
        ".js",
        ".c",
        ".cpp",
        ".cc",
        ".c++",
        ".java",
    }:
        source = file
        break

if source is None:
    raise RuntimeError("Nenhum arquivo fonte encontrado em /workspace.")

# ----------------------------------------------------------------------
# Compilação (quando necessário)
# ----------------------------------------------------------------------

match source.suffix:

    case ".py":
        command = ["python3", source.name]

    case ".js":
        command = ["node", source.name]

    case ".c":
        subprocess.run(
            [
                "gcc",
                source.name,
                "-O2",
                "-o",
                "program",
            ],
            cwd=workspace,
            check=True,
        )
        command = ["./program"]

    case ".cpp" | ".cc" | ".c++":
        subprocess.run(
            [
                "g++",
                source.name,
                "-std=gnu++20",
                "-O2",
                "-o",
                "program",
            ],
            cwd=workspace,
            check=True,
        )
        command = ["./program"]

    case ".java":
        subprocess.run(
            [
                "javac",
                source.name,
            ],
            cwd=workspace,
            check=True,
        )
        command = [
            "java",
            source.stem,
        ]

    case _:
        raise RuntimeError("Extensão não suportada.")

# ----------------------------------------------------------------------
# Executa todos os testes
# ----------------------------------------------------------------------

response = {
    "subtasks": [],
    "max_time": 0.0,
    "max_memory": -1,
}

MAX_TIME = 5

subtask_dirs = sorted(
    [p for p in tests_root.iterdir() if p.is_dir()],
    key=lambda p: p.name,
)

for subtask in subtask_dirs:

    subtask_result = {
        "tests": []
    }

    inputs = sorted(subtask.glob("*.in"))

    for input_file in inputs:

        expected = input_file.with_suffix(".sol")

        if not expected.exists():
            continue

        with input_file.open("r") as stdin:

            start = time.perf_counter()

            try:

                proc = subprocess.run(
                    command,
                    cwd=workspace,
                    stdin=stdin,
                    capture_output=True,
                    text=True,
                    timeout=MAX_TIME,
                )

                elapsed = time.perf_counter() - start

                expected_output = expected.read_text().strip()

                success = (
                    proc.returncode == 0
                    and proc.stderr.strip() == ""
                    and proc.stdout.strip() == expected_output
                )

                subtask_result["tests"].append(
                    {
                        "success": success,
                        "time": elapsed,
                        "memory": -1,
                    }
                )

                response["max_time"] = max(
                    response["max_time"],
                    elapsed,
                )

            except subprocess.TimeoutExpired:

                subtask_result["tests"].append(
                    {
                        "success": False,
                        "time": MAX_TIME,
                        "memory": -1,
                    }
                )

                response["max_time"] = max(
                    response["max_time"],
                    MAX_TIME,
                )

    response["subtasks"].append(subtask_result)

# ----------------------------------------------------------------------
# Salva o resultado para o sandbox_service
# ----------------------------------------------------------------------

with open(workspace / "result.json", "w", encoding="utf-8") as f:
    json.dump(response, f)