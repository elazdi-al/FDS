import subprocess
import os

def compile_latex_to_pdf(latex_file):
    if not os.path.exists(latex_file):
        print("The specified LaTeX file does not exist.")
        return

    # Setting up the command and arguments for pdflatex
    command = ["pdflatex",
               "-shell-escape",        # Allows running external commands; be cautious with untrusted inputs
               "-synctex=1",           # Enables SyncTeX
               "-interaction=nonstopmode",  # Continues compilation even when errors occur
               "-file-line-error",     # Shows errors in the format 'file:line:error' which is easier to debug
               latex_file]             # The LaTeX file to compile

    try:
        # Execute the pdflatex command with the specified arguments
        result = subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Print outputs for debugging purposes
        print("STDOUT from pdflatex:")
        print(result.stdout)
        print("STDERR from pdflatex:")
        print(result.stderr)

        if result.returncode == 0:
            print("Compilation successful, output written to PDF.")
        else:
            print("pdflatex completed with errors.")

    except subprocess.CalledProcessError as e:
        # Catch errors specifically related to the subprocess
        print("Failed to compile LaTeX file.")
        print(f"Error message: {e}")
    except Exception as e:
        # General exception handling for other unforeseen errors
        print("An error occurred.")
        print(str(e))

