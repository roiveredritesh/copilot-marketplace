#!/usr/bin/env bash
# Windows passes this path with backslashes; normalize before taking the dirname.
d=${BASH_SOURCE[0]//\\//}
bash "${d%/*}/../_fixture/shop.sh"
