import virtualenv, textwrap

for env in ('production','devel'):

    code = """
    import os, subprocess

    def adjust_options(options, args):
        if len(args) == 0:
            args.append('.')

    def after_install(options, home_dir):
        subprocess.call([
            os.path.join('bin', 'pip'),
            'install', '-r', '%s-requirements.txt'
        ])""" % env

    output = virtualenv.create_bootstrap_script(textwrap.dedent(code))
    f = open("%s-bootstrap.py" % env, 'w').write(output)
