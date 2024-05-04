import cv2
import openpose_python as op

# Configure OpenPose
params = {
    "model_folder": "../models",
    "hand": False,
    "face": False,
    "disable_blending": False,
    "display": 0,
}

# Initialize OpenPose
openpose = op.WrapperPython()
openpose.configure(params)
openpose.start()

# Open video file
video_path = "input_video.mp4"
cap = cv2.VideoCapture(video_path)

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_video.avi', fourcc, fps, (frame_width, frame_height))

# Process each frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Process the frame with OpenPose
    datum = op.Datum()
    datum.cvInputData = frame
    openpose.emplaceAndPop([datum])

    # Draw skeleton on the frame
    if datum.poseKeypoints is not None:
        keypoints = datum.poseKeypoints[0]  # Assuming only one person in the frame
        for point in keypoints:
            x, y = int(point[0]), int(point[1])
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    # Write the frame to the output video
    out.write(frame)

    # Display the frame
    cv2.imshow('Skeletonized Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and writer
cap.release()
out.release()
cv2.destroyAllWindows()