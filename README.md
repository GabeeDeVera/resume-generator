# Gabee's Resume Generator

A version control system and build tool for my resume.

This repository contains the *public-facing* code for my resume generator. In particular, details that fall under some form of NDA have been redacted. This repository is purely for demonstration purposes.

See the sample output resume [here](resume/compiler_outputs/resume.pdf). See the redacted resume [here](resume/compiler_outputs/resume_redacted.pdf).

I use jskherman's [imprecv](https://github.com/jskherman/imprecv), customized to match the formatting standards of the Nanyang Technological University (NTU) Community Template.

Like imprecv, this resume generator uses YAML to facilitate version control. I have added YAML post-processors to facilitate information redaction for feeding into LLMs or other online systems for automated feedback. Hence, the YAML used to write the resume is a modified version from the original that enables polymorphic compilation results.

Further, to make the resumes more ATS-friendly, I have added an OCR post-processing layer. Note that `compile.ps1` currently has this OCR post-processing set to false.

## Writing and Compiling a Resume

To write a resume, go to `resume > resume_data` and create a new `yml` file. You may use the provided example resume as reference.

The compilation procedure may depend on your system and shell. For a windows system, one may compile with PowerShell as follows:

To compile a resume, edit the `$infile` variable in `resume > compile.ps1` and `resume > compile_redacted.ps1`. Then, `cd` into the `resume` folder. Run `./compile.ps1` to compile the resume normally. Run `./compile_redacted.ps1` to compile the resume, redacting any personal information.

If you use a different shell, you may edit the `.ps1` file (eg., if you use bash, you may convert the `.ps1` files to their `.sh` equivalents). Follow the compilation format of `yml_generator.py`.

## Limitations

Currently, the resume post-processor overlays an invisible layer of text on top of Typst's generated raster image. NTU VMock (a system for checking resume quality) currently complains that the color of the text is not black. This most likely won't be an issue though, as most ATS would not care about the color of the resume. The font still appears black in the generated raster image.

Further, by overlaying a text layer, it seems that the clickable links Typst generates are lost.