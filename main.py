import sys
# BASIC CONFIGURATION
ELEANA_VERSION = 1              # Set the Eleana version. This will be stored in self.eleana.version
INTERPRETER = sys.executable    # Defines python version
DEVEL = True                    # For final product set to False - no errors will be displayed or print commands
                                # For development set to True. This is stored in self.eleana.devel_mode

# Import basic modules and add ./modules to sys.path
from pathlib import Path
import copy
import io
import re
import os
# Set paths for assets, modules, subprogs and widgets
PROJECT_PATH = Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "Eleana_interface.ui"
MODULES = PROJECT_PATH / "modules"
ASSETS = PROJECT_PATH / "assets"
SUBPROGS = PROJECT_PATH / "subprogs"
WIDGETS = PROJECT_PATH / "widgets"
PIXMAPS = PROJECT_PATH / "pixmaps"

sys.path.insert(0, str(MODULES))
sys.path.insert(0, str(ASSETS))
sys.path.insert(0, str(SUBPROGS))
sys.path.insert(0,str(WIDGETS))

# Import External modules required
import numpy as np
import pandas
import pyperclip

# Import modules from ./modules folder
import pygubu
from CTkListbox import CTkListbox
from CTkMessagebox import CTkMessagebox

# Import Eleana specific classes
from Eleana import Eleana
from LoadSave import Load, Save, Export
from Init import Init
from Grapher import Grapher
from Update import Update
from Menu import ContextMenu, MainMenu
from Sounds import Sound
from Error import Error
from CommandProcessor import CommandProcessor
from DataClasses import Stack

# Import Eleana subprograms and windows
# append.(['name of instance without self., 'Command to close']

list_of_subprogs = []
from polynomial_baseline.Polynomial_baseline import PolynomialBaseline
list_of_subprogs.append(['subprog_polynomial_baseline', 'cancel'])
from distance_read.Distance_read import DistanceRead
list_of_subprogs.append(['xy_distance', 'cancel'])
from integrate_region.IntegrateRegion import IntegrateRegion
list_of_subprogs.append(['integrate_region', 'cancel'])
from normalize.Normalize import Normalize
list_of_subprogs.append(['normalize', 'cancel'])
from group_edit.add_group import Groupcreate
list_of_subprogs.append(['group_create', 'cancel'])
from group_edit.assign_to_group import Groupassign
list_of_subprogs.append(['group_assign', 'cancel'])
from user_input.single_dialog import SingleDialog
list_of_subprogs.append(['single_dialog', 'cancel'])
from select_data.select_data import SelectData
list_of_subprogs.append(['select_items', 'cancel'])
from select_data.select_items import SelectItems
list_of_subprogs.append(['select_data', 'cancel'])
from notepad.notepad import Notepad
list_of_subprogs.append(['notepad', 'cancel'])
from table.table import CreateFromTable
list_of_subprogs.append(['spreadsheet', 'cancel'])
from edit_parameters.edit_parameters import EditParameters
list_of_subprogs.append(['edit_par', 'cancel'])
from modify.modify import ModifyData
list_of_subprogs.append(['modify_data', 'cancel'])
from group_edit.move_to_group import MoveToGroup
list_of_subprogs.append(['move_to_group', 'cancel'])
from preferences.preferences import PreferencesApp
list_of_subprogs.append(['prefereces', 'cancel'])
from group_edit.stack_to_group import StackToGroup
list_of_subprogs.append(['convert_stack_to_group', 'cancel'])

# Widgets used by main application
from widgets.CTkHorizontalSlider import CTkHorizontalSlider

