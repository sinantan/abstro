# Abstro

**Abstro** is a Python module for generating abstract procedural art using algorithmic patterns and randomness. It creates 2D abstract compositions with geometric shapes, colors, gradients, and noise effects.

## 🎨 Features

- **Geometric Shapes**: Circles, polygons, lines, bezier curves, and noise support
- **Oil Painting Simulation**: Realistic brush strokes, canvas texture, color mixing, and impasto effects
- **Seed-based Deterministic**: Reproducible results with seed support
- **Multiple Formats**: PNG, JPG, SVG export support
- **Color Palettes**: Predefined and custom color palettes
- **Modular Design**: Easy to extend with new pattern generators
- **CLI Support**: Command-line interface
- **16 Presets**: Including 4 oil painting styles: organic, mosaic, minimal, chaos, oil_painting, oil_impressionist, etc.

## 📦 Installation

```bash
git clone https://github.com/sinantan/abstro

cd abstro

pip install -r requirements.txt

pip install -e .
```

## 🚀 Quick Start

### Python API

```python
import abstro

# Simple usage
canvas = abstro.generate(
    width=800,
    height=600,
    preset="oil_painting",
    seed=42,
    output="myart.png"
)

# Custom configuration
from abstro import Canvas
from abstro.core.generator import OilPaintingGenerator

canvas = Canvas(800, 600, seed=123)
canvas.set_palette('sunset')

generator = OilPaintingGenerator(
    complexity=80,
    brush_size='mixed',
    paint_thickness=0.9,
    color_mixing=0.8,
    texture_density=0.5,
    stroke_variation=1.0
)

generator.apply(canvas)
canvas.save("oil_art.png")
```

### CLI Usage

```bash
# Basic usage
abstro -o art.png --preset oil_painting --seed 42

# More options
abstro -o impressionist.svg --preset oil_impressionist --complexity 80 --width 1200 --height 800

# With background color
abstro -o minimal.png --preset minimal --background "#f0f0f0"

# List available presets
abstro --list-presets

# List available color palettes
abstro --list-palettes
```

## 🎨 Available Presets

### Standard Presets
| Preset | Description |
|--------|-------------|
| `organic` | Natural, flowing shapes with earth colors |
| `mosaic` | Colorful geometric mosaic pattern |
| `minimal` | Clean, minimal design with limited elements |
| `chaos` | High energy, chaotic composition |
| `sunset` | Warm, sunset-inspired organic shapes |
| `geometric` | Clean geometric shapes and patterns |
| `flow` | Flowing, water-like bezier curves |
| `pastel_dream` | Soft, dreamy pastel circles |
| `line_art` | Minimalist line-based composition |
| `warm_abstract` | Warm, abstract organic forms |
| `grid_modern` | Modern grid-based geometric pattern |
| `forest` | Nature-inspired green organic shapes |


## 🎨 Color Palettes

- `warm` - Warm colors (red, orange, yellow)
- `cool` - Cool colors (blue, green, purple)
- `pastel` - Pastel tones
- `vibrant` - Vibrant colors
- `monochrome` - Grayscale tones
- `earth` - Earth colors
- `ocean` - Ocean colors
- `sunset` - Sunset colors
- `forest` - Forest colors
- `neon` - Neon colors


### **Technical Features:**
- **Canvas Texture**: Simulates real canvas grain
- **Layered Painting**: 4 layers (background, midground, highlights, details)
- **Brush Strokes**: Bezier curve-based brush stroke simulation
- **Color Mixing**: Realistic color blending between strokes
- **Impasto Effect**: Thick paint (impasto) technique simulation
- **Variable Brush Sizes**: fine, medium, thick, mixed
- **Natural Variation**: Natural brush stroke variations

### **Parameters:**
- `brush_size`: 'fine', 'medium', 'thick', 'mixed'
- `paint_thickness`: 0.0-1.0 (thickness of paint layers)
- `color_mixing`: 0.0-1.0 (amount of color blending)
- `texture_density`: 0.0-1.0 (canvas texture visibility)
- `stroke_variation`: 0.0-2.0 (natural stroke variation)

## 🛠 Advanced Usage

### Custom Pattern Generator

