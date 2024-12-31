"""
Seasonal Color Classification

This script classifies a person into a color season based on:
- Skin color in RGB
- Hair color in RGB
- Eye color in RGB
- Tone: "warm", "light warm", "neutral", "light cool", "cool"

Includes all seasons and sub-seasons.
"""

import math

# TODO: We're assuming convexity in this space which is a big assumption. 
# Likely untrue, should define more complex boundaries

SEASONS = [
    # -------------------- SPRING --------------------
    {
        "name": "Light Spring",
        "undertones": ["light warm", "neutral"],
        # LIGHT SPRING: Narrow range
        "skin_min": (190, 160, 140),
        "skin_max": (200, 170, 150),
        "hair_min": (130, 100, 80),
        "hair_max": (140, 110, 90),
        "eye_min":  (70,  70,  50),
        "eye_max":  (80,  80,  60)
    },
    {
        "name": "True Spring",
        "undertones": ["warm"],
        # TRUE SPRING: Next higher slice
        "skin_min": (201, 171, 151),
        "skin_max": (210, 180, 160),
        "hair_min": (141, 111, 91),
        "hair_max": (150, 120, 100),
        "eye_min":  (81,  71,  51),
        "eye_max":  (90,  80,  60)
    },
    {
        "name": "Warm Spring",
        "undertones": ["warm"],
        # WARM SPRING: Slightly darker slice
        "skin_min": (211, 181, 161),
        "skin_max": (220, 190, 170),
        "hair_min": (151, 121, 101),
        "hair_max": (160, 130, 110),
        "eye_min":  (91,  72,  52),
        "eye_max":  (100, 90,  70)
    },
    {
        "name": "Bright Spring",
        "undertones": ["warm", "neutral"],
        # BRIGHT SPRING: Highest slice for Spring
        "skin_min": (221, 191, 171),
        "skin_max": (230, 200, 180),
        "hair_min": (161, 131, 111),
        "hair_max": (170, 140, 120),
        "eye_min":  (101, 73,  53),
        "eye_max":  (110, 100, 80)
    },

    # -------------------- SUMMER --------------------
    {
        "name": "Light Summer",
        "undertones": ["light cool", "neutral"],
        # LIGHT SUMMER: Light, cool slice
        "skin_min": (180, 160, 150),
        "skin_max": (190, 170, 160),
        "hair_min": (100, 90,  90),
        "hair_max": (110, 100, 100),
        "eye_min":  (60,  60,  60),
        "eye_max":  (70,  70,  70)
    },
    {
        "name": "True Summer",
        "undertones": ["cool"],
        # TRUE SUMMER: Next slice
        "skin_min": (191, 171, 161),
        "skin_max": (200, 180, 170),
        "hair_min": (111, 101, 101),
        "hair_max": (120, 110, 110),
        "eye_min":  (71,  61,  61),
        "eye_max":  (80,  70,  70)
    },
    {
        "name": "Cool Summer",
        "undertones": ["cool"],
        # COOL SUMMER: Another distinct slice
        "skin_min": (201, 181, 171),
        "skin_max": (210, 190, 180),
        "hair_min": (121, 111, 111),
        "hair_max": (130, 120, 120),
        "eye_min":  (81,  62,  62),
        "eye_max":  (90,  80,  80)
    },
    {
        "name": "Soft Summer",
        "undertones": ["light cool", "neutral"],
        # SOFT SUMMER: Higher slice
        "skin_min": (211, 191, 181),
        "skin_max": (220, 200, 190),
        "hair_min": (131, 121, 121),
        "hair_max": (140, 130, 130),
        "eye_min":  (91,  63,  63),
        "eye_max":  (100, 90,  90)
    },

    # -------------------- AUTUMN --------------------
    {
        "name": "Soft Autumn",
        "undertones": ["neutral", "light warm"],
        # SOFT AUTUMN
        "skin_min": (160, 130, 110),
        "skin_max": (170, 140, 120),
        "hair_min": (90,  60,  40),
        "hair_max": (100, 70,  50),
        "eye_min":  (50,  50,  40),
        "eye_max":  (60,  60,  50)
    },
    {
        "name": "True Autumn",
        "undertones": ["warm"],
        # TRUE AUTUMN
        "skin_min": (171, 141, 121),
        "skin_max": (180, 150, 130),
        "hair_min": (101, 71,  51),
        "hair_max": (110, 80,  60),
        "eye_min":  (61,  51,  41),
        "eye_max":  (70,  60,  50)
    },
    {
        "name": "Warm Autumn",
        "undertones": ["warm"],
        # WARM AUTUMN
        "skin_min": (181, 151, 131),
        "skin_max": (190, 160, 140),
        "hair_min": (111, 81,  61),
        "hair_max": (120, 90,  70),
        "eye_min":  (71,  52,  42),
        "eye_max":  (80,  70,  60)
    },
    {
        "name": "Deep Autumn",
        "undertones": ["warm", "neutral"],
        # DEEP AUTUMN
        "skin_min": (191, 161, 141),
        "skin_max": (200, 170, 150),
        "hair_min": (121, 91,  71),
        "hair_max": (130, 100, 80),
        "eye_min":  (81,  53,  43),
        "eye_max":  (90,  80,  70)
    },

    # -------------------- WINTER --------------------
    {
        "name": "True Winter",
        "undertones": ["cool"],
        # TRUE WINTER
        "skin_min": (150, 130, 140),
        "skin_max": (160, 140, 150),
        "hair_min": (40,  40,  50),
        "hair_max": (50,  50,  60),
        "eye_min":  (30,  30,  40),
        "eye_max":  (40,  40,  50)
    },
    {
        "name": "Bright Winter",
        "undertones": ["cool", "neutral"],
        # BRIGHT WINTER
        "skin_min": (161, 141, 151),
        "skin_max": (170, 150, 160),
        "hair_min": (51,  51,  61),
        "hair_max": (60,  60,  70),
        "eye_min":  (41,  31,  41),
        "eye_max":  (50,  40,  50)
    },
    {
        "name": "Cool Winter",
        "undertones": ["cool", "light cool"],
        # COOL WINTER
        "skin_min": (171, 151, 161),
        "skin_max": (180, 160, 170),
        "hair_min": (61,  61,  71),
        "hair_max": (70,  70,  80),
        "eye_min":  (51,  32,  42),
        "eye_max":  (60,  50,  60)
    },
    {
        "name": "Deep Winter",
        "undertones": ["cool", "neutral"],
        # DEEP WINTER
        "skin_min": (181, 161, 171),
        "skin_max": (190, 170, 180),
        "hair_min": (71,  71,  81),
        "hair_max": (80,  80,  90),
        "eye_min":  (61,  33,  43),
        "eye_max":  (70,  60,  70)
    },
]

