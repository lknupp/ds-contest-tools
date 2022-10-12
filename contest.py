from latexutils import clean_auxiliary_files
from pdfutils import build_pdf, merge_pdfs
from boca import boca_pack
from utils import convert_idx_to_string
import sys
import os
import argparse
import shutil


def create_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-b', '--boca', action='store_true',
                        default=False, help='build problems in BOCA format.')
    parser.add_argument('mode', choices=['build', 'genpdf'], 
        help='build: create a contest.\n' +
        'genpdf: generates problem and tutorial PDFs.\n')
    parser.add_argument('problems_folder', help='problems directory.')
    parser.add_argument('contest_folder', help='directory which the contest will be saved.')
    return parser


"""
Builds a contest pdf from the PDFs from the list of problems
"""


def build_contest_pdf(problem_folder_l, output_folder):
    print('-Creating contest PDF')
    problem_pdf_l = []
    tutorial_pdf_l = []

    cls_file = os.path.join(os.path.dirname(__file__), 'arquivos')
    cls_file = os.path.join(cls_file, 'maratona.cls')
    shutil.copy(cls_file, output_folder)

    for i, folder in enumerate(problem_folder_l):
        label = convert_idx_to_string(i)
        options = {'display_author': False,
                   'problem_label': label}
        build_pdf(folder, output_folder, options)
        basename = os.path.basename(folder)
        problem_pdf_l.append(os.path.join(output_folder, basename+'.pdf'))
        tutorial_pdf_l.append(os.path.join(
            output_folder, basename+'-tutorial.pdf'))
    clean_auxiliary_files(output_folder)
    merge_pdf = os.path.join(output_folder, 'maratona.pdf')
    merge_tutorial_pdf = os.path.join(output_folder, 'tutoriais.pdf')
    merge_pdfs(problem_pdf_l, merge_pdf)
    merge_pdfs(tutorial_pdf_l, merge_tutorial_pdf)
    for f in problem_pdf_l:
        os.remove(f)
    for f in tutorial_pdf_l:
        os.remove(f)
    os.remove(os.path.join(output_folder, 'maratona.cls'))


"""
Builds BOCA packages from the list of problems
"""


def build_boca_packages(problem_folder_l, output_folder):
    print('-Creating BOCA Files')
    for i, folder in enumerate(problem_folder_l):
        label = convert_idx_to_string(i)
        options = {'display_author': False,
                   'problem_label': label}
        build_pdf(folder, folder, options)
        # build_checker(folder)
        boca_pack(folder)
        boca_file_path = os.path.join(folder, 'boca.zip')
        boca_file = os.path.join(output_folder, os.path.basename(folder) + '-boca.zip')
        shutil.copy(boca_file_path, boca_file)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    if not os.path.isdir(args.problems_folder):
        print(args.problems_folder + ' is not a valid directory')
        sys.exit(1)

    problems = []
    for f in os.listdir(args.problems_folder):
        problems.append(os.path.join(args.problems_folder, f))
    
    os.makedirs(args.contest_folder, exist_ok=True)

    if (args.mode == 'build' and args.boca):
        build_boca_packages(problems, args.contest_folder)
        build_contest_pdf(problems, args.contest_folder)
    elif (args.mode == 'build'):
        build_contest_pdf(problems, args.contest_folder)
    elif (args.mode == 'genpdf'):
        build_contest_pdf(problems, args.contest_folder)

