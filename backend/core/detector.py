import cv2
from ultralytics import YOLO
import os
import numpy as np
import time
import gc

class YOLODetector:
    def __init__(self, model_path='models/yolov8n.pt'):
        self.model = None
        self.load_model(model_path)

    def load_model(self, model_path):
        """Loads the YOLO model."""
        if not os.path.exists(model_path):
            print(f"Model not found: {model_path}")
            # Fallback or error
            return False
        print(f"Loading model: {model_path}")
        self.model = YOLO(model_path)
        return True

    def detect_frame(self, frame):
        """
        Runs inference on a single frame.
        Returns the annotated frame and the results.
        """
        if self.model is None:
            return frame, []

        results = self.model(frame)
        annotated_frame = results[0].plot()
        return annotated_frame, results

    def process_video_file(self, source_path, save_dir):
        """
        Generator that yields JPEG bytes for streaming,
        while saving the processed video to save_dir if provided.
        """
        cap = cv2.VideoCapture(source_path)
        if not cap.isOpened():
            return

        out = None
        
        # Setup VideoWriter only if save_dir is provided
        if save_dir:
            filename = os.path.basename(source_path)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(save_dir, f"{name}_processed.mp4")
            
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            # mp4v is generally compatible
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while True:
            success, frame = cap.read()
            if not success:
                break

            annotated_frame, _ = self.detect_frame(frame)
            
            # Write to file only if VideoWriter was created
            if out:
                out.write(annotated_frame)

            # Encode for streaming
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        cap.release()
        if out:
            out.release()

    def process_image_file(self, source_path, save_dir):
        """
        Processes a single image, saves it to save_dir if provided,
        and yields it for display.
        """
        frame = cv2.imread(source_path)
        if frame is None:
            return

        annotated_frame, _ = self.detect_frame(frame)
        
        # Save to file only if save_dir is provided
        if save_dir:
            filename = os.path.basename(source_path)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(save_dir, f"{name}_processed{ext}")
            
            cv2.imwrite(output_path, annotated_frame)

        # Encode for streaming (even though it's a static image, we send it as a single frame response)
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def process_camera(self, camera_id):
        """
        Generator for real-time camera inference.
        """
        print(f"Opening camera {camera_id}...")
        
        # FORCE DirectShow (CAP_DSHOW) as it is most reliable for USB cameras on Windows
        # Default (MSMF) often opens device but fails to start stream (Black frame / No light)
        cap = cv2.VideoCapture(int(camera_id), cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            print(f"Error: Could not open camera {camera_id} with CAP_DSHOW")
            return

        # Apply settings from the working script
        try:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            print("Camera parameters set to 640x480")
        except Exception as e:
            print(f"Error setting camera parameters: {e}")
        
        actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"Camera {camera_id} active resolution: {actual_width}x{actual_height}")
        
        frame_count = 0
        
        while True:
            success, frame = cap.read()
            if not success:
                print(f"Failed to read frame from camera {camera_id}")
                # Short sleep like in the working script to prevent CPU spin if camera glitches
                time.sleep(0.01)
                continue
            
            frame_count += 1
            
            # Mirror flip (like in the working script)
            frame = cv2.flip(frame, 1)

            annotated_frame, _ = self.detect_frame(frame)
            
            # GC periodically (like in the working script)
            if frame_count % 100 == 0:
                gc.collect()

            try:
                ret, buffer = cv2.imencode('.jpg', annotated_frame)
                if not ret:
                    continue
                frame_bytes = buffer.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            except Exception as e:
                print(f"Error encoding frame: {e}")
                continue
        
        cap.release()
        print(f"Camera {camera_id} released.")
