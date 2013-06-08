from ricky.utils import write_changes
from clint import args


def forge_changes():
    dist = None
    for flag in args.flags:
        if flag is None:
            break

        k, v = (x.strip() for x in flag.split("=", 1))
        if k == '--dist':
            dist = v

    if dist is None:
        raise Exception("No dist given with --dist=unstable")

    for what in args.files:
        changes = write_changes(what, dist)
