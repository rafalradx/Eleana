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
            return {'value':current_value, 'index_dataset':index_dataset, 'index_on_list':index_list, 'last_index_on_list':len(eleana.combobox_lists[which_combobox])-1}
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
