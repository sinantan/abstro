import random
import math
import numpy as np
from abc import ABC, abstractmethod

class PatternGenerator:
    def __init__(self, **kwargs):
        self.params = kwargs
        self.complexity = kwargs.get('complexity', 50)
        self.shape_type = kwargs.get('shape_type', 'mixed')
        self.blend_mode = kwargs.get('blend_mode', 'normal')
        self.generators = []
        
        self._setup_generators()
    
    def _setup_generators(self):
        if self.shape_type == 'circle' or self.shape_type == 'mixed':
            self.generators.append(CircleGenerator(**self.params))
        if self.shape_type == 'polygon' or self.shape_type == 'mixed':
            self.generators.append(PolygonGenerator(**self.params))
        if self.shape_type == 'line' or self.shape_type == 'mixed':
            self.generators.append(LineGenerator(**self.params))
        if self.shape_type == 'bezier' or self.shape_type == 'mixed':
            self.generators.append(BezierGenerator(**self.params))
        if self.shape_type == 'noise' or self.shape_type == 'mixed':
            self.generators.append(NoiseGenerator(**self.params))
    
    def apply(self, canvas):
        if self.shape_type == 'mixed':
            elements_per_generator = self.complexity // len(self.generators)
            remainder = self.complexity % len(self.generators)
            
            for i, generator in enumerate(self.generators):
                count = elements_per_generator + (1 if i < remainder else 0)
                generator.generate(canvas, count)
        else:
            if self.generators:
                self.generators[0].generate(canvas, self.complexity)

class BaseShapeGenerator(ABC):
    def __init__(self, **kwargs):
        self.params = kwargs
    
    @abstractmethod
    def generate(self, canvas, count):
        pass

class CircleGenerator(BaseShapeGenerator):
    def generate(self, canvas, count):
        for _ in range(count):
            x = random.randint(0, canvas.width)
            y = random.randint(0, canvas.height)
            radius = random.randint(5, min(canvas.width, canvas.height) // 10)
            
            fill = canvas.get_random_color(alpha=random.randint(100, 255))
            outline = canvas.get_random_color() if random.random() < 0.3 else None
            
            canvas.add_circle(x, y, radius, fill=fill, outline=outline)

class PolygonGenerator(BaseShapeGenerator):
    def generate(self, canvas, count):
        for _ in range(count):
            center_x = random.randint(0, canvas.width)
            center_y = random.randint(0, canvas.height)
            sides = random.randint(3, 8)
            radius = random.randint(10, min(canvas.width, canvas.height) // 8)
            
            points = []
            for i in range(sides):
                angle = (2 * math.pi * i) / sides + random.uniform(-0.5, 0.5)
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))
            
            fill = canvas.get_random_color(alpha=random.randint(120, 255))
            outline = canvas.get_random_color() if random.random() < 0.4 else None
            
            canvas.add_polygon(points, fill=fill, outline=outline)

class LineGenerator(BaseShapeGenerator):
    def generate(self, canvas, count):
        for _ in range(count):
            if random.random() < 0.6:  # Straight lines
                x1 = random.randint(0, canvas.width)
                y1 = random.randint(0, canvas.height)
                x2 = random.randint(0, canvas.width)
                y2 = random.randint(0, canvas.height)
            else:  # Connected lines (polylines)
                x1 = random.randint(0, canvas.width)
                y1 = random.randint(0, canvas.height)
                x2 = x1 + random.randint(-100, 100)
                y2 = y1 + random.randint(-100, 100)
            
            fill = canvas.get_random_color()
            width = random.randint(1, 8)
            
            canvas.add_line(x1, y1, x2, y2, fill=fill, width=width)

class BezierGenerator(BaseShapeGenerator):
    def generate(self, canvas, count):
        for _ in range(count):
            points = []
            start_x = random.randint(0, canvas.width)
            start_y = random.randint(0, canvas.height)
            
            for i in range(4):  # Cubic bezier needs 4 points
                if i == 0:
                    x, y = start_x, start_y
                else:
                    x = random.randint(max(0, start_x - 200), min(canvas.width, start_x + 200))
                    y = random.randint(max(0, start_y - 200), min(canvas.height, start_y + 200))
                points.append((x, y))
            
            fill = canvas.get_random_color()
            width = random.randint(2, 10)
            
            canvas.add_bezier(points, fill=fill, width=width)

