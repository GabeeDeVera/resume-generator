import yaml
import argparse
import subprocess
import time
import os
import shutil

# Parsing Arguments
parser = argparse.ArgumentParser(
    prog="Yaml Generator",
    description="Generates a redacted and regular version of a yml file to aid in feeding anonymized resumes to Gemini",
    epilog=""
)

parser.add_argument('filein', default="template_gen.yml") # first arg is filename
parser.add_argument('--yaml_out', default="compiler_artifacts/template.yml") # output yaml
parser.add_argument('--typst_in', default="imprecv_ntu/template.typ") # input typst file
parser.add_argument('--typst_out', default="compiler_artifacts/resume") # output typst file
parser.add_argument('-o', default="compiler_outputs/resume") # output file
parser.add_argument('--redact', action='store_true')
parser.add_argument('--disable_ocr', action='store_true')

args = parser.parse_args()

# Starting Diagnostic Timing
timing_start = time.perf_counter()

# Defining Extended YAML Semantics
g = {
    "DEFAULT_TOKEN": " -> ",
    "REDACT_TOKEN": "/ ",
    "KEYWORDS": {
        "REDACT_EMAIL": "example_email@gmail.com",
        "REDACT_LINK": "https://example.com",
        "REDACT_PHONE": "(+65) 91234567",
        "REDACT_USER": "ExampleHandle",
    }
}

# Transforms Reserved Keywords 
def transform_keyword(s):
    if(s in g["KEYWORDS"].keys()):
        return g["KEYWORDS"][s]
    else:
        return s

# Redacts a single string value
def redact_str(s, redact, p_obj_type, ind=-1, key=""):
    tokens = s.split(g["DEFAULT_TOKEN"])

    if(not redact):
        return transform_keyword(tokens[0])
    elif(len(tokens) == 1):
        if(p_obj_type is list):
            return f"<ITEM {ind}>"
        else:
            return f"<{key.upper()}>"
    else:
        return transform_keyword(tokens[1])
            
# Recursively redacts YAML data
def redact_inplace(obj, redact):
    # if(type)
    if(type(obj) is dict):
        for [k, v] in obj.items():
            if(type(v) is str):
                obj[k] = redact_str(v[2:], redact, dict, key=k) if v.startswith(g["REDACT_TOKEN"]) else v
            else:
                redact_inplace(v, redact)
    elif(type(obj) is list):
        for i in range(len(obj)):
            if(type(obj[i]) is str):
                obj[i] = redact_str(obj[i][2:], redact, list, ind=i) if obj[i].startswith(g["REDACT_TOKEN"]) else obj[i]
            else:
                redact_inplace(obj[i], redact)

# Creating directories for YAML post-processed output if they don't exist yet
os.makedirs(os.path.dirname(args.yaml_out), exist_ok=True)
with open(args.filein, 'r') as fin, open(args.yaml_out, 'w') as fout:
    # Preprocessing YAML and redacting if specified in args
    resume_data = yaml.safe_load(fin)

    redact_inplace(resume_data, args.redact)

    # Dumping processed YAML output
    yaml.dump(resume_data, fout)

    # Storing output file names and paths
    typst_out_fname = f"{args.typst_out}{'_redacted' if args.redact else ''}.pdf"
    pdf_out_fname = f"{args.o}{'_redacted' if args.redact else ''}.pdf"

    # Running Typst
    success = True
    try:
        os.makedirs(os.path.dirname(typst_out_fname), exist_ok=True)
        subprocess.run(f"typst compile {args.typst_in} {typst_out_fname} --pdf-standard a-3b --root=.", shell=True, check=True)
    except:
        print(f"COMPILATION FAIL")
        success = False

    # Running OCR Post-processor
    if(success):
        if(args.disable_ocr):
            # With OCR disabled, simply copy the intermediate output into the final output
            print("OCR disabled; directly generating output")

            try:
                os.makedirs(os.path.dirname(pdf_out_fname), exist_ok=True)
                shutil.copy(typst_out_fname, pdf_out_fname)
            except:
                print("PDF COPYING FAIL")
                success = False
        else:
            try:
                os.makedirs(os.path.dirname(pdf_out_fname), exist_ok=True)
                subprocess.run(f"ocrmypdf --output-type pdfa {typst_out_fname} {pdf_out_fname} --force-ocr --fast-web-view 0")
            except:
                print("OCR POST-PROCESS FAIL")
                success = False

    # Logging result of compilation
    if(success):
        print(f"Successfully generated resume (took {time.perf_counter() - timing_start:.2f} s)")
    else:
        print(f"Error generating resume (took {time.perf_counter() - timing_start:.2f} s)")