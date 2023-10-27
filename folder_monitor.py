import os
import time
import threading
import sys
from file_utils import TextFile, ImageFile, ProgramFile

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
        self.log_lock = threading.Lock() 

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
    
    def run_log_updater(self):
        while not self.exit_flag:
            self.update_status_log()
            time.sleep(5)
    
    def update_status_log(self):
        # Capture the current state of the folder
        current_files = set(os.listdir(self.folder_path))

        # Check for added files
        new_files = current_files - set(self.files.keys())
        for filename in new_files:
            if filename.endswith(".txt"):
                self.add_file(filename, TextFile(os.path.join(self.folder_path, filename)))
            elif filename.endswith((".png", ".jpg")):
                self.add_file(filename, ImageFile(os.path.join(self.folder_path, filename)))
            elif filename.endswith((".py", ".java")):
                self.add_file(filename, ProgramFile(os.path.join(self.folder_path, filename)))
            self.log.append(f"{filename} was added at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Check for deleted files
        deleted_files = set(self.files.keys()) - current_files
        for filename in deleted_files:
            self.log.append(f"{filename} was deleted at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            del self.files[filename]

        # Write changes to the log file
        with self.log_lock:
            with open(self.log_file, "a") as log:
                log.write("\n".join(self.log))
                log.write("\n")
    
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
    folder_path = 'D:/Documents/OOP/oop3/oop'  # Replace with the actual folder path
    monitor = FolderMonitor(folder_path)

    # Initial folder scan
    monitor.scan_folder()

    # Start monitoring and detecting changes in a separate thread
    monitoring_thread = threading.Thread(target=monitor.run_monitor)
    log_updater_thread = threading.Thread(target=monitor.run_log_updater)
    monitor.monitoring_thread = monitoring_thread
    monitor.log_updater_thread = log_updater_thread
    monitoring_thread.start()
    log_updater_thread.start()

    # Main loop for user input
    monitor.main_loop()