This tool is used internally to unzip the thousands of files we receive.
The tool expects input directories to periodically look for zip files
This is multiprocessing tool which takes into account of your CPU threads before delving into unzip
Since unzip involves both IO and CPU bound (mostly IO though), I've considered making the actual unzip as multiprocessing, than threaded