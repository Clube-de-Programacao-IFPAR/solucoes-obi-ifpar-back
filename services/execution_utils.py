import os
import pathlib
import tempfile
import subprocess
import time
import psutil
import shutil
import re

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
    lambda: shutil.rmtree(tempdir, ignore_errors=True)
  ]

  # write the code to a temporary file to pass as the code to run
  codefile, path = tempfile.mkstemp(dir=tempdir)
  os.write(codefile, file.encode())
  os.close(codefile)

  try:
    match ext:
      case ".py":
        cmd = ["python", path]
      case ".js":
        cmd = ["node", path]
      case ".c":
        # compile the file
        exe = os.path.join(tempdir, "a.out")
        subprocess.run(["gcc", "-lm", "-O2", "-x", "c", path, "-o", exe], check=True)
        cmd = [exe]
      case ".cpp" | ".c++" | ".cc":
        # compile the file
        exe = os.path.join(tempdir, "a.out")
        subprocess.run(["g++", "-std=gnu++20", "-O2", "-x", "c++", path, "-o", exe], check=True)
        cmd = [exe]
      case ".java":
        # get class/file name (both must be the same)
        # f-ing javac, have to rename the file
        os.rename(path, pathlib.Path(path).parent / f"{filename.name}")
        path = pathlib.Path(path).parent / f"{filename.name}"
        class_name = filename.stem
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
  #
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
      MAX_TIME = 10 # in seconds
      has_timeouted = False
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
      else:
        p.kill() # kill it >:(
        p.wait(10) # wait for it to die

      total_time = time.perf_counter() - stime

      inp_file.close()

      if has_timeouted:
        result = {
          "success": False,
          "time": total_time,
          "memory": peak_mem / (1024 * 1024) # return in Mb
        }
      else:
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
