"""An Air-Race Game Testing Script

This script is supplied so that you can test your code against the supplied test cases.

Instructions:
    1. Place this file in the same directory as your Python script (e.g., SU12345678.py)
    2. Place a folder called `supplied_test_cases` in the same directory as your Python script (e.g., SU12345678.py).
    3. Inside the `supplied_test_cases` folder, place the test cases (e.g., 1_input.txt, 1_output.txt, 2_input.txt, 2_output.txt, etc.)
    4. Run this script (e.g., `python diff_checker.py`)

Basic Usage:
Ensure the current directory contains this file, your Python script, and a folder called `supplied_test_cases` containing at least one test case's input and output files. To easily run this script, execute the following command:
    `python diff_checker.py [-s] [-w]`

The two optional arguments are: `-s` and `-w`. If you include `-s`, the output of the differencing script will be saved in the current directory. If you include `-w`, the script will open a web browser to display a side-by-side comparison of your program's output and expected output for each test case. If you include both `-s` and `-w`, both cases will apply.

After all test cases have been run, this script will produce a summary on how many of them passed and which of them failed, for example:
    Number of test cases passed: 1/ 2
        Test case 1: FAILED (2 mismatched lines)
        Test case 2: PASSED
"""
import os
import stdarray
import sys
import re
import subprocess
import difflib
import stdio
import webbrowser
import argparse

VERBOSE_MODE = False
SAVE_TESTING_SCRIPT_OUTPUT = False
SHOW_HTML_DIFF = False
PRINT_SIDE_BY_SIDE = False
MAX_LINE_MISMATCHES_PER_TEST_CASE = 10
TIMEOUT_DURATION = 10
SUPPLIED_TEST_CASES_DIR = os.path.join(os.getcwd(), "supplied_test_cases")
HTAB = " "*4

def get_supported_python_command(use_sys_executable=True):
    python_executable = sys.executable
    if use_sys_executable and python_executable is not None and len(python_executable) > 0:
        cmd_strings = [python_executable]
    else :
        cmd_strings = ['python', 'python3', 'py', 'python310']
        use_sys_executable = False
    code_s = "import sys; import stdio; import stdarray; my_input=stdio.readString(); "
    code_s += "x1=stdarray.create1D(2); osp=my_input+sys.argv[1]+str(len(x1)); stdio.write(osp.strip())"
    for cmd in cmd_strings:
        try:
            completed_sub = subprocess.run([cmd, "-c", code_s, "b"], capture_output=True, text=True, input='a', timeout=TIMEOUT_DURATION)
            if completed_sub.returncode != 0 and "ModuleNotFoundError" in completed_sub.stderr:
                not_found_module = completed_sub.stderr.split("ModuleNotFoundError: No module named '")[1].split("'")[0]
                print(f"Could not find module: {not_found_module}")
                termination(f"Please place the module's file {not_found_module}.py in the same directory as your SUxxxxxxxx.py script as a temporary fix.")
            elif completed_sub.returncode != 0:
                if VERBOSE_MODE:
                    print(f"Unknown Error: {completed_sub.stderr}")
            elif completed_sub.stdout == "ab2":
                return cmd
            else:
                if VERBOSE_MODE:
                    print(f"Unknown stdout: '{completed_sub.stdout}'")
                    print(f"\tstderr: '{completed_sub.stderr}'")
        except subprocess.TimeoutExpired:
            print(f"Timeout expired for command: {cmd} -c {code_s} b")
            print("This should not happen. Please contact Francois Nel at 19510748@sun.ac.za if you see this.")
            print("Please include the following information:")
        except subprocess.CalledProcessError as e:
            if VERBOSE_MODE:
                print(e)
        except FileNotFoundError as e:
            if VERBOSE_MODE:
                print(e)
        except Exception as e:
            if VERBOSE_MODE:
                print(e)
    if use_sys_executable:
        return get_supported_python_command(False)
    termination("Python command not found.")

