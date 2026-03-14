import os
import sys
import difflib
import shutil

# vars
args = sys.argv
crt = os.listdir('.')


# check folder
if ".mygit" in crt :
    mygit = os.listdir('.mygit')
else:
    os.mkdir(".mygit")
    with open(".mygit/cversion.mygit" , "w") as cuv:
        cuv.write("0")
    mygit = os.listdir('.mygit')

if "project" in crt :
    pass
else:
    os.mkdir("project")


def edit_project(version):
    # step 1 delete folder project
    shutil.rmtree(project)
    # step 2 recreate folder project
    os.mkdir("project")
    # step 3 copy files from .mygit
    for file in os.listdir(".mygit/" + str(version)):
        shutil.copy(".mygit/" + str(version) + "/" + file , "project")


# get current version
with open(".mygit/cversion.mygit" , "r") as cuv:
    current_version = int(cuv.read())

def edit_version(operation , number=1):
    global current_version
    number = int(number)
    with open(".mygit/cversion.mygit" , "w") as cuv:
        if operation == "add":
            cuv.write(str(current_version + number))
            current_version += number
        elif operation == "subtract":
            cuv.write(str(current_version - number))
            current_version -= number
        elif operation == "set":
            cuv.write(str(number))
            current_version = number
        else:
            return 0

def diff_files(file1, file2):
    with open(file1) as f1, open(file2) as f2:
        a = f1.readlines()
        b = f2.readlines()

    matcher = difflib.SequenceMatcher(None, a, b)

    changes = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        changes.append({
            "type": tag,
            "file1_lines": a[i1:i2],
            "file2_lines": b[j1:j2]
        })

    return changes

# main commands "push , rolbck , diff , merge"
if len(args) > 1:
    if args[1] == "merge":
        print("The merge feature is only available for python and needs human overviewing")
        print("Yet to be implemented")
    elif args[1] == "diff":
        if len(args) < 3 :
            print("please use as python mygit.py diff <file1> <file2>")
        else :
            print(diff_files(args[2] , args[3]))
    elif args[1] == "push":
        if len(args) < 2 :
            print("please use as python mygit.py push")
        edit_version("add")
        os.mkdir(".mygit/" + str(current_version))
        for file in os.listdir("project"):
            shutil.copy("project/" + file, ".mygit/" + str(current_version))

    elif args[1] == "rollback":
        if len(args) < 2:
            print("All versions after rollback will be deleted")
            print("please use as python mygit.py rollback <version>")
            print("type b for past version")
            return
        try:
            target = int(args[2])
            edit_project(target)
            for i in range(target + 1, current_version + 1):
                path = ".mygit/" + str(i)
                shutil.rmtree(path)
        except ValueError:
            if args[2] == "b":
                os.system("rm -rf .mygit/" + str(current_version))
                edit_version("subtract")
                edit_project(current_version)
            else:
                print("Unkown command")
    else:
        print("Unkown command")
else:
    print("Please Use Arguments")

# TODO:
# 1. A branching system
# 2. Implement merge
# 3. A rollback no delete flag
# 4. A REPL system