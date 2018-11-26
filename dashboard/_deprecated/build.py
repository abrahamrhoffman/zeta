import subprocess
import argparse

def build(version):
    cmd = ("docker build -t abehoffman/zeta-ui:{} .".format(version))
    subprocess.call(cmd, shell=True)

def push(version):
    cmd = ("docker push docker.io/abehoffman/zeta-ui:{}".format(version))
    subprocess.call(cmd, shell=True)

def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('Required arguments')
    required.add_argument('-v', '--version', action='store',
                                             help='Docker build version',
                                             required=True)
    args = parser.parse_args()
    build(args.version)
    push(args.version)

if __name__ == "__main__":
    main()
