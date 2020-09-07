"""Generate markdown report with licenses text.

It looks for licenses in the current virtual environment
and leaves only packages specified in requirements.txt.
"""
import json
import sys

import pkg_resources
from pip._internal.utils.misc import get_installed_distributions


INTERNAL_PKGS = set()  # packages to exclude
LICENSE_FILES = ['LICENSE', 'LICENSE.txt', 'LICENSE.md']
META_FILES = ['METADATA', 'PKG-INFO']
REQUIREMENTS_FILE = 'requirements.txt'


def pkg_to_dict(pkg) -> dict:
    return dict(
        name=pkg.project_name,
        version=pkg.version,
        url=pkg.url,
        license=pkg.license,
        license_text=pkg.license_text,
    )


def get_license_from_meta(meta: str) -> str:
    for line in meta.split('\n'):
        if line.startswith('License: '):
            return line.split(': ', 1)[1]
    for line in meta.split('\n'):
        if line.startswith('Classifier: License'):
            return line.split('::')[-1]
    return 'UNKNOWN'


def get_url_from_meta(meta: str) -> str:
    for line in meta.split('\n'):
        if line.startswith('Home-page: '):
            return line.split(': ', 1)[1]
    return 'UNKNOWN'


def get_pkg_metadata(pkg, files: list):
    for file in files:
        if pkg.has_metadata(file):
            return pkg.get_metadata(file)
    return None


def get_installed_pkgs():
    installed_pkgs = get_installed_distributions()
    for pkg in installed_pkgs:
        meta = get_pkg_metadata(pkg, META_FILES)
        pkg.license = get_license_from_meta(meta).strip()
        pkg.license_text = get_pkg_metadata(pkg, LICENSE_FILES)
        pkg.url = get_url_from_meta(meta).strip()
        pkg.project_name_lower = pkg.project_name.lower()
        yield pkg


def sort_pkgs(pkgs):
    return sorted(pkgs, key=lambda pkg: pkg.project_name_lower)


def make_license_text_safe(text: str) -> str:
    text = text.strip().replace('```', '')
    return '```\n{}\n```'.format(text)


def pkgs_to_md(all_pkgs: list):
    pkgs_with_license_text = {pkg for pkg in all_pkgs if pkg.license_text}
    all_pkgs -= pkgs_with_license_text

    pkgs_with_unknown_license = {
        pkg for pkg in all_pkgs if pkg.license == 'UNKNOWN'
    }
    all_pkgs -= pkgs_with_unknown_license

    pkgs_without_license_text = {
        pkg for pkg in all_pkgs if not pkg.license_text
    }
    all_pkgs -= pkgs_without_license_text

    # if any packages are left at this stage we need to add more categories
    assert len(all_pkgs) == 0, all_pkgs

    for pkg in sort_pkgs(pkgs_with_license_text):
        print(f'{pkg.project_name} {pkg.version} ({pkg.url}) - {pkg.license}')
        print()
        print(make_license_text_safe(pkg.license_text))
        print('\n-----\n')

    if pkgs_without_license_text:
        for pkg in sort_pkgs(pkgs_without_license_text):
            print(f'{pkg.project_name} {pkg.version} ({pkg.url}) - {pkg.license}')

    if pkgs_with_unknown_license:
        print('\n-----\n')
        for pkg in sort_pkgs(pkgs_with_unknown_license):
            print(f'{pkg.project_name} {pkg.version} ({pkg.url}) - {pkg.license}')

    print('\n-----\n')
    print('license detected:', len(pkgs_with_license_text))
    print('cannot detect license text:', len(pkgs_with_license_text))
    print('cannot detect license type:', len(pkgs_with_unknown_license))


def main():
    with open(REQUIREMENTS_FILE) as stream:
        reqs = list(pkg_resources.parse_requirements(stream))
    requirement_pkgs = [pkg.name.lower() for pkg in reqs]

    all_pkgs = set()
    for pkg in get_installed_pkgs():
        if pkg.project_name_lower not in requirement_pkgs:
            continue
        if pkg.project_name_lower in INTERNAL_PKGS:
            continue
        all_pkgs.add(pkg)

    if '--json' in sys.argv:
        print(json.dumps([pkg_to_dict(pkg) for pkg in all_pkgs]))
        return
    pkgs_to_md(all_pkgs)


if __name__ == '__main__':
    main()
