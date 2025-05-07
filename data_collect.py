import cv2
import argparse
import os

def video_record():
    parser = argparse.ArgumentParser(description='Video capture to disk')
    parser.add_argument('--device', type=int, default=0,
                        help='Camera device index')
    parser.add_argument('--name', type=str, default='test',
                        help='Video file name')
    parser.add_argument('--output_dir', type=str, default='raw_dataset',
                        help='Raw dataet folder with videos')
    args = parser.parse_args()


    os.makedirs(args.output_dir, exist_ok=True)
    out_path = os.path.join(args.output_dir, f"{args.name}.mp4")

    cap = cv2.VideoCapture(args.device)
    if not cap.isOpened():
        print(f"Error: cannot open camera {args.device}")
        return

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, 20.0, (w, h))

    print(f"Recording to {out_path}. Press 'q' to stop.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No frame! Breaking out.")
            break

        out.write(frame)
        cv2.imshow('Recording', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    video_record()
