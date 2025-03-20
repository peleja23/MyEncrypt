import os
import sys
import subprocess

def getFiles(path, file_type):
    # keep this function it might work as a filter later on
    files = os.listdir(path)
    file = []
    if file_type == 0:
        return files
    else:
        for f in files:
            if f.endswith(file_type):
                file.append(f)
        return file

def runFileSafety(operation, password, files, path):
    for file in files:
        file_path = os.path.join(path, file)
        if not os.path.isdir(os.path.join(path, file)):
            try:
                subprocess.run(["python3", "FileSafety.py", operation, password, file_path, file_path])
            except subprocess.CalledProcessError:
                print(f"Execution failed")

def main():
    # The user needs to give 5 arguments
    if len(sys.argv) != 5:
        print("Please insert the arguments in this order: python/python3 -script.py -operation -password -folder -type_of_file")
        return
    
    operation = sys.argv[1]
    password = sys.argv[2]
    input_folder = sys.argv[3]
    file_type = sys.argv[4]

    files = getFiles(input_folder, file_type)
    runFileSafety(operation, password, files, input_folder)

if __name__ == '__main__':
    main()