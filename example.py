#!/usr/bin/env python3

import abstro
from abstro import Canvas, ColorPalette
from abstro.core.generator import OrganicGenerator, GeometricGenerator

def basic_example():
    print("🎨 Basic Example - Organic preset...")
    canvas = abstro.generate(
        width=800, 
        height=600, 
        preset="organic", 
        seed=42,
        output="examples/organic_example.png"
    )
    print("✓ Saved: examples/organic_example.png")

def custom_example():
    print("\n🎨 Custom Canvas Example...")
    
    canvas = Canvas(600, 600, seed=123)
    canvas.set_palette('sunset')
    
    generator = OrganicGenerator(
        complexity=25,
        flow_field_strength=0.8,
        organic_factor=1.0,
        shape_type='mixed'
    )
    
    generator.apply(canvas)
    canvas.save("examples/custom_organic.png")
    print("✓ Saved: examples/custom_organic.png")

def mosaic_example():
    print("\n🎨 Mosaic Example...")
    canvas = abstro.generate(
        width=800,
        height=800,
        preset="mosaic",
        seed=999,
        output="examples/mosaic_example.png"
    )
    print("✓ Saved: examples/mosaic_example.png")

def geometric_example():
    print("\n🎨 Geometric Example...")
    
    canvas = Canvas(800, 600, seed=456)
    canvas.set_palette(ColorPalette.from_name('cool'))
    
    generator = GeometricGenerator(
        complexity=60,
        symmetry=True,
        shape_type='polygon'
    )
    
    generator.apply(canvas)
    canvas.save("examples/geometric_symmetric.png")
    print("✓ Saved: examples/geometric_symmetric.png")

def svg_example():
    print("\n🎨 SVG Example...")
    canvas = abstro.generate(
        width=400,
        height=400,
        preset="minimal",
        seed=789,
        output="examples/minimal.svg"
    )
    print("✓ Saved: examples/minimal.svg")

if __name__ == "__main__":
    import os
    os.makedirs("examples", exist_ok=True)
    
    print("🚀 Abstro Example Generator")
    print("=" * 30)
    
    basic_example()
    custom_example()
    mosaic_example()
    geometric_example()
    svg_example()
    
    print("\n✨ All examples generated successfully!")
    print("📁 Check the 'examples/' folder for results")
    
    print("\n🎯 CLI Usage Examples:")
    print("  abstro -o art.png --preset mosaic --seed 42")
    print("  abstro -o organic.svg --preset organic --complexity 30")
    print("  abstro -o minimal.jpg --preset minimal --width 1200 --height 800")
    print("  abstro --list-presets")
    print("  abstro --list-palettes") 