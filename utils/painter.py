import cv2
import numpy as np
from .ui import PALETTE

BRUSH_THICK = 12
ERASER_THICK = 60
SHAPE_THICK = 5

def create_canvas(W, H):
    return np.zeros((H, W, 3), dtype=np.uint8)

def draw_line(canvas, pt1, pt2, color_idx):
    color = PALETTE[color_idx][1]
    thick = BRUSH_THICK
    cv2.line(canvas, pt1, pt2, color, thick, lineType=cv2.LINE_AA)

def draw_shape(canvas, start_pt, end_pt, shape_idx, color_idx, preview=False, fill=False):
    """Draw shapes based on shape_idx: 0=rectangle, 1=circle, 2=triangle, 3=star, 4=arrow"""
    color = PALETTE[color_idx][1]
    thick = SHAPE_THICK if not preview else 3
    
    # Override thickness for filled shapes
    if fill and not preview:
        thick = -1
    
    if shape_idx == 0:  # Rectangle
        cv2.rectangle(canvas, start_pt, end_pt, color, thick)
    
    elif shape_idx == 1:  # Circle
        # Calculate radius as distance between start and end points
        radius = int(np.sqrt((end_pt[0] - start_pt[0])**2 + (end_pt[1] - start_pt[1])**2))
        cv2.circle(canvas, start_pt, radius, color, thick)
    
    elif shape_idx == 2:  # Triangle
        # Create triangle with start_pt as top vertex
        dx = end_pt[0] - start_pt[0]
        dy = end_pt[1] - start_pt[1]
        
        # Calculate triangle points
        pt1 = start_pt  # Top vertex
        pt2 = (start_pt[0] - dx, end_pt[1])  # Bottom left
        pt3 = (start_pt[0] + dx, end_pt[1])  # Bottom right
        
        triangle_pts = np.array([pt1, pt2, pt3], np.int32)
        triangle_pts = triangle_pts.reshape((-1, 1, 2))
        
        if thick == -1:  # Fill
            cv2.fillPoly(canvas, [triangle_pts], color)
        else:
            cv2.polylines(canvas, [triangle_pts], True, color, thick)
    
    elif shape_idx == 3:  # Star
        # Create 5-pointed star
        center_x, center_y = start_pt
        outer_radius = int(np.sqrt((end_pt[0] - start_pt[0])**2 + (end_pt[1] - start_pt[1])**2))
        inner_radius = outer_radius // 2
        
        star_pts = []
        for i in range(10):
            angle = i * np.pi / 5
            if i % 2 == 0:
                # Outer points
                x = int(center_x + outer_radius * np.cos(angle - np.pi/2))
                y = int(center_y + outer_radius * np.sin(angle - np.pi/2))
            else:
                # Inner points
                x = int(center_x + inner_radius * np.cos(angle - np.pi/2))
                y = int(center_y + inner_radius * np.sin(angle - np.pi/2))
            star_pts.append([x, y])
        
        star_pts = np.array(star_pts, np.int32)
        star_pts = star_pts.reshape((-1, 1, 2))
        
        if thick == -1:  # Fill
            cv2.fillPoly(canvas, [star_pts], color)
        else:
            cv2.polylines(canvas, [star_pts], True, color, thick)
    
    elif shape_idx == 4:  # Arrow
        line_thick = thick if thick != -1 else SHAPE_THICK
        # Draw arrow line
        cv2.line(canvas, start_pt, end_pt, color, line_thick)
        
        # Calculate arrow head
        angle = np.arctan2(end_pt[1] - start_pt[1], end_pt[0] - start_pt[0])
        arrow_length = 20
        arrow_angle = 0.5
        
        # Arrow head points
        pt1 = (int(end_pt[0] - arrow_length * np.cos(angle - arrow_angle)),
               int(end_pt[1] - arrow_length * np.sin(angle - arrow_angle)))
        pt2 = (int(end_pt[0] - arrow_length * np.cos(angle + arrow_angle)),
               int(end_pt[1] - arrow_length * np.sin(angle + arrow_angle)))
        
        cv2.line(canvas, end_pt, pt1, color, line_thick)
        cv2.line(canvas, end_pt, pt2, color, line_thick)

def clear_area(canvas, center_pt, radius=30):
    """Clear a circular area around the given point"""
    cv2.circle(canvas, center_pt, radius, (0, 0, 0), -1)

def fill_at_point(canvas, point, color_idx):
    """Fill area at point using flood fill algorithm"""
    color = PALETTE[color_idx][1]
    h, w = canvas.shape[:2]
    x, y = point
    
    # Make sure point is within canvas bounds
    if 0 <= x < w and 0 <= y < h:
        # Create a mask for flood fill
        mask = np.zeros((h + 2, w + 2), np.uint8)
        
        # Get the current color at the point
        current_color = tuple(canvas[y, x])
        
        # Only fill if the current color is different from target color
        if current_color != color:
            cv2.floodFill(canvas, mask, (x, y), color)

def merge_canvas(frame, canvas):
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
    base = cv2.bitwise_and(frame, inv)
    out = cv2.bitwise_or(base, canvas)
    return out