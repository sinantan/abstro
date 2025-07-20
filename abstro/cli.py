import click
import random
from pathlib import Path

from .core.canvas import Canvas
from .core.color import ColorPalette
from .core.generator import PatternGenerator, OrganicGenerator, GeometricGenerator, OilPaintingGenerator
from .presets.presets import get_preset, list_presets as get_preset_list, get_preset_description

@click.command()
@click.option('--output', '-o', help='Output file path (supports .png, .jpg, .svg)')
@click.option('--width', '-w', default=800, help='Canvas width in pixels', type=int)
@click.option('--height', '-h', default=600, help='Canvas height in pixels', type=int)
@click.option('--seed', '-s', help='Random seed for reproducible results', type=int)
@click.option('--preset', '-p', default='organic', help='Preset style name')
@click.option('--complexity', '-c', help='Number of elements to generate', type=int)
@click.option('--palette', help='Color palette name')
@click.option('--shape-type', help='Type of shapes to generate', 
              type=click.Choice(['circle', 'polygon', 'line', 'bezier', 'noise', 'mixed']))
@click.option('--list-presets', is_flag=True, help='List all available presets and exit')
@click.option('--list-palettes', is_flag=True, help='List all available color palettes and exit')
@click.option('--background', help='Background color as hex (e.g., #ffffff) or rgb (255,255,255)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def main(output, width, height, seed, preset, complexity, palette, shape_type, 
         list_presets, list_palettes, background, verbose):
    """Generate abstract procedural art with various styles and patterns.
    
    Examples:
        abstro -o art.png --preset mosaic --seed 42
        abstro -o organic.svg --preset organic --complexity 30
        abstro -o minimal.jpg --preset minimal --width 1200 --height 800
        abstro -o oil.png --preset oil_painting --seed 123
    """
    
    if list_presets:
        click.echo("Available presets:")
        for preset_name in get_preset_list():
            description = get_preset_description(preset_name)
            click.echo(f"  {preset_name:<15} - {description}")
        return
    
    if list_palettes:
        click.echo("Available color palettes:")
        for palette_name in ColorPalette.PREDEFINED_PALETTES.keys():
            colors = ColorPalette.PREDEFINED_PALETTES[palette_name]
            colors_str = ", ".join([f"rgb{c}" for c in colors[:3]])
            click.echo(f"  {palette_name:<12} - {colors_str}...")
        return
    
    # Output is required for actual image generation
    if not output:
        click.echo("Error: Missing option '--output' / '-o' for image generation.", err=True)
        click.echo("Use --list-presets or --list-palettes to see available options.", err=True)
        click.echo("Or provide an output file: abstro -o myart.png --preset organic")
        return
    
    if verbose:
        click.echo(f"Generating abstract art with preset '{preset}'...")
        click.echo(f"Canvas size: {width}x{height}")
        if seed is not None:
            click.echo(f"Random seed: {seed}")
    
    try:
        preset_config = get_preset(preset)
        
        if complexity is not None:
            preset_config['complexity'] = complexity
        if palette is not None:
            preset_config['palette'] = palette
        if shape_type is not None:
            preset_config['shape_type'] = shape_type
        
        background_color = None
        if background:
            background_color = parse_color(background)
        
        canvas = Canvas(width, height, seed=seed, background_color=background_color)
        
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
        
        if verbose:
            click.echo(f"Applying {generator_type} generator with {preset_config.get('complexity', 50)} elements...")
        
        generator.apply(canvas)
        
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        canvas.save(str(output_path))
        
        if verbose:
            click.echo(f"✓ Abstract art saved to: {output_path.absolute()}")
        else:
            click.echo(f"Generated: {output}")
        
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        exit(1)

def parse_color(color_str):
    """Parse color string as hex or rgb tuple."""
    color_str = color_str.strip()
    
    if color_str.startswith('#'):
        # Hex color
        hex_color = color_str.lstrip('#')
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        elif len(hex_color) == 3:
            return tuple(int(hex_color[i]*2, 16) for i in range(3))
        else:
            raise ValueError(f"Invalid hex color: {color_str}")
    
    elif color_str.startswith('(') and color_str.endswith(')'):
        # RGB tuple like (255,255,255)
        rgb_str = color_str.strip('()')
        rgb_parts = [int(x.strip()) for x in rgb_str.split(',')]
        if len(rgb_parts) == 3:
            return tuple(rgb_parts)
        else:
            raise ValueError(f"Invalid RGB color: {color_str}")
    
    elif ',' in color_str:
        # RGB tuple like 255,255,255
        rgb_parts = [int(x.strip()) for x in color_str.split(',')]
        if len(rgb_parts) == 3:
            return tuple(rgb_parts)
        else:
            raise ValueError(f"Invalid RGB color: {color_str}")
    
    else:
        raise ValueError(f"Invalid color format: {color_str}. Use hex (#ffffff) or RGB (255,255,255)")

@click.command()
@click.option('--count', '-n', default=1, help='Number of images to generate', type=int)
@click.option('--output-dir', '-d', default='generated', help='Output directory')
@click.option('--prefix', default='abstro', help='Filename prefix')
@click.option('--format', '-f', default='png', type=click.Choice(['png', 'jpg', 'svg']), 
              help='Output format')
@click.option('--width', '-w', default=800, type=int)
@click.option('--height', '-h', default=600, type=int)
@click.option('--random-presets', is_flag=True, help='Use random presets for each image')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def batch(count, output_dir, prefix, format, width, height, random_presets, verbose):
    """Generate multiple abstract art pieces in batch mode."""
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    presets = get_preset_list() if random_presets else ['organic']
    
    if verbose:
        click.echo(f"Generating {count} images in batch mode...")
        click.echo(f"Output directory: {output_path.absolute()}")
    
    for i in range(count):
        preset = random.choice(presets) if random_presets else presets[0]
        seed = random.randint(0, 999999)
        
        filename = f"{prefix}_{i+1:04d}_{preset}_{seed}.{format}"
        filepath = output_path / filename
        
        if verbose:
            click.echo(f"  [{i+1}/{count}] Generating {filename} with preset '{preset}' (seed: {seed})...")
        
        try:
            preset_config = get_preset(preset)
            canvas = Canvas(width, height, seed=seed)
            canvas.set_palette(preset_config['palette'])
            
            generator_type = preset_config.get('generator_type', 'pattern')
            if generator_type == 'organic':
                generator = OrganicGenerator(**preset_config)
            elif generator_type == 'geometric':
                generator = GeometricGenerator(**preset_config)
            elif generator_type == 'oil_painting':
                generator = OilPaintingGenerator(**preset_config)
            else:
                generator = PatternGenerator(**preset_config)
            
            generator.apply(canvas)
            canvas.save(str(filepath))
            
            if not verbose:
                click.echo(f"Generated: {filename}")
        
        except Exception as e:
            click.echo(f"Error generating {filename}: {e}", err=True)
    
    if verbose:
        click.echo(f"✓ Batch generation complete! {count} images saved to {output_path.absolute()}")

if __name__ == '__main__':
    main() 