import random
import colorsys

class ColorPalette:
    
    PREDEFINED_PALETTES = {
        'warm': [(255, 107, 107), (255, 142, 83), (255, 193, 7), (220, 53, 69), (255, 87, 51)],
        'cool': [(0, 123, 255), (23, 162, 184), (40, 167, 69), (111, 66, 193), (108, 117, 125)],
        'pastel': [(255, 179, 186), (255, 223, 186), (186, 255, 201), (186, 225, 255), (205, 180, 219)],
        'vibrant': [(255, 0, 128), (0, 255, 128), (128, 0, 255), (255, 128, 0), (0, 128, 255)],
        'monochrome': [(50, 50, 50), (100, 100, 100), (150, 150, 150), (200, 200, 200), (250, 250, 250)],
        'earth': [(139, 69, 19), (160, 82, 45), (210, 180, 140), (222, 184, 135), (245, 245, 220)],
        'ocean': [(0, 119, 190), (0, 180, 216), (144, 224, 239), (173, 232, 244), (202, 240, 248)],
        'sunset': [(255, 94, 77), (255, 154, 0), (255, 206, 84), (255, 238, 173), (161, 136, 127)],
        'forest': [(34, 139, 34), (107, 142, 35), (154, 205, 50), (124, 252, 0), (50, 205, 50)],
        'neon': [(255, 20, 147), (0, 255, 255), (255, 255, 0), (255, 105, 180), (0, 255, 0)]
    }
    
    def __init__(self, colors=None):
        if colors is None:
            self.colors = self.PREDEFINED_PALETTES['vibrant']
        elif isinstance(colors, str):
            self.colors = self.PREDEFINED_PALETTES.get(colors, self.PREDEFINED_PALETTES['vibrant'])
        else:
            self.colors = colors
    
    @classmethod
    def from_name(cls, name):
        return cls(cls.PREDEFINED_PALETTES.get(name, 'vibrant'))
    
    @classmethod
    def random_palette(cls, count=5):
        colors = []
        for _ in range(count):
            hue = random.random()
            saturation = random.uniform(0.5, 1.0)
            value = random.uniform(0.5, 1.0)
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            colors.append(tuple(int(c * 255) for c in rgb))
        return cls(colors)
    
    @classmethod
    def complementary_palette(cls, base_color):
        if isinstance(base_color, str):
            base_color = cls._hex_to_rgb(base_color)
        
        r, g, b = [c / 255.0 for c in base_color]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        
        colors = [base_color]
        
        complement_h = (h + 0.5) % 1.0
        complement_rgb = colorsys.hsv_to_rgb(complement_h, s, v)
        colors.append(tuple(int(c * 255) for c in complement_rgb))
        
        for i in [0.2, 0.8, 0.6]:
            new_v = min(1.0, v * i + 0.3)
            new_s = min(1.0, s * (1.5 - i))
            rgb = colorsys.hsv_to_rgb(h, new_s, new_v)
            colors.append(tuple(int(c * 255) for c in rgb))
        
        return cls(colors)
    
    @classmethod
    def analogous_palette(cls, base_color, count=5):
        if isinstance(base_color, str):
            base_color = cls._hex_to_rgb(base_color)
        
        r, g, b = [c / 255.0 for c in base_color]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        
        colors = []
        angle_step = 60 / count
        
        for i in range(count):
            new_h = (h + (i - count//2) * angle_step / 360) % 1.0
            new_s = min(1.0, s + random.uniform(-0.2, 0.2))
            new_v = min(1.0, v + random.uniform(-0.2, 0.2))
            rgb = colorsys.hsv_to_rgb(new_h, new_s, new_v)
            colors.append(tuple(int(c * 255) for c in rgb))
        
        return cls(colors)
    
    def get_random_color(self):
        return random.choice(self.colors)
    
    def get_color(self, index):
        return self.colors[index % len(self.colors)]
    
    def add_color(self, color):
        if isinstance(color, str):
            color = self._hex_to_rgb(color)
        self.colors.append(color)
    
    def blend_colors(self, color1, color2, ratio=0.5):
        if isinstance(color1, int):
            color1 = self.colors[color1]
        if isinstance(color2, int):
            color2 = self.colors[color2]
        
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        
        return (r, g, b)
    
    def get_gradient_colors(self, start_color, end_color, steps):
        if isinstance(start_color, int):
            start_color = self.colors[start_color]
        if isinstance(end_color, int):
            end_color = self.colors[end_color]
        
        gradient_colors = []
        for i in range(steps):
            ratio = i / (steps - 1) if steps > 1 else 0
            color = self.blend_colors(start_color, end_color, ratio)
            gradient_colors.append(color)
        
        return gradient_colors
    
    def darken_color(self, color, factor=0.8):
        if isinstance(color, int):
            color = self.colors[color]
        return tuple(int(c * factor) for c in color)
    
    def lighten_color(self, color, factor=1.2):
        if isinstance(color, int):
            color = self.colors[color]
        return tuple(min(255, int(c * factor)) for c in color)
    
    @staticmethod
    def _hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def _rgb_to_hex(rgb_color):
        return f"#{rgb_color[0]:02x}{rgb_color[1]:02x}{rgb_color[2]:02x}"
    
    def __len__(self):
        return len(self.colors)
    
    def __iter__(self):
        return iter(self.colors)
    
    def __getitem__(self, index):
        return self.colors[index] 