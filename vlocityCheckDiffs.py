import os
import subprocess
import sys

def main():    
    target_Branch = sys.argv[1]
    cmd=f'git diff --name-status {target_Branch} vlocity/'
    cmd_output, _=call_subprocess(cmd)
    print(cmd_output)
    if cmd_output:
        print("=====EXIT CODE 1=====")
        print("Changes detected")
        print(cmd_output)
        exit(1)
    else:
        print("=====EXIT CODE 0=====")
        print("No changes detected")
        print(cmd_output)
        exit(0)

def call_subprocess(command, verbose=True):
    ''' Calls subprocess, returns output and return code,
        if verbose flag is active it will print the output '''
    try:
        stdout = subprocess.check_output(command, stderr=subprocess.STDOUT,
                                         shell=True).decode('utf-8')
        if verbose:
            print_output(f'{stdout}')
        return stdout, 0
    except subprocess.CalledProcessError as exc:
        output = exc.output.decode('utf-8')
        returncode = exc.returncode
        if verbose:
            print(f'[ERROR]Subprocess returned non-zero exit '
                  f'status {returncode}')
            print_output(output)
        return output, returncode

def print_output(output, color='', tab_level=1):
    ''' Prints output in the color passed '''
    formated = '\t' * tab_level + output.replace('\n', '\n' + '\t' * tab_level)
    print(f'{formated}')
if __name__=='__main__':
    main()