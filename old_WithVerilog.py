import re
import subprocess
from multiprocessing import Pool
from threading import Thread

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def find_sections(content):
    return re.findall(r'\\section\{[^}]*Verilog[^}]*\}.*?(?=\\section|$)', content, flags=re.DOTALL)

def clean_section(section):
    section = re.sub(r'\\chapter\{[^}]*\}', '', section)
    section = re.sub(r'\\newpage', '', section)
    return section

def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def compile_latex_to_pdf(latex_file):
    try:
        result = subprocess.run(['pdflatex', latex_file], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Compilation successful, output written to PDF.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to compile LaTeX file. Error details:")
        print(e.stderr)

def main(filename):
    content = read_file(filename)
    sections = find_sections(content)
    
    if not sections:
        print("No sections with 'Verilog' in their title were found.")
        return

    with Pool(processes=4) as pool:
        cleaned_sections = pool.map(clean_section, sections)

    verilog_chapter = "\n\\chapter{All of Verilog}\n" + "\n".join(cleaned_sections)
    end_document_pos = content.rfind('\\end{document}')
    if end_document_pos != -1:
        modified_content = content[:end_document_pos] + verilog_chapter + content[end_document_pos:]
    else:
        modified_content = content + verilog_chapter

    new_filename = 'modified_' + filename
    t = Thread(target=write_file, args=(new_filename, modified_content))
    t.start()
    t.join()

    compile_latex_to_pdf(new_filename)

if __name__ == "__main__":
    main('fds.tex')
