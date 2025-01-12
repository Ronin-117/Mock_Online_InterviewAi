import os
os.environ["CMAKE_VERBOSE_MAKEFILE"]="1" # Set this variable so CMake's output is verbose
import subprocess

try:
    # run the program and redirect the output to a string
    result = subprocess.run(['python', 't1.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
    print("Standard output:\n", result.stdout)
    print("Standard error:\n", result.stderr)
except subprocess.CalledProcessError as e:
    print("Error during run:",e)
    print("Standard error:\n", e.stderr)