class Marker(object):
    def __init__(self, student_number: str, test_case_ids: list):
        self.test_case_ids = list(set(test_case_ids))
        self.test_case_ids.sort()
        if len(self.test_case_ids) == 0:
            termination("No test cases found.")
        self.student_number = student_number
        self.python_script_path = os.path.join(os.getcwd(), f"SU{self.student_number}.py")
        ensure_paths_exist(self.python_script_path, self.test_case_ids)
        self.tmp_output_path = os.path.join(SUPPLIED_TEST_CASES_DIR, f"SU{student_number}_tmp_output.txt")
        self.number_of_test_cases = len(self.test_case_ids)
        self.number_of_test_cases_passed = 0
        self.number_of_test_cases_failed = 0
        self.test_case_mismatched_lines = {}
        self.test_case_exceptions = {}
        self.test_case_time_outs = {}
        self.all_output_lines = []
        self.html_output_strings = []
        for i in self.test_case_ids:
            self.test_case_mismatched_lines[i] = 0
            self.test_case_exceptions[i] = False
            self.test_case_time_outs[i] = False
        if_f_exists_delete(self.tmp_output_path)
        self.python_command = get_supported_python_command()

    def pr(self, s: str=''):
        print(s)
        self.all_output_lines.append(s)

    def mark(self):
        for i in self.test_case_ids:
            self.__mark_test_case(i)
        self.pr("\nSummary:")
        self.pr(f"Number of test cases passed: {self.number_of_test_cases_passed}/ {self.number_of_test_cases}")
        for i in self.test_case_ids:
            if self.test_case_exceptions[i]:
                self.pr(f"\tTest case {i}: FAILED (Exception)")
            elif self.test_case_time_outs[i]:
                self.pr(f"\tTest case {i}: FAILED (Timeout)")
            elif self.test_case_mismatched_lines[i] == 0:
                self.pr(f"\tTest case {i}: PASSED")
            elif self.test_case_mismatched_lines[i] > MAX_LINE_MISMATCHES_PER_TEST_CASE:
                self.pr(f"\tTest case {i}: FAILED ({MAX_LINE_MISMATCHES_PER_TEST_CASE}+ mismatched lines)")
            else:
                self.pr(f"\tTest case {i}: FAILED ({self.test_case_mismatched_lines[i]} mismatched lines)")
        if self.number_of_test_cases == self.number_of_test_cases_passed:
            self.pr(f"All {self.number_of_test_cases} test cases passed.")
        self.pr(f"\nMarking Complete.\n")
        if SAVE_TESTING_SCRIPT_OUTPUT:
            self.__save_testing_script_output_to_file()
        if SHOW_HTML_DIFF:
            self.__display_html_diff()
        print("\nGoodbye.")

    def __display_html_diff(self):
        html_tables_string = ""
        if len(self.html_output_strings) == 0:
            print("No HTML output to display.")
            return
        for i in self.html_output_strings:
            html_tables_string += f"{i}\\n"
        diff = difflib.HtmlDiff(tabsize=len(HTAB)).make_file([], [], context=False, numlines=1)
        regex = r"^\s*<table class=\"diff\" summary=\"Legends\">.*<\/body>"
        legend_match = re.search(regex, diff, re.MULTILINE | re.DOTALL)
        legend = legend_match.group() if legend_match else ""
        regex = r"<body>(.|\n)*?<\/body>"
        subst = f"<body>\n{html_tables_string}\n{self.__get_html_summary()}\n</body>"
        result = re.sub(regex, subst, diff, 0, re.MULTILINE)
        regex = r"<table ([^>]+)"
        subst = '<table style=\"width: 100%\" class=\"diff\" id=\"difflib_chg_to1__top\" cellspacing=\"1\" cellpadding=\"1\" rules=\"groups\"'
        result = re.sub(regex, subst, result, 0, re.MULTILINE)
        if len(legend) > 0:
            legend = legend.replace("Added", "Addition")
            legend = legend.replace("Changed", "&nbsp;Modified&nbsp;")
            legend = legend.replace("Deleted", "&nbsp;Missing&nbsp;")
            legend = legend.replace("</body>", "")
            legend = "<body>\n" + legend
            result = result.replace("<body>", legend, 1)

        html_output_path = os.path.abspath(os.path.join(os.getcwd(), f"SU{self.student_number}_diffs.html"))
        safe_write_file(html_output_path, result)
        if not os.path.isfile(html_output_path):
            print(f"Failed to save HTML output to {html_output_path}.")
            return
        print(f"HTML output saved to {html_output_path}. If the script fails to open the HTML output in your browser, you can open it manually.")
        try:
            webbrowser.open(html_output_path, new=2)
        except Exception as e:
            print(f"Failed to open HTML output in browser:\n{e}")

    def __get_html_summary(self):
        html_summary = f'\n{HTAB}<hr>\n{HTAB}{tag("Summary:", align="left")}\n'
        brl = f"\n{HTAB}<br>\n"
        for start_i in range(len(self.all_output_lines)):
            if self.all_output_lines[start_i].strip() == "Summary:": break
        for i in range(start_i+1, len(self.all_output_lines)):
            if self.all_output_lines[i][0] == '\n':
                html_summary += brl
            post = brl if self.all_output_lines[i][-1] == '\n' else "\n"
            html_summary += f'{HTAB}{tag(self.all_output_lines[i], tt="h4", align="left")}{post}'
        return html_summary

    def __save_testing_script_output_to_file(self):
        output_path = os.path.join(os.getcwd(), f"SU{self.student_number}_diffs.txt")
        output_text = "\n".join(self.all_output_lines)
        # remove triple newlines from output_text
        result_text = re.sub(r"\n{3,}", "\n", output_text.strip(), 0, re.MULTILINE)
        safe_write_file(output_path, result_text)
        print(f"Output saved to: './{self.student_number}_diffs.txt'")
        if VERBOSE_MODE:
            print(f"\n(Absolute Path: {output_path})")

    def __mark_test_case(self, i):
        input_path = os.path.join(SUPPLIED_TEST_CASES_DIR, f"{i}_input.txt")
        output_path = os.path.join(SUPPLIED_TEST_CASES_DIR, f"{i}_output.txt")
        arguments_path = os.path.join(SUPPLIED_TEST_CASES_DIR, f"{i}_arguments.txt")
        header_text = f"Test case {i}"
        self.pr(get_header_block(header_text, start=True))
        arguments = ["0", "0"]
        if os.path.isfile(arguments_path):
            arguments = safe_read_file(arguments_path).strip().split()
        if not os.path.isfile(input_path):
            termination(f"Input file does not exist: {input_path}")
        if not os.path.isfile(output_path):
            termination(f"Output file does not exist: {output_path}")

        tmp_input_path = os.path.relpath(input_path, start=os.curdir)
        tmp_script_path = os.path.relpath(self.python_script_path, start=os.curdir)
        commands_list = [self.python_command, tmp_script_path] + arguments
        self.pr(f"Running test case {i} with command:\n{' '.join(commands_list)} < {tmp_input_path}\n")
        commands_list = [self.python_command, self.python_script_path] + arguments
        try:
            input_contents = safe_read_file(input_path)
            completed_sub = subprocess.run(commands_list, capture_output=True, text=True, input=input_contents, timeout=TIMEOUT_DURATION, check=True)
            if_f_exists_delete(self.tmp_output_path)
            safe_write_file(self.tmp_output_path, completed_sub.stdout)
            if self.__compare_output_files(i, output_path, self.tmp_output_path):
                self.number_of_test_cases_passed += 1
            else:
                self.number_of_test_cases_failed += 1
        except subprocess.CalledProcessError as e:
            self.pr(f"Test case {i} failed due to your program raising an Exception (error).")
            self.pr(f"Error:\n{e.stderr}")
            self.number_of_test_cases_failed += 1
            self.test_case_exceptions[i] = True
        except subprocess.TimeoutExpired:
            self.pr(f"Test case {i} failed because your program took longer than {TIMEOUT_DURATION}s to terminate.")
            self.pr("This should never be the case, even if you run the script on a calculator. This script uses a default timeout value of {TIMEOUT_DURATION}s before forcibly terminating your program.")
            self.pr("This is probably because your program is stuck in an infinite loop or is waiting for input by incorrectly reading from standard input.")
            self.pr("Please ensure that your program does not get stuck in an infinite loop.")
            self.number_of_test_cases_failed += 1
            self.test_case_time_outs[i] = True
        except Exception as e:
            self.pr("Unexpected error. Contact Francois Nel at 19510748@sun.ac.za if you were not able to fix this yourself.")
            self.pr(e)
        if_f_exists_delete(self.tmp_output_path)
        self.pr(get_header_block(header_text, end=True))

    def __compare_output_files(self, i, output_path: str, tmp_output_path: str) -> bool:
        exp_chr = "@"
        fnd_chr = "$"
        output_contents = safe_read_file(output_path).strip()
        tmp_output_contents = safe_read_file(tmp_output_path).strip()
        if_f_exists_delete(self.tmp_output_path)
        if output_contents == tmp_output_contents:
            passed_str = f"Test case {i} passed."
            self.pr(passed_str)
            self.html_output_strings.append(get_html_table_block(i, passed_str, passed=True))
            return True
        self.pr(f"Test case {i} failed due to differences in output. Mismatched lines:\n")
        expected_header = f"Expected ({i}_output.txt)"
        found_header = f"Found (SU{self.student_number}.py output)"
        expected = output_contents.splitlines()
        found = tmp_output_contents.splitlines()

        c = 0
        context = 1
        min_len = min(len(expected), len(found))
        for j in range(min_len):
            if expected[j] != found[j]:
                c += 1
                if c > MAX_LINE_MISMATCHES_PER_TEST_CASE:
                    min_len = min(j + 1, min_len)
                    break
        self.test_case_mismatched_lines[i] = c
        if len(expected) >= min_len + context:
            expected = expected[:min_len+context]
        if len(found) >= min_len + context:
            found = found[:min_len+context]
        max_width = 100
        def wrp(text):
            num_spaces = max(0, max_width - len(text))
            if num_spaces == 0:
                return text[:max_width]
            return text + " " * num_spaces

        if PRINT_SIDE_BY_SIDE:
            pre_j = -1
            nm1 = f"{' ':<4s}"
            hr_df = f"{'-' * (max_width*2 + 8)}"
            self.pr(hr_df)
            self.pr(f'{" ":<4s}@@{wrp("@@@ " + expected_header + " @@@@@")}$$$$$ {wrp(found_header + " $$$$$")}'.rstrip())
            for j in range(min_len):
                if expected[j] != found[j]:
                    if j - (pre_j+1) < 5:
                        for k in range(pre_j+1, j):
                            self.pr(f'{nm1}: {wrp(expected[k])}: {wrp(found[k])}')
                    else:
                        self.pr(hr_df)
                    ln = f'{j+1:<4d}@ {wrp(expected[j])}$ {wrp(found[j])}'
                    self.pr(ln)
                    pre_j = j
        else:
            regex = r"@@\s*-[^+]+[+][^@]+@@"
            better_lines = []
            hr_df = '*' * 120
            for line in difflib.unified_diff(expected, found, fromfile=expected_header, tofile=found_header, lineterm='', n=context):
                if line.startswith(f"--- {expected_header}"):
                    better_lines.append(f'{exp_chr*3} {expected_header}')
                elif line.startswith(f"+++ {found_header}"):
                    better_lines.append(f'{fnd_chr*3} {found_header}')
                elif line[0] == "@":
                    better_lines.append(f'{exp_chr}: {line[1:]}')
                elif line[0] == "$":
                    better_lines.append(f'{fnd_chr}: {line[1:]}')
                elif line[0] == " ":
                    better_lines.append(f' :{line}')
                elif re.search(regex, line):
                    line = f'{hr_df[0]}{line.replace("@@", "").center(118)}{hr_df[0]}'
                    better_lines.append(hr_df)
                    better_lines.append(line)
                    better_lines.append(hr_df)

            for line in better_lines:
                self.pr(line)

        if SHOW_HTML_DIFF:
            try:
                html_diff = difflib.HtmlDiff(tabsize=len(HTAB), wrapcolumn=90, charjunk=None)
                diff = html_diff.make_table(expected, found, expected_header, found_header, context=True, numlines=context)
                html_table = get_html_table_block(i, diff)
                self.html_output_strings.append(html_table)
            except Exception as e:
                if VERBOSE_MODE: print(f"Could not create HTML table for test case {i}. Error:\n{e}")
        return False