def in_range(color, cmin, cmax):
    """
    Check if a color (RGB tuple) falls within the specified range.
    """
    return all(cmin[i] <= color[i] <= cmax[i] for i in range(3))

def calculate_centroid(cmin, cmax):
    """
    Calculate the centroid (average RGB value) of a range.
    """
    return tuple((cmin[i] + cmax[i]) // 2 for i in range(3))

def euclidean_distance(color1, color2):
    """
    Calculate the Euclidean distance between two RGB tuples.
    """
    return math.sqrt(sum((color1[i] - color2[i]) ** 2 for i in range(3)))

def classify_season(skin_rgb, hair_rgb, eye_rgb, tone):
    """
    Classify a person into a color season based on skin, hair, and eye RGB values,
    along with their undertone. If no exact match, find the closest match.
    """
    print("classify_season triggered with following input")
    print("skin_color:", skin_rgb)
    print("eye color:")

    possible_matches = []
    distances = []

    for season in SEASONS:
        if tone not in season["undertones"]:
            continue
        if (
            in_range(skin_rgb, season["skin_min"], season["skin_max"]) and
            in_range(hair_rgb, season["hair_min"], season["hair_max"]) and
            in_range(eye_rgb, season["eye_min"], season["eye_max"])
        ):
            possible_matches.append(season["name"])

        # Calculate distances for potential fallback
        skin_centroid = calculate_centroid(season["skin_min"], season["skin_max"])
        hair_centroid = calculate_centroid(season["hair_min"], season["hair_max"])
        eye_centroid = calculate_centroid(season["eye_min"], season["eye_max"])

        skin_distance = euclidean_distance(skin_rgb, skin_centroid)
        hair_distance = euclidean_distance(hair_rgb, hair_centroid)
        eye_distance = euclidean_distance(eye_rgb, eye_centroid)

        total_distance = skin_distance + hair_distance + eye_distance
        distances.append((season["name"], total_distance))

    if possible_matches:
        return possible_matches[0] if len(possible_matches) == 1 else possible_matches[0] + " (multiple matches?)"
    
    # If no exact match, return the closest match
    closest_match = min(distances, key=lambda x: x[1])
    return f"Closest Match: {closest_match[0]}"

# Example Usage
if __name__ == "__main__":
    # Example that might not match exactly but will fall back to closest
    skin = (195, 165, 145)
    hair = (135, 105, 85)
    eyes = (75, 75, 55)
    tone = "light warm"

    result = classify_season(skin, hair, eyes, tone)
    print("Result:", result)

    # Example with a fallback closest match
    skin2 = (250, 250, 250)
    hair2 = (10, 10, 10)
    eyes2 = (200, 200, 200)
    tone2 = "warm"

    result2 = classify_season(skin2, hair2, eyes2, tone2)
    print("Result 2:", result2)
