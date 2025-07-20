import random
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import StringIO
import xml.etree.ElementTree as ET

from .color import ColorPalette

class Canvas:
    def __init__(self, width=800, height=600, seed=None, background_color=None):
        self.width = width
        self.height = height
        self.seed = seed
        
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        self.image = Image.new('RGB', (width, height), background_color or (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        self.palette = ColorPalette()
        self.elements = []
        
        # For SVG export
        self.svg_elements = []
    
    def set_palette(self, palette):
        if isinstance(palette, list):
            self.palette = ColorPalette(palette)
        elif isinstance(palette, ColorPalette):
            self.palette = palette
        else:
            self.palette = ColorPalette.from_name(palette)
    
    def get_random_color(self, alpha=255):
        color = self.palette.get_random_color()
        if alpha < 255:
            return (*color, alpha)
        return color
    
    def clear(self, color=(255, 255, 255)):
        self.image = Image.new('RGB', (self.width, self.height), color)
        self.draw = ImageDraw.Draw(self.image)
        self.elements = []
        self.svg_elements = []
    
    def add_circle(self, x, y, radius, fill=None, outline=None, width=1):
        fill = fill or self.get_random_color()
        bbox = (x - radius, y - radius, x + radius, y + radius)
        self.draw.ellipse(bbox, fill=fill, outline=outline, width=width)
        
        self.svg_elements.append({
            'type': 'circle',
            'cx': x, 'cy': y, 'r': radius,
            'fill': f'rgb{fill[:3]}',
            'stroke': f'rgb{outline[:3]}' if outline else 'none',
            'stroke-width': width
        })
        
        self.elements.append(('circle', x, y, radius, fill, outline, width))
    
    def add_polygon(self, points, fill=None, outline=None, width=1):
        fill = fill or self.get_random_color()
        self.draw.polygon(points, fill=fill, outline=outline, width=width)
        
        points_str = ' '.join([f'{x},{y}' for x, y in points])
        self.svg_elements.append({
            'type': 'polygon',
            'points': points_str,
            'fill': f'rgb{fill[:3]}',
            'stroke': f'rgb{outline[:3]}' if outline else 'none',
            'stroke-width': width
        })
        
        self.elements.append(('polygon', points, fill, outline, width))
    
    def add_line(self, x1, y1, x2, y2, fill=None, width=2):
        fill = fill or self.get_random_color()
        self.draw.line([(x1, y1), (x2, y2)], fill=fill, width=width)
        
        self.svg_elements.append({
            'type': 'line',
            'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
            'stroke': f'rgb{fill[:3]}',
            'stroke-width': width
        })
        
        self.elements.append(('line', x1, y1, x2, y2, fill, width))
    
    def add_bezier(self, points, fill=None, width=2):
        fill = fill or self.get_random_color()
        if len(points) >= 4:
            for i in range(0, len(points) - 3, 3):
                p1, p2, p3, p4 = points[i:i+4]
                self._draw_bezier_curve(p1, p2, p3, p4, fill, width)
    
    def _draw_bezier_curve(self, p1, p2, p3, p4, color, width):
        t_values = np.linspace(0, 1, 50)
        curve_points = []
        
        for t in t_values:
            x = (1-t)**3 * p1[0] + 3*(1-t)**2*t * p2[0] + 3*(1-t)*t**2 * p3[0] + t**3 * p4[0]
            y = (1-t)**3 * p1[1] + 3*(1-t)**2*t * p2[1] + 3*(1-t)*t**2 * p3[1] + t**3 * p4[1]
            curve_points.append((int(x), int(y)))
        
        for i in range(len(curve_points) - 1):
            self.draw.line([curve_points[i], curve_points[i+1]], fill=color, width=width)
        
        self.elements.append(('bezier', [p1, p2, p3, p4], color, width))
    
    def add_noise(self, density=0.1, color_range=None):
        num_pixels = int(self.width * self.height * density)
        for _ in range(num_pixels):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            color = self.get_random_color()
            if color_range:
                color = tuple(max(0, min(255, c + random.randint(-color_range, color_range))) for c in color)
            self.draw.point((x, y), fill=color)
    
    def save(self, filename, format=None):
        if filename.lower().endswith('.svg'):
            self._save_svg(filename)
        else:
            if format is None:
                if filename.lower().endswith('.png'):
                    format = 'PNG'
                elif filename.lower().endswith(('.jpg', '.jpeg')):
                    format = 'JPEG'
                else:
                    format = 'PNG'
            
            self.image.save(filename, format=format)
    
    def _save_svg(self, filename):
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">'''
        
        for element in self.svg_elements:
            if element['type'] == 'circle':
                svg_content += f'''
    <circle cx="{element['cx']}" cy="{element['cy']}" r="{element['r']}" 
            fill="{element['fill']}" stroke="{element['stroke']}" 
            stroke-width="{element['stroke-width']}"/>'''
            elif element['type'] == 'polygon':
                svg_content += f'''
    <polygon points="{element['points']}" 
             fill="{element['fill']}" stroke="{element['stroke']}" 
             stroke-width="{element['stroke-width']}"/>'''
            elif element['type'] == 'line':
                svg_content += f'''
    <line x1="{element['x1']}" y1="{element['y1']}" 
          x2="{element['x2']}" y2="{element['y2']}" 
          stroke="{element['stroke']}" stroke-width="{element['stroke-width']}"/>'''
        
        svg_content += '\n</svg>'
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(svg_content)
    
    def show(self):
        self.image.show()
    
    def copy(self):
        new_canvas = Canvas(self.width, self.height, seed=None)
        new_canvas.image = self.image.copy()
        new_canvas.draw = ImageDraw.Draw(new_canvas.image)
        new_canvas.palette = self.palette
        new_canvas.elements = self.elements.copy()
        new_canvas.svg_elements = self.svg_elements.copy()
        return new_canvas 