def tag(text, tt="h1", align="center"):
    return f'<{tt} align="{align}">{web_spacing(text)}</{tt}>'

def web_spacing(text):
    return text.replace("\t", HTAB).replace("\n", "").replace(" ", "&nbsp;")

def get_html_table_block(i, html_table_i, passed=False):
    html_hr = f'{HTAB}<hr style="border: 5px solid">\n'
    html_header_for_table = f'{html_hr}{HTAB}{tag(f"Start Test Case {i}")}'
    html_footer_for_table = f'\n{HTAB}{tag(f"End Test Case {i}")}\n{html_hr}'
    if passed:
        html_table_i = f"\n{HTAB}{tag(f'Test Case {i} Passed!', tt='h2')}"
        return f'{html_header_for_table}{html_table_i}{html_footer_for_table}'
    return f'{html_header_for_table}{html_table_i}{html_footer_for_table}'

def safe_read_file(path: str) -> str:
    if not os.path.isfile(path):
        termination(f"File does not exist: {path}")
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        termination(f"Error reading file: {path}\n{e}")

def safe_write_file(path: str, contents: str):
    try:
        with open(path, "w") as f:
            f.write(contents)
    except Exception as e:
        termination(f"Error writing output to file: {path}\n{e}")

def get_directory_file_names(dir=None):
    if dir is None:
        dir = os.getcwd()
    return [f.strip() for f in os.listdir(dir) if len(f.strip()) > 3 and os.path.isfile(os.path.join(dir, f))]

