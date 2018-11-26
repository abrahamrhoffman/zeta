import subprocess
import argparse

def stop():
    cmd = ("docker stop zeta-ui")
    subprocess.call(cmd, shell=True)
    cmd = ("docker rm zeta-ui")
    subprocess.call(cmd, shell=True)

def start(version):
    cmd = ("""docker run -d \
                         --network host \
                         --restart always \
                         --name zeta-ui \
                         abehoffman/zeta-ui:{}""".format(version))
    subprocess.call(cmd, shell=True)

def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('Required arguments')
    required.add_argument('-v', '--version', action='store',
                                             help='Zeta-ui container version \
                                                   to run',
                                             required=True)
    args = parser.parse_args()
    stop()
    start(args.version)

if __name__ == "__main__":
    main()
