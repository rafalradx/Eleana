from pathlib import Path
import tkinter as tk



from assets.LoadSave import Load, Save
import copy
from modules.CTkScrollableDropdown import CTkScrollableDropdown

PROJECT_PATH = Path(__file__).parent.parent
PROJECT_UI = PROJECT_PATH / "Eleana_interface.ui"

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
    def __init__(self, eleana, widgetsIDs, menu_recent, callbacks, scroll_start = 30):
        self.eleana = eleana
        self.widgetsIDs = widgetsIDs
        self.menu_recent = menu_recent
        self.callbacks = callbacks

        # scroll_start defines minimum numer of items in combobox when scroll in list is activated
        self.scroll_start = scroll_start
        self.active_scrollable_dropdowns = {}
        self.dropdowns = {}

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

    def application(self):
        # This updates all necessary elements of the application
        self.dataset_list()     # 1. Update dataset, check if anything changed
        self.groups()           # 2. Update groups that are defined in dataset
        self.all_lists()

    def dataset_list(self):
        ''' It scans the whole dataset, create numbered names, collects groups and assigns to groups'''
        i = 0
        while i < len(self.eleana.dataset):
            # Replace forbidden marks
            name = self.eleana.dataset[i].name
            name = name.replace('.', '-')
            name = name.replace(',', '-')
            name = name.replace('/', '-')
            name = name.replace(':', '-')
            self.eleana.dataset[i].name = name
            new_name_nr = str(i+1) + '. ' + self.eleana.dataset[i].name
            self.eleana.dataset[i].name_nr = new_name_nr
            i += 1

    def list_in_combobox(self, cb_id):
        comboboxID = cb_id
        box = self.widgetsIDs[cb_id]
        comboboxList = ['None']
        if comboboxID == 'sel_group':
            list_of_groups = self.eleana.assignmentToGroups['<group-list/>']
            box.configure(values = list_of_groups)
            CTkScrollableDropdown(attach=box, values=list_of_groups, justify="left", button_color="transparent",
                                       command=lambda selection: self.app.scrollable_dropdown(selection=selection,
                                                                                              combobox=comboboxID))
            return

        if len(self.eleana.dataset) == 0:
            box.configure(values=comboboxList)

            return

        # Fill list in FIRST or SECOND
        if comboboxID == 'sel_first' or comboboxID == 'sel_second':
            currentGroup = self.eleana.selections['group']
            if currentGroup not in self.eleana.assignmentToGroups['<group-list/>']:
                currentGroup = 'All'
                self.widgetsIDs['sel_group'].set('All')
            if currentGroup == 'All':
                for each in self.eleana.dataset:
                    comboboxList.append(each.name_nr)
            else:
                list_from_group = self.eleana.assignmentToGroups[currentGroup]
                for each in list_from_group:
                    item = self.eleana.dataset[each].name_nr
                    comboboxList.append(item)
            box.configure(values=comboboxList)
            #self.dropdowns[comboboxID] = CTkScrollableDropdown(attach = box, values=comboboxList, justify="left", button_color="transparent", command=lambda selection: self.app.scrollable_dropdown(selection=selection, combobox = comboboxID))
            self.dropdowns[comboboxID] = CTkScrollableDropdown(attach = box, values=comboboxList, justify="left", button_color="transparent", command = lambda selection: self.callbacks.get('scrollable_dropdown')(selection=selection, combobox=comboboxID))
            return

        # Fill list in RESULT
        elif comboboxID == 'sel_result':
            if len(self.eleana.results_dataset) == 0:
                self.widgetsIDs['resultFrame'].grid_remove()
                return
            self.widgetsIDs['resultFrame'].grid()
            for each in self.eleana.results_dataset:
                comboboxList.append(each.name)
            box.configure(values=comboboxList)
            self.dropdowns[comboboxID] = CTkScrollableDropdown(attach=box, values=comboboxList, justify="left", button_color="transparent",
                                       command=lambda selection: self.app.scrollable_dropdown(selection=selection,combobox=comboboxID))

            return

        # Fill list in f_stk if the data is type of stack
        elif comboboxID == 'f_stk':
            index = self.eleana.selections['first']
            if index < 0:
                self.widgetsIDs['firstStkFrame'].grid_remove()
                return
            if self.eleana.dataset[index].type == 'stack 2D':
                stk_list = self.eleana.dataset[index].stk_names
                box.configure(values=stk_list)
                self.dropdowns[comboboxID] = CTkScrollableDropdown(attach=box,
                                      values=stk_list,
                                      justify="left",
                                      button_color="transparent",
                                      alpha=0.95,
                                      scrollbar=True,
                                      button_height=10,
                                      autocomplete=True,
                                      command=lambda selection: self.app.scrollable_dropdown(selection=selection, combobox=comboboxID))
                self.widgetsIDs['firstStkFrame'].grid()
                box.set(stk_list[0])
            else:
                self.widgetsIDs['firstStkFrame'].grid_remove()
            return

        elif comboboxID == 's_stk':
            index = self.eleana.selections['second']
            if index < 0:
                self.widgetsIDs['secondStkFrame'].grid_remove()
                return
            if self.eleana.dataset[index].type == 'stack 2D':
                stk_list = self.eleana.dataset[index].stk_names
                box.configure(values=stk_list)
                self.dropdowns[comboboxID] = CTkScrollableDropdown(attach=box, values=stk_list, justify="left", button_color="transparent",
                                           command=lambda selection: self.app.scrollable_dropdown(selection=selection,
                                                                                                  combobox=comboboxID))
                self.widgetsIDs['secondStkFrame'].grid()
                box.set(stk_list[0])
            else:
                self.widgetsIDs['secondStkFrame'].grid_remove()
            return

        elif comboboxID == 'r_stk':
            index = self.eleana.selections['result']
            if index < 0:
                self.widgetsIDs['resultStkFrame'].grid_remove()
                return
            if self.eleana.results_dataset[index].type == 'stack 2D':
                stk_list = self.eleana.results_dataset[index].stk_names
                box.configure(values=stk_list)
                self.widgetsIDs['resultStkFrame'].grid()
                box.set(stk_list[0])
                if len(stk_list) >= self.scroll_start:
                    self.dropdowns[comboboxID] = CTkScrollableDropdown(attach=box, values=stk_list, justify="left", button_color="transparent",
                                          command=lambda selection: self.app.scrollable_dropdown(selection=selection,
                                                                                                 combobox = comboboxID))

            else:
                self.widgetsIDs['resultStkFrame'].grid_remove()
            return

    def all_lists(self):
        self.list_in_combobox('sel_first')
        self.list_in_combobox('sel_second')
        self.list_in_combobox('sel_result')
        self.list_in_combobox('f_stk')
        self.list_in_combobox('s_stk')
        self.list_in_combobox('r_stk')
        self.list_in_combobox('sel_group')

    # def ref_to_combobox(self, app: object, comboboxID: str):
    #     if comboboxID == 'sel_first':
    #         box = self.app.sel_first
    #     elif comboboxID == 'sel_second':
    #         box = self.app.sel_second
    #     elif comboboxID == 'sel_result':
    #         box = self.app.sel_resul
    #     treturn box
    #
    #     elif comboboxID == 'f_stk':
    #         box = self.app.f_stk
    #     elif comboboxID == 's_stk':
    #         box = self.app.s_stk
    #     elif comboboxID == 'r_stk':
    #         box = self.app.r_stk
    #     elif comboboxID == 'sel_group':
    #         box = self.app.sel_group
    #     return box

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
            self.widgetsIDs['firstStkFrame'].grid_remove()
            self.widgetsIDs['firstComplex'].grid_remove()

        elif first.type == "stack 2D":
            self.widgetsIDs['firstStkFrame'].grid(row=2, column=0)
            self.app.f_stk.configure(values=first.stk_names)
            entry_index = int(self.eleana.selections['f_stk'])
            entry = first.stk_names[entry_index]
            self.app.f_stk.set(value=entry)
        try:
            if first.complex and first_nr >= 0:
                self.widgetsIDs['firstComplex'].grid()
        except:
            pass

        # Update SECOND frame
        if len(self.eleana.dataset) == 0 or second.type != "stack 2D" or is_second_none:
            self.widgetsIDs['secondStkFrame'].grid_remove()
            self.widgetsIDs['secondComplex'].grid_remove()

        elif second.type == "stack 2D":
            self.widgetsIDs['secondStkFrame'].grid(row=2, column=0)
            self.widgetsIDs['s_stk'].configure(values=second.stk_names)
            entry_index = int(self.eleana.selections['s_stk'])
            entry = second.stk_names[entry_index]
            self.widgetsIDs['s_stk'].set(value=entry)
        try:
            if second.complex and second_nr >= 0:
                self.widgetsIDs['secondComplex'].grid()
        except:
            pass

        # Update RESULT frame
        if len(self.eleana.results_dataset) == 0:
            self.widgetsIDs['resultFrame'].grid_remove()
            return
        else:
            self.widgetsIDs['resultFrame'].grid()

        if result.type != "stack 2D" or is_result_none:
            self.widgetsIDs['resultStkFrame'].grid_remove()

        elif result.type == "stack 2D":
            self.widgetsIDs['resultStkFrame'].grid(row=2, column=0)
            self.widgetsIDs['r_stk'].configure(values=result.stk_names)

        if result.complex:
            self.widgetsIDs['resultComplex'].grid()
        else:
            self.widgetsIDs['resultComplex'].grid_remove()

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
        found_groups = ['All']

        for data in dataset:
            found_groups.extend(data.groups)
        found_groups = list(set(found_groups))
        found_groups.sort()
        assignToGroups = {'<group-list/>': found_groups}

        group_assignments = {}
        for group in found_groups:
            group_assignments[group] = []
            i = 0
            while i < len(dataset):
                if group == 'All':
                    group_assignments[group].append(i)
                elif group in dataset[i].groups:
                    group_assignments[group].append(i)
                i += 1
        self.eleana.assignmentToGroups = assignToGroups
        for key in group_assignments.keys():
            self.eleana.assignmentToGroups[key] = group_assignments[key]


