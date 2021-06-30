#!/bin/bash

set -e
cp src/optexcount.py src/__main__.py
zip -j optexcount.zip src/*.py 1> /dev/null
echo '#!/usr/bin/env python3' | cat - optexcount.zip > optexcount
chmod +x optexcount
rm optexcount.zip src/__main__.py
mv optexcount /usr/bin/optexcount
echo 'OpTeXcount successfully installed!'