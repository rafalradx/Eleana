from pathlib import Path
import tkinter as tk
'''
Update class contains methods for creating list in comboboxes
and adds the created lists to the ComboboxLists.entries
Arguments: app     <-- is the mani application object (=app)
           entries <-- list of elements that will added to the list
Example usage in main Eleana.py:

  entries = ['1. FeS', '2. Heme_bL', '3. Spin_label']
  update.second(app, entries)

This will create 3 positions in the list of Second combobox
'''
class Update:
    def __init__(self, app_instance, eleana_instance, main_menu_instance):
        self.app = app_instance
        self.eleana = eleana_instance
        self.main_menu = main_menu_instance

    def last_projects_menu(self):
        ''' Updates list of the recently loaded or saved projects and adds the list to the main menu'''
        list_for_menu = []
        i = 1
        for each in self.eleana.paths['last_projects']:
            item = Path(each)
            item = str(i) + '. ' + item.name
            list_for_menu.append(item)
            i += 1

        #recent_menu = self.app.builder.get_object("menu_recent", self.app.mainwindow)
        recent_menu = self.main_menu.menu_recent
        recent_menu.delete(0, tk.END)
        for label in list_for_menu:
            def create_command(l):
                return lambda: self.app.load_recent(l)

            icon_file = Path(self.eleana.paths['pixmaps'], 'x.png')
            icon_clear = tk.PhotoImage(file=icon_file)
            recent_menu.add_command(label=label, image=icon_clear, compound="left", command=create_command(label))

    def group_list(self):
        ''' This scans for groups and creates assignments in eleana.assignmentToGroups'''
        # 1. Scan each dataset and append index to the assignment
        assignments = {'<group-list/>': [], 'All': []}
        i = 0
        while i < len(self.eleana.dataset):
            groups = self.eleana.dataset[i].groups
            for group in groups:
                assignments[group] = []
            i += 1

        for key in assignments.keys():
            indexes = list(assignments[key])
            indexes.sort()
            assignments[key] = indexes

        i = 0
        while i < len(self.eleana.dataset):
            groups_in_dataset = self.eleana.dataset[i].groups
            if len(groups_in_dataset) == 0:
                assignments['All'].append(i)
            else:
                for each in groups_in_dataset:
                    assignments[each].append(i)
            i += 1

               # 3. Create list of groups in ascending order and save to eleana.assignmentToGroups
        list_of_groups = assignments
        del list_of_groups['<group-list/>']
        list_of_groups = assignments.keys()
        list_of_groups = list(list_of_groups)
        list_of_groups.sort()
        assignments['<group-list/>'] = list_of_groups
        self.eleana.assignmentToGroups = assignments

    def dataset_list(self):
        ''' It scans the whole dataset, create numbered names, collects groups and assigns to groups'''

        i = 0
        while i < len(self.eleana.dataset):
            # Replace comma to hyphen
            name = self.eleana.dataset[i].name
            name = name.replace(',', '-')
            self.eleana.dataset[i].name = name
            new_name_nr = str(i+1) + '. ' + self.eleana.dataset[i].name
            self.eleana.dataset[i].name_nr = new_name_nr
            i += 1


    def list_in_combobox(self, comboboxID):
        box = self.ref_to_combobox(self.app, comboboxID)
        comboboxList = ['None']
        if len(self.eleana.dataset) == 0:
            box.configure(values=comboboxList)
            return

        if comboboxID == 'sel_group':
            list_of_groups = self.eleana.assignmentToGroups['<group-list/>']
            box.configure(values = list_of_groups)
            return

        # Fill list in FIRST or SECOND
        if comboboxID == 'sel_first' or comboboxID == 'sel_second':
            currentGroup = self.eleana.selections['group']
            if currentGroup == 'All':
                for each in self.eleana.dataset:
                    comboboxList.append(each.name_nr)
            else:
                list_from_group = self.eleana.assignmentToGroups[currentGroup]
                for each in list_from_group:
                    item = self.eleana.dataset[each].name_nr
                    comboboxList.append(item)
            box.configure(values=comboboxList)
            return

        # Fill list in RESULT
        elif comboboxID == 'sel_result':
            if len(self.eleana.results_dataset) == 0:
                self.app.resultFrame.grid_remove()
                return
            self.app.resultFrame.grid()
            for each in self.eleana.results_dataset:
                comboboxList.append(each.name)
            box.configure(values=comboboxList)
            return

        # Fill list in f_stk if the data is type of stack
        elif comboboxID == 'f_stk':
            index = self.eleana.selections['first']
            if index < 0:
                self.app.firstStkFrame.grid_remove()
                return
            if self.eleana.dataset[index].type == 'stack 2D':
                stk_list = self.eleana.dataset[index].stk_names
                box.configure(values=stk_list)
                self.app.firstStkFrame.grid()
                box.set(stk_list[0])
            else:
                self.app.firstStkFrame.grid_remove()
            return

        elif comboboxID == 's_stk':
            index = self.eleana.selections['second']
            if index < 0:
                self.app.secondStkFrame.grid_remove()
                return
            if self.eleana.dataset[index].type == 'stack 2D':
                stk_list = self.eleana.dataset[index].stk_names
                box.configure(values=stk_list)
                self.app.secondStkFrame.grid()
                box.set(stk_list[0])
            else:
                self.app.secondStkFrame.grid_remove()
            return

        elif comboboxID == 'r_stk':
            index = self.eleana.selections['result']
            if index < 0:
                self.app.resultStkFrame.grid_remove()
                return
            if self.eleana.results_dataset[index].type == 'stack 2D':
                stk_list = self.eleana.results_dataset[index].stk_names
                box.configure(values=stk_list)
                self.app.resultStkFrame.grid()
                box.set(stk_list[0])
            else:
                self.app.resultStkFrame.grid_remove()
            return

    def all_lists(self):
        self.list_in_combobox('sel_first')
        self.list_in_combobox('sel_second')
        self.list_in_combobox('sel_result')
        self.list_in_combobox('f_stk')
        self.list_in_combobox('s_stk')
        self.list_in_combobox('r_stk')
        self.list_in_combobox('sel_group')

    def ref_to_combobox(self, app: object, comboboxID: str):
        if comboboxID == 'sel_first':
            box = self.app.sel_first
        elif comboboxID == 'sel_second':
            box = self.app.sel_second
        elif comboboxID == 'sel_result':
            box = self.app.sel_result
        elif comboboxID == 'f_stk':
            box = self.app.f_stk
        elif comboboxID == 's_stk':
            box = self.app.s_stk
        elif comboboxID == 'r_stk':
            box = self.app.r_stk
        elif comboboxID == 'sel_group':
            box = self.app.sel_group
        return box

    def gui_widgets(self):
        first_nr = self.eleana.selections['first']
        second_nr = self.eleana.selections['second']
        result_nr = self.eleana.selections['result']

        f_stk = self.eleana.selections['f_stk']
        s_stk = self.eleana.selections['s_stk']
        r_stk = self.eleana.selections['r_stk']

        try:
            first = self.eleana.dataset[first_nr]
            f_stk = self.eleana.selections['f_stk']
        except IndexError:
            pass

        try:
            second = self.eleana.dataset[second_nr]
            s_stk = self.eleana.selections['s_stk']
        except IndexError:
            pass

        try:
            result = self.eleana.results_dataset[result_nr]
            r_stk = self.eleana.selections['r_stk']
        except IndexError:
            pass

        # Show or hide widgets

        is_first_none = True if self.eleana.selections['first'] < 0 else False
        is_second_none = True if self.eleana.selections['second'] < 0 else False
        is_result_none = True if self.eleana.selections['result'] < 0 else False

        # FIRST frame
        if len(self.eleana.dataset) == 0 or first.type != "stack 2D" or is_first_none:
            self.app.firstStkFrame.grid_remove()
            self.app.firstComplex.grid_remove()


        elif first.type == "stack 2D":
            self.app.firstStkFrame.grid(row=2, column=0)
            self.app.f_stk.configure(values=first.parameters['stk_names'])
            entry_index = int(self.eleana.selections['f_stk'])
            entry = first.parameters['stk_names'][entry_index]
            self.app.f_stk.set(value=entry)

        try:
            if first.complex and first_nr >= 0:
                self.app.firstComplex.grid()
        except:
            pass

        # Update SECOND frame
        if len(self.eleana.dataset) == 0 or second.type != "stack 2D" or is_second_none:
            self.app.secondStkFrame.grid_remove()
            self.app.secondComplex.grid_remove()

        elif second.type == "stack 2D":
            self.app.secondStkFrame.grid(row=2, column=0)
            self.app.s_stk.configure(values=second.parameters['stk_names'])
            entry_index = int(self.eleana.selections['s_stk'])
            entry = second.parameters['stk_names'][entry_index]
            self.app.s_stk.set(value=entry)
        try:
            if second.complex and second_nr >= 0:
                self.app.secondComplex.grid()
        except:
            pass

        # Update RESULT frame
        if len(self.eleana.results_dataset) == 0:
            self.app.resultFrame.grid_remove()
            return
        else:
            self.app.resultFrame.grid()

        if result.type != "stack 2D" or is_result_none:
            self.app.resultStkFrame.grid_remove()

        elif result.type == "stack 2D":
            self.app.resultStkFrame.grid(row=2, column=0)
            self.app.r_stk.configure(values=result.parameters['stk_names'])

        if result.complex:
            self.app.resultComplex.grid()
        else:
            self.app.resultComplex.grid_remove()

    def results_list(self, results):
        names = []
        i = 1
        for data in dataset:
            name = data.name
            name = str(i) + ". " + name
            names.append(name)
            i += 1
        return names

    # Creating groups on basis of groups defined in eleana.dataset
    def groups(self):
        dataset = self.eleana.dataset
        found_groups = set()
        self.groups = []
        for data in dataset:
            self.groups.extend(data.groups)
        found_groups.update(self.groups)

        self.assignToGroups = {}
        for group_name in found_groups:

            i = 0
            spectra_numbers = []
            while i < len(dataset):
                groups_in_single_spectrum = dataset[i].groups
                if group_name in groups_in_single_spectrum:
                    spectra_numbers.append(i)
                i += 1
            self.assignToGroups[group_name] = spectra_numbers
        return self.assignToGroups


