import os
import re
import pathlib

from .sandbox_service import execute_submission

from dtos.validate_questions_dto import ValidateQuestionDTO
from errors.content_not_found import ContentNotFound
from errors.invalid_field import InvalidField

def is_subtask_folder(name: str) -> bool:
    return bool(re.match(r"^(:?\d+|teste\d+|test\d+)", name))

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
    
    response = execute_submission(
        filename=data.filename,
        source_code=data.file,
        subtasks=subtasks,
    )

    return {"data": response}, 200

# test .py
# curl -X POST -H "Content-Type: application/json" -d '{"year":"2019","level":"1","phase":"1","name":"jogo","filename":"jogo.py","file":"n=int(input())+1;print(n*(n+1)//2)"}' http://127.0.0.1:5000/questions/validate
# curl -X POST -H "Content-Type: application/json" -d "{\}"
# test .c
# curl -X POST -H "Content-Type: application/json" -d '{"year":"2019","level":"1","phase":"1","name":"jogo","filename":"jogo.c","file":"#include<stdio.h>\nint main() {int n;scanf(\"%d\", &n);printf(\"%d\\n\",(n+1)*(n+2)/2);return 0;}"}' http://127.0.0.1:5000/questions/validate
# test .java
# curl -X POST -H "Content-Type: application/json" -d "{\"year\":\"2019\",\"level\":\"1\",\"phase\":\"1\",\"name\":\"jogo\",\"filename\":\"jogo.java\",\"file\":\"import java.util.Scanner;public class jogo{public static void main(String[] args){Scanner s=new Scanner(System.in);int n=s.nextInt();int r=(n+1)*(n+2)/2;System.out.println(r);s.close();}}\"}" http://127.0.0.1:5000/questions/validate
