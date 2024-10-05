#!/home/tux/bin/python_pass/env/bin/python

import sys
from iterfzf import iterfzf
import subprocess
import traceback

# tree -i ~/.password-store/ | fzf | xargs -I {} echo ~/.password-store/{} | xargs gpg --decrypt
base = '/home/tux/.password-store/'
fzf_params = {
    'ansi': True,
    '__extra__': ['--height=50', '--border=bold', '--margin=35%'],
}

def iter_pass():
    # get the list of possible pass
    command = ["tree", "-i", "-f", "--noreport", base]
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout.splitlines()
    for i in result:
        if '.gpg' not in i:
            continue
        try:
            yield i.split(base)[1].strip()
        except Exception as e:
            print(e)
            print(traceback.print_exc())

def cleanup():
    cmd = 'sleep 5; echo "cleared" | xclip -sel clip'
    subprocess.Popen(cmd, shell=True)

# get the intended item
result = iterfzf(iter_pass(), **fzf_params)

# now, decrypt it using gpg
command = ["gpg", "--decrypt", f'{base}/{result}']
result = subprocess.run(command, capture_output=True, text=True)
result = result.stdout.splitlines()

dict_result = {}
try:
    dict_result['pass'] = result[0]
    for line in result[1:]:
        try:
            res = line.split(':')
            dict_result[res[0]] = res[1]
        except Exception:
            pass
            # print(result)
            # print(traceback.print_exc())
except Exception as e:
    print('No results found')

target = iterfzf(dict_result, multi=True, **fzf_params)
if target is None:
    cleanup()
    sys.exit(0)

for t in target:
    # First, echo the content and capture it
    echo_process = subprocess.Popen(['echo', dict_result[t]], stdout=subprocess.PIPE)

    # Then, pipe the output to xclip
    subprocess.Popen(['xclip', '-sel', 'clip'], stdin=echo_process.stdout)

    # Close the stdout of the first process to allow it to terminate
    echo_process.stdout.close()

cleanup()
