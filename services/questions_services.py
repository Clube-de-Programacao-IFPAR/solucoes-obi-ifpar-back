import os
import re
import pathlib
import tempfile
import subprocess
import time
import psutil
import shutil

from ..dtos.validate_questions_dto import ValidateQuestionDTO
from ..errors.content_not_found import ContentNotFound
from ..errors.not_implemented import NotSupported

def is_subtask_folder(name: str) -> bool:
    return bool(re.match(r"^(:?\d+|teste\d+|test\d+)", name))

def is_test_file(name: str) -> bool:
    # better get strapped in
    # why must the names vary so much :(
    # it varies between phases???
    return bool(re.match(r"^(:in\d+|entrada|\d+\.in|\w+\.i\d+|out\d+|saida|\d+\.sol|\w+\.o\d+)", name))

def extract_id(filename: str) -> str:
    # capture digits
    m = re.search(r"(\d+)", filename)
    if m:
        return m.group(1)
    # no digit, return the filename
    return filename

def pair_tests(tests_path: pathlib.Path) -> list[tuple[pathlib.Path, pathlib.Path]]:
    inputs, outputs = {}, {}
    files = os.listdir(tests_path)

    for file in files:
        if is_test_file(file):
            path = os.path.join(tests_path, file)
            if any(tag in file for tag in ["in", "entrada", ".i"]):
                test_id = extract_id(file)
                inputs[test_id] = pathlib.Path(path)
            elif any(tag in file for tag in ["out", "saida", ".sol", ".o"]):
                test_id = extract_id(file)
                outputs[test_id] = pathlib.Path(path)

    # pair the files
    pairs = []
    for test_id in sorted(inputs.keys()):
        if test_id in outputs:
            pairs.append((inputs[test_id], outputs[test_id]))
    return pairs

# returns run command and cleanup command
def compile_code(filename: pathlib.Path, file: str) -> tuple[list[str] | None, list[list[str]] | None]:
    _, ext = os.path.splitext(filename)
    cmd = None
    tempdir = tempfile.mkdtemp() # store compile artifacts
    cleanup = [
        lambda: shutil.rmtree(path, ignore_errors=True)
    ]

    # write the code to a temporary file to pass as the code to run
    codefile, path = tempfile.mkstemp(dir=tempdir)
    os.write(codefile, file.encode())
    os.close(codefile)

    try:
        match ext:
            case ".py":
                cmd = ["python3", path]
            case ".js":
                cmd = ["node", path]
            case ".c":
                # compile the file
                exe = os.path.join(tempdir, "a.out")
                subprocess.run(["gcc", "-lm", "-O2", "-static", "-x", "c", path, "-o", exe], check=True)
                cmd = [exe]
            case ".cpp" | ".c++" | ".cc":
                # compile the file
                exe = os.path.join(tempdir, "a.out")
                subprocess.run(["g++", "-std=gnu++20", "-O2", "-static", "-x", "c++", path, "-o", exe], check=True)
                cmd = [exe]
            case ".java":
                # get class/file name (both must be the same)
                # f-ing javac, have to rename the file
                os.rename(path, pathlib.Path(path) / f"../{filename.name.capitalize()}")
                path = pathlib.Path(path) / f"../{filename.name.capitalize()}"
                class_name = filename.stem.capitalize()
                subprocess.run(["javac", path], cwd=tempdir, check=True)
                cmd = ["java", "-cp", tempdir, class_name]
            
    except Exception as e:
        print(f"exception when getting command: {e}")
        print("running cleanup")
        for command in cleanup:
            if callable(command):
                command()
            else:
                subprocess.call(command)

    return cmd, cleanup

