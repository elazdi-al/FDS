import subprocess
def compile_latex_to_pdf(latex_file):
    try:
        result = subprocess.run(["pdflatex", latex_file], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Compilation successful, output written to PDF.")
        print(result.stdout)
    except:
        print("Failed to compile LaTeX file. Error details:")
