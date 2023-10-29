#!/usr/bin/python3

# Import Standard Python Modules
import json
import pickle
import pathlib
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import customtkinter
import pygubu
from CTkMessagebox import CTkMessagebox
import sys
import customtkinter as ctk
import io
import sys

# Import Eleana specific classes
from assets.GeneralEleana import Eleana
from assets.LoadSave import Load
from assets.LoadSave import Save
from assets.Initialization import Init
from assets.Grapher import Grapher
from assets.Update import Update
from subprogs.group_edit.add_group import Groupcreate
from subprogs.group_edit.assign_to_group import Groupassign


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ui" / "Eleana_main.ui"
VERSION = 1
INTERPRETER = sys.executable  # <-- Python version for subprocesses

DEVEL = True

class EleanaMainApp:
    def __init__(self, eleana_instance, master=None):

        # Initialize eleana
        self.eleana = eleana_instance

        # START BUILDER
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("Eleana", master)
        self.mainwindow.iconify()
        self.mainwindow.withdraw()

        # Main menu
        main_menu = builder.get_object("mainmenu", self.mainwindow)
        self.mainwindow.configure(menu=main_menu)

        self.group_down = None
        self.group_up = None
        self.group = None
        self.first_down = None
        builder.connect_callbacks(self)
        # END OF PYGUBU BUILDER

        # Create references to Widgets and Frames
        self.sel_group = builder.get_object("sel_group", self.mainwindow)
        self.sel_first = builder.get_object("sel_first", self.mainwindow)
        self.sel_second = builder.get_object("sel_second", self.mainwindow)
        self.sel_result = builder.get_object("sel_result", self.mainwindow)
        self.firstFrame = builder.get_object("firstFrame", self.mainwindow)
        self.resultFrame = builder.get_object("resultFrame", self.mainwindow)
        self.resultStkFrame = builder.get_object("resultStkFrame", self.mainwindow)
        self.firstStkFrame = builder.get_object("firstStkFrame", self.mainwindow)
        self.secondStkFrame = builder.get_object("secondStkFrame", self.mainwindow)
        self.firstComplex = builder.get_object("firstComplex", self.mainwindow)
        self.secondComplex = builder.get_object("secondComplex", self.mainwindow)
        self.resultComplex = builder.get_object("resultComplex", self.mainwindow)
        self.graphFrame = builder.get_object('graphFrame', self.mainwindow)
        self.f_stk = builder.get_object('f_stk', self.mainwindow)
        self.s_stk = builder.get_object('s_stk', self.mainwindow)
        self.r_stk = builder.get_object('r_stk', self.mainwindow)
        self.btn_clear_results = builder.get_object('btn_clear_results', self.mainwindow)
        self.check_first_show = builder.get_object('check_first_show', self.mainwindow)
        self.check_second_show = builder.get_object('check_second_show', self.mainwindow)
        self.check_result_show = builder.get_object('check_result_show', self.mainwindow)

        # Graph Buttons
        self.check_autoscale_x = builder.get_object('check_autoscale_X', self.mainwindow)
        self.check_autoscale_y = builder.get_object('check_autoscale_Y', self.mainwindow)
        self.check_log_x = builder.get_object('check_log_x', self.mainwindow)
        self.check_log_y = builder.get_object('check_log_y', self.mainwindow)
        self.check_indexed_x = builder.get_object('check_indexed_x', self.mainwindow)

        # Command line
        self.command_line = builder.get_object('command_line', self.mainwindow)
        self.command_line.bind("<Return>", self.execute_command)
        self.command_line.bind("<Up>", self.execute_command)
        self.command_line.bind("<Down>", self.execute_command)

        self.panedwindow2 = builder.get_object('panedwindow2', self.mainwindow)
        self.panedwindow4 = builder.get_object('panedwindow4', self.mainwindow)
        self.pane5 = builder.get_object('pane5', self.mainwindow)
        self.pane9 = builder.get_object('pane9', self.mainwindow)

        self.log_field = builder.get_object('log_field', self.mainwindow)

        self.command_history = {'index':0, 'lines':[]}

        # Context menu bindings
        self.label7 = builder.get_object('label7', self.mainwindow)
        self.label7.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        print('Context menu')

    # def create_command_menu(self):
    #     self.contex_menu.add_command(label="Print hello", command=self.on_print_hello_menu_clicked)
    # def on_print_hello_menu_clicked(self):
    #     print('Hello')







    def set_pane_height(self):
        self.panedwindow2.sashpos(0, 700)
        self.panedwindow4.sashpos(0, 300)
        return

    def run(self):
            self.mainwindow.deiconify()
            self.mainwindow.after(100, self.set_pane_height)
            self.mainwindow.mainloop()

    def group_down_clicked(self):
        current_group = self.sel_group.get()
        group_list = self.sel_group._values
        index = group_list.index(current_group)
        if index == 0:
            return
        index -= 1
        new_group = group_list[index]
        self.sel_group.set(new_group)
        self.group_selected(new_group)

    def group_up_clicked(self):
        current_group = self.sel_group.get()
        group_list = self.sel_group._values
        index = group_list.index(current_group)
        if index == len(group_list) - 1:
            return
        index += 1
        new_group = group_list[index]
        self.sel_group.set(new_group)
        self.group_selected(new_group)

    def group_selected(self, value):
        eleana.selections['group'] = value
        update.all_lists()

    def first_show(self):
        eleana.selections['f_dsp'] = bool(self.check_first_show.get())
        selection = self.sel_first.get()
        if selection == 'None':
            return
        self.first_selected(selection)

    def first_down_clicked(self):
        current_position = self.sel_first.get()
        list_of_items = self.sel_first._values
        if current_position == 'None':
            return
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_first not found')
            return
        try:
            new_position = list_of_items[index - 1]
            self.sel_first.set(new_position)
            self.first_selected(new_position)
        except IndexError:
            return

    def first_up_clicked(self):
        current_position = self.sel_first.get()
        list_of_items = self.sel_first._values
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_first not found.')
            return
        try:
            new_position = list_of_items[index + 1]
            self.sel_first.set(new_position)
            self.first_selected(new_position)
        except IndexError:
            return

    def first_complex_clicked(self, value):
            eleana.selections['f_cpl'] = value
            grapher.plot_graph()


    def first_selected(self, selected_value_text):
        if selected_value_text == 'None':
            eleana.selections['first'] = -1
            self.firstComplex.grid_remove()
            self.firstStkFrame.grid_remove()
            grapher.plot_graph()
            return

        i = 0
        while i < len(eleana.dataset):
            name = eleana.dataset[i].name_nr
            if name == selected_value_text:
                eleana.selections['first'] = i
                break
            i += 1
        update.list_in_combobox('sel_first')
        update.list_in_combobox('f_stk')
        if eleana.dataset[eleana.selections['first']].complex:
            self.firstComplex.grid()
        else:
            self.firstComplex.grid_remove()
        grapher.plot_graph()

    def f_stk_selected(self, selected_value_text):
        if selected_value_text in self.f_stk._values:
            index = self.f_stk._values.index(selected_value_text)
            eleana.selections['f_stk'] = index
        else:
            return
        grapher.plot_graph()


    def f_stk_up_clicked(self):
        current_position = self.f_stk.get()
        list_of_items = self.f_stk._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in f_stk not found.')
            return
        try:
            new_position = list_of_items[index + 1]
            self.f_stk.set(new_position)
            eleana.selections['f_stk'] = index + 1
        except IndexError:
            return
        grapher.plot_graph()


    def f_stk_down_clicked(self):
        current_position = self.f_stk.get()
        list_of_items = self.f_stk._values
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in f_stk not found.')
            return
        if index == 0:
            return
        try:
            new_position = list_of_items[index - 1]
            self.f_stk.set(new_position)
            eleana.selections['f_stk'] = index - 1
        except IndexError:
            return
        grapher.plot_graph()

    def second_show(self):
        eleana.selections['s_dsp'] = bool(self.check_second_show.get())
        selection = self.sel_second.get()
        if selection == 'None':
            return
        self.second_selected(selection)

    def second_selected(self, selected_value_text):
        if selected_value_text == 'None':
            eleana.selections['second'] = -1
            self.secondComplex.grid_remove()
            self.secondStkFrame.grid_remove()
            grapher.plot_graph()
            return
        i = 0
        while i < len(eleana.dataset):
            name = eleana.dataset[i].name_nr
            if name == selected_value_text:
                eleana.selections['second'] = i
                break
            i += 1
        update.list_in_combobox('sel_second')
        update.list_in_combobox('s_stk')

        if eleana.dataset[eleana.selections['second']].complex:
            self.secondComplex.grid()
        else:
            self.secondComplex.grid_remove()
        grapher.plot_graph()


    def second_down_clicked(self):
        current_position = self.sel_second.get()
        list_of_items = self.sel_second._values
        if current_position == 'None':
            return
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_second not found.')
            return

        try:
            new_position = list_of_items[index - 1]
            self.sel_second.set(new_position)
            self.second_selected(new_position)
        except IndexError:
            return


    def second_up_clicked(self):
        current_position = self.sel_second.get()
        list_of_items = self.sel_second._values
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_second not found.')
            return
        try:
            new_position = list_of_items[index + 1]
            self.sel_second.set(new_position)
            self.second_selected(new_position)
        except IndexError:
            return


    def s_stk_selected(self, selected_value_text):
        if selected_value_text in self.s_stk._values:
            index = self.s_stk._values.index(selected_value_text)
            eleana.selections['s_stk'] = index
        else:
            return
        grapher.plot_graph()

    def s_stk_up_clicked(self):
        current_position = self.s_stk.get()
        list_of_items = self.s_stk._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in s_stk not found.')
            return
        try:
            new_position = list_of_items[index + 1]
            self.s_stk.set(new_position)
            eleana.selections['s_stk'] = index + 1
        except IndexError:
            return
        grapher.plot_graph()


    def s_stk_down_clicked(self):
        current_position = self.s_stk.get()
        list_of_items = self.s_stk._values
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in s_stk not found.')
            return
        if index == 0:
            return
        try:
            new_position = list_of_items[index - 1]
            self.s_stk.set(new_position)
            eleana.selections['s_stk'] = index - 1
        except IndexError:
            return
        grapher.plot_graph()


    def second_complex_clicked(self, value):
            eleana.selections['s_cpl'] = value
            grapher.plot_graph()

    def swap_first_second(self):
        first_pos = self.sel_first.get()
        second_pos = self.sel_second.get()
        first_stk = self.f_stk.get()
        second_stk = self.s_stk.get()

        if first_pos == 'None':
            self.firstComplex.grid_remove()

        if first_pos == 'None':
            self.secondComplex.grid_remove()

        self.sel_first.set(second_pos)
        self.sel_second.set(first_pos)

        self.first_selected(second_pos)
        self.second_selected(first_pos)

        self.f_stk.set(second_stk)
        self.s_stk.set(first_stk)

        self.f_stk_selected(second_stk)
        self.s_stk_selected(first_stk)

        grapher.plot_graph()

    def second_to_result(self):
        current = self.sel_second.get()
        if current == 'None':
            return
        index = get_index_by_name(current)
        spectrum = eleana.dataset[index]

        # Check the name if the same already exists in eleana.result_dataset
        list_of_results = []
        try:
            for each in eleana.results_dataset:
                list_of_results.append(each.name)
        except:
            pass

        if spectrum.name in list_of_results:
            dialog = customtkinter.CTkInputDialog(
                text="There is data with the same name. Please enter a different name.", title="Enter new name")
            input = dialog.get_input()
            if type(input) == str and spectrum.name != input:
                spectrum.name = input
            else:
                return

        # Send to result and update lists
        eleana.results_dataset.append(spectrum)
        update.list_in_combobox('sel_result')
        update.list_in_combobox('r_stk')

        # Set the position to the last added item
        list_of_results = self.sel_result._values
        position = list_of_results[-1]
        self.sel_result.set(position)
        self.result_selected(position)

    def result_show(self):
        eleana.selections['r_dsp'] = bool(self.check_result_show.get())
        selection = self.sel_result.get()
        if selection == 'None':
            return
        self.result_selected(selection)

    def result_selected(self, selected_value_text):
        if selected_value_text == 'None':
            eleana.selections['result'] = -1
            self.resultComplex.grid_remove()
            self.resultStkFrame.grid_remove()
            grapher.plot_graph()
            return

        i = 0
        while i < len(eleana.results_dataset):
            name = eleana.results_dataset[i].name
            if name == selected_value_text:
                eleana.selections['result'] = i
                break
            i += 1

        update.list_in_combobox('sel_result')
        update.list_in_combobox('r_stk')

        if eleana.results_dataset[eleana.selections['result']].complex:
            self.resultComplex.grid()
        else:
            self.resultComplex.grid_remove()

        grapher.plot_graph()

    def result_up_clicked(self):
        current_position = self.sel_result.get()
        list_of_items = self.sel_result._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_result not found.')
            return

        try:
            new_position = list_of_items[index + 1]
            self.sel_result.set(new_position)
            self.result_selected(new_position)
        except IndexError:
            return

        grapher.plot_graph()
    def result_down_clicked(self):
        current_position = self.sel_result.get()
        list_of_items = self.sel_result._values
        if current_position == 'None':
            return
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_first not found')
            return

        try:
            new_position = list_of_items[index - 1]
            self.sel_result.set(new_position)
            self.result_selected(new_position)
        except IndexError:
            return

        grapher.plot_graph()
    def r_stk_up_clicked(self):
        current_position = self.r_stk.get()
        list_of_items = self.r_stk._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in r_stk not found.')
            return

        try:
            new_position = list_of_items[index + 1]
            self.r_stk.set(new_position)
            eleana.selections['r_stk'] = index + 1
        except IndexError:
            return

        grapher.plot_graph()
    def r_stk_down_clicked(self):
        current_position = self.r_stk.get()
        list_of_items = self.r_stk._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in r_stk not found.')
            return
        if index == 0:
            return
        try:
            new_position = list_of_items[index - 1]
            self.r_stk.set(new_position)
            eleana.selections['r_stk'] = index - 1
        except IndexError:
            return

        grapher.plot_graph()
    def first_to_result(self):
            current = self.sel_first.get()
            if current == 'None':
                 return
            index = get_index_by_name(current)
            spectrum = eleana.dataset[index]

            # Check the name if the same already exists in eleana.result_dataset
            list_of_results = []
            try:
                for each in eleana.results_dataset:
                    list_of_results.append(each.name)
            except:
                pass

            if spectrum.name in list_of_results:
                dialog = ctk.CTkInputDialog(text="There is data with the same name. Please enter a different name.", title="Enter new name")
                input = dialog.get_input()
                if type(input) == str and spectrum.name != input:
                    spectrum.name = input
                else:
                    return

            # Send to result and update lists
            eleana.results_dataset.append(spectrum)
            update.list_in_combobox('sel_result')
            update.list_in_combobox('r_stk')

            # Set the position to the last added item
            list_of_results = self.sel_result._values
            position = list_of_results[-1]
            self.sel_result.set(position)
            self.result_selected(position)

    def clear_results(self):
        quit_dialog = CTkMessagebox(title="Clear results", message="Are you sure you want to clear the entire dataset in the results?",
                                    icon="warning", option_1="No", option_2="Yes")
        response = quit_dialog.get()
        if response == "Yes":
            eleana.results_dataset = []
            eleana.selections['result'] = -1
            self.sel_result.configure(values = ['None'])
            self.r_stk.configure(values = [])
            self.resultFrame.grid_remove()
            grapher.plot_graph()

    def clear_dataset(self):
        quit_dialog = CTkMessagebox(title="Clear dataset",
                                    message="Are you sure you want to clear the entire dataset?",
                                    icon="warning", option_1="No", option_2="Yes")
        response = quit_dialog.get()
        if response == "Yes":
            init.main_window(app, eleana)
            self.resultFrame.grid_remove()
            self.firstComplex.grid_remove()
            self.firstStkFrame.grid_remove()
            self.secondComplex.grid_remove()
            self.secondStkFrame.grid_remove()

            init.eleana_variables(eleana)
            grapher.plot_graph()


    # FILE
    # --- Load Project
    def load_project(self, recent=None):
        project = load.load_project(recent)
        print(project['assignmentToGroups'])
        eleana.selections = project['selections']
        eleana.dataset = project['dataset']
        eleana.results_dataset = project['results_dataset']
        eleana.assignmentToGroups = project['assignmentToGroups']
        eleana.groupsHierarchy = project['groupsHierarchy']
        eleana.notes = project['notes']
        update.dataset_list()
        update.all_lists()
        try:
            selected_value_text = eleana.dataset[eleana.selections['first']].name_nr
            self.first_selected(selected_value_text)
            self.sel_first.set(selected_value_text)
        except:
            pass
        try:
            selected_value_text = eleana.dataset[eleana.selections['second']].name_nr
            self.second_selected(selected_value_text)
            self.sel_second.set(selected_value_text)
        except:
            pass
        try:
            selected_value_text = eleana.dataset[eleana.selections['result']].name_nr
            self.result_selected(selected_value_text)
            self.sel_result.set(selected_value_text)
        except:
            pass
        grapher.plot_graph()

    def load_recent(self, selected_value_text):
        index = selected_value_text.split('. ')
        index = int(index[0])
        index = index - 1
        recent = eleana.paths['last_projects'][index]
        self.load_project(recent)
        eleana.paths['last_project_dir'] = Path(recent).parent
        grapher.plot_graph()

    # --- Save as
    def save_as(self):
        report = save.save_project()
        if report['error']:
            CTkMessagebox(title="Error", message=report['desc'], icon="cancel")
        else:
            last_projects = eleana.paths['last_projects']
            last_projects.insert(0, report['return'].name)

        # Remove duplications and limit the list to 10 items
        last_projects = list(set(last_projects))

        # Write the list to eleana.paths
        eleana.paths['last_projects'] = last_projects
        eleana.paths['last_project_dir'] = Path(last_projects[0]).parent

        # Perform update to place the item into menu
        update.last_projects_menu()

    # --- Import EPR --> Bruker Elexsys

    def import_elexsys(self):
        ''' Open window that loads the spectra '''
        load.loadElexsys()
        update.dataset_list()
        update.all_lists()

    # --- Quit (also window close by clicking on X)
    def close_application(self):
        quit_dialog = CTkMessagebox(title="Quit", message="Do you want to close the program?",
                                    icon="warning", option_1="No", option_2="Yes")
        response = quit_dialog.get()
        if response == "Yes":

            # Save current settings:
            filename = Path(eleana.paths['home_dir'], '.EleanaPy', 'paths.pic')
            content = eleana.paths

            with open(filename, 'wb') as file:
                pickle.dump(content, file)

            self.mainwindow.iconify()
            self.mainwindow.destroy()

    # EDIT Menu:
    #   Notes
    def notes(self):
        filename = menuAction.notes()
        # Grab result
        file_back = eleana.read_tmp_file(filename)
        eleana.notes = json.loads(file_back)

    def create_new_group(self):
        group_create = Groupcreate(self.mainwindow, eleana)
        response = group_create.get()
        update.list_in_combobox('sel_group')

    def first_to_group(self):
        if eleana.selections['first'] < 0:
            return
        group_assign = Groupassign(app, eleana, 'first')
        response = group_assign.get()
        update.group_list()
        update.all_lists()
        print(eleana.assignmentToGroups)

    def second_to_group(self):
        if eleana.selections['second'] < 0:
            return
        group_assign = Groupassign(app, eleana, 'second')
        response = group_assign.get()

    ''' Commands for Graph Switches and buttons '''
    def switch_autoscale_x(self):
        autoscaling = {'x':self.check_autoscale_x.get(), 'y':grapher.autoscaling['y']}
        grapher.autoscale(autoscaling)
        grapher.plot_graph()
    def switch_autoscale_y(self):
        autoscaling = {'y':self.check_autoscale_y.get(), 'x':grapher.autoscaling['x']}
        grapher.autoscale(autoscaling)
        grapher.plot_graph()

    def set_log_scale_x(self):
        pass

    def execute_command(self,event):
        if event.keysym == "Up":
            try:
                previous = self.command_history['index'] - 1
                self.command_history['index'] = previous
                previous_command = self.command_history['lines'][previous]
                self.command_line.delete(0, "end")
                self.command_line.insert(0, previous_command)
            except:
                pass
            return
        if event.keysym == "Down":
            try:
                previous = self.command_history['index'] + 1
                self.command_history['index'] = previous
                previous_command = self.command_history['lines'][previous]
                self.command_line.delete(0, "end")
                self.command_line.insert(0, previous_command)
            except:
                pass
            return

        if event.keysym == "Return":
            command = self.command_line.get()
            self.command_history['lines'].append(command)
            self.command_history['index'] = len(self.command_history['lines']) - 1

            new_log = '\n>>> ' + command
            self.log_field.insert("end", new_log)
            self.command_line.delete(0, "end")

            stdout_backup = sys.stdout
            sys.stdout = io.StringIO()

            try:
                #exec(command, globals(), locals())
                eval(command, globals(), locals())
                output = sys.stdout.getvalue()
            except Exception as e:
                output = f"Error: {e}"
            finally:
                sys.stdout = stdout_backup

            new_log = '\n' + output
            self.log_field.insert("end", new_log)
            return output

# --- GENERAL BATCH METHODS ---

def get_index_by_name(selected_value_text):
    ''' Function returns index in dataset of spectrum
        having the name_nr '''
    i = 0
    while i < len(eleana.dataset):
        name = eleana.dataset[i].name_nr
        if name == selected_value_text:
            return i
        i += 1


''' Starting application'''
# Set default color appearance
ctk.set_appearance_mode("dark")

# Create general main instances for the program
eleana = Eleana()                # This contains all data, settings and selections etc.
app = EleanaMainApp(eleana)      # This is GUI
update = Update(app, eleana)     # This contains methods for update things like lists, settings, gui, groups etc.
load = Load(eleana)
save = Save(eleana)
grapher = Grapher(app, eleana)
init = Init(app, eleana, grapher)
#------------

# Initialize basic settings: geometry, icon, graph, binding, etc
init.main_window()
init.paths(update)
init.folders()
init.graph()


# Create Graph canvas
grapher.plot_graph()
# Hide or show widgets in GUI
update.gui_widgets()
update.all_lists()
# Set graph Frame scalable
app.graphFrame.columnconfigure(0, weight=1)
app.graphFrame.rowconfigure(0, weight=1)


# Run
if __name__ == "__main__":
    app.run()
