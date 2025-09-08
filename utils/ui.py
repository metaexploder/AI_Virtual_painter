import cv2

# Updated color palette with your requested colors
PALETTE = [
    ("Red", (0, 0, 255)),
    ("Blue", (255, 0, 0)),
    ("Green", (0, 255, 0)),
    ("Black", (0, 0, 0)),
    ("Yellow", (0, 255, 255)),
    ("Pink", (255, 0, 255)),
]

# Drawing modes for left side
DRAWING_MODES = [
    ("Freestyle", "✏️"),
    ("Shapes", "📐"),
    ("Eraser", "🧹"),
    ("Clear Shape", "✕"),
    ("Fill Shape", "◉"),
]

# Shapes for right side (only visible when needed)
SHAPES = [
    ("Rectangle", "▢"),
    ("Circle", "○"),
    ("Triangle", "△"),
    ("Star", "★"),
    ("Arrow", "→"),
]

# UI dimensions
PALETTE_BOX_W = 200
PALETTE_BOX_H = 80
PALETTE_Y1 = 10
PALETTE_Y2 = PALETTE_Y1 + PALETTE_BOX_H

# Left side - Drawing modes
MODE_BOX_W = 150
MODE_BOX_H = 90
MODE_X1 = 20
MODE_X2 = MODE_X1 + MODE_BOX_W

# Right side - Shapes
SHAPE_BOX_W = 150
SHAPE_BOX_H = 90
SHAPE_X1 = 1100  # Right side of 1280px screen with margin
SHAPE_X2 = SHAPE_X1 + SHAPE_BOX_W

FONT = cv2.FONT_HERSHEY_SIMPLEX

def draw_palette(img, current_idx):
    """Draw color palette at the top"""
    boxes = []
    x1 = 10
    for i, (name, color) in enumerate(PALETTE):
        x2 = x1 + PALETTE_BOX_W
        thickness = -1 if i == current_idx else 2
        cv2.rectangle(img, (x1, PALETTE_Y1), (x2, PALETTE_Y2), color, thickness)
        
        # Use white text for dark colors, black text for light colors
        text_color = (255, 255, 255) if name in ["Red", "Blue", "Green", "Black"] else (0, 0, 0)
        cv2.putText(img, name, (x1+10, PALETTE_Y1+45), FONT, 0.8, text_color, 2)
        
        boxes.append((x1, PALETTE_Y1, x2, PALETTE_Y2))
        x1 = x2 + 10
    return boxes

def draw_mode_selector(img, current_mode_idx):
    """Draw drawing modes on the left side"""
    boxes = []
    y1 = 110  # Start below the color palette with more space
    
    for i, (name, symbol) in enumerate(DRAWING_MODES):
        y2 = y1 + MODE_BOX_H
        
        # Determine colors
        if i == current_mode_idx:
            bg_color = (0, 0, 0)  # Black background
            border_color = (0, 200, 0)  # Green border for selected
            border_thickness = 4
            text_color = (0, 255, 0)  # Green text for selected
            symbol_color = (0, 255, 0)  # Green symbol
        else:
            bg_color = (0, 0, 0)  # Black background
            border_color = (255, 255, 255)  # White border
            border_thickness = 2
            text_color = (255, 255, 255)  # White text
            symbol_color = (255, 255, 255)  # White symbol
        
        # Draw mode box
        cv2.rectangle(img, (MODE_X1, y1), (MODE_X2, y2), bg_color, -1)
        cv2.rectangle(img, (MODE_X1, y1), (MODE_X2, y2), border_color, border_thickness)
        
        # Add text and symbol with better positioning
        cv2.putText(img, name, (MODE_X1+10, y1+30), FONT, 0.6, text_color, 2)
        cv2.putText(img, symbol, (MODE_X1+50, y1+65), FONT, 1.2, symbol_color, 2)
        
        boxes.append((MODE_X1, y1, MODE_X2, y2))
        y1 = y2 + 10  # More space between boxes
    
    return boxes

def draw_shape_selector(img, current_shape_idx):
    """Draw shape selector on the right side (only when shapes mode is active)"""
    boxes = []
    y1 = 110  # Start below the color palette with more space
    
    for i, (name, symbol) in enumerate(SHAPES):
        y2 = y1 + SHAPE_BOX_H
        
        # Determine colors
        if i == current_shape_idx:
            bg_color = (0, 0, 0)  # Black background
            border_color = (0, 200, 0)  # Green border for selected
            border_thickness = 4
            text_color = (0, 255, 0)  # Green text for selected
            symbol_color = (0, 255, 0)  # Green symbol
        else:
            bg_color = (0, 0, 0)  # Black background
            border_color = (255, 255, 255)  # White border
            border_thickness = 2
            text_color = (255, 255, 255)  # White text
            symbol_color = (255, 255, 255)  # White symbol
        
        # Draw shape box
        cv2.rectangle(img, (SHAPE_X1, y1), (SHAPE_X2, y2), bg_color, -1)
        cv2.rectangle(img, (SHAPE_X1, y1), (SHAPE_X2, y2), border_color, border_thickness)
        
        # Add text and symbol with better positioning
        cv2.putText(img, name, (SHAPE_X1+10, y1+30), FONT, 0.6, text_color, 2)
        cv2.putText(img, symbol, (SHAPE_X1+50, y1+65), FONT, 1.2, symbol_color, 2)
        
        boxes.append((SHAPE_X1, y1, SHAPE_X2, y2))
        y1 = y2 + 10  # More space between boxes
    
    return boxes

def inside_box(pt, box):
    x, y = pt
    x1, y1, x2, y2 = box
    return x1 <= x <= x2 and y1 <= y <= y2