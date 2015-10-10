#!/usr/bin/python
#
# script to automatically pull updates from remote

import git
import os
import shutil

def main():
    repo = git.Repo(".")
    origin = repo.remote()
    # first fetch any changes from the remote
    origin.fetch()
    # get a list of what's been changed locally
    localchanges = repo.index.diff(None)
    # if there are any differences, we're going to have to iterate over them
    for d in repo.head.commit.diff(origin):
        # file can either be modified, deleted, moved or created
        # check if a file we've been working on has been renamed
        if d.renamed and d.a_path in [ld.a_path for ld in localchanges]:
            # then copy the old version to a new location (untracked)
            copypath = get_copypath(d.a_path)
            shutil.copy(d.a_path, copypath)
        elif d.deleted_file and d.a_path in [ld.a_path for ld in localchanges]:
            # do the same as for modified (could refactor but might as well 
            # be explicit
            copypath = get_copypath(d.a_path)
            shutil.copy(d.a_path, copypath)
        elif d.new_file:
            # check this new file doesn't happen to exist already:
            if os.path.exists(d.b_path):
                # we're going to want to move whatever is there already
                movepath = get_copypath(d.b_path)
                shutil.move(d.b_path, movepath)
        else:
            # assuming the file's been modified in that case, check if it's
            # been modified locally as well
            if d.a_path in [ld.a_path for ld in localchanges]:
                copypath = get_copypath(d.a_path)
                shutil.copy(d.a_path, copypath)
    # now we can just stash any changes (paranoid) and then merge in all 
    # the new changes
    repo.git.stash('save')
    repo.git.merge('origin', 'master')

def get_copypath(oldpath):
    i=1
    copypath = oldpath
    while os.path.exists(copypath):
        copypath = oldpath.split(".")[0] + ".{0}.".format(i) \
                 + oldpath.split(".")[1]
        i += 1
    return copypath

if __name__ == "__main__":
    main()
