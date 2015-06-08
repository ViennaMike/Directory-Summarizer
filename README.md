# Directory-Summarizer
Changes in this version (6/8/2015): Writes summaries to a single consolidated output file, rather than generating one summary file per document summarized. Easier to browse through this way. 

Summarizes all pdf, docx, and .txt files in a directory, recursively including sub-directories as well.

The purpose of this "summarizer" or "digester" script is to go through all files and sub-directories in the input source directory and automatically create a short summary of each .txt, .docs (Word), and .pdf file that it finds. The number of sentences to be provided in the summary is specified by the user, as is the target patha and file to write the consolidated summaries to. It also creates a list of all found Powerpoint (.ppt and .pptx) files that it finds, but it does not summarize them. 

The summary consists of the first line of the original text (which is often the title or 1st part of the title), a summary generated by sumy (see https://github.com/miso-belica/sumy and https://pypi.python.org/pypi/sumy/0.3.0) and the original path to the file, starting at the user specified root. 

One of its intended uses is to generate automated summaries of all papers provided, for example, on a conference proceedings thumb drive. 

pdfminer (http://www.unixuser.org/~euske/python/pdfminer/and https://pypi.python.org/pypi/pdfminer/) is used for the pdf to text conversion.

