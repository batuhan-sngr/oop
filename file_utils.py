import os
import time
import ast
import re

class File:
    def __init__(self, filename):
        self.filename = filename
        self.snapshot_time = 0
        self.last_modified = os.path.getmtime(filename)

    def commit(self):
        self.snapshot_time = time.strftime("%Y-%m-%d, %H:%M:%S")
        self.last_modified = os.path.getmtime(self.filename)

    def info(self):
        return f"{self.filename} - Created: {time.ctime(os.path.getctime(self.filename))}, Last Modified: {time.ctime(self.last_modified)}"

    def has_changed(self):
        current_last_modified = os.path.getmtime(self.filename)
        return current_last_modified != self.last_modified


class TextFile(File):
    def info(self):
        file_info = super().info()
        with open(self.filename, 'r') as file:
            content = file.read()
        line_count = len(content.splitlines())
        word_count = len(content.split())
        char_count = len(content)
        return f"{file_info}\nLine count: {line_count}, Word count: {word_count}, Character count: {char_count}"

class ImageFile(File):
    def info(self):
        file_info = super().info()
        image_info = self.get_image_info()
        return f"{file_info}\n{image_info}"

    def get_image_info(self):
        try:
            with open(self.filename, 'rb') as f:
                f.seek(0, 2)
                size = f.tell()

            with open(self.filename, 'rb') as f:
                header = f.read(30)  # Read the header to extract image dimensions
                if header.startswith(b'\x89PNG\r\n\x1a\n'):  # Check if it's a PNG file
                    width = int.from_bytes(header[16:20], byteorder='big')
                    height = int.from_bytes(header[20:24], byteorder='big')
                    return f"Image Size: {width}x{height}, File Size: {size} bytes (PNG)"
                elif header.startswith(b'\xff\xd8\xff\xe0\x00\x10JFIF'):  # Check if it's a JPEG file
                    f.seek(163)  # Jump to the beginning of the dimensions info
                    height = int.from_bytes(f.read(2), byteorder='big')
                    width = int.from_bytes(f.read(2), byteorder='big')
                    return f"Image Size: {width}x{height}, File Size: {size} bytes (JPEG)"
                else:
                    return f"File Size: {size} bytes"
        except Exception as e:
            return f"Error: {str(e)}"
class ProgramFile(File):
    def info(self):
        file_info = super().info()
        program_info = self.get_program_info()
        return f"{file_info}\n{program_info}"

    def get_program_info(self):
        try:
            with open(self.filename, 'r') as file:
                content = file.read()

            if self.filename.endswith(".py"):
                tree = ast.parse(content)
                line_count = len(content.split('\n'))
                class_count = 0
                method_count = 0

                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        class_count += 1
                    elif isinstance(node, ast.FunctionDef):
                        method_count += 1

                return f"Line count: {line_count}, Class count: {class_count}, Method count: {method_count}"
            elif self.filename.endswith((".java", ".jav")):
                line_count = self.count_lines()
                class_count = self.count_classes()
                method_count = self.count_methods()

                return f"Line count: {line_count}, Class count: {class_count}, Method count: {method_count}"
            else:
                return "File type not supported"

        except Exception as e:
            return f"Error: {str(e)}"

    def count_lines(self):
        with open(self.filename, 'r') as java_file:
            return sum(1 for line in java_file)

    def count_classes(self):
        with open(self.filename, 'r') as java_file:
            class_pattern = re.compile(r'\bclass\b')
            return len(class_pattern.findall(java_file.read()))

    def count_methods(self):
        with open(self.filename, 'r') as java_file:
            method_pattern = re.compile(r'\b\w+\s+\w+\(.*\)\s*{')
            return len(method_pattern.findall(java_file.read()))

