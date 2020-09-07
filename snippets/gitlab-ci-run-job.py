"""
A small script to run GitLab CI jobs locally.
We need it because `exec` command of gitlab-runner
doesn't support `include` and `extend`.


Provided features:

    1. Config-level `include` support
    1. Job-level `extends` support
    1. Execute dependencies before running a job. Uses `needs` field (!5132)
    1. Share artifacts between jobs.
    1. Save artifacts from the job on the host machine.

Examples:

    sudo python3 scripts/run-job.py --exe $HOME/.local/bin/gitlab-runner --job flake8
    sudo python3 scripts/run-job.py --job build-packages --file GPG_KEY=/path/to/my/key.gpg
    sudo python3 scripts/run-job.py --job build-a-package --env PACKAGE_NAME=example

Should be run with `sudo` to use docker runner (depends on your local docker setup).

Gitlub CI runner is required to run the script:

    https://docs.gitlab.com/runner/install/

Options:

    --job (required): job name to run
    --exe: path to gitlab runner executable
    --conf: path to Gitlab CI config
    --env: env vars to set before running job
    --file: files to create before running job

Keep in mind that gitlab-runner runs a job only on commited changes.
Use `git commit --amend` to temporary commit changes you want to test.

When runs a job, edits in-place `.gitlab-ci.yml`
because `gitlab-runner` doesn't support specifying a custom path to the config.
"""

import shutil
import subprocess
from argparse import ArgumentParser
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml


CACHE_DIR = '/tmp/gitlab-cache'
YELLOW = '\033[1;33m'
RESET = '\033[0m'


def process_root_conf(root_conf: dict) -> None:
    # include subconfigs
    for include in root_conf.get('include', []):
        with open(include['local']) as stream:
            included_conf = yaml.load(stream=stream, Loader=yaml.SafeLoader)
        root_conf.update(included_conf)

    # evaluate `extends`
    for name, job in root_conf.items():
        if not isinstance(job, dict):
            continue
        if 'extends' not in job:
            continue
        base_job = root_conf[job['extends']]
        # merge `variables` section
        env_vars = base_job.get('variables', {}).copy()
        env_vars.update(job.get('variables', {}))
        # merge job configs
        new_job = base_job.copy()
        new_job.update(job)
        # set merged `variables`
        if env_vars:
            new_job['variables'] = env_vars
        root_conf[name] = new_job


def make_post_script(root_conf: dict, job: str) -> str:
    post_script = ['cd $CI_PROJECT_DIR']
    for artifact in root_conf[job].get('artifacts', {}).get('paths', []):
        post_script.append(f'cp -r {artifact} {CACHE_DIR}/')
    return '\n'.join(post_script)


def run_job(
    exe: str, job: str, cache_path: str, root_conf: dict, env_vars: dict,
) -> int:
    post_script = make_post_script(job=job, root_conf=root_conf)
    cmd = [exe, '--log-level=debug', 'exec', 'docker']
    cmd.extend(['--docker-cache-dir', cache_path])
    cmd.extend(['--docker-volumes', f'{cache_path}:{CACHE_DIR}'])
    # copy from cache artifacts created on previous stages
    cmd.extend(['--pre-build-script', f'cp -r {CACHE_DIR}/* ./ || true'])
    # save created artifacts into cache
    cmd.extend(['--post-build-script', post_script])
    for k, v in env_vars.items():
        cmd.extend(['--env', f'{k}={v}'])
    cmd.append(job)
    return subprocess.call(cmd)


def save_artifacts(cache_path: str) -> None:
    for artifact in Path(cache_path).iterdir():
        # remove the old artifact
        dst = Path(artifact.name)
        if dst.is_dir():
            shutil.rmtree(str(dst))
        elif dst.is_file():
            dst.unlink()
        # move or copy the new artifact
        shutil.move(str(artifact), '.')


def get_deps(job: str, root_conf: dict) -> list:
    job_conf = root_conf[job]
    result = []
    for subjob in job_conf.get('needs', []):
        for dep in get_deps(job=subjob, root_conf=root_conf):
            if dep not in result:
                result.append(dep)
        result.append(subjob)
    return result


def make_files(files: list, cache_path: str) -> dict:
    root = Path(cache_path)
    env_vars = dict()
    for line in files:
        var_name, file_path = line.split('=', maxsplit=1)
        file_path = file_path.strip()
        var_name = var_name.strip().lstrip('$')

        src = Path(file_path)
        dst_host = root / src.name
        dst_docker = Path(CACHE_DIR) / src.name
        shutil.copyfile(str(src), str(dst_host))
        env_vars[var_name] = str(dst_docker)
    return env_vars


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--job', required=True)
    parser.add_argument('--exe', default='gitlab-runner')
    parser.add_argument('--conf', default='.gitlab-ci.yml')
    parser.add_argument('--file', nargs='*', default=[])
    parser.add_argument('--env', nargs='*', default=[])
    args = parser.parse_args()
    conf_path = Path(args.conf)

    # read and fix Gitlab CI root config
    with conf_path.open() as stream:
        root_conf = yaml.load(stream=stream, Loader=yaml.SafeLoader)
    process_root_conf(root_conf)

    old_content = conf_path.read_text()
    try:
        with conf_path.open('w') as stream:
            yaml.dump(root_conf, stream=stream)
        jobs = get_deps(job=args.job, root_conf=root_conf) + [args.job]
        with TemporaryDirectory('_gitlab_cache') as cache_path:
            env_vars = dict(line.split('=', maxsplit=1) for line in args.env)
            env_vars.update(make_files(files=args.file, cache_path=cache_path))
            for job in jobs:
                print(YELLOW, '-' * 80, RESET)
                print(f'{YELLOW}# Running {job}{RESET}')
                retcode = run_job(
                    exe=args.exe,
                    job=job,
                    cache_path=cache_path,
                    root_conf=root_conf,
                    env_vars=env_vars,
                )
                if retcode:
                    exit(retcode)
            save_artifacts(cache_path=cache_path)
    finally:
        conf_path.write_text(old_content)