# class Comboboxes():
#     def select_combobox(self, which_combobox: str):
#         if which_combobox == 'sel_first':
#             box = self.app.sel_first
#         elif which_combobox == 'sel_second':
#             box = self.app.sel_second
#         elif which_combobox == 'sel_result':
#             box = self.app.sel_result
#         elif which_combobox == 'f_stk':
#             box = self.app.f_stk
#         elif which_combobox == 's_stk':
#             box = self.app.s_stk
#         elif which_combobox == 'r_stk':
#             box = self.app.r_stk
#         return box
#
#     def get_current_position(self, eleana: object, which_combobox: str):
#         box = self.select_combobox(which_combobox)
#         current_value = box.get()
#         if current_value in self.eleana.combobox_lists[which_combobox]:
#             index_list = self.eleana.combobox_lists[which_combobox].index(current_value)
#             index_dataset = index_list - 1
#             return {'value': current_value, 'index_dataset': index_dataset, 'index_on_list': index_list,
#                     'last_index_on_list': len(eleana.combobox_lists[which_combobox]) - 1}
#         return {}
#
#     def set_on_position_value(self, app, eleana, which_combobox: str, entry: str):
#         ''' Set the value in combobox defined in 'which_combobox
#         on the value 'entry' which is a string name of the position on the combobox list
#         '''
#
#         if which_combobox == 'r_stk':
#             box = self.select_combobox(app, which_combobox)
#             box.set(entry)
#             return
#
#         if which_combobox != 'sel_result':
#             # Set value in eleana.selections
#
#             if entry == 'None':
#                 box = self.select_combobox(app, which_combobox)
#                 box.set(entry)
#                 return
#
#             names = []
#
#             for each in eleana.dataset:
#                 names.append(each.name_nr)
#
#             if entry in names:
#                 index = names.index(entry)
#                 value = eleana.dataset[index].name_nr
#                 box = self.select_combobox(app, which_combobox)
#                 box.set(value)
#         else:
#             box = self.select_combobox(app, which_combobox)
#             box.set(entry)
#
#     def set_on_position_index(self, app: object, eleana: object, which_combobox: str, index: int):
#         ''' Set the value in combobox defined in 'which_combobox'
#         on the position number defined by 'index'.
#         'index' argument is the number of the position in the combobox list
#         '''
#         list_in_combobox = eleana.combobox_lists[which_combobox]
#         try:
#             new_val = list_in_combobox[index]
#             self.set_on_position_value(app, eleana, which_combobox, new_val)
#         except:
#             pass
#
#     def populate_lists(self, app, eleana):
#         # Save FIRST list
#         box = app.sel_first
#         box_list = eleana.combobox_lists['sel_first']
#         box.configure(values=box_list)
#
#         # Save FIRST stk_list
#         box = app.f_stk
#         box_list = eleana.combobox_lists['f_stk']
#         box.configure(values=box_list)
#
#         # Save SECOND list
#         box = app.sel_second
#         box_list = eleana.combobox_lists['sel_second']
#         box.configure(values=box_list)
#
#         # Save SECOND stk_list
#         box = app.f_stk
#         box_list = eleana.combobox_lists['s_stk']
#         box.configure(values=box_list)
#
#         # Save RESULT list
#         box = app.sel_result
#         box_list = eleana.combobox_lists['sel_result']
#         box.configure(values=box_list)
#
#         # Save RESULT stk_list
#         box = app.r_stk
#         box_list = eleana.combobox_lists['r_stk']
#         box.configure(values=box_list)
