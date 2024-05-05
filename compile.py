import subprocess
def compile_latex_to_pdf(latex_file):
    try:
        print(latex_file)
        subprocess.run(["pdflatex", latex_file], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Compilation successful, output written to PDF.")
        
    except:
        print("Failed to compile LaTeX file. Error details:")
