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
class Update():

    def dataset_list(self, eleana):

        # Create numbered names in the eleana.dataset[X].names_nr
        i = 0
        while i < len(eleana.dataset):
            eleana.dataset[i].name_nr = str(i+1) + '. ' + eleana.dataset[i].name
            i += 1
        # ----- END OF CREATING NUMBERED NAMES IN DATASET ----


        # Search for groups to which particular spectrum belong and create list of the group
        collection_of_groups = []
        i = 0
        while i < len(eleana.dataset):
            groups = eleana.dataset[i].groups
            if len(groups) == 0:
                groups = ['All']
                eleana.dataset[i].groups = groups
            collection_of_groups.extend(groups)
            i += 1
        # ----- END OF GENERATING LIST OF GROUPS -------

        # Prepare list of groups for assignments
        assignment_to_groups = {}
        groups = set(collection_of_groups)
        for each in groups:
            assignment_to_groups[each] = []

        for key in assignment_to_groups:
            i = 0
            while i < len(eleana.dataset)-1:
                if key in eleana.dataset[i].groups:
                   assignment_to_groups[key].append(i)
                i += 1
        eleana.assignmentToGroups = assignment_to_groups
        # ------------ END OF ASSIGNMENT TO GROUPS ----------

    def list_in_combobox(self, app, eleana, comboboxID):
        box = self.ref_to_combobox(app, comboboxID)
        comboboxList = ['None']

        # Fill list in FIRST or SECOND
        if comboboxID == 'sel_first' or comboboxID == 'sel_second':
            currentGroup = eleana.selections['group']
            if currentGroup == 'All':
                for each in eleana.dataset:
                    comboboxList.append(each.name_nr)

            else:
                list_from_group = eleana.assignmentToGroups[currentGroup]
                for each in list_from_group:
                    item = eleana.dataset[each].name_nr
                    comboboxList.append(item)
            box.configure(values=comboboxList)
            return

        # Fill list in RESULT
        elif comboboxID == 'sel_result':
            for each in eleana.results_dataset:
                comboboxList.append(each.name)
            box.configure(values=comboboxList)
            return

        # Fill list in f_stk if the data is type of stack
        elif comboboxID == 'f_stk':
            index = eleana.selections['first']
            if index < 0:
                app.firstStkFrame.grid_remove()
                return
            if eleana.dataset[index].type == 'stack 2D':
                stk_list = eleana.dataset[index].stk_names
                box.configure(values=stk_list)
                app.firstStkFrame.grid()
                box.set(stk_list[0])
            else:
                app.firstStkFrame.grid_remove()
            return

        elif comboboxID == 's_stk':
            index = eleana.selections['second']
            if index < 0:
                app.secondStkFrame.grid_remove()
                return
            if eleana.dataset[index].type == 'stack 2D':
                stk_list = eleana.dataset[index].stk_names
                box.configure(values=stk_list)
                app.secondStkFrame.grid()
                box.set(stk_list[0])
            else:
                app.secondStkFrame.grid_remove()
            return

        elif comboboxID == 'r_stk':
            index = eleana.selections['result']
            if index < 0:
                app.resultStkFrame.grid_remove()
                return
            if eleana.results_dataset[index].type == 'stack 2D':
                stk_list = eleana.results_dataset[index].stk_names
                box.configure(values=stk_list)
                app.resultStkFrame.grid()
                box.set(stk_list[0])
            else:
                app.resultStkFrame.grid_remove()
            return

    def all_lists(self, app, eleana):
        self.list_in_combobox(app, eleana, 'sel_first')
        self.list_in_combobox(app, eleana, 'sel_second')
        self.list_in_combobox(app, eleana, 'sel_result')
        self.list_in_combobox(app, eleana, 'f_stk')
        self.list_in_combobox(app, eleana, 's_stk')
        self.list_in_combobox(app, eleana, 'r_stk')

    def ref_to_combobox(self, app: object, comboboxID: str):
        if comboboxID == 'sel_first':
            box = app.sel_first
        elif comboboxID == 'sel_second':
            box = app.sel_second
        elif comboboxID == 'sel_result':
            box = app.sel_result
        elif comboboxID == 'f_stk':
            box = app.f_stk
        elif comboboxID == 's_stk':
            box = app.s_stk
        elif comboboxID == 'r_stk':
            box = app.r_stk
        return box

    def combobox_create_list(self, app, eleana, which_combobox):
        box = self.ref_to_combobox(app, which_combobox)

        # Main list
        list_items = ['None']
        # List for stack
        stk_list = []

        ''' This part is performed when Group is set to All.
            Therefore combobox lists will be created for 
            all elements in the eleana.dataset 
        '''
        # Take all names from dataset when Group is set to All
        if eleana.selections['group'] == 'All':
            for each in eleana.dataset:
                list_items.append(each.name_nr)

            # Create list for the FIRST list to eleana.combobox_lists
            if which_combobox == 'sel_first':
                eleana.combobox_lists['sel_first'] = list_items
                first_index = eleana.selections['first']
                if first_index >= 0:
                    try:
                        stk_list = eleana.dataset[first_index]
                    except:
                        stk_list = []
                    eleana.combobox_lists['f_stk'] = stk_list
                return

            # Create list for the SECOND to eleana.combobox_lists
            elif which_combobox == 'sel_second':
                eleana.combobox_lists['sel_second'] = list_items
                second_index = eleana.selections['second']
                if second_index >= 0:
                    try:
                        stk_list = eleana.dataset[second_index]
                    except:
                        stk_list = []
                    eleana.combobox_lists['f_stk'] = stk_list
                return

            # Create list for RESULTS
            elif which_combobox == 'sel_result':
                list_items = ['None']
                for each in eleana.results_dataset:
                    list_items.append(each.name_nr)

                eleana.combobox_lists['sel_result'] = list_items
                result_index = eleana.selections['result']

                try:
                    stk_list = eleana.results_dataset[result_index].parameters['stk_names']
                    eleana.combobox_lists['r_stk'] = stk_list
                except:
                    pass

                return


        else:
            print(
                "Utwórz metodę w ComboboxLists().create_list() do zrobienia listy widm na podstawie innej grupy niż All")
            exit()

        ''' This part is performed when Group is not All.
            Then the lists will be created according to  
            which element is present in assignmentToGroups 

            TO DO
        '''

    def combobox_all_lists(self, app, eleana):
        ids = list(eleana.combobox_lists.keys())
        for each in ids:
            self.combobox_create_list(app, eleana, each)

    ''' 
    Show or hide First, Second or Result frames
    '''

    def gui_widgets(self, app: object, eleana, comboboxes):
        # selections = eleana.selections
        first_nr = eleana.selections['first']
        second_nr = eleana.selections['second']
        result_nr = eleana.selections['result']

        f_stk = eleana.selections['f_stk']
        s_stk = eleana.selections['s_stk']
        r_stk = eleana.selections['r_stk']

        try:
            first = eleana.dataset[first_nr]
            f_stk = eleana.selections['f_stk']
        except IndexError:
            pass

        try:
            second = eleana.dataset[second_nr]
            s_stk = eleana.selections['s_stk']
        except IndexError:
            pass

        try:
            result = eleana.results_dataset[result_nr]
            r_stk = eleana.selections['r_stk']
        except IndexError:
            pass

        # Show or hide widgets

        is_first_none = True if eleana.selections['first'] < 0 else False
        is_second_none = True if eleana.selections['second'] < 0 else False
        is_result_none = True if eleana.selections['result'] < 0 else False

        # FIRST frame
        if len(eleana.dataset) == 0 or first.type != "stack 2D" or is_first_none:
            app.firstStkFrame.grid_remove()
            app.firstComplex.grid_remove()


        elif first.type == "stack 2D":
            app.firstStkFrame.grid(row=2, column=0)
            app.f_stk.configure(values=first.parameters['stk_names'])
            entry_index = int(eleana.selections['f_stk'])
            entry = first.parameters['stk_names'][entry_index]
            app.f_stk.set(value=entry)

        try:
            if first.complex and first_nr >= 0:
                app.firstComplex.grid()
        except:
            pass

        # Update SECOND frame
        if len(eleana.dataset) == 0 or second.type != "stack 2D" or is_second_none:
            app.secondStkFrame.grid_remove()
            app.secondComplex.grid_remove()

        elif second.type == "stack 2D":
            app.secondStkFrame.grid(row=2, column=0)
            app.s_stk.configure(values=second.parameters['stk_names'])
            entry_index = int(eleana.selections['s_stk'])
            entry = second.parameters['stk_names'][entry_index]
            app.s_stk.set(value=entry)
        try:
            if second.complex and second_nr >= 0:
                app.secondComplex.grid()
        except:
            pass

        # Update RESULT frame
        if len(eleana.results_dataset) == 0:
            app.resultFrame.grid_remove()
            return
        else:
            app.resultFrame.grid()

        if result.type != "stack 2D" or is_result_none:
            app.resultStkFrame.grid_remove()


        elif result.type == "stack 2D":
            app.resultStkFrame.grid(row=2, column=0)
            app.r_stk.configure(values=result.parameters['stk_names'])

        if result.complex:
            app.resultComplex.grid()
        else:
            app.resultComplex.grid_remove()

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
    def groups(self, dataset):
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

    ''' Set position on 'entry' in combobox of id = which_combobox'''


