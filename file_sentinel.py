import os
import shutil
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
# UPDATE THIS PATH to your actual Downloads folder
SOURCE_DIR = r"C:\Users\samael\Downloads" 

# Destination Categories
DEST_DIRS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx", ".csv"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Video": [".mp4", ".mkv", ".mov", ".avi"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".msi"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".c", ".java"]
}

class SentinelHandler(FileSystemEventHandler):
    """The 'Brain' of the operation. Reacts to file system events."""
    
    def on_created(self, event):
        # We only care about files, not folders
        if event.is_directory:
            return
        
        # Adding a small delay to ensure file write is complete (crucial for large downloads)
        time.sleep(1)
        self.sort_file(event.src_path)

    def sort_file(self, file_path):
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        ext = ext.lower()

        # Logic: Find the correct silo for the extension
        moved = False
        for category, extensions in DEST_DIRS.items():
            if ext in extensions:
                target_folder = os.path.join(SOURCE_DIR, category)
                self.move_to_target(file_path, target_folder)
                moved = True
                break
        
        if not moved:
            logging.info(f"Skipped: {filename} (Unknown extension)")

    def move_to_target(self, file_path, target_folder):
        # Ensure target directory exists
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            logging.info(f"Created directory: {target_folder}")

        # Handle duplicate filenames
        filename = os.path.basename(file_path)
        destination_path = os.path.join(target_folder, filename)
        
        counter = 1
        while os.path.exists(destination_path):
            name, ext = os.path.splitext(filename)
            destination_path = os.path.join(target_folder, f"{name}_{counter}{ext}")
            counter += 1

        try:
            shutil.move(file_path, destination_path)
            logging.info(f"MOVED: {filename} -> {target_folder}")
        except Exception as e:
            logging.error(f"Error moving {filename}: {e}")

if __name__ == "__main__":
    # Setup Logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    path = SOURCE_DIR
    event_handler = SentinelHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    
    logging.info(f"SENTINEL ACTIVE. Monitoring: {path}")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("SENTINEL DEACTIVATED.")
    
    observer.join()
