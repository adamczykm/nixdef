# nixdef
Very simple python script for finding definition of Nix functions (top-level packages).

### Start here

This is a very simple tool I've created for myself and may not work in all cases, but I decided it may be of use to some of you folks :)  
Read the source code to understand how it works.  
If you have an idea on how to improve it, put it in issues or prepare a PR.

### Installation

Make the script executable and put it in your PATH.

```bash
git clone https://github.com/adamczykm/nixdef
cd nixdef
chmod u+x nix-def.py
ln -s nix-def.py ~/.local/bin/nixdef 
```

### Example usages

```bash
nixdef fetchFromGithub
```  

```bash
nixdef ../build-support/fetchgit/private.nix
```  

Raw output:

```bash
nixdef (--noless|--raw|-nl) grep_arg
```  
