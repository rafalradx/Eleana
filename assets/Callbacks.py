def main_menubar_callbacks(application_instance):
    ''' This creates callbacks for mein menubar to methods in Application.py '''
    return {
             "load_project": application_instance.load_project,
             "save_as": application_instance.save_as,
             "import_elexsys": application_instance.import_elexsys,
             "import_EMX": application_instance.import_EMX,
             "import_magnettech1": application_instance.import_magnettech1,
             "import_magnettech2": application_instance.import_magnettech2,
             "import_adani_dat": application_instance.import_adani_dat,
             "import_shimadzu_spc": application_instance.import_shimadzu_spc,
             "import_ascii": application_instance.import_ascii,
             "import_excel": application_instance.import_excel,
             "export_first": application_instance.export_first,
             "export_group": application_instance.export_group,
             "close_application": application_instance.close_application,
            }

def contextmenu_callbacks(application_instance):
    return {'gui_references':
                {
                    "groupFrame": application_instance.groupFrame,
                    "sel_group": application_instance.sel_group,
                    "firstFrame": application_instance.firstFrame,
                    "sel_first": application_instance.sel_first,
                    "firstStkFrame": application_instance.firstStkFrame,
                    "f_stk": application_instance.f_stk,
                    "seconFrame": application_instance.secondFrame,
                    "sel_second": application_instance.sel_second,
                    "secondStkFrame": application_instance.secondStkFrame,
                    "s_stk": application_instance.s_stk,
                    "resultFrame": application_instance.resultFrame,
                    "sel_result": application_instance.sel_result
                },
            'callbacks':
                {
                    "delete_group": application_instance.delete_group,
                    "data_to_other_group": application_instance.data_to_other_group,
                    "delete_data_from_group": application_instance.delete_data_from_group,
                    "convert_group_to_stack": application_instance.convert_group_to_stack,
                    "rename_data": application_instance.rename_data,
                    "delete_data": application_instance.delete_data,
                    "duplicate_data": application_instance.duplicate_data,
                    "first_to_group": application_instance.first_to_group,
                    "stack_to_group": application_instance.stack_to_group,
                    "edit_comment": application_instance.edit_comment,
                    "edit_parameters": application_instance.edit_parameters,
                    "delete_single_stk_data": application_instance.delete_single_stk_data,
                }
            }

def grapher_callbacks(application_instance):
    return {'gui_references':
                {
                    'sel_cursor_mode': application_instance.sel_cursor_mode,
                    'btn_clear_cursors': application_instance.btn_clear_cursors,
                    'sel_cursor_mode': application_instance.sel_cursor_mode,
                    'annotationsFrame': application_instance.annotationsFrame,
                    'infoframe': application_instance.infoframe,
                    'info': application_instance.info
                    
                },
            'callbacks':
                {
                    
                }
            }   

def update_callbacks(application_instance):
    return {'gui_references':
                {
                    'sel_group': application_instance.sel_group,
                    'sel_first': application_instance.sel_first,
                    'sel_second': application_instance.sel_second,
                    'sel_result': application_instance.sel_result,
                    'f_stk': application_instance.f_stk,
                    's_stk': application_instance.s_stk,
                    'r_stk': application_instance.r_stk,
                    'scrollabledropdown': application_instance.scrollable_dropdown,
                    'resultFrame': application_instance.resultFrame,
                    'firstStkFrame': application_instance.firstStkFrame,
                    'secondStkFrame': application_instance.secondStkFrame,
                    'resultStkFrame': application_instance.resultStkFrame,
                    'firstComplex': application_instance.firstComplex,
                    'secondComplex': application_instance.secondComplex,
                    'resultComplex': application_instance.resultComplex
                },
            'callbacks':
                {
                    'scrollable_dropdown': application_instance.scrollable_dropdown
                }
            }