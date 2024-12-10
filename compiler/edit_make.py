import os, sys, ctypes, json

with open("Makefile copy", "r") as file_read:
    lines = file_read.readlines()

    for i, v in enumerate(lines):
        if "Define target platform" in v:
            lines[i+1] = "PLATFORM             ?= PLATFORM_WEB\n"
        if "RAYLIB_RELEASE_PATH  ?= $(RAYLIB_SRC_PATH)" in v:
            lines[i] = "RAYLIB_RELEASE_PATH  ?= $(RAYLIB_SRC_PATH)/web\n"
    
    with open("Makefile copy", "w") as file_edit:
        file_edit.writelines(lines)