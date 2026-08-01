import os
import re
import pathlib
import tempfile
import subprocess
import time
import psutil
import shutil

from dtos.validate_questions_dto import ValidateQuestionDTO
from errors.content_not_found import ContentNotFound
from errors.not_implemented import NotSupported
from errors.invalid_field import InvalidField

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

    compile_error = None

    cleanup = [
        lambda: shutil.rmtree(tempdir, ignore_errors=True)
    ]

    # write the code to a temporary file to pass as the code to run
    codefile, path = tempfile.mkstemp(dir=tempdir)
    os.write(codefile, file.encode())
    os.close(codefile)

    try:
        match ext:
            case ".py":
                result = subprocess.run(["python", "-m", "py_compile", path], capture_output=True, text=True)
                if result.returncode != 0:
                    compile_error = (result.stderr.strip() or result.stdout.strip())
                else:
                    cmd = ["python", path]
            case ".js":
                cmd = ["node", path]
            case ".c":
                # compile the file
                exe = os.path.join(tempdir, "a.out")
                result = subprocess.run(["gcc", "-lm", "-O2", "-static", "-x", "c", path, "-o", exe], capture_output=True, text=True)
                if result.returncode != 0:
                    compile_error = (result.stderr.strip() or result.stdout.strip())
                else:
                    cmd = [exe]
            case ".cpp" | ".c++" | ".cc":
                # compile the file
                exe = os.path.join(tempdir, "a.out")
                result = subprocess.run(["g++", "-std=gnu++20", "-O2", "-static", "-x", "c++", path, "-o", exe], capture_output=True, text=True)
                if result.returncode != 0:
                    compile_error = (result.stderr.strip() or result.stdout.strip())
                else:
                    cmd = [exe]
            case ".java":
                # get class/file name (both must be the same)
                # f-ing javac, have to rename the file
                os.rename(path, pathlib.Path(path).parent / f"{filename.name}")
                path = pathlib.Path(path).parent / f"{filename.name}"
                class_name = filename.stem
                result = subprocess.run(["javac", path], cwd=tempdir, capture_output=True, text=True)
                if result.returncode != 0:
                    compile_error = (result.stderr.strip() or result.stdout.strip())
                else:
                    cmd = ["java", "-cp", tempdir, class_name]
            case _:
                compile_error = "Unsupported file extension."
    except Exception as e:
        compile_error = str(e)

    return cmd, cleanup, compile_error

def validate_subtask(path: pathlib.Path, command: list[str]):
    # this folder should contain a list of tasks to compare the file against
    # the current code assumes that it goes in the structure past like 2017 idk
    tests = pair_tests(path)
    correct_tests = 0

    #  This variable will be later used as an attribute for results
    tests_attribute = []



    # We'll have four possible success results for all tests 
    # Priorly, success was a boolean variable which only indicated if the test was successful
    # Now, we'll send an integer indicating or success, ow which kind of failure happened during the process 
    # All possible results are: 
    # 0 -> Error (Outputs do not correspond)
    # 1 -> Success
    # 2 -> TLE (Time Limit exceeded)
    # 3 -> MLE (Memory limit exceeded)
    # 4 -> RTE (Run Time Error) 

    for inp, out in tests:
        try:
            inp_file = inp.open()
            stime = time.perf_counter()
            p = subprocess.Popen(
                command,
                stdin=inp_file,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            ps_proc = psutil.Process(p.pid)

            peak_mem = -1
            MAX_TIME = 5 # in seconds
            MAX_MEMORY = 512 * 1024 * 1024

            has_timeouted = False
            has_exceeded_max_memory = False
            # poll process every 10ms to check it's memory usage
            while True:
                if p.poll() is not None:
                    break # process has finished
                elif time.perf_counter() - stime >= MAX_TIME:
                    has_timeouted = True
                    break # timeout
                try:
                    mem_info = ps_proc.memory_info()
                    peak_mem = max(peak_mem, mem_info.rss)

                    if peak_mem > MAX_MEMORY: 
                        has_exceeded_max_memory = True 
                        break 

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break
                time.sleep(0.010)
            
            # final check
            try:
                mem_info = ps_proc.memory_info()
                peak_mem = max(peak_mem, mem_info.rss)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            
            if not has_timeouted:
                stdout, stderr = p.communicate(timeout=10)
                stdout = stdout.strip()
                stderr = stderr.strip()
            else:
                p.kill() # kill it >:(
                p.wait(10) # wait for it to die

            total_time = time.perf_counter() - stime

            inp_file.close()

            if has_timeouted:
                result = {
                    "success": 2,
                    "error": "",
                    "time": total_time,
                    "memory": peak_mem / (1024 * 1024) # return in Mb
                }

            elif has_exceeded_max_memory:
                result = {
                    "success": 3,
                    "error": "",
                    "time": total_time, 
                    "memory": peak_mem
                }

            else:
                # compare stdout with the output file

                output = out.read_text().strip()

                if stderr == "" and stdout == output:
                    correct_tests += 1

                    result = {
                        "success": 1,
                        "error": "",
                        "time": total_time,
                        "memory": peak_mem / (1024 * 1024) # return in Mb
                    }
                elif stderr != "":
                    result = {
                        "success": 4,
                        "error": stderr,
                        "time": total_time,
                        "memory": peak_mem  / (1024 * 1024) # return in Mb
                    }
                else:
                    result = {
                        "success": 0,
                        "error": "",
                        "time": total_time,
                        "memory": peak_mem / (1024 * 1024) # return in Mb
                    }
        
        except subprocess.TimeoutExpired:
            result = {
                "success": 2,
                "error": "",
                "time": -1,
                "memory": -1
            }

        tests_attribute.append(result)

    results = {
      "total_tests": len(tests),
       "correct_tests": correct_tests,
       "tests": tests_attribute
    }

    return results


def validate_answers(data: ValidateQuestionDTO):
    year = data.year
    #level = data.level unneeded to get the folder name and path
    phase = data.phase
    name = data.name

    # validate parameters
    if any(re.search(r"[^\w]", e) for e in [year, phase, name]):
        raise InvalidField("Year, phase or name contained an invalid character")

    # re-assemble the folder name from the data
    folder_name = f"{year}_{phase}_{name}"

    folder_path = pathlib.Path(os.path.abspath("questions/answers/" + folder_name))

    if not os.path.exists(folder_path):
        raise ContentNotFound("Problem answer path not found")

    # answers may be inside a tmp/ folder for some reason
    if os.path.isdir(folder_path / "tmp"):
        folder_path = folder_path / "tmp"

    # unzipped zip may sometimes not have a folder inside it idk
    for folder in os.listdir(folder_path):
        if name in str(folder):
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

    correct_subtasks = 0 

    response = {
        "total_subtasks": len(subtasks),
        "correct_subtasks": correct_subtasks,
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
    #          "total_tests": int
    #          "correct_tests": int 
    #         "success": int,
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
    
    cmd, cleanup, compile_error = compile_code(pathlib.Path(data.filename), data.file)

    if compile_error is not None:
        for command in cleanup:
            if callable(command):
                command()
            else:
                subprocess.call(command)
        return {"error": compile_error}, 400

    for i, subtask in enumerate(subtasks):
        response["subtasks"][i] = validate_subtask(subtask, cmd)
        
        if response["subtasks"][i]["total_tests"] == response["subtasks"][i]["correct_tests"]:
            correct_subtasks += 1

    response["correct_subtasks"] = correct_subtasks

    for command in cleanup:
        if callable(command):
            command()
        else:
            subprocess.call(command)

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
