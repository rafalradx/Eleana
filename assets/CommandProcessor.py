import re
import argparse

class CommandProcessor:
    ''' Contains methods to parse command lines'''

    def __init__(self):

        # DICTIONARIES
        # ---- Eleana variables ----
        self.eleana_variables = {
            "$f": "self.eleana.selections['first']",
            "$f_sub": "self.eleana.selections['f_stk']",
            "$f_disp": "self.eleana.selections['f_dsp']",
            "$f_cpl": "self.eleana.selections['f_cpl']",
            "$s": "self.eleana.selections['second']",
            "$s_sub": "self.eleana.selections['s_stk']",
            "$s_disp": "self.eleana.selections['s_dsp']",
            "$s_cpl": "self.eleana.selections['s_cpl']",
            "$r": "self.eleana.selections['result']",
            "$r_sub": "self.eleana.selections['r_stk']",
            "$r_disp": "self.eleana.selections['r_dsp']",
            "$r_cpl": "self.eleana.selections['r_cpl']",
            "$g": "self.eleana.selections['group']",
            "$dataset": "self.eleana.dataset",
            "$results": "self.eleana.results_dataset",
            "$notes": "self.eleana.notes",
            "$lastproject": "self.eleana.paths['last_project']",
            "$projectpath": "self.eleana.paths['last_project_dir']"
        }

        # --- Eleana actions on GUI
        self.eleana_gui_buttons = {
            "$g+": "self.group_down_clicked()",
            "$g-": "self.group_up_clicked()",
            "$f+": "self.first_up_clicked()",
            "$f-": "self.first_down_clicked()",
            "$s+": "self.second_up_clicked()",
            "$s-": "self.second_down_clicked()",
            "$r+": "self.result_up_clicked()",
            "$r-": "self.result_down_clicked()",

        }

        # Combining Eleana dictionaries into one
        self.cmd_dictionary = {**self.eleana_variables, **self.eleana_gui_buttons}

        # DICTIONARY USED TO BUILD PARSER FOR ARGPARSE
        self.argparse_commands = {
            'loadproject': {
                'args': [('filename', str, 'The path to project file')],
                'kwargs': {'-append': (bool, 'False - delete data in memory and load project, True - append loaded project to existing data.', True)}
            },

            'import': {
                'args': [('filename', str, 'The path to project file')],
                'kwargs': {'-format': (str, 'The format of the project', 'default_format')}
            },

            'save': {
                'args': [('filename', str, 'The filename to save')],
                'kwargs': {}
            },
        }

        # Create parser
        self.parser = self.create_parser()

    def create_parser(self):
        '''Create parser for script that will use argparse'''
        parser = argparse.ArgumentParser(description="Command processor")
        subparsers = parser.add_subparsers(dest='command')
        for command, params in self.argparse_commands.items():
            cmd_parser = subparsers.add_parser(command)
            for arg_name, arg_type, arg_help in params['args']:
                cmd_parser.add_argument(arg_name, type=arg_type, help=arg_help)
            for kwarg_name, (kwarg_type, kwarg_help, kwarg_default) in params['kwargs'].items():
                cmd_parser.add_argument(kwarg_name, type=kwarg_type, help=kwarg_help, default=kwarg_default)
        return parser

    def process_script(self, script):
        ''' Function used to transcript commands into executable script'''
        def _transcription(line):
            ''' Replaces the simple commands, variables to eleana compatible '''
            for substring, replacement in sorted(self.cmd_dictionary.items(), key=lambda x: -len(x[0])):
                pattern = re.compile(r'(?<![\w\d])' + re.escape(substring) + r'(?![\w\d])', re.IGNORECASE)
                line = pattern.sub(replacement, line)
            return line

        def _argparse_analyse(line_for_argparse, indent):
            ''' Parse the line using argparse and convert to method call '''
            args = line_for_argparse.split()
            if not args:
                return line_for_argparse  # Return the line unchanged if there are no arguments

            # --------- DEFINE REPLACEMENT FOR ARPARSED LINES ------------------
            if args[0] in self.argparse_commands:
                try:
                    parsed_args = self.parser.parse_args(args)
                    if parsed_args.command == 'loadproject':
                        return f'{indent}self.loadproject(filename="{parsed_args.filename}", append={parsed_args.append})'
                    elif parsed_args.command == 'saveproject':
                        return f'{indent}self.saveproject(filename="{parsed_args.filename}")'
                except SystemExit:
                    # Ignore argparse errors
                    return None
                    return f'{indent}{line_for_argparse}'
            else:
                # Argparse command not found - ignore line
                return f'{indent}{line_for_argparse}'

        # Divide script into lines
        lines = script.split('\n')
        # Scan each line and argparse
        transcript_lines = []
        for line in lines:
            if line.strip():  # Check if the line is not empty
                indent = re.match(r'\s*', line).group(0)
                # Transcript eleana variables and gui commands
                transcripted_line = _transcription(line.strip())
                # Argparse lines
                try:
                    parsed_line = _argparse_analyse(transcripted_line, indent)
                except:
                    parsed_line = None
                if not parsed_line:
                    line_nr = str(len(transcript_lines))
                    transcript_lines.append(' ---- ERROR IN LINE: ' + line_nr + ' ----> ' + line)
                    parsed_script = "\n".join(transcript_lines)
                    return True, parsed_script
                transcript_lines.append(parsed_line)
            else:
                transcript_lines.append(line)  # Preserve empty lines
        # Create script from lines
        parsed_script = "\n".join(transcript_lines)
        return False, parsed_script

class CmdFunctions:
    '''This provides wrapper functions to activate appropriate methods in the program'''
    def __init__(self, app_instance):
        pass



# Run
if __name__ == "__main__":
    cmd = CommandProcessor()
    script = """
# First
i = $f
    $f+
    $f-
b = $f
while i>1:
    loadproject filename.ele -append=True 
    i+=1
save file.ele
for i in variable:
    lines.append(i)
    """
    error, skrypt = cmd.process_script(script)

    print(skrypt)
