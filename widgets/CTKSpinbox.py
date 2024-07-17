import customtkinter as ctk
from tkinter import TclError


class CTkSpinbox(ctk.CTkFrame):
    def __init__(self,
                 master: any,
                 width: int = 100,
                 height: int = 30,
                 start_value: float = 0,
                 min_value: float = -1000000,
                 max_value: float = 1000000,
                 step_value: float = 1,
                 scroll_value: float = 5,
                 variable: any = None,
                 font: tuple = ('X', 12),
                 fg_color: str = None,
                 border_color: str = ('#AAA', '#555'),
                 text_color: str = ('Black', 'White'),
                 button_color: str = ('#BBB', '#444'),
                 button_hover_color: str = ('#AAA', '#555'),
                 border_width: int = 1,
                 corner_radius: int = 0,
                 button_corner_radius: int = 0,
                 button_border_width: int = 1,
                 button_border_color: str = ('#AAA', '#555'),
                 state: str = 'normal',
                 command: any = None):
        super().__init__(master,
                         height=height,
                         width=width,
                         fg_color=fg_color,
                         border_color=border_color,
                         border_width=border_width,
                         corner_radius=corner_radius)

        # values
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
        self.button_font: tuple = ('Arial', 14)
        self.scroll_update_id = None
        self.last_valid_value = self.start_value  # Last valid value

        # counter entry
        self.counter_var = ctk.DoubleVar(value=self.start_value)

        # Add validation command
        vcmd = (self.register(self.validate_entry), '%P')

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

        # decrement button
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

        # increment button
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

        # grid
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)  # Make column 0 expandable
        self.columnconfigure(1, weight=0, minsize=height)  # Set fixed width for column 1
        self.columnconfigure(2, weight=0, minsize=height)  # Set fixed width for column 2
        self.grid_propagate(False)

        # layout
        self.counter.grid(row=0, column=0, sticky='ew', padx=(2, 0), pady=2)
        self.increment.grid(row=0, column=1, sticky='news', padx=0, pady=2)
        self.decrement.grid(row=0, column=2, sticky='news', padx=(0, 2), pady=2)

        # scroll bind
        # FOR WINDOWS
        self.bind('<MouseWheel>', self.scroll)

        # FOR LINUX
        self.bind('<Button-4>', self.scroll_up)
        self.bind('<Button-5>', self.scroll_down)

        # update state
        if self.state == 'disabled':
            self.disable()

    def validate_entry(self, new_value):
        '''Validates the entry field to allow only integers and floats.'''
        if new_value == "":
            return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    def decrement_counter(self):
        '''Decrements the value of the counter by the step value.'''
        self.counter_var.set(self.counter_var.get() - self.step_value)
        self.update_counter(None)

    def increment_counter(self):
        '''Increments the value of the counter by the step value.'''
        self.counter_var.set(self.counter_var.get() + self.step_value)
        self.update_counter(None)

    def scroll(self, scroll):
        '''Handles mouse wheel scrolling to increment or decrement the value.'''
        if self.state == 'normal':
            dirn = 1 if scroll.delta > 0 else -1
            if dirn == -1:
                self.counter_var.set(self.counter_var.get() - self.scroll_value)
            else:
                self.counter_var.set(self.counter_var.get() + self.scroll_value)

            # Cancel previous scheduled update if exists
            if self.scroll_update_id:
                self.after_cancel(self.scroll_update_id)

            # Schedule update
            self.scroll_update_id = self.after(50, self.update_counter, None)

    def scroll_up(self, event=None):
        '''Handles scroll up for Linux.'''
        if self.state == 'normal':
            self.counter_var.set(self.counter_var.get() + self.scroll_value)
            if self.scroll_update_id:
                self.after_cancel(self.scroll_update_id)
            self.scroll_update_id = self.after(50, self.update_counter, None)

    def scroll_down(self, event=None):
        '''Handles scroll down for Linux.'''
        if self.state == 'normal':
            self.counter_var.set(self.counter_var.get() - self.scroll_value)
            if self.scroll_update_id:
                self.after_cancel(self.scroll_update_id)
            self.scroll_update_id = self.after(50, self.update_counter, None)

    def get(self):
        '''Returns the value of the counter.'''
        try:
            value = float(self.counter_var.get())
        except TclError:
            value = self.min_value
        if not value:
            value = 0.0
        return value

    def set(self, value):
        '''Sets the counter to a particular value.'''
        self.counter_var.set(max(min(value, self.max_value), self.min_value))

    def disable(self):
        '''Disables the functionality of the counter.'''
        self.state = 'disabled'
        self.increment.configure(state='disabled')
        self.decrement.configure(state='disabled')
        self.counter.configure(state='disabled')

    def enable(self):
        '''Enables the functionality of the counter.'''
        self.state = 'normal'
        self.increment.configure(state='normal')
        self.decrement.configure(state='normal')
        self.counter.configure(state='normal')

    def bind(self, key, function, add=True):
        '''binds a key to a function.'''

        super().bind(key, function, add)
        self.counter.bind(key, function, add)
        self.increment.bind(key, function, add)
        self.decrement.bind(key, function, add)

    def update_counter(self, event=None):
        '''Updates the counter variable and calls the counter command.'''
        try:
            value = float(self.counter_var.get())
            self.last_valid_value = value  # Update last valid value
        except (ValueError, TclError):
            value = self.last_valid_value  # Use last valid value if current value is invalid

        float_nr = str(self.step_value)
        if '.' in float_nr:
            splitted = float_nr.split('.')[1]
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
        '''Update widget values.'''

        # conditions
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


# Test the CTkSpinbox
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