def get_possible_test_case_ids(test_case_dir):
    return [int(re.match(r"(\d+)_input\.txt", f).group(1)) for f in get_directory_file_names(test_case_dir) if re.fullmatch(r"[1-9]\d*_input\.txt", f)]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Compare the output of your CS113/4 Air-Race python script against a set of test cases.")
    parser.add_argument("-s", "--save_output", action="store_true", help="Save the output of the script to a file. The file will be saved in the same directory as the python script, as a file named 'SUxxxxxxxx_diffs.txt', where 'xxxxxxxx' is your student number.")
    parser.add_argument("-w", "--webpage", action="store_true", help="Output the differences side-by-side in an HTML file which you can open in your browser. The program will save an HTML file in the current directory as a file named 'SUxxxxxxxx_diffs.html'. The program will attempt to open the HTML file in your default browser automatically, if your operating system allows it.")
    parser.add_argument("-ss", "--side_by_side", action="store_true", help="Output the differences side-by-side in the terminal. If this option is not specified, the program will output the differences in a unified diff format, meaning that the differences will be shown in a single column.")
    parser.add_argument("-m", "--max_allowed_mismatched_lines", type=int, default=10, help="The maximum number of lines that can be mismatched in a test case before the script will no longer print any more mismatches.")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    global VERBOSE_MODE, SAVE_TESTING_SCRIPT_OUTPUT, SHOW_HTML_DIFF, PRINT_SIDE_BY_SIDE, MAX_LINE_MISMATCHES_PER_TEST_CASE
    if args.verbose:
        VERBOSE_MODE = True
    if args.save_output:
        SAVE_TESTING_SCRIPT_OUTPUT = True
    if args.webpage:
        SHOW_HTML_DIFF = True
    if args.side_by_side:
        PRINT_SIDE_BY_SIDE = True
    MAX_LINE_MISMATCHES_PER_TEST_CASE = min(2000, max(0, args.max_allowed_mismatched_lines))