class MainApp:
    def __init__(self, eleana_instance, command_processor, master=None):
        # Initialize eleana
        self.eleana = eleana_instance
        self.notify = self.eleana.notify_on
        self.commandprocessor = command_processor
        self.devel = DEVEL

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

        # Frames must be configured due to a bug in Pygubu
        self.selectionsFrame = builder.get_object("selectionsFrame", self.mainwindow)
        self.groupFrame = builder.get_object("groupFrame", self.mainwindow)
        self.rightFrame = builder.get_object("rightFrame", self.mainwindow)
        self.graphButtons = builder.get_object('graphButtons', self.mainwindow)
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
        self.btn_clear_cursors = builder.get_object("btn_clear_cursors", self.mainwindow)
        self.info = builder.get_object('info', self.mainwindow)
        self.infoframe = builder.get_object('infoframe', self.mainwindow)
        self.infoframe.grid_remove()
        self.btn_clear_cursors.grid_remove()
        self.annotationsFrame.grid_remove()

        # Command line
        self.command_line = builder.get_object('command_line', self.mainwindow)
        self.command_line.bind("<Return>", self.execute_command)
        self.command_line.bind("<Up>", self.execute_command)
        self.command_line.bind("<Down>", self.execute_command)
        self.command_history = {'index': 0, 'lines': []}
        self.log_field = builder.get_object('log_field', self.mainwindow)

        # Paned windows
        self.panedwindow2 = builder.get_object('panedwindow2', self.mainwindow)
        self.panedwindow4 = builder.get_object('panedwindow4', self.mainwindow)
        self.pane5 = builder.get_object('pane5', self.mainwindow)
        self.pane9 = builder.get_object('pane9', self.mainwindow)
        #self.pane6 = builder.get_object('pane6', self.mainwindow)

        # Keyboard bindings
        self.mainwindow.bind("<Control-c>", self.copy_to_clipboard)
        self.mainwindow.bind("<Control-s>", self.save_current)
        self.mainwindow.bind("<Control-q>", self.close_application)
        self.mainwindow.bind("<Control-o>", self.load_project)
        self.mainwindow.bind("<Control-v>", self.quick_paste)

        # This keeps the information if any information or dialog should be displayed.
        # This is useful to constantly display the same information in a loop etc.
        self.info_show = True
        self.repeated_items = []

        # Comparison view
        self.comparison_settings = {'vsep': 0, 'hsep': 0, 'indexes': (), 'v_factor': '1', 'h_factor': '1'}

        # Ctk styles
        self.gui_appearence = 'light'
        self.color_theme = 'dark-blue'

    def set_grapher(self, grapher):
        self.grapher = grapher

    def set_update(self, update):
        self.update = update

    def set_pane_height(self):
        self.mainwindow.update_idletasks()
        self.panedwindow2.sashpos(0, 700)
        self.panedwindow4.sashpos(0, 300)
        self.pane5.sashpos(0, 1000)

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def run(self):
        self.mainwindow.after(100, self.set_pane_height)
        self.mainwindow.deiconify()
        self.mainwindow.mainloop()

    ''' *********************************************
    *              COMPARISON VIEW                  *
    **********************************************'''

    def comparison_view(self):
        self.info_show = True
        self.repeated_items = []
        comparison_mode = bool(self.switch_comparison.get())
        if comparison_mode:
            self.graphButtons.grid_remove()
            self.firstFrame.grid_remove()
            self.secondFrame.grid_remove()
            self.resultFrame.grid_remove()
            self.swapFrame.grid_remove()
            self.listFrame.grid(column=0, row=2, rowspan=3)
            self.listbox = CTkListbox(self.listFrame, command=self.list_selected, multiple_selection=True, height=400)
            self.listbox.grid(column=0, columnspan=1, rowspan=4, padx=4, pady=4, row=0, sticky="nsew")

            self.ver_slider = CTkHorizontalSlider('Vertical separation', 'vsep', [0, 1], self.listFrame, self)
            self.ver_slider.grid(column=0, columnspan=1, rowspan=3, padx=4, pady=4, row=5, sticky="nsew")

            self.hor_slider = CTkHorizontalSlider('Horizontal separation', 'hsep', [-1, 1], self.listFrame, self)
            self.hor_slider.grid(column=0, columnspan=1, rowspan=3, padx=4, pady=4, row=8, sticky="nsew")
            self.ver_slider.factor.delete(0, 'end')
            self.ver_slider.factor.insert(0, self.comparison_settings['v_factor'])
            self.hor_slider.factor.delete(0, 'end')
            self.hor_slider.factor.insert(0, self.comparison_settings['h_factor'])

            # Get names from group to be used for the list
            group = self.eleana.selections['group']
            names_nr = []
            indexes = []
            if group == 'All':
                i = 0
                while i < len(self.eleana.dataset):
                    names_nr.append(self.eleana.dataset[i].name_nr)
                    indexes.append(i)
                    i += 1
            else:
                indexes = self.eleana.assignmentToGroups[group]
                for i in indexes:
                    names_nr.append(self.eleana.dataset[i].name_nr)
            i = 0
            while i < len(names_nr) - 1:
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
            self.graphButtons.grid()
            self.firstFrame.grid()
            self.secondFrame.grid()
            self.swapFrame.grid()
            if len(self.eleana.results_dataset) > 0:
                self.resultFrame.grid()
            self.grapher.plot_graph()

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
        self.grapher.plot_comparison(self.comparison_settings['indexes'], vsep, hsep)
        self.comparison_settings['v_factor'] = self.ver_slider.factor.get()
        self.comparison_settings['h_factor'] = self.hor_slider.factor.get()
        self.mainwindow.config(cursor='arrow')

    def list_selected(self, selected_items=None):
        if selected_items != None:
            previous_selection = self.comparison_settings['indexes']
            self.repeated_items.extend(selected_items)
            for each in selected_items:
                index = int(self.eleana.get_index_by_name(each))
                type = self.eleana.dataset[index].type
                name_nr = self.eleana.dataset[index].name_nr
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
                items_list.append(int(self.eleana.get_index_by_name(each)))
            items_list.sort()
            self.comparison_settings['indexes'] = tuple(items_list)
            self.separate_plots_by()
        else:
            self.comparison_settings['indexes'] = ()
            self.grapher.clear_plot()

    ''' *********************************************
    *              COMBOBOX SELECTIONS              *
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
        self.eleana.set_selections('group', value)
        # self.eleana.selections['group'] = value
        update.all_lists()
        self.sel_first.set('None')
        self.sel_second.set('None')
        self.eleana.set_selections('first', - 1)
        self.eleana.set_selections('second', -1)
        update.gui_widgets()
        self.grapher.plot_graph()
        self.comparison_view()

    def delete_group(self):
        current_group = self.eleana.selections['group']
        if current_group == 'All':
            info = CTkMessagebox(title='',
                                 message="The group 'All' cannot be removed.",
                                 icon='cancel')
            return
        av_data = self.sel_first._values
        av_data.pop(0)
        self.select_data = SelectData(master=app.mainwindow, title='Select data', group=self.eleana.selections['group'],
                                      items=av_data)
        names = self.select_data.get()
        if not names:
            return
        indexes = self.get_indexes_by_name(names)
        if not indexes:
            return
        for index in indexes:
            data_groups = self.eleana.dataset[index].groups
            if current_group in data_groups:
                data_groups.remove(current_group)
                self.eleana.dataset[index].groups = data_groups
        update.dataset_list()
        update.groups()
        update.all_lists()
        if current_group not in self.eleana.assignmentToGroups['<group-list/>']:
            self.sel_group.set('All')
            self.eleana.selections['group'] = 'All'

    def data_to_other_group(self, move = True):
        if self.eleana.selections['group'] == 'All' and move:
            info = CTkMessagebox(title='', message="Data from the 'All' group cannot be moved to another group. However, you can make an additional assignment.",
                             icon='cancel')
            return

        # Select data
        av_data = self.sel_first._values
        av_data.pop(0)
        self.select_data = SelectData(master=app.mainwindow, title='Select data', group=self.eleana.selections['group'],
                                      items=av_data)
        names = self.select_data.get()
        if not names:
            return
        indexes = self.get_indexes_by_name(names)
        if not indexes:
            return

        # Open dialog
        self.move_to_group = MoveToGroup(self.mainwindow, self)
        new_group = self.move_to_group.get()
        if new_group == None:
            return
        elif new_group == 'All' and move:
            info = CTkMessagebox(title = '', message = "You cannot move data from the group 'All' to another one.", icon='cancel')
            return

        # Replace current_group with new_group
        current_group = self.eleana.selections['group']
        for index in indexes:
            groups = self.eleana.dataset[index].groups
            if current_group in groups and move:
                position = groups.index(current_group)
                groups[position] = new_group
                self.eleana.dataset[index].groups = groups
            elif new_group in groups and not move:
                return
            elif new_group not in groups and not move:
                groups.append(new_group)
                self.eleana.dataset[index].groups = groups
            else:
                return
        update.dataset_list()
        update.groups()
        update.all_lists()
        self.sel_group.set('All')

    def delete_data_from_group(self):
        group = self.eleana.selections['group']
        data_indexes = self.eleana.assignmentToGroups.get(group, None)
        if group == 'All':
            info = CTkMessagebox(title = 'Delete Data from Group', message = 'You cannot delete data from the group "All". Please use "Delete Dataset" instead.', icon = 'cancel' )
        else:
            info = CTkMessagebox(title= 'Delete Data from Group', icon="warning", option_1="Cancel", option_2="Delete", message = f'Are you sure you want to delete data from the group "{group}"?')
            response = info.get()
            if response == 'Cancel' or not data_indexes:
                return
        data_indexes = sorted(data_indexes, reverse=True)
        for index in data_indexes:
            self.eleana.dataset.pop(index)
        group_list = self.eleana.assignmentToGroups['<group-list/>']
        if group in group_list:
            group_list.remove(group)
            self.eleana.assignmentToGroups['<group-list/>'] = group_list
        update.dataset_list()
        update.groups()
        update.all_lists()
        update.gui_widgets()
        self.sel_group.set('All')
        self.sel_first.set('None')
        self.sel_second.set('None')

    def convert_group_to_stack(self, all = False):
        if all:
            # Convert whole data in the group to a stack
            indexes = self.eleana.get_indexes_from_group()
        else:
            # Ask to select
            av_data = self.sel_first._values
            av_data.pop(0)
            selected_data = SelectData(master=app.mainwindow, title='Select data', group=self.eleana.selections['group'],
                                      items=av_data)
            response = selected_data.get()
            if response == None:
                return
            indexes = [self.eleana.get_index_by_name(i) for i in response]
        # Check if data are of the same type
        template = self.eleana.dataset[indexes[0]]
        new_stack = {}
        stk_names = []
        list_of_y = []
        for i in indexes:
            compared = self.eleana.dataset[i]
            stk_name = str(i+1) + '_' + template.name
            stk_names.append(stk_name)
            y = compared.y
            list_of_y.append(y)
            parameters = template.parameters
            comment = ''
            if template.type != compared.type:
                info = CTkMessagebox(title='Convert to a Stack', message='At least one of the data elements is of a different type (for example, 2D and 3D).')
                return
            if template.complex != compared.complex:
                info = CTkMessagebox(title='Convert to a Stack', message='At least one of the data elements has a different type of numbers (for example, real and complex).')
                return
            if template.x.size != compared.x.size:
                info = CTkMessagebox(title='Convert to a Stack', message='At least one of the data elements has a different number of points. You can convert the data to a stack only if all of them are the same size.')
                return
            if not np.array_equal(template.x, compared.x):
                dialog = CTkMessagebox(title="Convert to Stack", message="The x-axes of the selected items are not identical. You may still proceed, but the differing axes will be replaced with the x-axis from the first item in the list.", icon="warning", option_1="Cancel", option_2="OK")
                response = dialog.get()
                if response == 'Cancel':
                    return
        # Now create a stack
        name = self.eleana.selections['group'] + ':TO_STACK'
        x = template.x
        y = np.array(list_of_y)
        new_stack = {'parameters':parameters,
                'name':name,
                'stk_names':stk_names,
                'x':x,
                'y':y,
                'origin':'converted from group',
                'type':'stack 2D',
                'name_nr':'',
                'comment':'',
                'complex':template.complex,
                'groups':'All',
                }
        created_stack = Stack(new_stack)
        self.add_to_results(created_stack)

    def first_show(self):
        self.eleana.set_selections('f_dsp', bool(self.check_first_show.get()))
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
            return
        try:
            new_position = list_of_items[index + 1]
            self.sel_first.set(new_position)
            self.first_selected(new_position)
        except IndexError:
            return

    def first_complex_clicked(self, value):
        self.eleana.set_selections('f_cpl', value)
        self.grapher.plot_graph()

    def first_selected(self, selected_value_text):
        if selected_value_text == 'None':
            self.eleana.set_selections('first', -1)
            self.firstComplex.grid_remove()
            self.firstStkFrame.grid_remove()
            self.grapher.plot_graph()
            return
        i = 0
        while i < len(self.eleana.dataset):
            name = self.eleana.dataset[i].name_nr
            if name == selected_value_text:
                self.eleana.set_selections('first', i)
                break
            i += 1
        update.list_in_combobox('sel_first')
        update.list_in_combobox('f_stk')
        if self.eleana.dataset[self.eleana.selections['first']].complex:
            self.firstComplex.grid()
        else:
            self.firstComplex.grid_remove()
        self.grapher.plot_graph()

    def f_stk_selected(self, selected_value_text):
        if selected_value_text in self.f_stk._values:
            index = self.f_stk._values.index(selected_value_text)
            self.eleana.set_selections('f_stk', index)
        else:
            return
        self.grapher.plot_graph()

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
            self.eleana.set_selections('f_stk', index + 1)
        except IndexError:
            return
        self.grapher.plot_graph()

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
            self.eleana.set_selections('f_stk', index - 1)
        except IndexError:
            return
        self.grapher.plot_graph()

    def modify_first(self):
        self.modify('first')

    def modify_second(self):
        self.modify('second')

    def modify(self, which=None):
        if len(self.eleana.dataset) == 0:
            info = CTkMessagebox(title='', message='Empty dataset')
            return
        if not which:
            which = 'first'
        try:
            self.modify_data.cancel()
        except AttributeError:
            pass
        self.modify_data = ModifyData(self, which)
        response = self.modify_data.get()

    def second_show(self):
        self.eleana.set_selections('s_dsp', bool(self.check_second_show.get()))
        selection = self.sel_second.get()
        if selection == 'None':
            return
        self.second_selected(selection)

    def second_selected(self, selected_value_text):
        if selected_value_text == 'None':
            self.eleana.set_selections('second', -1)
            self.secondComplex.grid_remove()
            self.secondStkFrame.grid_remove()
            self.grapher.plot_graph()
            return
        i = 0
        while i < len(self.eleana.dataset):
            name = self.eleana.dataset[i].name_nr
            if name == selected_value_text:
                self.eleana.set_selections('second', i)
                break
            i += 1
        update.list_in_combobox('sel_second')
        update.list_in_combobox('s_stk')
        if self.eleana.dataset[self.eleana.selections['second']].complex:
            self.secondComplex.grid()
        else:
            self.secondComplex.grid_remove()
        self.grapher.plot_graph()

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
            self.eleana.set_selections('s_stk', index)
        else:
            return
        self.grapher.plot_graph()

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
            self.eleana.set_selections('s_stk', index + 1)
        except IndexError:
            return
        self.grapher.plot_graph()

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
            self.eleana.set_selections('s_stk', index - 1)
        except IndexError:
            return
        self.grapher.plot_graph()

    def second_complex_clicked(self, value):
        self.eleana.set_selections('s_cpl', value)
        self.grapher.plot_graph()

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
        self.grapher.plot_graph()

    def second_to_result(self):
        current = self.sel_second.get()
        if current == 'None':
            return
        index = self.eleana.get_index_by_name(current)
        spectrum = copy.deepcopy(self.eleana.dataset[index])
        self.add_to_results(spectrum)

    def add_to_results(self, spectrum):
        # Check the name if the same already exists in eleana.result_dataset
        list_of_results = []
        try:
            for each in self.eleana.results_dataset:
                list_of_results.append(each.name)
        except:
            pass
        name__ = self.generate_name_suffix(spectrum.name, list_of_results)
        spectrum.name = name__
        spectrum.name_nr = name__

        # Send to result and update lists
        self.eleana.results_dataset.append(spectrum)
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
        self.eleana.set_selections('r_dsp', bool(self.check_result_show.get()))
        selection = self.sel_result.get()
        if selection == 'None':
            return
        self.result_selected(selection)

    def result_selected(self, selected_value_text):
        if selected_value_text == 'None':
            self.eleana.set_selections('result', -1)
            self.resultComplex.grid_remove()
            self.resultStkFrame.grid_remove()
            self.grapher.plot_graph()
            return
        i = 0
        while i < len(self.eleana.results_dataset):
            name = self.eleana.results_dataset[i].name
            if name == selected_value_text:
                self.eleana.set_selections('result', i)
                break
            i += 1
        update.list_in_combobox('sel_result')
        update.list_in_combobox('r_stk')
        if self.eleana.results_dataset[self.eleana.selections['result']].complex:
            self.resultComplex.grid()
        else:
            self.resultComplex.grid_remove()
        self.grapher.plot_graph()

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
        self.grapher.plot_graph()

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
        self.grapher.plot_graph()

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
            self.eleana.set_selections('r_stk', index + 1)
        except IndexError:
            return
        self.grapher.plot_graph()

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
            self.eleana.set_selections('r_stk', index - 1)
        except IndexError:
            return
        self.grapher.plot_graph()

    def result_complex_clicked(self, value):
        self.eleana.set_selections('r_cpl', value)
        self.grapher.plot_graph()

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

    def all_results_to_new_group(self):
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
        self.first_selected(name)
        self.mainwindow.update_idletasks()
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
        index = self.eleana.selections['result']
        if index < 0:
            return
        self.eleana.results_dataset.pop(index)
        self.eleana.set_selections('result', -1)
        update.all_lists()
        update.gui_widgets()
        self.sel_result.set('None')
        self.grapher.plot_graph()

    def first_to_result(self, name = None):
        if name is not None:
            current = name
            skip_grapher = True
        else:
            current = self.sel_first.get()
            skip_grapher = False
        if current == 'None':
            return
        index = self.eleana.get_index_by_name(current)
        spectrum = copy.deepcopy(self.eleana.dataset[index])
        # Check the name if the same already exists in eleana.result_dataset
        list_of_results = []
        try:
            for each in self.eleana.results_dataset:
                list_of_results.append(each.name)
        except:
            pass
        # Create numbered name if similar exists in the Result Dataset
        name__ = self.generate_name_suffix(spectrum.name, list_of_results)
        spectrum.name = name__
        spectrum.name_nr = name__

        # Send to result and update lists
        self.eleana.results_dataset.append(spectrum)
        update.list_in_combobox('sel_result')
        update.list_in_combobox('r_stk')
        # Set the position to the last added item
        list_of_results = self.sel_result._values
        position = list_of_results[-1]
        self.sel_result.set(position)
        self.result_selected(position)
        if skip_grapher:
            return
        self.grapher.plot_graph()

    def generate_name_suffix(self, name, list_of_results):
        name_lists = []
        i = 0
        while i < len(list_of_results):
            from_list = list_of_results[i]
            from_list = re.split(r'(_#\d+$)', from_list)
            head = from_list[0]
            try:
                number = int(from_list[1][2:])
            except IndexError:
                number = 0
            name_lists.append({'name': head, 'nr': number})
            i += 1
        numbers = [-1]
        for each in name_lists:
            if each['name'] == name:
                numbers.append(each['nr'])
            else:
                numbers.append(-1)
        last_number = max(numbers)
        if last_number == 0:
            name = name + '_#1'
        elif last_number == -1:
            pass
        else:
            name = name + '_#' + str(last_number + 1)
        return name

    def get_indexes_by_name(self, names = None) -> list:
        if not names:
            return
        if type(names) == str:
            names = list(names)
        indexes = []
        for each in names:
            index = self.eleana.get_index_by_name(each)
            indexes.append(index)
        return indexes

    ''' *****************************************
    *            METHODS FOR MENU               *
    ******************************************'''

    # --------------------------------------------
    # MENU: Analysis
    # --------------------------------------------
    def integrate_region(self):
        ''' Integration of the selected range '''
        self.integrate_region = IntegrateRegion(self, which = 'first')

    def normalize(self):
        ''' Normalization of the amplitutes'''
        self.normalize = Normalize(self, which = 'first')

    def delete_selected_data(self, index_to_delete=None):
        av_data = self.sel_first._values
        av_data.pop(0)
        # Open dialog if index_to_delete was not set
        if index_to_delete is None:
            self.select_data = SelectData(master=app.mainwindow, title='Select data', group=self.eleana.selections['group'],
                                      items=av_data)
            response = self.select_data.get()
            if response == None:
                return
            # Get indexes of selected data to remove
            indexes = self.get_indexes_by_name(response)
        # Delete data with selected indexes or given by index_to_delete
        else:
            indexes = [index_to_delete]
        indexes.sort(reverse=True)
        for each in indexes:
            eleana.dataset.pop(each)
        # Set all data to None
        self.eleana.set_selections('first', -1)
        self.eleana.set_selections('second', -1)
        self.sel_first.set('None')
        self.sel_first.set('None')
        self.comparison_settings['indexes'] = []
        update.dataset_list()
        update.group_list()
        update.all_lists()
        update.gui_widgets()
        self.comparison_view()

    def delete_data(self, which, dialog=True):
        if which == 'result':
            self.delete_sel_result()
            return
        index = self.eleana.selections[which]
        if index < 0:
            return
        dialog = CTkMessagebox(title="Delete",
                                    message=f"Do you want to delete data selected in {which}?",
                                    icon="warning", option_1="No", option_2="Yes")
        response = dialog.get()
        if response == 'No':
            return
        self.delete_selected_data(index_to_delete=index)

    def duplicate_data(self, which):
        index = self.eleana.selections[which]
        if index < 0:
            return
        if which == 'result':
            new_data = copy.deepcopy(self.eleana.results_dataset[index])
        else:
            new_data = copy.deepcopy(self.eleana.dataset[index])
        dialog = SingleDialog(master = self, title = 'Enter', label = 'New name', text = new_data.name)
        name = dialog.get()

        if not name:
            info = CTkMessagebox(title='', message='Name cannot be empty')
            return
        dataset = []
        try:
            if which == 'result':
                for each in self.eleana.result_dataset:
                    dataset.append(each.name)
            else:
                for each in self.eleana.result_dataset:
                    dataset.append(each.name)
        except:
            pass
        new_data.name = self.generate_name_suffix(name, dataset)
        if which == 'result':
            self.eleana.result_dataset.append(new_data)
        else:
            self.eleana.dataset.append(new_data)
        update.dataset_list()
        update.all_lists()

    def clear_results(self, skip_question = True):
        if not skip_question:
            quit_dialog = CTkMessagebox(title="Clear results",
                                        message="Are you sure you want to clear the entire dataset in the results?",
                                        icon="warning", option_1="No", option_2="Yes")
            response = quit_dialog.get()
        else:
            response = 'Yes'

        if response == "Yes":
            self.eleana.results_dataset = []
            self.eleana.selections['result'] = -1
            self.sel_result.configure(values=['None'])
            self.r_stk.configure(values=[])
            self.resultFrame.grid_remove()
            self.grapher.plot_graph()

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
            self.grapher.plot_graph()

    def preferences(self):
        ''' Open window for editing preferences '''
        #preferences = PreferencesApp(self.mainwindow, self.grapher, self.color_theme, self.gui_appearence)
        preferences = PreferencesApp(self)
        response = preferences.get()
        if not response:
            return
        self.grapher.plot_graph()
        self.gui_appearence = response['gui_appearance']
        self.color_theme = response['color_theme']

    def load_project(self, event=None, recent=None):
        ''' Load project created with the Application '''
        project = load.load_project(recent)
        if not project:
            return
        update.dataset_list()
        update.groups()
        update.all_lists()
        path_to_file = Path(self.eleana.paths['last_projects'][0])
        name = path_to_file.name
        app.mainwindow.title(name + ' - Eleana')
        self.eleana.paths['last_project_dir'] = str(Path(path_to_file).parent)
        main_menu.last_projects_menu()
        try:
            selected_value_text = self.eleana.dataset[self.eleana.selections['first']].name_nr
            self.first_selected(selected_value_text)
            self.sel_first.set(selected_value_text)
        except:
            pass
        try:
            selected_value_text = self.eleana.dataset[self.eleana.selections['second']].name_nr
            self.second_selected(selected_value_text)
            self.sel_second.set(selected_value_text)
        except:
            pass
        try:
            selected_value_text = self.eleana.results_dataset[self.eleana.selections['result']].name
            self.result_selected(selected_value_text)
            self.sel_result.set(selected_value_text)
        except:
            pass
        self.grapher.plot_graph()

    def load_recent(self, selected_value_text):
        """ Load a project selected from Last Projects Menu"""
        index = selected_value_text.split('. ')
        index = int(index[0])
        index = index - 1
        recent = self.eleana.paths['last_projects'][index]
        self.load_project(recent=recent)
        self.eleana.paths['last_project_dir'] = Path(recent).parent
        self.grapher.plot_graph()

    def save_as(self, filename = None):
        file_saved = save.save_project(filename)
        if not file_saved:
            return
        else:
            last_projects = self.eleana.paths['last_projects']
            saved_path_string = str(file_saved)
            if saved_path_string in last_projects:
                index = last_projects.index(saved_path_string)
                del last_projects[index]
            last_projects.insert(0, str(saved_path_string))
        last_projects = last_projects[:20]
        # Write the list to eleana.paths
        self.eleana.paths['last_projects'] = last_projects
        self.eleana.paths['last_project_dir'] = Path(last_projects[0]).parent
        Save.save_settings_paths(self.eleana)
        # Perform update to place the item into menu
        main_menu.last_projects_menu()
        app.mainwindow.title(Path(last_projects[0]).name[:-4] + ' - Eleana')

    def save_current(self, event=None):
        win_title = self.mainwindow.title()
        if win_title == 'new project - Eleana':
            self.save_as(filename = None)
        else:
            file = win_title[:-9].strip()
            file = file + '.ele'
            filename = Path(self.eleana.paths['last_project_dir'], file)
            self.save_as(filename)

    '''******************************************
              IMPORT EXTERNAL DATA             
    *********************************************'''

    def import_elexsys(self):
        ''' Open window that loads the spectra '''
        try:
            load.loadElexsys()
            update.dataset_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
        except Exception as e:
            Error.show(info='Unable to import Elexsys file. Please verify that you have selected the correct format for import.', details=e)

    def import_EMX(self):
        try:
            load.loadEMX()
            update.dataset_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
        except Exception as e:
            Error.show(info='Unable to import EMX file. Please verify that you have selected the correct format for import.', details=e)

    def import_magnettech1(self):
        try:
            load.loadMagnettech(1)
            update.dataset_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
        except Exception as e:
            Error.show(info='Unable to import Magnettech file. Please verify that you have selected the correct format for import.', details=e)

    def import_magnettech2(self):
        try:
            load.loadMagnettech(2)
            update.dataset_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
        except Exception as e:
            Error.show(info='Unable to import Magnettech file. Please verify that you have selected the correct format for import.', details=e)

    def import_adani_dat(self):
        try:
            load.loadAdaniDat()
            update.dataset_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
        except Exception as e:
            Error.show(info='Unable to import Adani file. Please verify that you have selected the correct format for import.', details=e)

    def import_shimadzu_spc(self):
        try:
            load.loadShimadzuSPC()
            update.dataset_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
        except Exception as e:
            Error.show(info='Unable to import Shimadzu file. Please verify that you have selected the correct format for import.', details=e)

    def import_ascii(self, clipboard=None):
        try:
            load.loadAscii(clipboard)
            update.dataset_list()
            update.group_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
        except Exception as e:
            Error.show(info='Unable to import Ascii file. Please verify that you have selected the correct format for import.', details=e)

    def load_excel(self):
        try:
            x = [['', ''], ['', '']]
            headers = ['A', 'B']
            empty = pandas.DataFrame(x, columns=headers)
            table = CreateFromTable(eleana_app=self.eleana, master=self.mainwindow, df=empty, loadOnStart='excel')
            response = table.get()
            update.dataset_list()
            update.group_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
        except Exception as e:
            Error.show(info='Unable to import Excel file. Please verify that you have selected the correct format for import.', details=e)

    def quick_paste(self, event=None):
        text = pyperclip.paste()
        self.import_ascii(text)

    def export_first(self):
        export.csv('first')

    def export_group(self):
        export.group_csv(self.eleana.selections['group'])

    # --- Quit (also window close by clicking on X)
    def close_application(self, event=None):
        global list_of_subprogs
        quit_dialog = CTkMessagebox(title="Quit", message="Do you want to close the program?",
                                    icon="warning", option_1="No", option_2="Yes")
        response = quit_dialog.get()
        if response == "Yes":
            # # Save current settings:
            Save.save_settings_paths(self.eleana)
            Save.save_preferences(self.eleana, self, self.grapher)
            self.mainwindow.iconify()
            # Close all subprograms from the list
            for each in list_of_subprogs:
                close_cmd = 'self.' + each[0] + '.' + each[1] + '()'
                try:
                    exec(close_cmd)
                except:
                    pass
            # Close all static_plot windows from self.eleana.active_static_windows
            if self.eleana.active_static_plot_windows:
                for window_nr in self.eleana.active_static_plot_windows:
                    close_cmd = "self.grapher.static_plot_" + str(window_nr) + ".cancel()"
                    try:
                        exec(close_cmd)
                    except:
                        print("Error: " + close_cmd)
            self.mainwindow.destroy()

    def notes(self):
        self.notepad = Notepad(master=self.mainwindow, title="Edit notes", text=self.eleana.notes)
        response = self.notepad.get()
        if response == None:
            return
        else:
            self.eleana.notes = response

    def create_new_group(self):
        self.group_create = Groupcreate(self.mainwindow, eleana)
        response = self.group_create.get()
        update.list_in_combobox('sel_group')

    def create_from_table(self):
        headers = ['A', 'B', 'C']
        date = [['', '', '']]
        df = pandas.DataFrame(columns=headers, data=date)
        name = 'new'
        self.spreadsheet = CreateFromTable(self.eleana, self.mainwindow, df=df, name=name,
                                           group=self.eleana.selections['group'])

    def first_to_group(self):
        if self.eleana.selections['first'] < 0:
            return
        self.group_assign = Groupassign(master=app, which='first')
        response = self.group_assign.get()
        update.group_list()
        update.all_lists()

    def second_to_group(self):
        if self.eleana.selections['second'] < 0:
            return
        group_assign = Groupassign(master=app, which='second')
        response = group_assign.get()

    def create_simple_static_plot(self):
        '''
        Get data from the current graph and create a new data for simple graph
        that will be used to display independet matplotlib window
        '''
        if bool(self.switch_comparison.get()) == True:
            info = CTkMessagebox(title="Info", message="This function is not yet available for comparison view.")
            return
        static_plot = self.grapher.get_static_plot_data()
        if not static_plot:
            info = CTkMessagebox(title="Info", message="An error occurred or there is no data for graph creation.")
            return
        dialog = SingleDialog(master=app, title='Enter a name for the graph', label='Enter the graph name', text='')
        name = dialog.get()
        if not name:
            return
        static_plot['name'] = name
        self.eleana.static_plots.append(static_plot)
        main_menu.create_showplots_menu()
        self.grapher.show_static_graph_window(len(self.eleana.static_plots)-1)

    def clear_selected_ranges(self):
        self.grapher.clear_selected_ranges()
        self.grapher.clear_all_annotations()

    def delete_simple_static_plot(self):
        '''
        Opens window to ask which plots
        from created Static Plots will be removed
        '''
        plots = self.eleana.static_plots
        if not plots:
            return
        av_plots = []
        for plot in plots:
            av_plots.append(plot['name_nr'])
        self.select_items = SelectItems(master=app.mainwindow, title='Select plots',
                                  items=av_plots)
        names = self.select_items.get()
        if not names:
            return
        to_delete = []
        for name in names:
            to_delete.append(names.index(name))
        to_delete.sort(reverse=True)
        for i in to_delete:
            self.eleana.static_plots.pop(i)
        main_menu.create_showplots_menu()

    def xy_distance(self):
        self.xy_distance = DistanceRead(self, which = 'first')

    def polynomial_baseline(self):
        self.subprog_polynomial_baseline = PolynomialBaseline(self, which = 'first')

    '''***********************************************
    *           GRAPH SWITCHES AND BUTTONS           *
    ***********************************************'''

    def switch_autoscale_x(self):
        self.grapher.plot_graph()

    def switch_autoscale_y(self):
        self.grapher.plot_graph()

    def set_log_scale_x(self):
        self.grapher.plot_graph()

    def set_log_scale_y(self):
        self.grapher.plot_graph()

    def indexed_x(self):
        self.grapher.indexed_x = bool(self.check_indexed_x.get())
        self.grapher.plot_graph()

    def invert_x_axis(self):
        self.grapher.inverted_x_axis = bool(self.check_invert_x.get())
        self.grapher.plot_graph()

    '''***********************************************
    *                    CURSORS                     *
    ***********************************************'''
    def clear_cursors(self):
        self.grapher.clear_all_annotations()

    def sel_graph_cursor(self, value, clear_annotations=True):
        if clear_annotations:
            self.grapher.clear_all_annotations(True)
        self.grapher.current_cursor_mode['label'] = value
        self.grapher.plot_graph()
        self.grapher.cursor_on_off()

    '''***********************************************
    *           METHODS FOR CONTEXT MENU             *
    ***********************************************'''

    def stack_to_group(self, which):
        index = self.eleana.selections[which]
        if index < 0:
            return
        data = copy.deepcopy(self.eleana.dataset[index])
        if not data.type == 'stack 2D':
            CTkMessagebox(title="Conversion to group", message="The data you selected is not a 2D stack")
        else:
            self.convert_stack_to_group = StackToGroup(app, which)
            response = self.convert_stack_to_group.get()
            if response == None:
                 return
            update.dataset_list()
            update.group_list()
            update.all_lists()

    def rename_data(self, which):
        index = self.eleana.selections[which]
        index_f = self.eleana.selections['first']
        index_s = self.eleana.selections['second']
        index_r = self.eleana.selections['result']
        if index < 0:
            return
        name = self.eleana.dataset[index].name
        if which == 'first':
            title = 'Rename First'
        elif which == 'second':
            title = 'Rename Second'
        elif which == 'result':
            title = 'Rename Result'
            name = self.eleana.results_dataset[index_r].name
        self.single_dialog = SingleDialog(master=app, title=title, label='Enter new name', text=name)
        response = self.single_dialog.get()
        if response == None:
            return
        if not which == 'result':
            self.eleana.dataset[index].name = response
            update.dataset_list()
            update.group_list()
            update.all_lists()
            if index_f >= 0:
                self.sel_first.set(self.eleana.dataset[index_f].name_nr)
            if index_s >= 0:
                self.sel_second.set(self.eleana.dataset[index_s].name_nr)
        else:
            self.eleana.results_dataset[index_r].name = response
            self.eleana.results_dataset[index_r].name_nr = response
            update.dataset_list()
            update.all_lists()
        if index_r >= 0:
            self.sel_result.set(self.eleana.results_dataset[index_r].name_nr)

    def edit_comment(self, which):
        index = self.eleana.selections[which]
        if index < 0:
            return
        comment = self.eleana.dataset[index].comment
        name = 'Comment to: ' + str(self.eleana.dataset[index].name_nr)
        text = Notepad(self.mainwindow, title=name, text=comment)
        response = text.get()
        self.eleana.dataset[index].comment = response

    def edit_parameters(self, which='first'):
        idx = self.eleana.selections.get(which, - 1)
        if idx < 0:
            return
        par_to_edit = self.eleana.dataset[idx].parameters
        name_nr = self.eleana.dataset[idx].name_nr
        self.edit_par = EditParameters(self.mainwindow, parameters=par_to_edit, name=name_nr)
        response = self.edit_par.get()
        if response:
            self.eleana.dataset[idx].parameters = response
        else:
            return

    def execute_command(self, event):
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
            error, executable_command = self.commandprocessor.process_script(command)
            print(command)
            print(executable_command)
            stdout_backup = sys.stdout
            sys.stdout = io.StringIO()
            try:
                eval(executable_command, globals(), locals())
                output = sys.stdout.getvalue()
            except Exception as e:
                output = f"Error: {e}"
            finally:
                sys.stdout = stdout_backup
            new_log = '\n' + output
            self.log_field.insert("end", new_log)
            return output

    def copy_to_clipboard(self, event):
        print('Copy to clipboard. (1395)')

''' STARTING THE APPLICATION '''

# Create general main instances for the program
if not DEVEL:
    # Switch off the error display in final product
    if os.name == 'posix':  # Unix/Linux/macOS
        sys.stderr = open(os.devnull, 'w')
    elif os.name == 'nt':  # Windows
        sys.stderr = open('nul', 'w')

eleana = Eleana(version = ELEANA_VERSION, devel = DEVEL)
if not DEVEL:
    # Switch off the error display in final product
    if os.name == 'posix':  # Unix/Linux/macOS
        sys.stderr = open(os.devnull, 'w')
    elif os.name == 'nt':  # Windows
        sys.stderr = open('nul', 'w')

sound = Sound()
cmd = CommandProcessor()

# Create GUI
app = MainApp(eleana, cmd)  # This is GUI
main_menu = MainMenu(app)
grapher = Grapher(main_menu)
app.set_grapher(grapher)

load = Load(main_menu)
save = Save(app)
export = Export(app)
init = Init(main_menu)
context_menu = ContextMenu(app)
update = Update(main_menu)  # This contains methods for update things like lists, settings, gui, groups etc.
app.set_update(update)

# Initialize basic settings: geometry, icon, graph, binding, etc
init.main_window()
init.paths(update)
init.folders()
init.graph()

# Command Line and tests

# Create Graph canvas
grapher.plot_graph()
# Hide or show widgets in GUI
update.gui_widgets()
update.all_lists()


# Set graph Frame scalable
app.graphFrame.columnconfigure(0, weight=1)
app.graphFrame.rowconfigure(0, weight=1)
main_menu.last_projects_menu()

# Run
if __name__ == "__main__":
    app.run()