def validate_subtask(path: pathlib.Path, command: list[str]):
    # this folder should contain a list of tasks to compare the file against
    # the current code assumes that it goes in the structure past like 2017 idk
    tests = pair_tests(path)
    results = {
        "tests": []
    }


    for inp, out in tests:
        try:
            stime = time.perf_counter()
            p = subprocess.Popen(
                command,
                stdin=inp.open(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            ps_proc = psutil.Process(p.pid)

            peak_mem = -1

            # poll process every 10ms to check it's memory usage
            while True:
                if p.poll() is not None:
                    break # process has finished
                try:
                    mem_info = ps_proc.memory_info()
                    peak_mem = max(peak_mem, mem_info.rss)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break
                time.sleep(0.010)
            
            # final check
            try:
                mem_info = ps_proc.memory_info()
                peak_mem = max(peak_mem, mem_info.rss)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            
            stdout, stderr = p.communicate(timeout=10)

            total_time = time.perf_counter() - stime

            # compare stdout with the output file

            output = out.read_text().strip()

            if stderr.strip() == "" and stdout.strip() == output:
                result = {
                    "success": True,
                    "time": total_time,
                    "memory": peak_mem / (1024 * 1024) # return in Mb
                }
            else:
                result = {
                    "success": False,
                    "time": total_time,
                    "memory": peak_mem / (1024 * 1024) # return in Mb
                }
        
        except subprocess.TimeoutExpired:
            result = {
                "success": False,
                "time": -1,
                "memory": -1
            }

        results["tests"].append(result)
    
    return results


def validate_answers(data: ValidateQuestionDTO):
    year = data.year
    level = data.level
    phase = data.phase
    name = data.name

    # re-assemble the folder name from the data
    folder_name = f"{year}f{phase}p{level}_{name}"

    folder_path = pathlib.Path(os.path.abspath("questions/answers/" + folder_name))

    if not os.path.exists(folder_path):
        raise ContentNotFound("Problem answer path not found")

    # answers may be inside a tmp/ folder for some reason
    if os.path.isdir(folder_path / "tmp"):
        folder_path = folder_path / "tmp"

    # unzipped zip may sometimes not have a folder inside it idk
    for folder in os.listdir(folder_path):
        if str(folder).endswith(name):
            folder_path = folder_path / folder
    if os.path.isdir(folder_path / folder_name):
        folder_path = folder_path / folder_name
    if os.path.isdir(folder_path / name):
        folder_path = folder_path / name

    # folder path should now contain the sub-task folders

    # fastest way i could think to do this
    subtasks: list[pathlib.Path] = list(filter(
        lambda path: is_subtask_folder(str(path.stem)),
        map(lambda path: folder_path / path,
         os.listdir(folder_path))
    ))

    response = {
        "subtasks": [None for _ in range(len(subtasks))],
        "max_time": float("inf"),
        "max_memory": -1
    }
    # data structure is:
    # response: {
    #   "subtasks": [
    #     { # subtask 0 indexed
    #       "tests": [ # also 0 indexed
    #         {
    #         "success": bool,
    #         "time": float,
    #         "memory": int
    #         }
    #       ]
    #     }
    #   ],
    #   "max_time": float,
    #   "max_memory": int
    # }

    # compile/make the command to run the code properly
    
    if ((result := compile_code(pathlib.Path(data.filename), data.file)) is not None
        and result[0] is not None):
        cmd, cleanup = result

        for i, subtask in enumerate(subtasks):
            response["subtasks"][i] = validate_subtask(subtask, cmd)
        
        # cleanup tmp dirs and files
        for command in cleanup:
            if callable(command):
                command()
            else:
                subprocess.call(command)
    else:
        # no command to run the code was returned
        # can't fulfill request
        raise NotSupported("File extension not supported")

    # add in the max time and max memory
    response["max_time"] = max(test["time"] for sub in response["subtasks"] for test in sub["tests"])
    response["max_memory"] = max(test["memory"] for sub in response["subtasks"] for test in sub["tests"])

    # data gotten, just return it
    return {"data": response}, 200

# test .py
# curl -X POST -H "Content-Type: application/json" -d '{"year":"2019","level":"1","phase":"1","name":"jogo","filename":"jogo.py","file":"n=int(input())+1;print(n*(n+1)//2)"}' http://127.0.0.1:5000/questions/validate
# curl -X POST -H "Content-Type: application/json" -d "{\}"
# test .c
# curl -X POST -H "Content-Type: application/json" -d '{"year":"2019","level":"1","phase":"1","name":"jogo","filename":"jogo.c","file":"#include<stdio.h>\nint main() {int n;scanf(\"%d\", &n);printf(\"%d\\n\",(n+1)*(n+2)/2);return 0;}"}' http://127.0.0.1:5000/questions/validate
# test .java
# curl -X POST -H "Content-Type: application/json" -d "{\"year\":\"2019\",\"level\":\"1\",\"phase\":\"1\",\"name\":\"jogo\",\"filename\":\"jogo.java\",\"file\":\"import java.util.Scanner;public class jogo{public static void main(String[] args){Scanner s=new Scanner(System.in);int n=s.nextInt();int r=(n+1)*(n+2)/2;System.out.println(r);s.close();}}\"}" http://127.0.0.1:5000/questions/validate
