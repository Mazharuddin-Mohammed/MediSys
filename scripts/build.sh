#!/bin/bash
mkdir -p build
cd build
cmake ..
make -j$(nproc)
cd ..
cppcheck --enable=all src/backend
pylint src/frontend/python