def main():
    stdio.writeln("Python Air-Race Marking Script v1.0\n")
    parse_arguments()
    test_case_directory_exists()
    pos_scripts = [f for f in get_directory_file_names() if re.fullmatch(r"SU[1-9]\d{7}\.py", f)]
    if len(pos_scripts) == 0:
        display_usuage()
        termination("No python script in the form of SUxxxxxxxx.py found in the current directory.\nNote, the student number (represented by 'xxxxxxxx') must be 8 integers long, the 'SU' prefix (start of the string) must be included as uppercase characters, the file extension must be '.py' (lowercase), and no other characters should appear in the name.")
    elif len(pos_scripts) > 1:
        display_usuage()
        print("Multiple python scripts in the form of SUxxxxxxxx.py found in the current directory:")
        for i, script in enumerate(pos_scripts):
            print(f"\t{i+1}. {script}")
        termination("\nPlease ensure you only have one python script in the form of SUxxxxxxxx.py in the current directory.")
    python_script_path = os.path.join(os.getcwd(), pos_scripts[0])
    student_number = pos_scripts[0][2:10]
    pos_test_case_ids = list(set(get_possible_test_case_ids(SUPPLIED_TEST_CASES_DIR)))
    pos_test_case_ids.sort()
    val_test_case_ids = []
    for i in pos_test_case_ids:
        tmp_in_path = os.path.join(SUPPLIED_TEST_CASES_DIR, f"{i}_input.txt")
        tmp_out_path = os.path.join(SUPPLIED_TEST_CASES_DIR, f"{i}_output.txt")
        if os.path.isfile(tmp_in_path) and os.path.isfile(tmp_out_path):
            val_test_case_ids.append(i)
    if len(val_test_case_ids) == 0:
        display_usuage()
        print(f"No valid test cases found in the supplied test case folder: {SUPPLIED_TEST_CASES_DIR}.")
        print(f"Test cases must be in the form of n_input.txt and n_output.txt, where n is a positive, non-zero integer corresponding to the test case ID.")
        termination()
    print(f"Auto-detected student number: {student_number}")
    print(f"Auto-detected python script: {python_script_path}")
    print(f"Auto-detected test case IDs: {val_test_case_ids}\n")
    marker = Marker(student_number, val_test_case_ids)
    marker.mark()

