#!/usr/bin/python3

import json
# Import Standard Python Modules
import pathlib
import customtkinter
import pygubu
from CTkMessagebox import CTkMessagebox
import sys

# Import Eleana specific classes
from assets.general_eleana_methods import Eleana
from assets.menuActions import MenuAction
from assets.initialization import Init
from assets.graph_plotter import plotter
from assets.update_methods import Update
from assets.comboboxes_methods import Comboboxes


# PROJECT_PATH = pathlib.Path(__file__).parent
# PROJECT_UI = PROJECT_PATH / "Eleana_main.ui"
# class EleanaMainApp:
#     def __init__(self, master=None):
#         self.builder = builder = pygubu.Builder()
#         builder.add_resource_path(PROJECT_PATH)
#         builder.add_from_file(PROJECT_UI)
#         # Main widget
#         self.mainwindow = builder.get_object("Eleana", master)
#         self.mainwindow.withdraw()
#
#         # Main menu
#         _main_menu = builder.get_object("mainmenu", self.mainwindow)
#         self.mainwindow.configure(menu=_main_menu)
#
#         self.group_down = None
#         self.group_up = None
#         self.group = None
#         self.first_down = None
#         builder.connect_callbacks(self)
#         # END OF PYGUBU BUILDER
#
#         # Create references to Widgets and Frames
#         self.sel_group = builder.get_object("sel_group", self.mainwindow)
#         self.sel_first = builder.get_object("sel_first", self.mainwindow)
#         self.sel_second = builder.get_object("sel_second", self.mainwindow)
#         self.sel_result = builder.get_object("sel_result", self.mainwindow)
#         self.firstFrame = builder.get_object("firstFrame", self.mainwindow)
#         self.resultFrame = builder.get_object("resultFrame", self.mainwindow)
#         self.resultStkFrame = builder.get_object("resultStkFrame", self.mainwindow)
#         self.firstStkFrame = builder.get_object("firstStkFrame", self.mainwindow)
#         self.secondStkFrame = builder.get_object("secondStkFrame", self.mainwindow)
#         self.firstComplex = builder.get_object("firstComplex", self.mainwindow)
#         self.secondComplex = builder.get_object("secondComplex", self.mainwindow)
#         self.resultComplex = builder.get_object("resultComplex", self.mainwindow)
#         self.graphFrame = builder.get_object('graphFrame', self.mainwindow)
#         self.f_stk = builder.get_object('f_stk', self.mainwindow)
#         self.s_stk = builder.get_object('s_stk', self.mainwindow)
#         self.r_stk = builder.get_object('r_stk', self.mainwindow)
#
#         # Set default values
#         self.firstComplex.set(value="re")
#         self.secondComplex.set(value="re")
#         self.legendFrame = builder.get_object('legendFrame', self.mainwindow)
#
#     # def run(self):
#     #     self.mainwindow.deiconify()
#     #     self.mainwindow.mainloop()
#
#     def group_down_clicked(self):
#         pass
#
#     def group_up_clicked(self):
#         pass
#
#     def group_selected(self, value):
#         pass
#
#     def first_down_clicked(self):
#         first_down_clicked()
#     def first_up_clicked(self):
#         first_up_clicked()
#     def first_complex_clicked(self, value):
#         first_complex_clicked(value)
#
#     def first_selected(self, selected_value_text: str):
#         first_selected(selected_value_text)
#     def f_stk_selected(self, selected_value_text):
#         f_stk_selected(selected_value_text)
#     def f_stk_up_clicked(self):
#         f_stk_up_clicked()
#     def f_stk_down_clicked(self):
#         f_stk_down_clicked()
#     def second_selected(self, selected_value_text):
#         second_selected(selected_value_text)
#     def second_down_clicked(self):
#         second_down_clicked()
#     def second_up_clicked(self):
#         second_up_clicked()
#     def s_stk_selected(self, selected_value_text):
#         s_stk_selected(selected_value_text)
#     def s_stk_up_clicked(self):
#         s_stk_up_clicked()
#     def s_stk_down_clicked(self):
#         s_stk_down_clicked()
#     def second_complex_clicked(self, value):
#         second_complex_clicked(value)
#     def swap_first_second(self):
#         swap_first_second()
#     def second_to_result(self):
#         second_to_result()
#     def result_selected(self, selected_value_text):
#         result_selected(selected_value_text)
#     def result_up_clicked(self):
#         result_up_clicked()
#
#     def result_down_clicked(self):
#         result_down_clicked()
#     def first_to_result(self):
#         first_to_result()
#     def load_project(self):
#         load_project()
#     def save_as(self):
#         save_as()
#     def import_elexsys(self):
#         import_elexsys()
#
#     # --- Quit (also window close by clicking on X)
#     def close_application(self):
#         close_application()
#
#     def notes(self):
#         notes()

if __name__ == "__main__":
    pass