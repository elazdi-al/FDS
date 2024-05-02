import re
import subprocess

def parse_latex_sections(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    
    sections = re.findall(r'\\section\{[^}]*Verilog[^}]*\}.*?(?=\\section|$)', content, flags=re.DOTALL)

    if not sections:
        print("No sections with 'Verilog' in their title were found.")
        return None

    
    verilog_chapter = "\n\\chapter{All of Verilog}\n"
    for section in sections:
        
        clean_section = re.sub(r'\\chapter\{[^}]*\}', '', section)  
        clean_section = re.sub(r'\\newpage', '', clean_section)  
        verilog_chapter += clean_section + "\n"

    
    end_document_pos = content.rfind('\\end{document}')
    if end_document_pos != -1:
        
        modified_content = content[:end_document_pos] + verilog_chapter + content[end_document_pos:]
    else:
        
        modified_content = content + verilog_chapter

    
    new_filename = 'modified_' + filename
    with open(new_filename, 'w', encoding='utf-8') as file:
        file.write(modified_content)

    return new_filename

def compile_latex_to_pdf(latex_file):
    try:
        
        result = subprocess.run(['pdflatex', latex_file], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Compilation successful, output written to PDF.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to compile LaTeX file. Error details:")
        print(e.stderr)

if __name__ == "__main__":
    modified_file = parse_latex_sections('fds.tex')
    if modified_file:
        compile_latex_to_pdf(modified_file)
    else:
        print("No modifications were made to the LaTeX file.")
