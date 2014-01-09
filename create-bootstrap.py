import virtualenv, textwrap

output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess

def adjust_options(options, args):
    if len(args) == 0:
        args.append('.')

def after_install(options, home_dir):
    subprocess.call([
        os.path.join('bin', 'pip'),
        'install', '-r', 'devel-requirements.txt'
    ])
"""))
f = open('bootstrap.py', 'w').write(output)

