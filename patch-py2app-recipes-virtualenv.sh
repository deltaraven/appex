#!/bin/sh

# Copyright (c) 2015, Joel Miller <joel@deltaraven.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


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
