#!/bin/sh

# Nasty hack to patch py2app virtualenv recipe bug
# see:
#   http://stackoverflow.com/questions/25394320/py2app-modulegraph-missing-scan-code
#   https://bitbucket.org/ronaldoussoren/py2app/issue/156
#

pymodule="py2app.recipes.virtualenv"
pyscript='import '$pymodule'; x='$pymodule'.__file__; print(x[:-1] if x.lower().endswith(".pyc") else x)'
source_file=$(python -c "$pyscript")

if [ -f "$source_file" ]; then
    sed -Ei "" 's/\.(scan_code|load_module)\(/._\1(/g' "$source_file"
    echo "patched python module: $source_file" 1>&2
else
    echo "cannot locate python module: $pymodule" 1>&2
    exit 1
fi
