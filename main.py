import tkinter as tk
import math
import time
import random

class FloatingHeart:
    def __init__(self, root):
        self.root = root
        self.root.title("Magic Heart")
        self.root.overrideredirect(True)
        self.root.attributes('-transparentcolor', 'gray10')
        self.root.attributes('-topmost', True)

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        self.canvas = tk.Canvas(root, width=self.screen_width, height=self.screen_height, bg='gray10', highlightthickness=0)
        self.canvas.pack()

        self.angle = 0
        self.scale_factor = 1
        self.scale_direction = 1
        self.y_offset = 0
        self.y_direction = 1

        self.x = 0
        self.y = 0

        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.do_move)
        self.canvas.bind("<Double-Button-1>", self.reverse_animation)

        self.animate()

    def draw_heart(self, scale=1, y_offset=0, color="#ff0000"):
        self.canvas.delete("heart")
        points = []
        for t in range(0, 628, 10):
            t = t / 100
            x = 16 * math.sin(t) ** 3
            y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            points.append((self.screen_width // 2 + x * 10 * scale, self.screen_height // 2 + y * 10 * scale + y_offset))

        self.canvas.create_polygon(points, fill=color, outline="white", width=2, smooth=True, tags="heart")

    def animate(self):
        while True:
            hue = (time.time() * 100) % 360
            color = self.hsl_to_rgb(hue, 0.9, 0.6)

            self.scale_factor += 0.005 * self.scale_direction
            if self.scale_factor >= 1.2 or self.scale_factor <= 0.8:
                self.scale_direction *= -1  

            self.y_offset += 0.5 * self.y_direction
            if self.y_offset >= 10 or self.y_offset <= -10:
                self.y_direction *= -1  

            self.draw_heart(scale=self.scale_factor, y_offset=self.y_offset, color=color)
            self.canvas.update()
            time.sleep(0.01)

    def hsl_to_rgb(self, h, s, l):
        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = l - c / 2
        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        return f"#{int((r + m) * 255):02x}{int((g + m) * 255):02x}{int((b + m) * 255):02x}"

    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        self.spawn_heart_emojis(event.x, event.y)

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def reverse_animation(self, event):
        self.scale_direction *= -1
        self.y_direction *= -1

    def spawn_heart_emojis(self, x, y):
        emojis = ['❤️', '💛', '💚', '💙', '💜', '🧡', '💖']
        for _ in range(100):
            size = random.randint(25, 50)
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(15, 30)
            self.animate_emoji(x, y, angle, speed, size, random.choice(emojis))

    def animate_emoji(self, start_x, start_y, angle, speed, size, emoji):
        emoji_id = self.canvas.create_text(start_x, start_y, text=emoji, font=("Arial", size), fill="white")
        dx = speed * math.cos(angle)
        dy = speed * math.sin(angle)
        gravity = 0.5  
        resistance = 0.98  

        def move_emoji():
            nonlocal start_x, start_y, dx, dy
            start_x += dx
            start_y += dy
            dy += gravity  
            dx *= resistance  
            dy *= resistance  

            self.canvas.coords(emoji_id, start_x, start_y)

            if 0 <= start_x <= self.screen_width and 0 <= start_y <= self.screen_height:
                self.canvas.after(30, move_emoji)
            else:
                self.canvas.delete(emoji_id)

        move_emoji()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    app = FloatingHeart(root)
    root.mainloop()
