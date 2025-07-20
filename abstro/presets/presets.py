PRESETS = {
    'organic': {
        'generator_type': 'organic',
        'complexity': 40,
        'palette': 'earth',
        'flow_field_strength': 0.7,
        'organic_factor': 0.8,
        'shape_type': 'mixed'
    },
    
    'mosaic': {
        'generator_type': 'geometric',
        'complexity': 100,
        'palette': 'vibrant',
        'grid_based': True,
        'shape_type': 'polygon'
    },
    
    'minimal': {
        'generator_type': 'geometric',
        'complexity': 15,
        'palette': 'monochrome',
        'symmetry': True,
        'shape_type': 'circle'
    },
    
    'chaos': {
        'generator_type': 'pattern',
        'complexity': 200,
        'palette': 'neon',
        'shape_type': 'mixed',
        'noise_density': 0.005,
        'noise_color_range': 50
    },
    
    'sunset': {
        'generator_type': 'organic',
        'complexity': 30,
        'palette': 'sunset',
        'flow_field_strength': 0.4,
        'organic_factor': 0.6,
        'shape_type': 'circle'
    },
    
    'geometric': {
        'generator_type': 'geometric',
        'complexity': 60,
        'palette': 'cool',
        'symmetry': False,
        'grid_based': False,
        'shape_type': 'polygon'
    },
    
    'flow': {
        'generator_type': 'organic',
        'complexity': 25,
        'palette': 'ocean',
        'flow_field_strength': 1.2,
        'organic_factor': 1.0,
        'shape_type': 'bezier'
    },
    
    'pastel_dream': {
        'generator_type': 'pattern',
        'complexity': 80,
        'palette': 'pastel',
        'shape_type': 'circle',
        'noise_density': 0.001
    },
    
    'line_art': {
        'generator_type': 'pattern',
        'complexity': 120,
        'palette': 'monochrome',
        'shape_type': 'line'
    },
    
    'warm_abstract': {
        'generator_type': 'organic',
        'complexity': 50,
        'palette': 'warm',
        'flow_field_strength': 0.8,
        'organic_factor': 0.9,
        'shape_type': 'mixed'
    },
    
    'grid_modern': {
        'generator_type': 'geometric',
        'complexity': 144,  # 12x12 grid
        'palette': 'vibrant',
        'grid_based': True,
        'shape_type': 'mixed'
    },
    
    'forest': {
        'generator_type': 'organic',
        'complexity': 35,
        'palette': 'forest',
        'flow_field_strength': 0.6,
        'organic_factor': 1.2,
        'shape_type': 'mixed'
    },
    
    'oil_painting': {
        'generator_type': 'oil_painting',
        'complexity': 60,
        'palette': 'warm',
        'brush_size': 'medium',
        'paint_thickness': 0.8,
        'color_mixing': 0.9,
        'texture_density': 0.4,
        'stroke_variation': 0.8
    },
    
    'oil_impressionist': {
        'generator_type': 'oil_painting',
        'complexity': 80,
        'palette': 'pastel',
        'brush_size': 'fine',
        'paint_thickness': 0.6,
        'color_mixing': 0.7,
        'texture_density': 0.2,
        'stroke_variation': 1.0
    },
    
    'oil_abstract': {
        'generator_type': 'oil_painting',
        'complexity': 45,
        'palette': 'vibrant',
        'brush_size': 'thick',
        'paint_thickness': 1.0,
        'color_mixing': 0.8,
        'texture_density': 0.6,
        'stroke_variation': 0.9
    },
    
    'oil_portrait': {
        'generator_type': 'oil_painting',
        'complexity': 70,
        'palette': 'earth',
        'brush_size': 'mixed',
        'paint_thickness': 0.7,
        'color_mixing': 0.6,
        'texture_density': 0.3,
        'stroke_variation': 0.5
    }
}

def get_preset(name):
    preset = PRESETS.get(name.lower())
    if preset is None:
        available = ', '.join(PRESETS.keys())
        raise ValueError(f"Preset '{name}' not found. Available presets: {available}")
    return preset.copy()

def list_presets():
    return list(PRESETS.keys())

def get_preset_description(name):
    descriptions = {
        'organic': 'Organic, flowing shapes with natural colors',
        'mosaic': 'Colorful geometric mosaic pattern',
        'minimal': 'Clean, minimal design with limited elements',
        'chaos': 'High energy, chaotic composition with many elements',
        'sunset': 'Warm, sunset-inspired organic shapes',
        'geometric': 'Clean geometric shapes and patterns',
        'flow': 'Flowing, water-like bezier curves',
        'pastel_dream': 'Soft, dreamy pastel circles',
        'line_art': 'Minimalist line-based composition',
        'warm_abstract': 'Warm, abstract organic forms',
        'grid_modern': 'Modern grid-based geometric pattern',
        'forest': 'Nature-inspired green organic shapes',
        'oil_painting': 'Traditional oil painting style with brush strokes',
        'oil_impressionist': 'Impressionist oil painting with fine brush work',
        'oil_abstract': 'Abstract oil painting with thick impasto technique',
        'oil_portrait': 'Oil painting suitable for portrait-like compositions'
    }
    return descriptions.get(name.lower(), 'No description available') 