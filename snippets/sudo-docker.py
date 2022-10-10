"""A small script to automatically add `sudo` to `docker` commands.

It's similar to `alias docker="sudo docker"`, but aliases aren't used by default
by Makefile and similar. So, if you're stuck with a Makefile that assumes docker
can be run without `sudo`, use this script.

Also, you could allow running docker without sudo, but it's not safe. Very unsafe.
"""
from pathlib import Path
from shutil import which
from textwrap import dedent

TEMPLATE = """
    #!/bin/bash
    sudo real-{exe} $@
"""


def main(exe: str):
    docker = which(exe)
    assert docker, f'{exe} not found'
    docker_path = Path(docker)
    real_docker_path = docker_path.parent / f'real-{exe}'
    real_content = docker_path.read_bytes()
    if len(real_content) < 200 and b'sudo real-' in real_content:
        print(f'{exe} already patched')
        return
    real_docker_path.write_bytes(real_content)
    patched_content = dedent(TEMPLATE.format(exe=exe))
    docker_path.write_text(patched_content)
    print(f'{exe} patched')


main('docker')
main('docker-compose')
