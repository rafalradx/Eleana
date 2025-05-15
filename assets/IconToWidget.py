import customtkinter as ctk
from PIL import Image
from pathlib import Path

class IconToWidget:
    @staticmethod
    def set(widget, png, iconset = 'default', size = (20,20)):
        png = png + '.png'
        icon_folder = Path('pixmaps', 'widget_icons', iconset, png)
        image = ctk.CTkImage(light_image=Image.open(icon_folder), size=size)
        widget.configure(image = image, compound='left')

    @staticmethod
    def set2id(id, png, app, iconset='default', size = (20,20)):
        widget = app.builder.get_object(id, app.mainwindow)
        IconToWidget.set(widget, png, iconset = iconset, size=size)

    @staticmethod
    def eleana(app, iconset = 'default'):

         #          PYGUBU ID                   PNG FILE (no suffix)                SIZE
         #          ----------------------      --------------------------          ------------
         items = (( 'btn_swap'                  ,'btn_swap',                        (30,20)),
                  ( 'btn_second_modify'         ,'btn_modify',                      (20,20)),
                  ( 'btn_first_modify'          ,'btn_modify',                      (20,20)),
                  ( 'btn_first_to_result'       ,'to_result',                       (20,20)),
                  ( 'btn_second_to_result'      ,'to_result',                       (20,20)),
                  ( 'btn_replace_first'         ,'replace_first',                   (20,20)),
                  ( 'btn_replace_group'         ,'replace_group',                   (20,20)),
                  ( 'btn_clear_results'         ,'clear_results',                   (20,20)),
                  ( 'btn_add_to_group'          ,'btn_add_to_group',                (20,20)),
                  ( 'btn_delete_selected'       ,'btn_delete_selected',             (20,20)),
                  ( 'btn_all_to_group'          ,'btn_all_to_group',                (20,20)),

                )

         for item in items:
             id = item[0]
             png = item[1]
             size = item[2]
             IconToWidget.set2id(id=id, png=png, app = app, iconset = iconset, size = size)






