import cv2
from utils import hand_tracker, painter, ui

W, H = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3, W)
cap.set(4, H)

canvas = painter.create_canvas(W, H)
current_color_idx = 0
current_mode_idx = 0   # Index for modes (0: Freestyle, 1: Shapes, 2: Eraser, 3: Clear Shape, 4: Fill Shape)
current_shape_idx = 0  # Index for shapes (0-4: Rectangle to Arrow)
prev_pt = None
shape_start_pt = None
shape_end_pt = None

while True:
    ok, frame = cap.read()
    if not ok: break
    frame = cv2.flip(frame, 1)

    # Draw UI elements
    color_boxes = ui.draw_palette(frame, current_color_idx)
    mode_boxes = ui.draw_mode_selector(frame, current_mode_idx)
    
    # Only show shapes if in shapes mode
    shape_boxes = []
    if current_mode_idx == 1:  # Only shapes mode
        shape_boxes = ui.draw_shape_selector(frame, current_shape_idx)
    
    lm, frame = hand_tracker.get_landmarks(frame)
    state = hand_tracker.fingers_up(lm)

    if state['index'] and state['middle']:
        # Selection mode AND shape completion
        if lm:
            idx_tip = lm[8]
            
            # Complete shape drawing if we were in shape drawing mode
            if shape_start_pt is not None and shape_end_pt is not None and current_mode_idx == 1:
                painter.draw_shape(canvas, shape_start_pt, shape_end_pt, current_shape_idx, current_color_idx, preview=False, fill=False)
            
            # Reset drawing points after shape completion
            prev_pt = None
            shape_start_pt = None
            shape_end_pt = None
            
            # Check color palette selection
            for i, box in enumerate(color_boxes):
                if ui.inside_box(idx_tip, box):
                    current_color_idx = i
            
            # Check mode selector (left side)
            for i, box in enumerate(mode_boxes):
                if ui.inside_box(idx_tip, box):
                    current_mode_idx = i
                    # Reset shape selection when changing modes
                    shape_start_pt = None
                    shape_end_pt = None
            
            # Check shape selector (right side) - only if in shapes mode
            if current_mode_idx == 1:
                for i, box in enumerate(shape_boxes):
                    if ui.inside_box(idx_tip, box):
                        current_shape_idx = i

    elif state['index'] and not state['middle']:
        # Drawing mode
        if lm:
            idx_tip = lm[8]
            
            if current_mode_idx == 0:  # Freestyle drawing
                if prev_pt is not None:
                    painter.draw_line(canvas, prev_pt, idx_tip, current_color_idx)
                prev_pt = idx_tip
            elif current_mode_idx == 2:  # Eraser mode
                painter.clear_area(canvas, idx_tip, radius=30)
            elif current_mode_idx == 3:  # Clear Shape mode
                painter.clear_area(canvas, idx_tip, radius=30)
            elif current_mode_idx == 1:  # Shape drawing mode (outline)
                if shape_start_pt is None:
                    shape_start_pt = idx_tip
                # Update end point and show preview
                shape_end_pt = idx_tip
                temp_frame = frame.copy()
                painter.draw_shape(temp_frame, shape_start_pt, shape_end_pt, current_shape_idx, current_color_idx, preview=True, fill=False)
                frame = temp_frame
            elif current_mode_idx == 4:  # Fill shape mode
                painter.fill_at_point(canvas, idx_tip, current_color_idx)
    else:
        # Reset drawing points when no fingers detected (safety reset)
        if not state['index']:
            prev_pt = None

    out = painter.merge_canvas(frame, canvas)
    cv2.imshow("AI Virtual Painter", out)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
    if key == ord('c'): canvas[:] = 0

cap.release()
cv2.destroyAllWindows()