import os
import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def parse_latex_document(latex_file_path):
    # Initialize the counters for chapter, section, subsection, and subsubsection
    chapter_counter = 0
    section_counter = 0
    subsection_counter = 0
    subsubsection_counter = 0
    
    # Compile regular expressions to match only numbered chapters, sections, subsections, and subsubsections
    chapter_pattern = re.compile(r'^\\chapter(?!\*)')
    section_pattern = re.compile(r'^\\section(?!\*)')
    subsection_pattern = re.compile(r'^\\subsection(?!\*)')
    subsubsection_pattern = re.compile(r'^\\subsubsection(?!\*)')
    
    with open(latex_file_path, 'r') as file:
        for line in file.readlines():
            if chapter_pattern.search(line):
                chapter_counter += 1
                section_counter = 0
                subsection_counter = 0
                subsubsection_counter = 0
            elif section_pattern.search(line):
                section_counter += 1
                subsection_counter = 0
                subsubsection_counter = 0
            elif subsection_pattern.search(line):
                subsection_counter += 1
                subsubsection_counter = 0
            elif subsubsection_pattern.search(line):
                subsubsection_counter += 1

    chapter_sectioning_str = f"{chapter_counter}.{section_counter if section_counter > 0 else '0'}.{subsection_counter if subsection_counter > 0 else '0'}"
    return chapter_sectioning_str

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.check_and_rename_file(event.src_path)
    def check_and_rename_file(self, file_path):
        pattern = r"^(\d+)\.(\d+)(\.(\d+))?(_(\d+))?\.(jpg|jpeg|png|gif)$"
        if not re.match(pattern, os.path.basename(file_path)):
            latest_sectioning = parse_latex_document('FDS.tex')
            extension = file_path.split('.')[-1]
            new_name = f"{latest_sectioning}.{extension}"
            new_path = os.path.join(os.path.dirname(file_path), new_name)
            # Check if file exists before attempting to rename
            if os.path.exists(file_path):
                try:
                    os.rename(file_path, new_path)
                    print(f"Renamed '{file_path}' to '{new_path}'")
                except FileNotFoundError as e:
                    print(f"Failed to rename {file_path} to {new_path}: {e}")
            else:
                print(f"File {file_path} does not exist, skipping.")

def start_watching(folder_path):
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist. Creating it now.")
        os.makedirs(folder_path, exist_ok=True)
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Example usage
folder_path = './circuits'
start_watching(folder_path)
