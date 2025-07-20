from .core.canvas import Canvas
from .core.color import ColorPalette
from .core.generator import PatternGenerator, OrganicGenerator, GeometricGenerator, OilPaintingGenerator
from .presets.presets import get_preset

__version__ = "0.1.0"
__all__ = ["Canvas", "ColorPalette", "PatternGenerator", "OrganicGenerator", "GeometricGenerator", "OilPaintingGenerator", "get_preset", "generate"]

def generate(width=800, height=600, preset="organic", seed=None, output=None, **kwargs):
    """Generate an abstract image with the given parameters."""
    preset_config = get_preset(preset)
    preset_config.update(kwargs)
    
    canvas = Canvas(width, height, seed=seed)
    
    if preset_config.get('palette'):
        canvas.set_palette(preset_config['palette'])
    
    generator_type = preset_config.get('generator_type', 'pattern')
    
    if generator_type == 'organic':
        generator = OrganicGenerator(**preset_config)
    elif generator_type == 'geometric':
        generator = GeometricGenerator(**preset_config)
    elif generator_type == 'oil_painting':
        generator = OilPaintingGenerator(**preset_config)
    else:  # pattern
        generator = PatternGenerator(**preset_config)
    
    generator.apply(canvas)
    
    if output:
        canvas.save(output)
    
    return canvas 