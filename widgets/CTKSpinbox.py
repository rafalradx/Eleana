import customtkinter as ctk


class CTkSpinbox(ctk.CTkFrame):
    def __init__(self,
                 master: any,
                 width: int = 100,
                 height: int = 30,
                 start_value: int = 0,
                 min_value: int = 0,
                 max_value: int = 100,
                 step_value: int = 1,
                 scroll_value: int = 5,
                 variable: any = None,
                 font: tuple = ('X', 12),
                 fg_color: str = None,
                 border_color: str = ('#AAA', '#555'),
                 text_color: str = ('Black', 'White'),
                 button_color: str = ('#BBB', '#444'),
                 button_hover_color: str = ('#AAA', '#555'),
                 border_width: int = 2,
                 corner_radius: int = 5,
                 button_corner_radius: int = 0,
                 button_border_width: int = 2,
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

        # counter entry
        self.counter_var = ctk.IntVar(value=self.start_value)

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

        # decrement button
        self.decrement = ctk.CTkButton(self,
                                       text='-',
                                       font=self.font,
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
                                       text='+',
                                       font=self.font,
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
        self.counter.grid(row=0, column=0, sticky='ew', padx=(4, 0), pady=4)
        self.increment.grid(row=0, column=1, sticky='news', padx=0, pady=4)
        self.decrement.grid(row=0, column=2, sticky='news', padx=(0, 4), pady=4)

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
        '''Increments/Decrements the value of the counter by the scroll value depending on scroll direction.

            THIS IS FOR WINDOWS
        '''

        if self.state == 'normal':
            dirn = 1 if scroll.delta > 0 else -1
            if dirn == -1:
                self.counter_var.set(self.counter_var.get() - self.scroll_value)
            else:
                self.counter_var.set(self.counter_var.get() + self.scroll_value)
            self.update_counter(None)

    def scroll_up(self, event=None):
        '''Increments/Decrements the value of the counter by the scroll value depending on scroll direction.'''
        if self.state == 'normal':
            self.counter_var.set(self.counter_var.get() + self.scroll_value)
            self.update_counter(None)

    def scroll_down(self, event=None):
        '''Increments/Decrements the value of the counter by the scroll value depending on scroll direction.'''
        if self.state == 'normal':
            self.counter_var.set(self.counter_var.get() - self.scroll_value)
            self.update_counter(None)

    def get(self):
        '''Returns the value of the counter.'''
        return self.counter_var.get()

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

    def update_counter(self, event):
        '''Updates the counter variable and calls the counter command.'''
        try:
            value = float(self.counter_var.get())
        except ValueError:
            value = self.min_value

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
                        exec(f"self.counter.configure({value} = '{new_value}')")
                    value = {'button_color': 'fg_color'}[value] if value in ['button_color',
                                                                             'button_corner_radius'] else value
                    exec(f"self.increment.configure({value} = '{new_value}')")
                    exec(f"self.decrement.configure({value} = '{new_value}')")
                else:
                    value = {'button_corner_radius': 'corner_radius'}[value] if value in ['button_color',
                                                                                          'button_corner_radius'] else value
                    exec(f"self.increment.configure({value} = {new_value})")
                    exec(f"self.decrement.configure({value} = {new_value})")
                    if value == 'font':
                        exec(f"self.counter.configure({value} = {new_value})")

        for value in ['min_value', 'max_value', 'step_value', 'scroll_value', 'variable']:
            if value in kwargs:
                new_value = kwargs.pop(value)
                exec(f'self.{value} = {new_value}')

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
    import customtkinter as ctk


    def print_label(count):
        print(count)


    window = ctk.CTk()
    window.geometry('200x150')

    spin_var = ctk.IntVar()
    spinbox = CTkSpinbox(window,
                         start_value=10,
                         min_value=0,
                         max_value=20,
                         scroll_value=2,
                         variable=spin_var,
                         command=print_label)
    spinbox.pack(expand=True, fill='x')  # Use fill='x' to make it expand horizontally

    window.mainloop()
