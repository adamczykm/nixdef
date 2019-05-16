#!/usr/bin/env python
import subprocess
import sys
import os.path
from os.path import join, dirname


# TODO make it smarter..
def t():
    findret = subprocess.run([
        "find", "/nix/store", "-iname", "*all-packages.nix*", "-print", "-quit"
    ],
                             capture_output=True)
    if findret.stderr != b'':
        raise Exception(
            f"Couldn't find all-packages.nix. Stderr {findret.stderr}")
    elif findret.stdout == b'':
        raise Exception(f"Couldn't find all-packages.nix.")

    allpkgspath = findret.stdout.decode("utf-8").strip()
    top_level = os.path.dirname(allpkgspath)
    return allpkgspath, top_level


def list_matching_nixfiles(allpkgs_path, name):
    allpkgs = []
    with open(allpkgs_path, "r") as f:
        allpkgs = f.readlines()

    def parse_package_paths(callpkg_line):
        return filter(lambda x: x.startswith("../"), callpkg_line.split())

    # print(join(dirname(allpkgs_path),"asd"))
    call_package_sites = filter(
        lambda x: name in x.lower() and "callPackage" in x, allpkgs)

    ret = []
    for cps in call_package_sites:
        ret.extend(parse_package_paths(cps))

    for cps in ret:
        name = cps
        if not cps.endswith(".nix"):
            cps = join(cps, "default.nix")
        yield (name, join(dirname(allpkgs_path), cps))


def go_to_def(name, noless=False):
    nixfiles = list(list_matching_nixfiles(t()[0], name))
    if len(nixfiles) == 0:
        print(
            "Not found any matching definitions in nixpkgs' all-packages.nix.")
    elif len(nixfiles) == 1:
        if noless:
            with open(nixfiles[0][1]) as f:
                print(f.read())
        else:
            subprocess.call(['less', nixfiles[0][1]])
    else:
        intr = "Found multiple matching definitions in nixpkgs:"
        if not noless and len(nixfiles) > 20:
            inp = intr + "\n" + "\n".join([n[0] for n in nixfiles])
            subprocess.run(['less'], input=bytes(inp, 'utf-8'))
        else:
            print(intr)
            for n in nixfiles:
                print(n[0])


def test():
    go_to_def("fetchFromGitHub")


def main():
    name = sys.argv[1]
    noless = False
    if sys.argv[1] in ["--noless", "--raw", "-nl"]:
        name = sys.argv[2]
        noless = True
    go_to_def(name, noless)


if __name__ == '__main__':
    main()
