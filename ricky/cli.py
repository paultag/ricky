from ricky.utils import write_changes, fetch_and_upload
from clint import Args

args = Args()

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


def upload_package():
    opts = {
        "dist": "unstable",
        "source": None,
        "version": None,
        "group": None
    }

    for flag in args.flags:
        if flag is None:
            break

        k, v = (x.strip() for x in flag.split("=", 1))
        if k.startswith('--'):
            k = k[2:]
        opts[k] = v

    for k, v in opts.items():
        if v is None:
            raise KeyError(
                "give me --dist=unstable --source=fluxbox --version=1.3.5-1 --group=test"
            )

    if opts['group']:
        opts['X-Debile-Group'] = opts.pop('group')
    else:
        opts.pop('group')

    fetch_and_upload(**opts)
