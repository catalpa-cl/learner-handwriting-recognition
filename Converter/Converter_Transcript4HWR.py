"""
Converter_Transcript4HWR.py

Author: Christian Gold
Date: June, 2023

Description: This file contains Python code that accomplishes a specific purpose.
It serves as an implementation for the conversion from the handwritten transcriptions into a line-wise,
raw text for Handwriting Recognition.

For more details, please refer to the accompanying paper titled:

Preserving the Authenticity of Handwritten Learner Language:
Annotation Guidelines for Creating Transcripts Retaining Orthographic Features.
by Christian Gold, Ronja Laarmann-Quante, Torsten Zesch
at 1st Computation and Written Language (CAWL) Workshop at ACL. 2023

"""

#standard import
import argparse
import os

#additional library:
import pyparsing

# replace the first character with the second character of tuple to reduce the number of characters
replacement_chars = [["‘", "'"],
                     ['“', '"'],
                     ['”', '"'],
                     ['_', '-'],
                     ['…', '...'],
                     ['→', '>'],
                     ['€', 'E']]

word_chars = "'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzäöüÄÖÜß"

#global variables for meta analysis:
dictionary = []
charlist = ''
char_occ = []


def get_file_paths(input_path, output_path, file_ext):
    """
        Get the list of input and output file paths based on the input path and output path.

        Args:
            input_path (str): Path to the input file or folder.
            output_path (str): Path to the output file or folder.
            file_ext (str): The desired file extension.

        Returns:
            list_files_input_paths (list): List of input file paths.
            list_files_output_paths (list): List of output file paths.

        Description:
        - This function takes the input path, output path, and file extension as parameters.
        - It checks the input path and output path to determine if they are a file or folder.
        - If the input path is a folder and the output path is a folder, it creates the output folder if it doesn't exist.
        - It retrieves the list of input file paths and corresponding output file paths based on the file extension.
        - If the input path is a file and the output path is a file, it performs validity checks on the file extensions.
        - It returns the list of input file paths and output file paths.

        Raises:
            ValueError: If the input or output file format is invalid.
            FileNotFoundError: If the input path is not found.

        """
    list_files_input_paths = []
    list_files_output_paths = []

    # Create the output folder if it doesn't exist
    if os.path.isdir(input_path):
        if not os.path.isfile(output_path):
            if not os.path.exists(output_path):
                os.makedirs(output_path)
                os.makedirs(output_path+'/metadata')

            for root, dirs, files in os.walk(input_path):
                list_files_input_paths += [os.path.join(root, file) for file in files if file.endswith(file_ext)]

                if len(list_files_input_paths) == 0:
                    raise ValueError('No .txt files found in the input folder.')

                list_files_output_paths += [os.path.join(output_path + os.path.basename(file))
                                            for file in files if file.endswith(file_ext)]

        else:
            raise FileNotFoundError('According to the input, the output path should be a folder too.')

    else:
        if os.path.isfile(input_path):
            if not input_path.lower().endswith(file_ext):
                raise ValueError('Invalid input file format. Only .txt files are allowed.')

            if not output_path.lower().endswith(file_ext):
                raise ValueError('Invalid output file format. Only .txt files are allowed.')

            list_files_input_paths = [input_path]
            list_files_output_paths = [output_path]


    return list_files_input_paths, list_files_output_paths


def reduce_characters(text):
    """
    Reduce characters in the provided text based on the replacement_chars list.

    Args:
        text (str): The text to be processed.

    Returns:
        processed_text (str): The processed text with reduced characters.

    """
    processed_text = text
    for char, replacement in replacement_chars:
        processed_text = processed_text.replace(char, replacement)

    return processed_text


def meta_analyse(text):
    global charlist
    for word in text.split(' '):
        for char in word:
            if char not in word_chars:
                word = word.replace(char, '')
        if len(word) < 1:
            continue
        if word not in dictionary:
            dictionary.append(word)

    for i in range(len(text)):
        if text[i] not in charlist:
            charlist += text[i]
            char_occ.append(1)
        else:
            char_occ[charlist.find(text[i])] += 1

    return 0


