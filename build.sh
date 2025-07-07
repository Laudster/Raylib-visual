DIR="$1"
OUTPUT_DIR="${DIR}/web-build"
SOURCE_FILE="${DIR}/project_file.c"
RAYLIB_PATH="/home/dependencies/raylib" # Adjust if raylib is somewhere else

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