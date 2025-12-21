import cv2

def get_available_cameras(max_check=5):
    """
    Check the first `max_check` indices to see if a camera is available.
    Returns a list of dictionaries with 'id' and 'name'.
    """
    available_cameras = []
    for i in range(max_check):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW) # CAP_DSHOW is good for Windows
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                # Try to get backend name or just use generic name
                name = f"Camera {i}"
                if i == 0:
                    name += " (Built-in/Default)"
                else:
                    name += " (External/USB)"
                
                print(f"Found camera: {name} at index {i}")
                available_cameras.append({"id": i, "name": name})
            cap.release()
    if not available_cameras:
        print("No cameras found!")
    return available_cameras
