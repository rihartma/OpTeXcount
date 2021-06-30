#!/bin/bash

set -e
mv src/optexcount.py src/__main__.py
zip -j optexcount.zip src/*.py
echo '#!/usr/bin/env python3' | cat - optexcount.zip > optexcount
chmod +x optexcount
mv src/__main__.py src/optexcount.py
rm optexcount.zip
mv optexcount /usr/bin/optexcount