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
        eleana_variables = {
                    "$f":           "self.eleana.selections['first']",
                    "$f_sub":       "self.eleana.selections['f_stk']",
                    "$f_disp":      "self.eleana.selections['f_dsp']",
                    "$f_cpl":       "self.eleana.selections['f_cpl']",

                    "$s":           "self.eleana.selections['second']",
                    "$s_sub":       "self.eleana.selections['s_stk']",
                    "$s_disp":      "self.eleana.selections['s_dsp']",
                    "$s_cpl":       "self.eleana.selections['s_cpl']",

                    "$r":           "self.eleana.selections['result']",
                    "$r_sub":       "self.eleana.selections['r_stk']",
                    "$r_disp":      "self.eleana.selections['r_dsp']",
                    "$r_cpl":       "self.eleana.selections[r_cpl]",

                    "$g":           "self.eleana.selections['group']",

                    "$dataset":     "self.eleana.dataset",
                    "$results":     "self.eleana.results_dataset",
                    "$notes":       "self.eleana.notes",
                    "$lastproject": "self.eleana.paths['last_project']",
                    "$projectpath": "self.eleana.paths['last_project_dir']",

                    }

        eleana_gui_commands = {autoscale_X}
        # Combine all dictionaries into one
        self.cmd_dictionary = {**eleana_variables, **eleana_simple_comands}

        # Create references to main objects
        if not app_instance:
            return
        # References to main eleana objects
        self.app = app_instance
        self.eleana = app_instance.eleana

    def process_script(self, script):
        def _transcription(line):
            ''' Replaces the simple commands to eleana compatible '''
            for substring, replacement in self.cmd_dictionary.items():
                pattern = re.compile(re.escape(substring), re.IGNORECASE)
                line = pattern.sub(replacement, line)
            return line

        # Divide script into lines
        lines = script.split('\n')
        # Scan each line and argparse
        transcript_lines = []
        for line in lines:
            transcript_lines.append(_transcription(line))

        # Create script from lines
        script = "\n".join(transcript_lines)
        print(script)



# Run
if __name__ == "__main__":
    cmd = CommandProcessor()
    script = "To jest niesmienione\n $F = 'dUżE'\n to znowu takie same\n$g = 4\n$LastProject"
    cmd.process_script(script)