import customtkinter as ctk
from tkinter import TclError

class CustomDoubleVar(ctk.DoubleVar):
    def get(self):
        try:
            try:
                return float(self._tk.globalgetvar(self._name))
            except:
                return 0.0
        except TclError:
            return 0.0

class CTkSpinbox(ctk.CTkFrame):
    def __init__(self, master, width=100, height=30, start_value=0, min_value=-1000000, max_value=1000000,
                 step_value=1, scroll_value=5, variable=None, font=('X', 12), fg_color=None,
                 border_color=('#AAA', '#555'), text_color=('Black', 'White'), button_color=('#BBB', '#444'),
                 button_hover_color=('#AAA', '#555'), border_width=1, corner_radius=0, button_corner_radius=0,
                 button_border_width=1, button_border_color=('#AAA', '#555'), state='normal', wait=30, command=None):

        super().__init__(master, height=height, width=width, fg_color=fg_color, border_color=border_color,
                         border_width=border_width, corner_radius=corner_radius)

        self.start_value = max(min(start_value, max_value), min_value)
        self.min_value = min_value
        self.max_value = max_value
        self.step_value = abs(step_value)
        self.scroll_value = abs(scroll_value)
        self.variable = variable
        if self.variable:
            self.variable.set(self.start_value)
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        self.button_corner_radius = button_corner_radius
        self.button_border_width = button_border_width
        self.button_border_color = button_border_color
        self.state = state
        self.command = command
        self.button_font = ('Arial', 14)
        self.scroll_update_id = None
        self.last_valid_value = self.start_value
        self.wait = wait

        self.counter_var = CustomDoubleVar(value=self.start_value)

        vcmd = (self.register(self.validate_entry), '%d', '%P', '%S')

        self.counter = ctk.CTkEntry(self,
                                    textvariable=self.counter_var,
                                    font=self.font,
                                    text_color=self.text_color,
                                    justify='center',
                                    validate='key',
                                    validatecommand=vcmd,
                                    corner_radius=self.button_corner_radius)
        self.counter.bind('<Return>', self.update_counter)
        self.counter.bind('<FocusOut>', self.update_counter)

        self.decrement = ctk.CTkButton(self,
                                       text='▼',
                                       font=self.button_font,
                                       text_color=self.text_color,
                                       fg_color=self.button_color,
                                       hover_color=self.button_hover_color,
                                       text_color_disabled='#888',
                                       corner_radius=self.button_corner_radius,
                                       border_width=self.button_border_width,
                                       border_color=self.button_border_color,
                                       width=height,
                                       height=height,
                                       command=self.decrement_counter)

        self.increment = ctk.CTkButton(self,
                                       text='▲',
                                       font=self.button_font,
                                       text_color=self.text_color,
                                       fg_color=self.button_color,
                                       hover_color=self.button_hover_color,
                                       text_color_disabled='#888',
                                       corner_radius=self.button_corner_radius,
                                       border_width=self.button_border_width,
                                       border_color=self.button_border_color,
                                       width=height,
                                       height=height,
                                       command=self.increment_counter)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0, minsize=height)
        self.columnconfigure(2, weight=0, minsize=height)
        self.grid_propagate(False)

        self.counter.grid(row=0, column=0, sticky='ew', padx=(2, 0), pady=2)
        self.increment.grid(row=0, column=1, sticky='news', padx=0, pady=2)
        self.decrement.grid(row=0, column=2, sticky='news', padx=(0, 2), pady=2)

        self.bind('<MouseWheel>', self.scroll)
        self.bind('<Button-4>', self.scroll_up)
        self.bind('<Button-5>', self.scroll_down)

        if self.state == 'disabled':
            self.disable()

    def validate_entry(self, action, new_value, char):
        if action == '1':
            if char in ('\b', '\x7f'):
                return True
            if not new_value:
                return True
            try:
                float(new_value)
                return True
            except ValueError:
                return False
        return True

    def decrement_counter(self):
        self.counter_var.set(self.counter_var.get() - self.step_value)
        self.update_counter(None)

    def increment_counter(self):
        self.counter_var.set(self.counter_var.get() + self.step_value)
        self.update_counter(None)

    def scroll(self, scroll):
        if self.state == 'normal':
            dirn = 1 if scroll.delta > 0 else -1
            if dirn == -1:
                self.counter_var.set(self.counter_var.get() - self.scroll_value)
            else:
                self.counter_var.set(self.counter_var.get() + self.scroll_value)

            if self.scroll_update_id:
                self.after_cancel(self.scroll_update_id)

            self.scroll_update_id = self.after(self.wait, self.update_counter, None)

    def scroll_up(self, event=None):
        if self.state == 'normal':
            self.counter_var.set(self.counter_var.get() + self.scroll_value)
            if self.scroll_update_id:
                self.after_cancel(self.scroll_update_id)
            self.scroll_update_id = self.after(self.wait, self.update_counter, None)

    def scroll_down(self, event=None):
        if self.state == 'normal':
            self.counter_var.set(self.counter_var.get() - self.scroll_value)
            if self.scroll_update_id:
                self.after_cancel(self.scroll_update_id)
            self.scroll_update_id = self.after(self.wait, self.update_counter, None)

    def get(self):
        value = self.counter_var.get()
        if value == "":
            return 0.0
        try:
            return float(value)
        except ValueError:
            return 0.0

    def set(self, value):
        self.counter_var.set(max(min(value, self.max_value), self.min_value))

    def disable(self):
        self.state = 'disabled'
        self.increment.configure(state='disabled')
        self.decrement.configure(state='disabled')
        self.counter.configure(state='disabled')

    def enable(self):
        self.state = 'normal'
        self.increment.configure(state='normal')
        self.decrement.configure(state='normal')
        self.counter.configure(state='normal')

    def bind(self, key, function, add=True):
        super().bind(key, function, add)
        self.counter.bind(key, function, add)
        self.increment.bind(key, function, add)
        self.decrement.bind(key, function, add)

    def update_counter(self, event=None):
        try:
            value = float(self.counter_var.get())
        except ValueError:
            value = self.last_valid_value
        except TclError:
            value = self.last_valid_value
        except Exception as e:
            print(f'Unexpected error: {e}')
            value = self.last_valid_value

        if '.' in str(self.step_value):
            splitted = str(self.step_value).split('.')[1]
            after_dot = len(splitted)
            value = round(value, after_dot)
        else:
            value = int(value)
        self.counter_var.set(max(min(value, self.max_value), self.min_value))
        if self.variable:
            self.variable.set(self.counter_var.get())
        if self.command:
            self.command(self.counter_var.get())

    def configure(self, **kwargs):
        for value in ['font', 'text_color', 'button_color', 'button_hover_color', 'button_corner_radius',
                      'button_border_color', 'button_border_width']:
            if value in kwargs:
                new_value = kwargs.pop(value)
                if value not in ['font', 'button_corner_radius']:
                    if value not in ['button_hover_color', 'button_color', 'button_corner_radius']:
                        self.counter.configure({value: new_value})
                    value = {'button_color': 'fg_color'}[value] if value in ['button_color',
                                                                             'button_corner_radius'] else value
                    self.increment.configure({value: new_value})
                    self.decrement.configure({value: new_value})
                else:
                    value = {'button_corner_radius': 'corner_radius'}[value] if value in ['button_color',
                                                                                          'button_corner_radius'] else value
                    self.increment.configure({value: new_value})
                    self.decrement.configure({value: new_value})
                    if value == 'font':
                        self.counter.configure({value: new_value})

        for value in ['min_value', 'max_value', 'step_value', 'scroll_value', 'variable']:
            if value in kwargs:
                new_value = kwargs.pop(value)
                setattr(self, value, new_value)

        if 'command' in kwargs:
            self.command = kwargs.pop('command')
        elif 'state' in kwargs:
            self.state = kwargs.pop('state')
            if self.state == 'normal':
                self.enable()
            elif self.state == 'disabled':
                self.disable()

        super().configure(**kwargs)

# Testowanie CTkSpinbox
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry('600x400')

    def on_value_change(value):
        print(f'Spinbox value changed to: {value}')

    spinbox = CTkSpinbox(app,
                         width=150,
                         height=30,
                         start_value=10,
                         min_value=0,
                         max_value=100,
                         step_value=1,
                         scroll_value=5,
                         command=on_value_change)
    spinbox.grid(row=0, column=0, padx=20, pady=20)

    app.mainloop()
