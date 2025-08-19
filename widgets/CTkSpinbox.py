import sys
import io
import customtkinter as ctk
import tkinter as tk
import threading

class SilentStdErr(io.TextIOBase):
    def write(self, message):
        # Ignore all messages
        pass

    def flush(self):
        pass


class CTkSpinbox(ctk.CTkFrame):
    def __init__(self,
                 master: any,
                 width: int = 100,
                 height: int = 30,
                 start_value: float = 0.0,
                 min_value: float = -1000000000000.0,
                 max_value: float = 1000000000000.0,
                 step_value: float = 1.0,
                 scroll_value: float = 5.0,
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
                 command: any = None,
                 wait_for: float = 0.05,
                 logarithm_step: bool = True,
                 disable_wheel = False):  # Add wait_for parameter

        super().__init__(master,
                         height=height,
                         width=width,
                         fg_color=fg_color,
                         border_color=border_color,
                         border_width=border_width,
                         corner_radius=corner_radius)

        self.logarithm_step = logarithm_step
        self.command = command
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
        self.manual_input = False  # Track if the input was manual

        self.update_timer = None  # Timer for delayed update
        self.wait_for = wait_for  # Set wait_for to delay the update

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
                                       text='▲',
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
        # if logarithm_step:
        #     disable_wheel = True
        if disable_wheel == False:
            self.bind('<MouseWheel>', self.scroll)

            # FOR LINUX
            self.bind('<Button-4>', self.scroll_up)
            self.bind('<Button-5>', self.scroll_down)

        # update state
        if self.state == 'disabled':
            self.disable()

    def validate_entry(self, new_value):
        '''Validates the entry field to allow only floats.'''
        if new_value == "":
            self.counter_var.set(0)
            return True
        try:
            float(new_value)
            self.manual_input = True
            return True
        except ValueError:
            return False

    def round_value(self, value):
        '''Rounds the value to the same precision as step_value.'''
        precision = len(str(self.step_value).split('.')[1]) if '.' in str(self.step_value) else 0
        return round(value, precision)

    def decrement_counter(self):
        '''Decrements the value of the counter by the step value.'''
        if self.logarithm_step == False:
            new_value = self.counter_var.get() - self.step_value
            if new_value >= self.min_value:
                self.counter_var.set(self.round_value(new_value))
            self.manual_input = False
        else:
            self.use_log_step(increment=False)

        if self.command is not None:
            self.command()

    def increment_counter(self):
        '''Increments the value of the counter by the step value.'''
        if self.logarithm_step == False:
            new_value = self.counter_var.get() + self.step_value
            if new_value <= self.max_value:
                self.counter_var.set(self.round_value(new_value))
            self.manual_input = False
            self.schedule_update()
        else:
            self.use_log_step(increment=True)
        if self.command is not None:
            self.command()

    def scroll(self, scroll):
        '''Increments/Decrements the value of the counter by the scroll value depending on scroll direction.

            THIS IS FOR WINDOWS
        '''
        if self.state == 'normal':
            dirn = 1 if scroll.delta > 0 else -1
            new_value = self.counter_var.get() + dirn * self.scroll_value
            self.counter_var.set(self.round_value(new_value))
            self.manual_input = False
            self.schedule_update()

    def scroll_up(self, event=None):
        '''Increments the value of the counter by the scroll value.'''
        if self.state == 'normal':
            self.use_log_step(increment=True)
            if self.logarithm_step == False:
                new_value = self.counter_var.get() + self.scroll_value
                if new_value <= self.max_value:
                    self.counter_var.set(self.round_value(new_value))
                self.manual_input = False
                self.schedule_update()


    def scroll_down(self, event=None):
        '''Decrements the value of the counter by the scroll value.'''
        if self.state == 'normal':
            self.use_log_step(increment=False)
            if self.logarithm_step == False:
                new_value = self.counter_var.get() - self.scroll_value
                if new_value >= self.min_value:
                    self.counter_var.set(self.round_value(new_value))
                self.manual_input = False
                self.schedule_update()

    def schedule_update(self):
        '''Schedules an update of the counter after a delay.'''
        if self.update_timer:
            self.update_timer.cancel()
        self.update_timer = threading.Timer(self.wait_for, self.update_counter, [None])
        self.update_timer.start()

        if self.command is not None:
            self.command()


    def get(self):
        '''Returns the value of the counter.'''
        return self.counter_var.get()

    def set(self, value):
        '''Sets the counter to a particular value.'''
        self.counter_var.set(self.round_value(max(min(value, self.max_value), self.min_value)))
        self.manual_input = False

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
        '''Binds a key to a function.'''
        super().bind(key, function, add)
        self.counter.bind(key, function, add)
        self.increment.bind(key, function, add)
        self.decrement.bind(key, function, add)

    def update_counter(self, event):
        '''Updates the counter variable and calls the counter command.'''
        if self.update_timer:
            self.update_timer.cancel()
            self.update_timer = None

        if self.manual_input:
            try:
                value = float(self.counter_var.get())
            except ValueError:
                value = self.min_value
        else:
            try:
                value = float(self.counter_var.get())
                value = self.round_value(value)
            except ValueError:
                value = self.min_value

        # Ensure the value is within bounds
        value = max(min(value, self.max_value), self.min_value)

        # Set the counter variable to the adjusted value
        self.counter_var.set(value)

        # Update the variable if provided
        if self.variable:
            self.variable.set(value)

        # Call the command if provided
        if self.command:
            self.command(value)

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

        for value in ['min_value', 'max_value', 'step_value', 'scroll_value', 'variable', 'wait_for']:
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

    def use_log_step(self, increment):
        v = self.counter_var.get()
        if self.logarithm_step:
            if increment:
                new_v = v * 10 # Decrement
            else:
                new_v = v / 10
            if new_v < self.max_value and new_v > self.min_value:
                self.counter_var.set(new_v)

    def destroy(self):
        if self.update_timer:
            self.update_timer.cancel()
            self.update_timer = None
        super().destroy()

# Test the CTkSpinbox
if __name__ == "__main__":
    def print_label(count):
        print(count)

    window = ctk.CTk()
    window.geometry('200x150')

    spin_var = ctk.DoubleVar()
    spinbox = CTkSpinbox(window,
                         start_value=1.5,
                         min_value=-2,
                         max_value=7,
                         step_value=1,
                         scroll_value=1,
                         variable=spin_var,
                         command=print_label,
                         logarithm_step=False,
                         disable_wheel = False
                         )

    spinbox.pack(expand=True, fill='x')  # Use fill='x' to make it expand horizontally
    window.mainloop()