class NoiseGenerator(BaseShapeGenerator):
    def generate(self, canvas, count):
        density = self.params.get('noise_density', 0.001)
        color_range = self.params.get('noise_color_range', 30)
        
        canvas.add_noise(density=density, color_range=color_range)

class OrganicGenerator(PatternGenerator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flow_field_strength = kwargs.get('flow_field_strength', 0.5)
        self.organic_factor = kwargs.get('organic_factor', 0.8)
    
    def apply(self, canvas):
        for _ in range(self.complexity):
            if random.random() < 0.4:
                self._generate_organic_shape(canvas)
            elif random.random() < 0.7:
                self._generate_flowing_line(canvas)
            else:
                self._generate_blob(canvas)
    
    def _generate_organic_shape(self, canvas):
        center_x = random.randint(50, canvas.width - 50)
        center_y = random.randint(50, canvas.height - 50)
        base_radius = random.randint(20, 80)
        
        points = []
        sides = random.randint(6, 16)
        
        for i in range(sides):
            angle = (2 * math.pi * i) / sides
            noise_factor = 1 + random.uniform(-self.organic_factor, self.organic_factor)
            radius = base_radius * noise_factor
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        
        fill = canvas.get_random_color(alpha=random.randint(80, 200))
        canvas.add_polygon(points, fill=fill)
    
    def _generate_flowing_line(self, canvas):
        start_x = random.randint(0, canvas.width)
        start_y = random.randint(0, canvas.height)
        
        points = [(start_x, start_y)]
        current_x, current_y = start_x, start_y
        
        for _ in range(random.randint(5, 15)):
            angle = random.uniform(0, 2 * math.pi)
            length = random.randint(10, 50)
            
            current_x += length * math.cos(angle) * self.flow_field_strength
            current_y += length * math.sin(angle) * self.flow_field_strength
            
            current_x = max(0, min(canvas.width, current_x))
            current_y = max(0, min(canvas.height, current_y))
            
            points.append((current_x, current_y))
        
        if len(points) >= 4:
            fill = canvas.get_random_color()
            width = random.randint(2, 8)
            canvas.add_bezier(points, fill=fill, width=width)
    
    def _generate_blob(self, canvas):
        x = random.randint(0, canvas.width)
        y = random.randint(0, canvas.height)
        radius = random.randint(5, 40)
        
        fill = canvas.get_random_color(alpha=random.randint(100, 180))
        canvas.add_circle(x, y, radius, fill=fill)

class GeometricGenerator(PatternGenerator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.symmetry = kwargs.get('symmetry', False)
        self.grid_based = kwargs.get('grid_based', False)
    
    def apply(self, canvas):
        if self.grid_based:
            self._generate_grid_pattern(canvas)
        elif self.symmetry:
            self._generate_symmetric_pattern(canvas)
        else:
            self._generate_geometric_shapes(canvas)
    
    def _generate_grid_pattern(self, canvas):
        grid_size = int(math.sqrt(self.complexity))
        cell_width = canvas.width // grid_size
        cell_height = canvas.height // grid_size
        
        for i in range(grid_size):
            for j in range(grid_size):
                center_x = i * cell_width + cell_width // 2
                center_y = j * cell_height + cell_height // 2
                
                shape_type = random.choice(['circle', 'polygon', 'line'])
                fill = canvas.get_random_color()
                
                if shape_type == 'circle':
                    radius = min(cell_width, cell_height) // 4
                    canvas.add_circle(center_x, center_y, radius, fill=fill)
                elif shape_type == 'polygon':
                    sides = random.randint(3, 6)
                    radius = min(cell_width, cell_height) // 4
                    points = []
                    for k in range(sides):
                        angle = (2 * math.pi * k) / sides
                        x = center_x + radius * math.cos(angle)
                        y = center_y + radius * math.sin(angle)
                        points.append((x, y))
                    canvas.add_polygon(points, fill=fill)
    
    def _generate_symmetric_pattern(self, canvas):
        center_x = canvas.width // 2
        center_y = canvas.height // 2
        
        for _ in range(self.complexity // 4):  # Generate quarter, then mirror
            x = random.randint(center_x, canvas.width - 50)
            y = random.randint(center_y, canvas.height - 50)
            
            shape_type = random.choice(['circle', 'polygon'])
            fill = canvas.get_random_color()
            
            if shape_type == 'circle':
                radius = random.randint(5, 30)
                # Four quadrants
                canvas.add_circle(x, y, radius, fill=fill)
                canvas.add_circle(canvas.width - x, y, radius, fill=fill)
                canvas.add_circle(x, canvas.height - y, radius, fill=fill)
                canvas.add_circle(canvas.width - x, canvas.height - y, radius, fill=fill)
            
    def _generate_geometric_shapes(self, canvas):
        for _ in range(self.complexity):
            shape_type = random.choice(['triangle', 'square', 'pentagon', 'hexagon'])
            center_x = random.randint(0, canvas.width)
            center_y = random.randint(0, canvas.height)
            size = random.randint(10, 60)
            
            if shape_type == 'triangle':
                points = [
                    (center_x, center_y - size),
                    (center_x - size * 0.866, center_y + size * 0.5),
                    (center_x + size * 0.866, center_y + size * 0.5)
                ]
            elif shape_type == 'square':
                points = [
                    (center_x - size, center_y - size),
                    (center_x + size, center_y - size),
                    (center_x + size, center_y + size),
                    (center_x - size, center_y + size)
                ]
            else:  # Pentagon, hexagon
                sides = 5 if shape_type == 'pentagon' else 6
                points = []
                for i in range(sides):
                    angle = (2 * math.pi * i) / sides
                    x = center_x + size * math.cos(angle)
                    y = center_y + size * math.sin(angle)
                    points.append((x, y))
            
            fill = canvas.get_random_color(alpha=random.randint(120, 255))
            canvas.add_polygon(points, fill=fill)

class OilPaintingGenerator(PatternGenerator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.brush_size = kwargs.get('brush_size', 'medium')
        self.paint_thickness = kwargs.get('paint_thickness', 0.7)
        self.color_mixing = kwargs.get('color_mixing', 0.8)
        self.texture_density = kwargs.get('texture_density', 0.3)
        self.stroke_variation = kwargs.get('stroke_variation', 0.9)
    
    def apply(self, canvas):
        # Base texture layer
        self._add_canvas_texture(canvas)
        
        # Paint layers - simulate oil painting technique
        layers = ['background', 'midground', 'highlights', 'details']
        
        for i, layer in enumerate(layers):
            layer_complexity = self.complexity // len(layers)
            alpha_range = self._get_alpha_for_layer(i)
            
            for _ in range(layer_complexity):
                if random.random() < 0.6:
                    self._paint_brush_stroke(canvas, alpha_range, layer)
                elif random.random() < 0.8:
                    self._paint_color_blob(canvas, alpha_range, layer)
                else:
                    self._paint_impasto_effect(canvas, alpha_range)
    
    def _add_canvas_texture(self, canvas):
        # Simulate canvas texture with noise
        texture_density = self.texture_density * 0.005
        for _ in range(int(canvas.width * canvas.height * texture_density)):
            x = random.randint(0, canvas.width - 1)
            y = random.randint(0, canvas.height - 1)
            
            # Subtle canvas color variations
            base_color = canvas.get_random_color()
            noise_color = tuple(
                max(0, min(255, c + random.randint(-15, 15))) for c in base_color
            )
            canvas.draw.point((x, y), fill=noise_color)
    
    def _paint_brush_stroke(self, canvas, alpha_range, layer):
        # Simulate brush strokes with bezier curves
        start_x = random.randint(0, canvas.width)
        start_y = random.randint(0, canvas.height)
        
        # Brush stroke direction and flow
        stroke_length = random.randint(30, 120)
        stroke_angle = random.uniform(0, 2 * math.pi)
        
        points = [(start_x, start_y)]
        current_x, current_y = start_x, start_y
        
        # Create brush stroke path
        segments = random.randint(3, 6)
        for i in range(segments):
            # Add some natural variation to the stroke
            angle_variation = random.uniform(-0.3, 0.3) * self.stroke_variation
            length_segment = stroke_length / segments
            
            current_x += length_segment * math.cos(stroke_angle + angle_variation)
            current_y += length_segment * math.sin(stroke_angle + angle_variation)
            
            # Keep within canvas bounds
            current_x = max(0, min(canvas.width, current_x))
            current_y = max(0, min(canvas.height, current_y))
            
            points.append((current_x, current_y))
        
        if len(points) >= 4:
            color = self._get_paint_color(canvas, layer)
            alpha = random.randint(*alpha_range)
            paint_color = (*color[:3], alpha) if len(color) == 3 else color
            
            # Brush stroke width varies based on pressure
            brush_width = self._get_brush_width()
            canvas.add_bezier(points, fill=paint_color, width=brush_width)
    
    def _paint_color_blob(self, canvas, alpha_range, layer):
        # Simulate paint blobs and color mixing
        x = random.randint(0, canvas.width)
        y = random.randint(0, canvas.height)
        
        # Irregular blob shape
        blob_size = random.randint(10, 40)
        sides = random.randint(8, 16)  # More sides for organic shape
        
        points = []
        for i in range(sides):
            angle = (2 * math.pi * i) / sides
            # Irregular radius for organic blob shape
            radius = blob_size * random.uniform(0.5, 1.5)
            point_x = x + radius * math.cos(angle)
            point_y = y + radius * math.sin(angle)
            points.append((point_x, point_y))
        
        color = self._get_paint_color(canvas, layer)
        alpha = random.randint(*alpha_range)
        paint_color = (*color[:3], alpha) if len(color) == 3 else color
        
        canvas.add_polygon(points, fill=paint_color)
    
    def _paint_impasto_effect(self, canvas, alpha_range):
        # Simulate thick paint (impasto) technique
        x = random.randint(0, canvas.width)
        y = random.randint(0, canvas.height)
        
        # Multiple small thick paint dabs
        for _ in range(random.randint(2, 5)):
            dab_x = x + random.randint(-15, 15)
            dab_y = y + random.randint(-15, 15)
            dab_size = random.randint(3, 12)
            
            if 0 <= dab_x <= canvas.width and 0 <= dab_y <= canvas.height:
                color = canvas.get_random_color()
                alpha = random.randint(180, 255)  # Thick paint is more opaque
                paint_color = (*color[:3], alpha)
                
                canvas.add_circle(dab_x, dab_y, dab_size, fill=paint_color)
    
    def _get_paint_color(self, canvas, layer):
        base_color = canvas.get_random_color()
        
        if self.color_mixing > 0.5:
            # Simulate color mixing
            mix_color = canvas.get_random_color()
            mixing_ratio = random.uniform(0.2, 0.8) * self.color_mixing
            
            mixed_color = (
                int(base_color[0] * (1 - mixing_ratio) + mix_color[0] * mixing_ratio),
                int(base_color[1] * (1 - mixing_ratio) + mix_color[1] * mixing_ratio),
                int(base_color[2] * (1 - mixing_ratio) + mix_color[2] * mixing_ratio)
            )
            return mixed_color
        
        return base_color
    
    def _get_alpha_for_layer(self, layer_index):
        # Different opacity for different layers
        alpha_ranges = [
            (120, 200),  # background
            (100, 180),  # midground
            (150, 220),  # highlights
            (180, 255)   # details
        ]
        return alpha_ranges[layer_index]
    
    def _get_brush_width(self):
        if self.brush_size == 'fine':
            return random.randint(1, 4)
        elif self.brush_size == 'medium':
            return random.randint(3, 8)
        elif self.brush_size == 'thick':
            return random.randint(6, 15)
        else:  # mixed
            return random.randint(1, 12) 