```python
from abstro.core.generator import PatternGenerator
import random

class CustomGenerator(PatternGenerator):
    def apply(self, canvas):
        for _ in range(self.complexity):
            # Your custom pattern logic
            x = random.randint(0, canvas.width)
            y = random.randint(0, canvas.height)
            canvas.add_circle(x, y, 20, fill=canvas.get_random_color())
```

### Custom Oil Painting

```python
from abstro import Canvas
from abstro.core.generator import OilPaintingGenerator

canvas = Canvas(800, 600, seed=42)
canvas.set_palette('warm')

generator = OilPaintingGenerator(
    complexity=100,
    brush_size='thick',
    paint_thickness=1.0,    # Very thick paint
    color_mixing=0.9,       # High color mixing
    texture_density=0.7,    # Visible canvas texture
    stroke_variation=1.2    # High stroke variation
)

generator.apply(canvas)
canvas.save("thick_impasto.png")
```

### Custom Color Palette

```python
from abstro import ColorPalette

# Custom colors
custom_colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
palette = ColorPalette(custom_colors)

# Complementary palette
palette = ColorPalette.complementary_palette((255, 0, 0))

# Random palette
palette = ColorPalette.random_palette(count=5)
```

## 📁 Project Structure

```
abstro/
├── abstro/
│   ├── __init__.py          # Main module interface
│   ├── cli.py               # CLI commands
│   ├── core/
│   │   ├── canvas.py        # Canvas class
│   │   ├── color.py         # Color management
│   │   └── generator.py     # Pattern generators 
│   ├── generators/          # Generator modules
│   └── presets/
│       └── presets.py       # Predefined styles
├── requirements.txt         # Dependencies
├── setup.py                # Installation script
├── example.py              # Example usage
└── README.md               # This file
```

## 🔧 Dependencies

- `Pillow>=10.0.0` - Image processing
- `numpy>=1.24.0` - Mathematical operations
- `matplotlib>=3.7.0` - Plotting (for future features)
- `click>=8.0.0` - CLI interface

## 📖 Examples

### Run the example scripts:

```bash
# Basic examples
python example.py

```

### CLI Examples:

```bash
# Oil painting styles
python -m abstro.cli -o classic_oil.png --preset oil_painting --seed 42
python -m abstro.cli -o impressionist.png --preset oil_impressionist --width 1200
python -m abstro.cli -o abstract_oil.svg --preset oil_abstract --complexity 100
python -m abstro.cli -o portrait_oil.jpg --preset oil_portrait --seed 999

# Other styles  
python -m abstro.cli -o organic.png --preset organic --complexity 50
python -m abstro.cli -o mosaic.png --preset mosaic --palette vibrant
python -m abstro.cli -o minimal.svg --preset minimal --background "#ffffff"

# Custom parameters
python -m abstro.cli -o custom.png --preset organic --complexity 80 --palette sunset
```

## 🎯 CLI Commands Reference

```bash
# Generate single image
abstro -o OUTPUT --preset PRESET [OPTIONS]

# Options:
  -o, --output PATH           Output file path (required)
  -w, --width INTEGER         Canvas width in pixels (default: 800)
  -h, --height INTEGER        Canvas height in pixels (default: 600) 
  -s, --seed INTEGER          Random seed for reproducible results
  -p, --preset TEXT           Preset style name (default: organic)
  -c, --complexity INTEGER    Number of elements to generate
  --palette TEXT              Color palette name
  --shape-type [circle|polygon|line|bezier|noise|mixed]
  --background TEXT           Background color (hex or rgb)
  --list-presets              Show all available presets
  --list-palettes             Show all available color palettes
  --verbose                   Verbose output
```
## 🖼️ Example Images

Here are some examples of what Abstro can generate:

![Example 1](https://raw.githubusercontent.com/sinantan/abstro/refs/heads/main/abstro/examples/chaos.png)

![Example 2](https://raw.githubusercontent.com/sinantan/abstro/refs/heads/main/abstro/examples/oil_abstract.png)

![Example 3](https://raw.githubusercontent.com/sinantan/abstro/refs/heads/main/abstro/examples/oil_impressionist.png)

![Example 4](https://raw.githubusercontent.com/sinantan/abstro/refs/heads/main/abstro/examples/line_art.png)



## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

