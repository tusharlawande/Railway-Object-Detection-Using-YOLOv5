import cv2  # For handling the video and image processing
import torch  # PyTorch powers our ML model
import pandas as pd  # For organizing and summarizing the results
from pathlib import Path  # Handy for checking if the video file exists
import time  # To track how long this takes

# Here’s the list of railway objects we’re looking for, straight from those OCR pages
railway_objects = [
    "ROW-Land Boundary Stone", "OHE-Pole", "Chainage Pole", "K.M.Stone", "Lamp Post",
    "Board-Tl-For Passengers Train (T1-Termination Indicator)", "Board-Tractive Effort (TE)",
    "Board-W-For Curve_Cutting_Tunnel", "Catch Water Drain or Side Water Drain", "Fence",
    "Height Gauge", "Pole-OHE", "Pole-Traffic Signal", "Post-Gradient", "Post-Hectometer",
    "Sign Pole", "Sign Board", "Silver Box"
]

# Since we’re using YOLOv5 (a pre-trained model), we need to map our railway stuff to things it can recognize
# It’s not perfect, but it’s a good start without training our own model
yolo_mappings = {
    "OHE-Pole": "pole", "Pole-OHE": "pole", "Lamp Post": "pole", "Pole-Traffic Signal": "pole",
    "Sign Pole": "pole", "Post-Gradient": "pole", "Post-Hectometer": "pole", "Chainage Pole": "pole",
    "Sign Board": "sign", "Board-Tl-For Passengers Train (T1-Termination Indicator)": "sign",
    "Board-Tractive Effort (TE)": "sign", "Board-W-For Curve_Cutting_Tunnel": "sign",
    "Fence": "fence", "Height Gauge": "object", "Silver Box": "box",
    "K.M.Stone": "stone", "ROW-Land Boundary Stone": "stone",
    "Catch Water Drain or Side Water Drain": "object"
}

# Load up YOLOv5 - the small version (yolov5s) is fast and good enough for this
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Where’s the video and where do we save our results?
video_path = "railway_track_video.mp4"  # Change this to wherever your 11-minute video lives
output_csv = "railway_detections.csv"  # Detailed list of what we find
output_summary = "railway_detection_summary.txt"  # Quick summary for the boss

def detect_railway_objects(video_path):
    """Let’s go through the video and spot those railway objects."""
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Whoops, couldn’t open the video. Check the path!")
        return None

    # Get some basics about the video
    fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total number of frames
    minutes = total_frames / fps / 60  # How long in minutes
    print(f"Okay, we’ve got a {minutes:.2f}-minute video with {total_frames} frames at {fps} FPS.")

    # Keep track of everything we find
    detections = []
    frame_count = 0
    start_time = time.time()  # Let’s see how long this takes

    # Loop through every frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:  # No more frames? We’re done!
            break

        frame_count += 1
        timestamp = frame_count / fps  # When in the video are we?

        # Make the frame smaller so this doesn’t take forever
        frame = cv2.resize(frame, (640, 480))
        # YOLO likes RGB, not BGR, so flip the colors
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Ask YOLO to find stuff in this frame
        results = model(rgb_frame)
        labels = results.pred[0][:, -1].cpu().numpy()  # What it thinks it sees
        confidences = results.pred[0][:, 4].cpu().numpy()  # How sure it is
        boxes = results.pred[0][:, :4].cpu().numpy()  # Where it is in the frame

        # Check if any of these match our railway objects
        for label, conf, box in zip(labels, confidences, boxes):
            class_name = model.names[int(label)]
            if conf > 0.6:  # Only trust it if it’s pretty confident
                for railway_obj, yolo_label in yolo_mappings.items():
                    if yolo_label in class_name.lower():
                        x, y, w, h = box  # Where and how big is it?
                        detections.append({
                            "frame": frame_count,
                            "timestamp_sec": round(timestamp, 2),
                            "object": railway_obj,
                            "confidence": round(conf, 2),
                            "x": int(x),
                            "y": int(y),
                            "width": int(w),
                            "height": int(h)
                        })
                        print(f"Found a {railway_obj} at {timestamp:.2f} seconds (confidence: {conf:.2f})")

        # Give a heads-up every 200 frames so we know it’s working
        if frame_count % 200 == 0:
            progress = frame_count / total_frames * 100
            print(f"Done with {frame_count}/{total_frames} frames ({progress:.1f}%)")

    # Clean up and let’s see how long it took
    cap.release()
    elapsed = time.time() - start_time
    print(f"All done with the video! Took {elapsed:.2f} seconds.")
    return detections

def save_and_summarize(detections, csv_file, summary_file):
    """Save what we found and make a nice summary."""
    if not detections:
        with open(summary_file, "w") as f:
            f.write("Didn’t find any railway objects. Hmm...")
        print("Nothing detected. Bummer!")
        return

    # Turn our findings into a neat table with Pandas
    df = pd.DataFrame(detections)
    df.to_csv(csv_file, index=False)  # Save all the details
    print(f"Saved the full list to {csv_file}")

    # Count how many of each thing we found
    object_counts = df["object"].value_counts()
    total_detections = len(df)
    unique_objects = len(object_counts)

    # Write up a little report
    with open(summary_file, "w") as f:
        f.write("Railway Track Object Detection Report\n")
        f.write("Went through an 11-minute railway track video and here’s what I found:\n")
        f.write(f"Total Detections: {total_detections}\n")
        f.write(f"Unique Objects Spotted: {unique_objects}\n\n")
        f.write("Here’s the breakdown:\n")
        f.write(object_counts.to_string())
    print(f"Wrote a summary to {summary_file}")

# Let’s get this show on the road!
if __name__ == "__main__":
    if not Path(video_path).exists():
        print(f"Hey, I can’t find the video at '{video_path}'. Can you fix the path?")
    else:
        print("Alright, let’s hunt for some railway objects!")
        detections = detect_railway_objects(video_path)
        if detections is not None:
            save_and_summarize(detections, output_csv, output_summary)
        print("All wrapped up! Check out the CSV and summary files.") 