# -*- coding: utf-8 -*-
"""
Created on Thu Jun 04-06 21:24:16 2015

@author: Mike McGurrin
"""

# for sumy
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser # Keep in case add html later
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import os, os.path
import errno
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re

import pdf2txt
import docx2txt

# Safe opening whether or not path exists
# Taken from http://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    """ Create directory if needed"""
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')

def recursive_glob(rootdir='.', suffix=''):
    """ recursively traverses full path from route, returns
        paths and file names for files with given suffix """
    pathlist = []
    filelist = []
    for looproot,dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            if filename.endswith(suffix):
                pathlist.append(os.path.join(looproot, filename))
                filelist.append(filename)
    return pathlist, filelist
    
def use_sumy(input, SENTENCES_COUNT, method, parser_option):
    """Code to run sumy
    # Supported summarization methods:
    #    Luhn - heurestic method, reference
    #    Edmundson heurestic method with previous statistic research, reference
    #    Latent Semantic Analysis, LSA - one of the algorithm from http://scholar.google.com/citations?user=0fTuW_YAAAAJ&hl=en I think the author is using more advanced algorithms now. Steinberger, J. a Ježek, K. Using latent semantic an and summary evaluation. In In Proceedings ISIM '04. 2004. S. 93-100.
    #    LexRank - Unsupervised approach inspired by algorithms PageRank and HITS, reference
    #    TextRank - some sort of combination of a few resources that I found on the internet. I really don't remember the sources. Probably Wikipedia and some papers in 1st page of Google :)"""
    LANGUAGE = "english"
    #parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    if parser_option == 'file':
        parser = PlaintextParser.from_file(input, Tokenizer(LANGUAGE))
    elif parser_option == 'string':
        parser = PlaintextParser.from_string(input, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    summary = []
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        summary.append(sentence)
    return summary

def summarize_save(text, length, destination):   
    """ summarized text string and saves in appropriate file"""
    possible_title = text.split('\n')[0]
    file_name = (possible_title[:25]) if len(possible_title) > 25 else possible_title
    # make sure character OK for file name:
    regex = re.compile('[^a-zA-Z]')
    #First parameter is the replacement, second parameter is your input string
    file_name = regex.sub('', file_name) + '.txt'    
#    for index, char in enumerate(file_name):
#        if char not in string.letters:
#            file_name = file_name[: index] + file_name[index+1 :]

    summary = use_sumy(text, length, 'textrank', 'string')
    with safe_open_w(destination+file_name) as f:
        f.writelines('Possible Title: '+possible_title+'\n\n')
        for line in summary:
            f.writelines(str(line)+'\n')
        f.writelines('\nfile path: ' + path)
        f.close()
 
startpath = raw_input("starting path for search: ")  
destination = raw_input("path to store summaries: ")
length = raw_input("how many sentences in each summary?")

# Get paths and file names for supported document types
pdf_paths, pdf_files = recursive_glob(startpath, '.pdf')
txt_paths, txt_files = recursive_glob(startpath, '.txt')
docx_paths, docx_files = recursive_glob(startpath, '.docx')
html_paths, html_files = recursive_glob(startpath, '.htm')
more_html_paths, more_html_files = recursive_glob(startpath, '.html')
for item in more_html_paths: html_paths.append(item)
for item in more_html_files: html_files.append(item)
    
# Doesn't summarize powerpoint, but creates list
pptx_paths, pptx_files = recursive_glob(startpath, '.pptx')
more_pptx_paths, more_pptx_files = recursive_glob(startpath, '.ppt')
for item in more_pptx_paths: pptx_paths.append(item)
for item in more_pptx_files: pptx_files.append(item)
    
# Process Powerpoint files
with safe_open_w(destination+'PowerpointFiles.txt') as f:
    for path in pptx_paths:
        f.writelines('Presentation: '+path+'\n\n')
    f.close()
    
# Process pdf files
for idx, path in enumerate(pdf_paths):
    path = pdf_paths[idx]
    full_text = pdf2txt.convert_pdf_to_txt(path)
    summarize_save(full_text, length, destination) 
 
# Process text files
for idx, path in enumerate(txt_paths):
    path = txt_paths[idx]
    with open(path, 'r') as fp:
        full_text = fp.read
    
    summarize_save(full_text, length, destination)    
    
 # Process docx Word files
for idx, path in enumerate(docx_paths):
    path = docx_paths[idx]
#    with open(path, 'r') as fp:
#        full_text = fp.read
    full_text = docx2txt.get_docx_text(path)
    summarize_save(full_text, length, destination) 