import customtkinter as ctk
import math

class EncoderKnob(ctk.CTkCanvas):
    def __init__(self, master, command=None, width=150, height=150, bg_color = '#222', outline_color = '#222', **kwargs):
        super().__init__(master, width=width, height=height, highlightthickness=0, **kwargs)

        self.command = command
        self.width = width
        self.height = height
        self.value = 0

        self.center = (width // 2, height // 2)
        self.radius = min(width, height) // 2 - 10
        self.angle = 0

        # Tło pokrętła
        self.bg_circle = self.create_oval(
            10, 10, width - 10, height - 10,
            outline=outline_color, fill=bg_color, width=3
        )

        self.draw_ticks()
        self.indicator = self.create_triangle(self.angle)  # spiczasta wskazówka

        # Punkt centralny
        self.create_oval(
            self.center[0] - 6, self.center[1] - 6,
            self.center[0] + 6, self.center[1] + 6,
            fill="#00BFFF", outline=""
        )

        self.bind("<Button-1>", self.start_rotate)
        self.bind("<B1-Motion>", self.rotate)
        self.bind_all("<MouseWheel>", self.mouse_wheel)  # Obsługa scrolla myszy
        self.last_angle = None

    def draw_ticks(self, count=20):
        for i in range(count):
            angle = math.radians(i * (360 / count))
            inner = (
                self.center[0] + (self.radius - 8) * math.cos(angle),
                self.center[1] - (self.radius - 8) * math.sin(angle)
            )
            outer = (
                self.center[0] + self.radius * math.cos(angle),
                self.center[1] - self.radius * math.sin(angle)
            )
            self.create_line(inner[0], inner[1], outer[0], outer[1], fill="#555", width=1)

    def create_triangle(self, angle):
        # Współrzędne spiczastej wskazówki (trójkąt)
        base_radius = self.radius - 30
        tip_radius = self.radius - 4
        width = 6  # szerokość podstawy

        angle_rad = math.radians(angle)
        x_tip = self.center[0] + tip_radius * math.cos(angle_rad)
        y_tip = self.center[1] - tip_radius * math.sin(angle_rad)

        left_rad = math.radians(angle + 90)
        x_left = self.center[0] + base_radius * math.cos(angle_rad) + width * math.cos(left_rad)
        y_left = self.center[1] - base_radius * math.sin(angle_rad) - width * math.sin(left_rad)

        right_rad = math.radians(angle - 90)
        x_right = self.center[0] + base_radius * math.cos(angle_rad) + width * math.cos(right_rad)
        y_right = self.center[1] - base_radius * math.sin(angle_rad) - width * math.sin(right_rad)

        return self.create_polygon(x_tip, y_tip, x_left, y_left, x_right, y_right,
                                   fill="#00BFFF", outline="#00BFFF")

    def update_indicator(self, angle):
        self.angle = angle
        self.delete(self.indicator)
        self.indicator = self.create_triangle(angle)

    def get_angle(self, x, y):
        dx = x - self.center[0]
        dy = y - self.center[1]
        angle = math.degrees(math.atan2(-dy, dx)) % 360
        return angle

    def start_rotate(self, event):
        self.last_angle = self.get_angle(event.x, event.y)

    def rotate(self, event):
        angle = self.get_angle(event.x, event.y)
        delta = (angle - self.last_angle) % 360
        if delta > 180:
            delta -= 360
        self.last_angle = angle

        self.value += int(delta / 5)
        if self.command:
            self.command(self.value)
        self.update_indicator(angle)

    def mouse_wheel(self, event):
        delta = event.delta // 120  # standardowe skoki
        self.value += delta
        self.angle = (self.angle + delta * 5) % 360  # zmiana kąta wskazówki
        self.update_indicator(self.angle)
        if self.command:
            self.command(self.value)

if __name__ == "__main__":
    def on_knob_change(val):
        print("Nowa wartość:", val)

    root = ctk.CTk()
    root.title("Endless Encoder z trójkątną wskazówką i scroll'em")

    knob = EncoderKnob(root, command=on_knob_change, width=150, height=150)
    knob.pack(padx=20, pady=20)

    root.mainloop()
