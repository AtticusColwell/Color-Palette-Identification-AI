import json
from colorspacious import cspace_convert
from scipy.spatial import distance

def hex_to_rgb(hex_color):
    """Convert a hex color to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_lch(rgb_color):
    """Convert an RGB color to LCH."""
    return cspace_convert(rgb_color, "sRGB1", "CAM02-UCS")

def color_difference_cie2000(lch1, lch2):
    """Calculate the CIE2000 color difference between two LCH colors."""
    return distance.euclidean(lch1, lch2)

def color_is_allowed(color, color_palette, threshold=40):
    # Load the JSON color palettes
    with open('palettes.json', 'r') as f:
        color_palettes = json.load(f)
    
    allowed_colors = color_palettes[color_palette]
    color_lch = rgb_to_lch(color)

    for allowed_color in allowed_colors:
        allowed_color_lch = rgb_to_lch(hex_to_rgb(allowed_color))
        if color_difference_cie2000(color_lch, allowed_color_lch) < threshold:
            return True
    return False




