def main_menubar_callbacks(inst):
    ''' This creates callbacks for mein menubar to methods in Application.py '''
    return {
             # FILE
             "load_project": inst.load_project,
             "save_as": inst.save_as,
             "import_elexsys": inst.import_elexsys,
             "import_EMX": inst.import_EMX,
             "import_magnettech1": inst.import_magnettech1,
             "import_magnettech2": inst.import_magnettech2,
             "import_adani_dat": inst.import_adani_dat,
             "import_shimadzu_spc": inst.import_shimadzu_spc,
             "import_ascii": inst.import_ascii,
             "import_excel": inst.import_excel,
             "export_first": inst.export_first,
             "export_group": inst.export_group,
             "close_application": inst.close_application,
             # EDIT
             "edit_values_in_table": inst.edit_values_in_table,
             "create_from_table": inst.create_from_table,
             "edit_parameters": inst.edit_parameters,
             "quick_copy": inst.quick_copy,
             "quick_paste": inst.quick_paste,
             "delete_selected_data": inst.delete_selected_data,
             "notes" : inst.notes,
             "clear_dataset": inst.clear_dataset,
             "clear_results": inst.clear_results,
             "first_to_group": inst.first_to_group,
             "second_to_group": inst.second_to_group,
             "preferences": inst.preferences,
             # ANALYSIS
             "xy_distance": inst.xy_distance,
             "integrate_region": inst.integrate_region,

             # MODIFICATION
             "normalize": inst.normalize,
             "spectra_subtraction": inst.spectra_subtraction,
            }

def contextmenu_callbacks(inst):
    return {'gui_references':
                {
                    "groupFrame": inst.groupFrame,
                    "sel_group": inst.sel_group,
                    "firstFrame": inst.firstFrame,
                    "sel_first": inst.sel_first,
                    "firstStkFrame": inst.firstStkFrame,
                    "f_stk": inst.f_stk,
                    "seconFrame": inst.secondFrame,
                    "sel_second": inst.sel_second,
                    "secondStkFrame": inst.secondStkFrame,
                    "s_stk": inst.s_stk,
                    "resultFrame": inst.resultFrame,
                    "sel_result": inst.sel_result
                },
            'callbacks':
                {
                    "delete_group": inst.delete_group,
                    "data_to_other_group": inst.data_to_other_group,
                    "delete_data_from_group": inst.delete_data_from_group,
                    "convert_group_to_stack": inst.convert_group_to_stack,
                    "rename_data": inst.rename_data,
                    "delete_data": inst.delete_data,
                    "duplicate_data": inst.duplicate_data,
                    "first_to_group": inst.first_to_group,
                    "stack_to_group": inst.stack_to_group,
                    "edit_comment": inst.edit_comment,
                    "edit_parameters": inst.edit_parameters,
                    "delete_single_stk_data": inst.delete_single_stk_data,
                }
            }

def grapher_callbacks(inst):
    return {'gui_references':
                {
                    'sel_cursor_mode': inst.sel_cursor_mode,
                    'btn_clear_cursors': inst.btn_clear_cursors,
                    'sel_cursor_mode': inst.sel_cursor_mode,
                    'annotationsFrame': inst.annotationsFrame,
                    'infoframe': inst.infoframe,
                    'info': inst.info,
                    'check_autoscale_x': inst.check_autoscale_x,
                    'check_autoscale_y': inst.check_autoscale_y
                },
            'callbacks':
                {
                    
                }
            }   

def update_callbacks(inst):
    return {'gui_references':
                {
                    'sel_group': inst.sel_group,
                    'sel_first': inst.sel_first,
                    'sel_second': inst.sel_second,
                    'sel_result': inst.sel_result,
                    'f_stk': inst.f_stk,
                    's_stk': inst.s_stk,
                    'r_stk': inst.r_stk,
                    'scrollabledropdown': inst.scrollable_dropdown,
                    'resultFrame': inst.resultFrame,
                    'firstStkFrame': inst.firstStkFrame,
                    'secondStkFrame': inst.secondStkFrame,
                    'resultStkFrame': inst.resultStkFrame,
                    'firstComplex': inst.firstComplex,
                    'secondComplex': inst.secondComplex,
                    'resultComplex': inst.resultComplex
                },
            'callbacks':
                {
                    'scrollable_dropdown': inst.scrollable_dropdown
                }
            }
def loadsave_callbacks(inst):
    return {
        'callbacks':{
            'clear_dataset': inst.clear_dataset
        }

    }
    pass