'''
ComboboxesLists() contains attribute entries, which stores the current lists of
entries in comboboxes.
Methods:
      current_position <-- returns dict with text of current position,
                           index on the list, and the last item on the list
Example. If there is a combobox list = ['None', '1. FeS', '2. Heme_bL', '3. Spin_label'],
and selection is now on 2. Heme bL then in eleana:
      pozycja = comboboxLists.current_position(app, 'sel_first')
gives in pozycja = {'current: '2. Heme bL', 'index':2, 'last_index':3}
'''


class Comboboxes():
    def select_combobox(self, app: object, which_combobox: str):
        if which_combobox == 'sel_first':
            box = app.sel_first
        elif which_combobox == 'sel_second':
            box = app.sel_second
        elif which_combobox == 'sel_result':
            box = app.sel_result
        elif which_combobox == 'f_stk':
            box = app.f_stk
        elif which_combobox == 's_stk':
            box = app.s_stk
        elif which_combobox == 'r_stk':
            box = app.r_stk
        return box

    def get_current_position(self, app: object, eleana: object, which_combobox: str):
        box = self.select_combobox(app, which_combobox)
        current_value = box.get()
        if current_value in eleana.combobox_lists[which_combobox]:
            index_list = eleana.combobox_lists[which_combobox].index(current_value)
            index_dataset = index_list - 1
            return {'value': current_value, 'index_dataset': index_dataset, 'index_on_list': index_list,
                    'last_index_on_list': len(eleana.combobox_lists[which_combobox]) - 1}
        return {}

    def set_on_position_value(self, app, eleana, which_combobox: str, entry: str):
        ''' Set the value in combobox defined in 'which_combobox
        on the value 'entry' which is a string name of the position on the combobox list
        '''

        if which_combobox == 'r_stk':
            box = self.select_combobox(app, which_combobox)
            box.set(entry)
            return

        if which_combobox != 'sel_result':
            # Set value in eleana.selections

            if entry == 'None':
                box = self.select_combobox(app, which_combobox)
                box.set(entry)
                return

            names = []

            for each in eleana.dataset:
                names.append(each.name_nr)

            if entry in names:
                index = names.index(entry)
                value = eleana.dataset[index].name_nr
                box = self.select_combobox(app, which_combobox)
                box.set(value)
        else:
            box = self.select_combobox(app, which_combobox)
            box.set(entry)

    def set_on_position_index(self, app: object, eleana: object, which_combobox: str, index: int):
        ''' Set the value in combobox defined in 'which_combobox'
        on the position number defined by 'index'.
        'index' argument is the number of the position in the combobox list
        '''
        list_in_combobox = eleana.combobox_lists[which_combobox]
        try:
            new_val = list_in_combobox[index]
            self.set_on_position_value(app, eleana, which_combobox, new_val)
        except:
            pass

    def populate_lists(self, app, eleana):
        # Save FIRST list
        box = app.sel_first
        box_list = eleana.combobox_lists['sel_first']
        box.configure(values=box_list)

        # Save FIRST stk_list
        box = app.f_stk
        box_list = eleana.combobox_lists['f_stk']
        box.configure(values=box_list)

        # Save SECOND list
        box = app.sel_second
        box_list = eleana.combobox_lists['sel_second']
        box.configure(values=box_list)

        # Save SECOND stk_list
        box = app.f_stk
        box_list = eleana.combobox_lists['s_stk']
        box.configure(values=box_list)

        # Save RESULT list
        box = app.sel_result
        box_list = eleana.combobox_lists['sel_result']
        box.configure(values=box_list)

        # Save RESULT stk_list
        box = app.r_stk
        box_list = eleana.combobox_lists['r_stk']
        box.configure(values=box_list)
