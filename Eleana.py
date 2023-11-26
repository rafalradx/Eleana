#!/usr/bin/python3

# Import Python Modules
print("IMPORT PYTHON MODULES")
import json
import pickle
import copy
import pathlib
from pathlib import Path
import customtkinter
import customtkinter as ctk
import pygubu
import numpy as np
import io
import sys
import pandas
import pyperclip

# Third-party modules fin Eleana project
print("Load third-party modules.")
from modules.CTkListbox import *
from modules.CTkMessagebox import CTkMessagebox
from modules.CTkColorPicker import *

# Import Eleana specific classes
from assets.GeneralEleana import Eleana
from assets.LoadSave import Load, Save, Export
from assets.Initialization import Init
from assets.Grapher import Grapher, GraphPreferences
from assets.Update import Update
from assets.Menu import ContextMenu, MainMenu

# Import Eleana subprograms and windows
from subprogs.group_edit.add_group import Groupcreate
from subprogs.group_edit.stack_to_group import StackToGroup
from subprogs.group_edit.assign_to_group import Groupassign
from subprogs.user_input.single_dialog import SingleDialog
from subprogs.select_data.select_data import SelectData
from subprogs.notepad.notepad import Notepad
from subprogs.table.table import CreateFromTable

# Widgets used by main application
from widgets.CTkHorizontalSlider import CTkHorizontalSlider

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
        builder.connect_callbacks(self)
        # END OF PYGUBU BUILDER

        # Create references to Widgets and Frames
        self.switch_comparison = builder.get_object("switch_comp_view", self.mainwindow)
        self.sel_group = builder.get_object("sel_group", self.mainwindow)
        self.sel_first = builder.get_object("sel_first", self.mainwindow)
        self.sel_second = builder.get_object("sel_second", self.mainwindow)
        self.sel_result = builder.get_object("sel_result", self.mainwindow)
        self.listFrame = builder.get_object("listFrame", self.mainwindow)
        self.listFrame.grid_remove()
        self.firstFrame = builder.get_object("firstFrame", self.mainwindow)
        self.secondFrame = builder.get_object("secondFrame", self.mainwindow)
        self.resultFrame = builder.get_object("resultFrame", self.mainwindow)
        self.resultStkFrame = builder.get_object("resultStkFrame", self.mainwindow)
        self.firstStkFrame = builder.get_object("firstStkFrame", self.mainwindow)
        self.secondStkFrame = builder.get_object("secondStkFrame", self.mainwindow)
        self.firstComplex = builder.get_object("firstComplex", self.mainwindow)
        self.secondComplex = builder.get_object("secondComplex", self.mainwindow)
        self.resultComplex = builder.get_object("resultComplex", self.mainwindow)
        self.graphFrame = builder.get_object('graphFrame', self.mainwindow)
        self.swapFrame = builder.get_object('swapFrame', self.mainwindow)
        self.f_stk = builder.get_object('f_stk', self.mainwindow)
        self.s_stk = builder.get_object('s_stk', self.mainwindow)
        self.r_stk = builder.get_object('r_stk', self.mainwindow)
        self.btn_clear_results = builder.get_object('btn_clear_results', self.mainwindow)
        self.check_first_show = builder.get_object('check_first_show', self.mainwindow)
        self.check_second_show = builder.get_object('check_second_show', self.mainwindow)
        self.check_result_show = builder.get_object('check_result_show', self.mainwindow)
        self.annotationsFrame = builder.get_object('annotationsFrame', self.mainwindow)

        # Graph Buttons
        self.check_autoscale_x = builder.get_object('check_autoscale_X', self.mainwindow)
        self.check_autoscale_y = builder.get_object('check_autoscale_Y', self.mainwindow)
        self.check_log_x = builder.get_object('check_log_x', self.mainwindow)
        self.check_log_y = builder.get_object('check_log_y', self.mainwindow)
        self.check_indexed_x = builder.get_object('check_indexed_x', self.mainwindow)
        self.sel_cursor_mode = builder.get_object('sel_cursor_mode', self.mainwindow)
        self.check_invert_x = builder.get_object('check_invert_x', self.mainwindow)

        # Command line
        self.command_line = builder.get_object('command_line', self.mainwindow)
        self.command_line.bind("<Return>", self.execute_command)
        self.command_line.bind("<Up>", self.execute_command)
        self.command_line.bind("<Down>", self.execute_command)
        self.command_history = {'index':0, 'lines':[]}
        self.log_field = builder.get_object('log_field', self.mainwindow)

        # Paned windows
        try:
            self.panedwindow2 = builder.get_object('panedwindow2', self.mainwindow)
            self.panedwindow4 = builder.get_object('panedwindow4', self.mainwindow)
            self.pane5 = builder.get_object('pane5', self.mainwindow)
            self.pane9 = builder.get_object('pane9', self.mainwindow)
        except:
            print('Unable to resize paned window.')

        # Keyboard bindings
        self.mainwindow.bind("<Control-c>", self.copy_to_clipboard)
        self.mainwindow.bind("<Control-s>", self.save_as)
        self.mainwindow.bind("<Control-q>", self.close_application)
        self.mainwindow.bind("<Control-o>", self.load_project)
        self.mainwindow.bind("<Control-v>", self.quick_paste)

        # This keeps the information if any information or dialog should be displayed.
        # This is useful to constantly display the same information in a loop etc.
        self.info_show = True
        self.repeated_items = []

        # Comparison view
        self.comparison_settings = {'vsep': 0, 'hsep': 0, 'indexes': (), 'v_factor':'1', 'h_factor':'1'}

    def set_pane_height(self):
        self.mainwindow.update_idletasks()
        self.panedwindow2.sashpos(0, 700)
        self.panedwindow4.sashpos(0, 300)
        return

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def run(self):
            self.mainwindow.deiconify()
            self.mainwindow.after(100, self.set_pane_height)
            self.mainwindow.mainloop()

    ''' *********************************************
    *                                               *
    *              COMPARISON VIEW                  *
    *                                               *
    **********************************************'''
    def comparison_view(self):
        self.info_show =True
        self.repeated_items = []
        comparison_mode = bool(self.switch_comparison.get())
        if comparison_mode:
            self.firstFrame.grid_remove()
            self.secondFrame.grid_remove()
            self.resultFrame.grid_remove()
            self.swapFrame.grid_remove()
            self.listFrame.grid(column=0, row = 2, rowspan=3)
            self.listbox = CTkListbox(self.listFrame, command=self.list_selected, multiple_selection=True, height=400)
            self.listbox.grid(column=0, columnspan=1, rowspan=4, padx=4, pady=4, row=0, sticky="nsew")
            self.ver_slider = CTkHorizontalSlider('Vertical separation', 'vsep', [0,1], self.listFrame, self)
            self.ver_slider.grid(column=0, columnspan=1, rowspan=3, padx=4, pady=4, row=5, sticky="nsew")
            self.hor_slider = CTkHorizontalSlider('Horizontal separation', 'hsep', [-1,1], self.listFrame, self)
            self.hor_slider.grid(column=0, columnspan=1, rowspan=3, padx=4, pady=4, row=8, sticky="nsew")
            self.ver_slider.factor.delete(0, 'end')
            self.ver_slider.factor.insert(0, self.comparison_settings['v_factor'])
            self.hor_slider.factor.delete(0, 'end')
            self.hor_slider.factor.insert(0, self.comparison_settings['h_factor'])

            # Get names from group to be used for the list
            group = eleana.selections['group']
            names_nr = []
            indexes = []
            if group == 'All':
                i = 0
                while i < len(eleana.dataset):
                    names_nr.append(eleana.dataset[i].name_nr)
                    indexes.append(i)
                    i += 1
            else:
                indexes = eleana.assignmentToGroups[group]
                for i in indexes:
                    names_nr.append(eleana.dataset[i].name_nr)
            i = 0
            while i < len(names_nr)-1:
                self.listbox.insert(indexes[i], names_nr[i])
                i += 1
            try:
                self.listbox.insert("END", names_nr[i])
            except:
                pass
            if len(self.comparison_settings['indexes']) > 0:
                for each in self.comparison_settings['indexes']:
                    self.listbox.activate(each)
            self.list_selected()
        else:
            self.listFrame.grid_remove()
            self.firstFrame.grid()
            self.secondFrame.grid()
            self.swapFrame.grid()
            if len(eleana.results_dataset) > 0:
                self.resultFrame.grid()
            grapher.plot_graph()

    def separate_plots_by(self, direction=None, value=None):
        self.mainwindow.config(cursor="watch")
        if direction != None or value != None:
            self.comparison_settings[direction] = value
        vsep = np.array([0])
        vstep = self.comparison_settings['vsep']
        hsep = np.array([0])
        hstep = self.comparison_settings['hsep']
        i = 1
        while i < len(self.comparison_settings['indexes']):
            next_h = i * hstep
            next_v = i * vstep
            vsep = np.append(vsep, next_v)
            hsep = np.append(hsep, next_h)
            i += 1

        grapher.plot_comparison(self.comparison_settings['indexes'], vsep, hsep)
        self.comparison_settings['v_factor'] = self.ver_slider.factor.get()
        self.comparison_settings['h_factor'] = self.hor_slider.factor.get()
        self.mainwindow.config(cursor='arrow')

    def list_selected(self, selected_items=None):
        if selected_items != None:
            previous_selection = self.comparison_settings['indexes']
            self.repeated_items.extend(selected_items)
            for each in selected_items:
                index = int(get_index_by_name(each))
                type = eleana.dataset[index].type
                name_nr = eleana.dataset[index].name_nr
                if name_nr in set(self.repeated_items):
                    self.info_show = True
                if type == 'stack 2D' and self.info_show:
                    info = 'Data "' + name_nr + '" is a 2D stack. You need to convert the stack into a group to display it.'
                    CTkMessagebox(title="", message=info)
                    selected_stack = self.listbox.curselection()
                    difference = set(selected_stack) - set(previous_selection)
                    difference = list(difference)
                    if len(difference) > 0:
                        self.listbox.deselect(difference[0])
                    self.info_show = False
                    return

            items_list = []
            for each in selected_items:
                items_list.append(int(get_index_by_name(each)))
            items_list.sort()
            self.comparison_settings['indexes'] = tuple(items_list)
            self.separate_plots_by()
        else:
            self.comparison_settings['indexes'] = ()
            grapher.clear_plot()

    ''' *********************************************
    *                                               *
    *              COMBOBOX SELECTIONS              *
    *                                               *
    **********************************************'''

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
        self.sel_first.set('None')
        self.sel_second.set('None')
        self.eleana.selections['first'] = - 1
        self.eleana.selections['second'] = - 1
        update.gui_widgets()
        grapher.plot_graph()
        self.comparison_view()

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
        spectrum = copy.deepcopy(eleana.dataset[index])

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

    ''' ***************************************
    *                RESULT                   *
    ****************************************'''

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

    def all_results_to_current_group(self):
        if len(self.eleana.results_dataset) == 0:
            return

        for each in self.eleana.results_dataset:
            result = copy.deepcopy(each)
            result.groups = [self.sel_group.get()]
            self.eleana.dataset.append(result)
        update.dataset_list()
        update.all_lists()
        added_item = self.eleana.dataset[-1].name_nr
        group = self.sel_group.get()
        self.group_selected(group)
        self.sel_first.set(added_item)
        self.first_selected(added_item)

    def replace_first(self):
        if self.eleana.selections['result'] < 0:
            return
        index = self.eleana.selections['result']
        index_first = self.eleana.selections['first']
        result = copy.deepcopy(self.eleana.results_dataset[index])
        result.groups = [self.sel_group.get()]
        self.eleana.dataset.pop(index_first)
        self.eleana.dataset.insert(index_first, result)
        update.dataset_list()
        update.all_lists()
        group = self.sel_group.get()
        self.group_selected(group)
        name = self.eleana.dataset[index_first].name_nr
        print(name)
        self.first_selected(name)
        self.sel_first.set(name)

    def result_to_main(self):
        if self.eleana.selections['result'] < 0:
            return
        index = self.eleana.selections['result']
        result = copy.deepcopy(self.eleana.results_dataset[index])
        result.groups = [self.sel_group.get()]
        self.eleana.dataset.append(result)
        update.dataset_list()
        update.all_lists()
        added_item = self.eleana.dataset[-1].name_nr
        group = self.sel_group.get()
        self.group_selected(group)
        self.sel_first.set(added_item)
        self.first_selected(added_item)


    def delete_sel_result(self):
        index = eleana.selections['result']
        if index < 0:
            return
        eleana.results_dataset.pop(index)
        eleana.selections['result'] = -1
        update.all_lists()
        update.gui_widgets()
        self.sel_result.set('None')
        grapher.plot_graph()

    def first_to_result(self):
            current = self.sel_first.get()
            if current == 'None':
                 return
            index = get_index_by_name(current)
            spectrum = copy.deepcopy(eleana.dataset[index])

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
            grapher.plot_graph()

    ''' *****************************************
    *                                           *
    *                MAIN MENU                  *
    *                                           *
    ******************************************'''

    ''' EDIT: Delete selected data                             '''
    def delete_selected_data(self):
        current_first = self.sel_first.get()
        current_second = self.sel_second.get()
        av_data = self.sel_first._values
        av_data.pop(0)
        # Open dialog
        selected_data = SelectData(master=app.mainwindow, title='Select data', group=eleana.selections['group'], items=av_data)
        response = selected_data.get()
        if response == None:
            return
        # Get indexes of selected data to remove
        indexes = []
        for each in response:
            index = get_index_by_name(each)
            indexes.append(index)
        # Delete data with selected indexes
        indexes.sort(reverse = True)
        for each in indexes:
            eleana.dataset.pop(each)
        # Set all data to None

        eleana.selections['first'] = -1
        eleana.selections['second'] = -1
        self.sel_first.set('None')
        self.sel_first.set('None')
        self.comparison_settings['indexes'] = []
        update.dataset_list()
        update.group_list()
        update.all_lists()
        update.gui_widgets()
        self.comparison_view()


    ''' EDIT: Delete Results dataset                            '''
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

    ''' EDIT: Delete Main Dataset dataset                            '''
    def clear_dataset(self):
        quit_dialog = CTkMessagebox(title="Clear dataset",
                                    message="Are you sure you want to clear the entire dataset?",
                                    icon="warning", option_1="No", option_2="Yes")
        response = quit_dialog.get()
        if response == "Yes":
            init.main_window()
            self.resultFrame.grid_remove()
            self.firstComplex.grid_remove()
            self.firstStkFrame.grid_remove()
            self.secondComplex.grid_remove()
            self.secondStkFrame.grid_remove()

            init.eleana_variables()
            grapher.plot_graph()

    ''' EDIT: Graph preferences                                     '''
    def graph_preferences(self):
        pick_color = AskColor()  # open the color picker
        color = pick_color.get()  # get the color string
        print(color)

    ''' FILE: Load Project                                          '''
    def load_project(self, event=None, recent=None):
        project = load.load_project(recent)
        if len(self.eleana.dataset) > 0:
            question = CTkMessagebox(title="Dataset is not empty", message="There are data in the dataset. Choose what you want to",
                        icon="question", option_3="Append to the dataset", option_2="Replace the dataset", option_1="Cancel")
            response = question.get()
            if response == None or response == 'Cancel':
                return
            elif response == 'Replace the dataset':
                eleana.selections = project['selections']
                eleana.dataset = project['dataset']
                eleana.results_dataset = project['results_dataset']
                eleana.assignmentToGroups = project['assignmentToGroups']
                eleana.groupsHierarchy = project['groupsHierarchy']
                eleana.notes = project['notes']
            else:
                eleana.dataset.extend(project['dataset'])
                eleana.results_dataset.extend(project['results_dataset'])
        else:
            eleana.selections = project['selections']
            eleana.dataset = project['dataset']
            eleana.results_dataset = project['results_dataset']
            eleana.assignmentToGroups = project['assignmentToGroups']
            eleana.groupsHierarchy = project['groupsHierarchy']
            eleana.notes = project['notes']

        update.dataset_list()
        update.get_groups()
        update.all_lists()
        path_to_file = Path(eleana.paths['last_projects'][0])
        name = path_to_file.name
        app.mainwindow.title(name + ' - Eleana')

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
            selected_value_text = eleana.results_dataset[eleana.selections['result']].name
            self.result_selected(selected_value_text)
            self.sel_result.set(selected_value_text)
        except:
            pass
        grapher.plot_graph()

    ''' FILE: Load Recent project                                     '''
    def load_recent(self, selected_value_text):
        index = selected_value_text.split('. ')
        index = int(index[0])
        index = index - 1
        recent = eleana.paths['last_projects'][index]
        self.load_project(recent=recent)
        eleana.paths['last_project_dir'] = Path(recent).parent
        grapher.plot_graph()

    ''' FILE: Save As                                                 '''
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
        app.mainwindow.title(Path(last_projects[0]).name[:-4] + ' - Eleana')

    '''******************************************
    *                                           *
    *          IMPORT EXTERNAL DATA             *
    *                                           *
    *********************************************'''
    def import_elexsys(self):
        ''' Open window that loads the spectra '''
        load.loadElexsys()
        update.dataset_list()
        update.all_lists()

    def import_EMX(self):
        load.loadEMX()
        update.dataset_list()
        update.all_lists()

    def import_magnettech1(self):
        load.loadMagnettech(1)
        update.dataset_list()
        update.all_lists()

    def import_magnettech2(self):
        load.loadMagnettech(2)
        update.dataset_list()
        update.all_lists()

    def import_adani_dat(self):
        load.loadAdaniDat()
        update.dataset_list()
        update.all_lists()

    def import_shimadzu_spc(self):
        load.loadShimadzuSPC()
        update.dataset_list()
        update.all_lists()

    def import_ascii(self, clipboard = None):
        load.loadAscii(clipboard)
        update.dataset_list()
        update.groups()
        update.all_lists()

    def load_excel(self):
        x = [['', ''], ['', '']]
        headers = ['A', 'B']
        empty = pandas.DataFrame(x, columns=headers)
        table = CreateFromTable(eleana_app=self.eleana, master=self.mainwindow, df=empty, loadOnStart='excel')
        response = table.get()
        update.dataset_list()
        update.groups()
        update.all_lists()

    def quick_paste(self, event = None):
        text = pyperclip.paste()
        self.import_ascii(text)
        print(text)

    def export_first(self):
        export.csv('first')

    def export_group(self):
        export.group_csv(eleana.selections['group'])

    # --- Quit (also window close by clicking on X)
    def close_application(self, event = None):
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
        notes = Notepad(master = self.mainwindow, title="Edit notes", text = self.eleana.notes)
        response = notes.get()
        if response == None:
            return
        else:
            eleana.notes = response

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

    def second_to_group(self):
        if eleana.selections['second'] < 0:
            return
        group_assign = Groupassign(app, eleana, 'second')
        response = group_assign.get()

    '''***********************************************
    *                                                *
    *           GRAPH SWITCHES AND BUTTONS           *
    *                                                *  
    ***********************************************'''
    def switch_autoscale_x(self):
        autoscaling = {'x':self.check_autoscale_x.get(), 'y':grapher.autoscaling['y']}
        grapher.autoscale(autoscaling)
        grapher.plot_graph()
    def switch_autoscale_y(self):
        autoscaling = {'y':self.check_autoscale_y.get(), 'x':grapher.autoscaling['x']}
        grapher.autoscale(autoscaling)
        grapher.plot_graph()

    def set_log_scale_x(self):
        grapher.log_scales['x'] = bool(self.check_log_x.get())
        grapher.plot_graph()

    def set_log_scale_y(self):
        grapher.log_scales['y'] = bool(self.check_log_y.get())
        grapher.plot_graph()

    def indexed_x(self):
        grapher.indexed_x = bool(self.check_indexed_x.get())
        grapher.plot_graph()

    def invert_x_axis(self):
        grapher.inverted_x_axis = bool(self.check_invert_x.get())
        grapher.plot_graph()

    '''***********************************************
    *                                                *
    *                    CURSORS                     *
    *                                                *  
    ***********************************************'''

    def clear_cursors(self):
        grapher.clear_all_annotations()
    def sel_graph_cursor(self, value):
         grapher.clear_all_annotations(True)
         grapher.current_cursor_mode['label'] = value
         grapher.plot_graph()

    '''***********************************************
    *                                                *
    *           METHODS FOR CONTEXT MENU             *
    *                                                *  
    ***********************************************'''

    def stack_to_group(self, which):
        index = eleana.selections[which]
        if index < 0:
            return
        data = copy.deepcopy(eleana.dataset[index])
        if not data.type == 'stack 2D':
            CTkMessagebox(title="Conversion to group", message="The data you selected is not a 2D stack")
        else:
            select_group = StackToGroup(app, eleana, which)
            response = select_group.get()
            if response == None:
                return
            update.dataset_list()
            update.group_list()
            update.all_lists()
    def rename_data(self, which):
        index = eleana.selections[which]
        index_f = eleana.selections['first']
        index_s = eleana.selections['second']
        index_r = eleana.selections['result']
        if index < 0:
            return
        name = eleana.dataset[index].name
        if which == 'first':
            title = 'Rename First'
        elif which == 'second':
            title = 'Rename Second'
        elif which == 'result':
            title = 'Rename Result'
            name = eleana.results_dataset[index_r].name
        dialog = SingleDialog(master=app, title=title, label='Enter new name', text=name)
        response = dialog.get()
        if response == None:
            return
        if not which == 'result':
            eleana.dataset[index].name = response
            update.dataset_list()
            update.group_list()
            update.all_lists()
            if index_f >= 0:
                self.sel_first.set(eleana.dataset[index_f].name_nr)
            if index_s >= 0:
                self.sel_second.set(eleana.dataset[index_s].name_nr)
        else:
            eleana.results_dataset[index_r].name = response
            eleana.results_dataset[index_r].name_nr = response
            update.dataset_list()
            update.all_lists()
        if index_r >= 0:
            self.sel_result.set(eleana.results_dataset[index_r].name_nr)

    def edit_comment(self, which):
        index = eleana.selections[which]
        if index < 0:
            return
        comment = eleana.dataset[index].comment
        name = 'Comment to: ' + str(eleana.dataset[index].name_nr)
        text = Notepad(self.mainwindow, title = name, text = comment)
        response = text.get()
        eleana.dataset[index].comment = response

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
                eval(command, globals(), locals())
                output = sys.stdout.getvalue()
            except Exception as e:
                output = f"Error: {e}"
            finally:
                sys.stdout = stdout_backup

            new_log = '\n' + output
            self.log_field.insert("end", new_log)
            return output

    ''' Keyboard bindings '''
    def copy_to_clipboard(self, event):
        print('Copy to clipboard')

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
print('INITIATE ELEANA: ', end="")
eleana = Eleana()
print('create GUI, ', end="")
app = EleanaMainApp(eleana)      # This is GUI
print('build grapher, ', end="")
grapher = Grapher(app, eleana)
load = Load(app, eleana)
save = Save(eleana)
export = Export(eleana)

print('build menu')
main_menu = MainMenu(app, eleana)
init = Init(app, eleana, grapher, main_menu)
context_menu = ContextMenu(app, eleana)
update = Update(app, eleana, main_menu)     # This contains methods for update things like lists, settings, gui, groups etc.


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
