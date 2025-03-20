import os
import sys
import subprocess

def GetFiles():
    print()

def RunFileSafety(operation, password, input_file, output_file):
    try:
        subprocess.run(["python3", "FileSafety.py", operation, password, input_file, output_file])
    except subprocess.CalledProcessError as e:
        print(f"Execution failed")

def main():
    #operation = sys.argv[1]
    #password = sys.argv[2]
    #input_file = sys.argv[3]
    #output_file = sys.argv[4]

    input_folder = sys.argv[1]
    GetFiles(input_folder)
    #RunFileSafety(operation, password, input_file, output_file)


if __name__ == '__main__':
    main()