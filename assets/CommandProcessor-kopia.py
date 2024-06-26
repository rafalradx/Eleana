import re
import argparse

'''
Schemat działania:
tekst skryptu --> podział na linie --> argparse i utworzenie komend --> zamiana nazw własnych na eleana -->
konwersja liniii na tekst
'''

class CommandProcessor:
    ''' Contains methods to parse command lines'''

    def __init__(self, app_instance=None):
        # Dictionary of commands
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
            "$projectpath": "self.eleana.paths['last_project_dir']",
        }

        self.eleana_gui_buttons = {

        }

        # Combine all dictionaries into one
        self.cmd_dictionary = {**self.eleana_variables, **self.eleana_gui_buttons}

        # Dictionary for argparse commands
        self.argparse_commands = {
            'load': {
                'args': [('filename', str, 'The filename to load')],
                'kwargs': {'-format': (str, 'The format of the project', 'default_format')}
            },

            'save': {
                'args': [('filename', str, 'The filename to save')],
                'kwargs': {}
            },
            '$f+': {
                'args': [],
                'kwargs': {}
            }
        }

        # Create parser
        self.parser = self.create_parser()

        # Create references to main objects
        if not app_instance:
            return
        # References to main eleana objects
        self.app = app_instance
        self.eleana = app_instance.eleana

    def create_parser(self):
        '''Create parser for script that will use argparse to modify script'''
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
        def _transcription(line):
            ''' Replaces the simple commands to eleana compatible '''
            for substring, replacement in sorted(self.cmd_dictionary.items(), key=lambda x: -len(x[0])):
                pattern = re.compile(r'(?<![\w\d])' + re.escape(substring) + r'(?![\w\d])', re.IGNORECASE)
                line = pattern.sub(replacement, line)
            return line

        def _argparse_analyse(line_for_argparse, indent):
            ''' Parse the line using argparse and convert to method call '''
            args = line_for_argparse.split()
            if not args:
                return line_for_argparse  # Return the line unchanged if there are no arguments

            if args[0] in self.argparse_commands:
                try:
                    parsed_args = self.parser.parse_args(args)
                    if parsed_args.command == 'load':
                        return f'{indent}self.loadproject(file="{parsed_args.filename}", type="{parsed_args.format}")'
                    elif parsed_args.command == 'save':
                        return f'{indent}self.saveproject(file="{parsed_args.filename}")'
                    elif parsed_args.command == '$f+':
                        return f'{indent}zwiększ'


                except SystemExit:
                    # Ignore argparse errors
                    return None
                    return f'{indent}{line_for_argparse}'
            else:
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
                    #line_nr = len()
                    transcript_lines.append('--- ERROR -->' + line)
                    parsed_script = "\n".join(transcript_lines)
                    return True, parsed_script
                transcript_lines.append(parsed_line)
            else:
                transcript_lines.append(line)  # Preserve empty lines

        # Create script from lines
        parsed_script = "\n".join(transcript_lines)
        return False, parsed_script


# Run
if __name__ == "__main__":
    cmd = CommandProcessor()
    script = """
# First
$f+
    """
    error, skrypt = cmd.process_script(script)

    print(skrypt)
