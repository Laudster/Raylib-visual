#!/bin/bash

<<<<<<< HEAD
# Set the directory passed as the argument
DIR="$1"
OUTPUT_DIR="$DIR/web-build"
SOURCE_FILE="$DIR/project_file.c"

# Run the emcc command
emcc -o "$OUTPUT_DIR/project.html" "$SOURCE_FILE" -Wall -std=c99 \
    -D_DEFAULT_SOURCE -Wno-missing-braces -Wunused-result -Os -I. \
    -I C:/raylib/raylib/src -I C:/raylib/raylib/src/external -L. \
    -L C:/raylib/raylib/src -s USE_GLFW=3 -s ASYNCIFY -s TOTAL_MEMORY=67108864 \
    -s FORCE_FILESYSTEM=1 --preload-file sounds \
    --shell-file C:/raylib/raylib/src/shell.html \
    C:/raylib/raylib/src/web/libraylib.a -DPLATFORM_WEB \
    -s "EXPORTED_FUNCTIONS=[_free,_malloc,_main]" \
    -s EXPORTED_RUNTIME_METHODS=ccall
=======
# The script is now called with /app as the argument within Docker
DIR="$1"
OUTPUT_DIR="${DIR}/web-build"
SOURCE_FILE="${DIR}/project_file.c"

# Adjust these paths to where raylib is located INSIDE THE DOCKER CONTAINER
# You might need to copy raylib into the builder stage or mount it.
# For simplicity, let's assume raylib is also copied to /app/raylib
RAYLIB_PATH="raylib" # Adjust if raylib is somewhere else

echo "Starting Emscripten compilation..."
echo "Source: ${SOURCE_FILE}"
echo "Output: ${OUTPUT_DIR}/project.html"

# Create the output directory if it doesn't exist
mkdir -p "${OUTPUT_DIR}"

emcc -o "${OUTPUT_DIR}/project.html" \
  "${SOURCE_FILE}" \
  -Wall \
  -std=c99 \
  -D_DEFAULT_SOURCE \
  -Wno-missing-braces \
  -Wunused-result \
  -Os \
  -I. \
  -I "${RAYLIB_PATH}/src" \
  -I "${RAYLIB_PATH}/src/external" \
  -L. \
  -L "${RAYLIB_PATH}/src" \
  -s USE_GLFW=3 \
  -s ASYNCIFY \
  -s TOTAL_MEMORY=67108864 \
  -s FORCE_FILESYSTEM=1 \
  --shell-file "${RAYLIB_PATH}/src/shell.html" \
  "${RAYLIB_PATH}/src/web/libraylib.web.a" \
  -DPLATFORM_WEB \
  -s "EXPORTED_FUNCTIONS=[_free,_malloc,_main]" \
  -s EXPORTED_RUNTIME_METHODS=ccall

if [ $? -eq 0 ]; then
    echo "Emscripten compilation successful!"
else
    echo "Emscripten compilation failed!"
    exit 1
fi
>>>>>>> origin/main