def if_f_exists_delete(f):
    try:
        if os.path.exists(f):
            os.remove(f)
    except Exception as e:
        termination(f"Error deleting file: {f}\n{e}")

def ensure_paths_exist(python_script_path, test_case_ids):
    should_terminate = False
    if not os.path.exists(python_script_path):
        print(f"Python script does not exist: {python_script_path}")
        print("Note, the student number (represented by 'xxxxxxxx') must be 8 integers long, the 'SU' prefix (start of the string) must be included as uppercase characters, the file extension must be '.py' (lowercase), and no other characters should appear in the name.")
        should_terminate = True
    if not os.path.exists(SUPPLIED_TEST_CASES_DIR):
        termination(f"Supplied test cases folder does not exist: {SUPPLIED_TEST_CASES_DIR}")
    for i in test_case_ids:
        temp_input_path = os.path.join(SUPPLIED_TEST_CASES_DIR, f"{i}_input.txt")
        temp_output_path = os.path.join(SUPPLIED_TEST_CASES_DIR, f"{i}_output.txt")
        if not os.path.exists(temp_input_path):
            print(f"Input file does not exist: {temp_input_path}")
            should_terminate = True
        if not os.path.exists(temp_output_path):
            print(f"Output file does not exist: {temp_output_path}")
            should_terminate = True
    if should_terminate:
        termination()

def safe_make_dir(path):
    if os.path.isfile(path): print(f"Could not create directory {path} as a file with the same name already exists.")
    if os.path.exists(path): return os.path.isdir(path)
    try:
        os.mkdir(path)
    except Exception as e:
        print(f"Could not create directory {path}. Error:\n{e}")
    return os.path.isdir(path)

def test_case_directory_exists() -> None:
    if not os.path.isdir(SUPPLIED_TEST_CASES_DIR):
        if os.path.exists(os.path.join(os.getcwd(), "supplied_test_cases_1")):
            print("WARNING: The supplied_test_cases folder was not found but supplied_test_cases_1 was found. This script uses supplied_test_cases folder.")
        termination(f"The supplied test case folder does not exist or is not a directory: {SUPPLIED_TEST_CASES_DIR}")

def display_usuage():
    print("Place this script in the same directory as your SUxxxxxxxx.py script and the folder containing the test cases.")
    print("The folder containing the test cases should be called supplied_test_cases.")
    print("For each test case with ID n, the following files should exist:")
    print("\tn_input.txt")
    print("\tn_output.txt")
    print("\tn_arguments.txt (optional -- if it doesn't exist, the script will assume default Air-Race arugments of 0 0)\n")
    print("Usage:\n\t'python diff_checker.py [-s] [-w]'")
    print("\tThe -s flag will save the text output of the differencing script to a file in the current directory.")
    print("\tThe -w flag will save the output of the differencing script as an HTML file which you can open in your browser. The program will attempt to open the file automatically, if your operating system supports it.")
    print("The program will attempt to auto-detect file paths in the current directory by attempts to find a Python script in the form of SUxxxxxxxx.py, and a folder called supplied_test_cases which contains the test case files.\n")

def get_header_block(text, start=False, end=False) -> str:
    line = '='*120
    if start:
        text = f"START {text}"
    elif end:
        text = f"END {text}"
    return f"\n{line}\n{text.center(120)}\n{line}\n"

def validate_student_number(student_number):
    return re.fullmatch(r"\d{8}", student_number)

def validate_test_case_id(test_case_id):
    if not re.fullmatch(r"\d+", test_case_id):
        termination(f"Invalid test case ID supplied. {test_case_id} is not a valid integer.")
    if test_case_id.startswith("0"):
        termination(f"Invalid test case ID supplied. {test_case_id} starts with a zero.")
    test_case_id = int(test_case_id)
    if test_case_id < 1:
        termination(f"Invalid test case ID supplied. {test_case_id} is less than 1.")
    return test_case_id

def termination(x=None):
    if x is not None:
        print(x)
    print("Terminating.")
    sys.exit(1)

if __name__ == "__main__":
    main()
