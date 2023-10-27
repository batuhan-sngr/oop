import os
import time
import threading
import ast
import re
import sys

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


class FolderMonitor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.files = {}
        self.snapshot_time = 0
        self.last_modified = 0  
        self.log = []
        self.exit_flag = False 
        self.monitoring_thread = None
        self.log_file = "status_log.txt"
        self.previous_files = set()

    def add_file(self, filename, file_obj):
        self.files[filename] = file_obj

    def scan_folder(self):
        for root, _, files in os.walk(self.folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                if filename.endswith(".txt"):
                    self.files[filename] = TextFile(file_path)
                elif filename.endswith((".png", ".jpg")):
                    self.files[filename] = ImageFile(file_path)
                elif filename.endswith(".py"):
                    self.files[filename] = ProgramFile(file_path)
                elif filename.endswith(".java"):
                    self.files[filename] = ProgramFile(file_path)

    def commit_all(self):
        self.snapshot_time = time.strftime("%Y-%m-d, %H:%M:%S")
        for file in self.files.values():
            file.commit()
    
    def commit(self):
        # Check if the file exists
        if os.path.exists(self.filename):
            # Update the snapshot time to the current time
            self.snapshot_time = time.strftime("%Y-%m-%d, %H:%M:%S")
            # Update the last modified time
            self.last_modified = os.path.getmtime(self.filename)
        else:
            print(f"File '{self.filename}' does not exist.")

    def info(self):
        # Check if the file exists
        if os.path.exists(self.filename):
            # Update the last modified time
            self.last_modified = os.path.getmtime(self.filename)
            file_info = super().info()
            # Include file creation and last modified times in the info
            created_time = time.ctime(os.path.getctime(self.filename))
            modified_time = time.ctime(self.last_modified)
            return f"{file_info} - Created: {created_time}, Last Modified: {modified_time}"
        else:
            return f"File '{self.filename}' does not exist."

    def has_changed(self):
        if os.path.exists(self.filename):
            current_modified = os.path.getmtime(self.filename)
            return current_modified > self.last_modified
        return False

    def status(self):
        current_files = set(self.files.keys())
        changes = []

        # Check for added files
        added_files = current_files - self.previous_files
        for filename in added_files:
            changes.append(f"{filename} was added at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Check for deleted files
        deleted_files = self.previous_files - current_files
        for filename in deleted_files:
            changes.append(f"{filename} was deleted at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        for filename, file_obj in self.files.items():
            if file_obj.has_changed():
                changes.append(f"{file_obj.filename} has changed since the snapshot time of {file_obj.snapshot_time}")

        # Update the previous list of files
        self.previous_files = current_files

        # Write the status to the log file
        with open(self.log_file, "a") as log:
            log.write("\n".join(changes))
        
        if changes:
            print("\n".join(changes))
        else:
            print("No changes since the last snapshot.")

    def run_monitor(self):
        while not self.exit_flag:
            self.check_for_changes()
            time.sleep(5)

    def main_loop(self):
        try:
            while not self.exit_flag:
                user_input = input("Enter 'commit', 'info <filename>', 'status', or 'exit': ")
                if user_input.startswith("commit"):
                    self.commit_all()
                elif user_input.startswith("info"):
                    _, filename = user_input.split(" ", 1)
                    if filename in self.files:
                        file = self.files[filename]
                        print(file.info())
                    else:
                        print("File not found.")
                elif user_input == "status":
                    self.status()
                elif user_input == "exit":
                    self.exit_flag = True
                    self.monitoring_thread.join()
                    sys.exit(0)
                    break  # Exit the main loop
                else:
                    print("Invalid command.")
        except KeyboardInterrupt:
            pass  # Handle Ctrl+C gracefully
    def check_for_changes(self):
        while not self.exit_flag:
            time.sleep(5)  # Schedule to run every 5 seconds

            # Capture the current state of the folder
            current_files = set(os.listdir(self.folder_path))

            # Check for new files
            new_files = current_files - set(self.files.keys())
            for filename in new_files:
                if filename.endswith(".txt"):
                    self.add_file(filename, TextFile(os.path.join(self.folder_path, filename)))
                elif filename.endswith((".png", ".jpg")):
                    self.add_file(filename, ImageFile(os.path.join(self.folder_path, filename)))
                elif filename.endswith(".py"):
                    self.add_file(filename, ProgramFile(os.path.join(self.folder_path, filename)))
                elif filename.endswith(".java"):
                    self.add_file(filename, ProgramFile(os.path.join(self.folder_path, filename)))
                self.log.append(f"{filename} is a new file.")

            # Check for deleted files
            deleted_files = set(self.files.keys()) - current_files
            for filename in deleted_files:
                self.log.append(f"{filename} was deleted since the last snapshot.")
                del self.files[filename]

if __name__ == '__main__':
    folder_path = 'D:/Documents/OOP/oop3'  # Replace with the actual folder path
    monitor = FolderMonitor(folder_path)

    # Initial folder scan
    monitor.scan_folder()

    # Start monitoring and detecting changes in a separate thread
    monitoring_thread = threading.Thread(target=monitor.run_monitor)
    monitor.monitoring_thread = monitoring_thread
    monitoring_thread.start()

    # Main loop for user input
    monitor.main_loop()
