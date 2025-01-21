from moviepy.editor import VideoFileClip, concatenate_videoclips
from models import Video, db, SharedLink
import os
from datetime import datetime, timedelta

UPLOAD_FOLDER = 'uploads'


def save_video(file):
    # Generate a unique filename (you can also use file extensions here)
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Save the file to the disk
    file.save(filepath)

    # Get video details (size and duration)
    video_clip = VideoFileClip(filepath)
    size = os.path.getsize(filepath) / (1024 * 1024)  # Convert bytes to MB
    duration = video_clip.duration  # Duration in seconds

    # Create and save the video record in the database
    new_video = Video(filename=filename, size=size, duration=duration, path=filepath)
    db.session.add(new_video)

    return new_video, None


def trim_video(filename, start_time, end_time):
    video_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(video_path):
        print("not found")
        return None, "Video file not found."


    # Load the video using the filename
    video_clip = VideoFileClip(video_path)

    # Ensure the start and end times are within the video duration
    if start_time < 0 or end_time > video_clip.duration or start_time >= end_time:
        return None, "Invalid trim times."

    # Trim the video
    trimmed_clip = video_clip.subclip(start_time, end_time)

    # Generate a new filename for the trimmed video
    trimmed_filename = f"trimmed_{filename}"
    trimmed_path = os.path.join(UPLOAD_FOLDER, trimmed_filename)

    # Write the trimmed video to disk
    trimmed_clip.write_videofile(trimmed_path, audio_codec="aac")

    # Get new video details
    size = os.path.getsize(trimmed_path) / (1024 * 1024)  # Convert bytes to MB
    duration = trimmed_clip.duration  # Duration in seconds

    # Create a new video record for the trimmed video
    trimmed_video = Video(filename=trimmed_filename, size=size, duration=duration, path=trimmed_path)
    db.session.add(trimmed_video)

    return trimmed_video, None


def merge_videos(video_files):
    # List to store the video clips
    clips = []

    for filename in video_files:
        video_path = os.path.join(UPLOAD_FOLDER, filename)

        if not os.path.exists(video_path):
            return None, f"Video file {filename} not found."

        # Load the video using the filename
        video_clip = VideoFileClip(video_path)
        clips.append(video_clip)

    # Concatenate the clips into one video
    final_clip = concatenate_videoclips(clips)

    # Generate a new filename for the merged video
    merged_filename = "merged_video.mp4"
    merged_path = os.path.join(UPLOAD_FOLDER, merged_filename)

    # Write the merged video to disk
    final_clip.write_videofile(merged_path, audio_codec="aac")

    # Get new video details
    size = os.path.getsize(merged_path) / (1024 * 1024)  # Convert bytes to MB
    duration = final_clip.duration  # Duration in seconds

    # Create a new video record for the merged video
    merged_video = Video(filename=merged_filename, size=size, duration=duration, path=merged_path)
    db.session.add(merged_video)

    return merged_video, None


def generate_link(video_id, expiry_time_minutes):
    video = Video.query.get(video_id)

    if not video:
        return None, "Video not found."

    # Generate a unique token for the link
    token = os.urandom(24).hex()
    expiry_time = datetime.now() + timedelta(minutes=expiry_time_minutes)

    # Create the shared link record
    shared_link = SharedLink(video_id=video_id, token=token, expiry_time=expiry_time)
    db.session.add(shared_link)

    return shared_link, expiry_time