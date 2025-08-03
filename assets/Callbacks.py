def main_menubar_callbacks(main_menubar_instance):
    ''' This creates callbacks for mein menubar to methods in Application.py '''
    return {
             "load_project": main_menubar_instance.load_project,
             "save_as": main_menubar_instance.save_as,
             "import_elexsys": main_menubar_instance.import_elexsys,
             "import_EMX": main_menubar_instance.import_EMX,
             "import_magnettech1": main_menubar_instance.import_magnettech1,
             "import_magnettech2": main_menubar_instance.import_magnettech2,
             "import_adani_dat": main_menubar_instance.import_adani_dat,
             "import_shimadzu_spc": main_menubar_instance.import_shimadzu_spc,
             "import_ascii": main_menubar_instance.import_ascii,
             "import_excel": main_menubar_instance.import_excel,
             "export_first": main_menubar_instance.export_first,
             "export_group": main_menubar_instance.export_group,
             "close_application": main_menubar_instance.close_application,
            }

def contextmenu_callbacks(contextmenu_instance):
    return {'gui_references':
                {
                    "groupFrame": contextmenu_instance.groupFrame,
                    "sel_group": contextmenu_instance.sel_group,
                    "firstFrame": contextmenu_instance.firstFrame,
                    "sel_first": contextmenu_instance.sel_first,
                    "firstStkFrame": contextmenu_instance.firstStkFrame,
                    "f_stk": contextmenu_instance.f_stk,
                    "seconFrame": contextmenu_instance.secondFrame,
                    "sel_second": contextmenu_instance.sel_second,
                    "secondStkFrame": contextmenu_instance.secondStkFrame,
                    "s_stk": contextmenu_instance.s_stk,
                    "resultFrame": contextmenu_instance.resultFrame,
                    "sel_result": contextmenu_instance.sel_result
                },
            'callbacks':
                {
                    "delete_group": contextmenu_instance.delete_group,
                    "data_to_other_group": contextmenu_instance.data_to_other_group,
                    "delete_data_from_group": contextmenu_instance.delete_data_from_group,
                    "convert_group_to_stack": contextmenu_instance.convert_group_to_stack,
                    "rename_data": contextmenu_instance.rename_data,
                    "delete_data": contextmenu_instance.delete_data,
                    "duplicate_data": contextmenu_instance.duplicate_data,
                    "first_to_group": contextmenu_instance.first_to_group,
                    "stack_to_group": contextmenu_instance.stack_to_group,
                    "edit_comment": contextmenu_instance.edit_comment,
                    "edit_parameters": contextmenu_instance.edit_parameters,
                    "delete_single_stk_data": contextmenu_instance.delete_single_stk_data,
                }
            }