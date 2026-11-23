# slurm_mgr

A Python 3.9+ wrapper for Slurm output. Requires `sinfo` on your PATH and access
to a Slurm controller.

Clone the project:

```bash
git clone git@github.com:JonShelley/slurm_mgr.git
cd slurm_mgr
```

```bash
./slurm_mgr info -R
```

Displays `USER`, `TIMESTAMP`, `NODELIST`, and the full `REASON`, in that order.
Newlines inside a reason become `;`. Node groups and the header keep their own
lines. Slurm error messages and exit statuses are preserved.

Edit `INFO_FORMAT` near the top of `slurm_mgr` to change column order or widths.
The default is `%9u %19H %60N %E`. Keep `%E` without a width to display the full
reason, and last so it can extend to the end of the line.

To call it as `slurm_mgr info -R`, install it on your Slurm host from the directory
containing the script:

```bash
mkdir -p ~/.local/bin
install -m 755 slurm_mgr ~/.local/bin/slurm_mgr
export PATH="$HOME/.local/bin:$PATH"
slurm_mgr info -R
```

If needed, add the `export PATH` line to your shell startup file.

Run the checks with `python3 -m unittest -v`.
