import os
import sys
import difflib

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


# get current version
with open(".mygit/cversion.mygit" , "r") as cuv:
    current_version = int(cuv.read())

def edit_version():
    with open(".mygit/cversion.mygit" , "w") as cuv:
        cuv.write(str(current_version + 1))

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
    elif args[1] == "diff":
        if len(args) < 3 :
            print("please use as python mygit.py diff <file1> <file2>")
        else :
            print(diff_files(args[2] , args[3]))

    else:
        print("Unkown command")
else:
    print("Please Use Arguments")