def main(*args):
    """
    Main function for processing command-line arguments.

    """
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-i', '--input', help='Path to the input file or folder')
    parser.add_argument('-o', '--output', help='Path to the output file or folder')
    parser.add_argument('-r', '--reduce_chars', action='store_true', default=False, help='Whether to reduce characters by replace characters according to replacement_chars.')

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    global reduce_chars
    reduce_chars = args.reduce_chars

    #input_path = "src/test_data.txt"
    #output_path = "result/test_data_result_4HWR.txt"
    #reduce_chars = False

    files_input, files_output = get_file_paths(input_path, output_path, '.txt')

    # Process each file
    for idx, original_file_path in enumerate(files_input):
        with open(original_file_path, 'r') as input_file:
            # Read and process the file data
            original_lines = input_file.readlines()
            processed_lines = process_lines(original_lines)

        # Write the processed lines to the output file
        with open(files_output[idx], 'w') as output_file:
            for line in processed_lines:
                output_file.write(line)


def process_lines(original_lines):
    """
    Process the provided lines and return the processed lines.

    Args:
        lines (list): List of lines to be processed.

    Returns:
        processed_lines (list): List of processed lines.

    """
    global reduce_chars

    processed_lines = []

    max_len = 0
    open_flag = False

    for idx, line in enumerate(original_lines):
        if line.startswith('#'):
            processed_lines.append(line)
            continue

        # Remove the line break from the string:
        line = line.replace('\n', '')

        line_split = line.split('\t')

        # Filename #LineNumber #Status #Text #Comment
        if len(line_split) > 5:
            raise ValueError('Invalid input file format. More than 5 columns are present. \n'
                             'Please make sure only 4 or 5 columns are present and follow this order: '
                             'Filename \t LineNumber \t Status \t Text \t Comment. \n'
                             'Where the Comment column is the only optional.')

        original_text_line = line_split[3]


        if '{' in line_split[3]:
            line_split[3] = get_innerExpression(line_split[3])

        if '{insert' in line_split[3]:
            line_split[3] = line_split[3].replace('{insert', '')
            open_flag = True

        if '}' in line_split[3] and open_flag:
            open_flag = False
            line_split[3] = line_split[3].replace('}', '')

        if '{' in line_split[3] or '}' in line_split[3]:
            raise ValueError('Missed a { bracket in: ', line_split[3], line_split[0], line_split[1])

        if reduce_chars:
            line_split[3] = reduce_characters(line_split[3])

        #metadata:
        meta_analyse(line_split[3])

        str_to_print = ''
        for element in line_split:
            str_to_print += element + '\t'

        str_to_print = str_to_print[:-1]
        str_to_print += '\n'

        processed_line = '\t'.join(line_split) + '\n'
        processed_lines.append(processed_line)

    return processed_lines


def get_innerExpression(text):
    elements = pyparsing.originalTextFor(pyparsing.nestedExpr('{', '}')).searchString(text)
    for element in elements:
        if '{' in element[0]:
            result = replace_innerExpression(get_innerExpression(element[0][1:-1]))
            loc = text.find(element[0])
            bis = loc+len(element[0])+1
            text = text[:loc] + text[loc:bis].replace(element[0], result) + text[bis:]

    return text


def replace_innerExpression(text):
    if len(text) == 0:
        print('invalid text length: zero')
        return text
    if len(text) == 1:
        if text[0] in word_chars:
            #global ctr_unclear_characters
            #ctr_unclear_characters += 1
            return text

    # remove emoticon
    if '🙂' in text:
        text = text.replace('🙂', '')
        #global ctr_emoji
        #ctr_emoji += 1
        return text

    # '-' Trennzeichen >>> space
    if text[0] == '-':
        text = ' ' + text[1:]
        #global ctr_separator
        #ctr_separator += 1
        return text

    # '<' direct insert
    if text[0] == '<':
        text = text[1:] #cutoff first char
        #global ctr_inserts_di
        #ctr_inserts_di += 1
        return text

    # '+' two characters, second the wrong one -> take first character
    # {e+E} <<< take 'e' only
    if len(text) > 1:
        if text[1] == '+':
            #global ctr_overlay
            #ctr_overlay += 1
            text = text.split('+')[0]
            return text

        # '|' -> mirrored
        if text[1] == '|':
            text = text[0]
            return text

        # '&' -> tally mark
        if text[1] == '&':
            text = text[0] #cutoff first char
            #global ctr_tally_marks
            #ctr_tally_marks += 1


        if text.startswith('insert'):
            if len(text) == 7:
                return ''
            #global ctr_inserts_indi
            #ctr_inserts_indi += 1
            text = text[8:]

    return text


if __name__ == '__main__':
    main()