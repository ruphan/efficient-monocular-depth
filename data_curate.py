import cv2
import argparse
import os
from glob import glob

def create_dataset():
    parser = argparse.ArgumentParser(description='Data curation params')
    parser.add_argument('--input_dir', type=str, default='raw_dataset',
                        help='Raw dataset directory containing video files')
    parser.add_argument('--output_dir', type=str, default='curated_dataset',
                        help='Directory where extracted frames will be saved')
    parser.add_argument('--frame_rate', type=int, default=5,
                        help='Number of frames to extract per second of video')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    videos = [v for v in glob(os.path.join(args.input_dir, '*')) if os.path.isfile(v)]

    for video_path in videos:
        video_name = os.path.splitext(os.path.basename(video_path))[0]

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Could not open {video_path}, skipping.")
            continue

        video_fps = cap.get(cv2.CAP_PROP_FPS)
        interval = max(1, video_fps // args.frame_rate)

        frame_idx = 0
        count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % interval == 0:
                fname = f"{video_name}_{count:05d}.jpg"
                cv2.imwrite(os.path.join(args.output_dir, fname), frame)
                count += 1

            frame_idx += 1

        cap.release()
        print(f"Extracted {count} frames from {video_name}")

if __name__ == '__main__':
    create_dataset()
