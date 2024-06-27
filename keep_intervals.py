from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips

def keep_intervals(video_path, intervals, output_path):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # List to store the edited clips
    edited_clips = []

    # Use the existing fps value if available, otherwise set to a default value (e.g., 25 fps)
    fps = video_clip.fps if video_clip.fps is not None else 25

    # Cut the specified intervals
    for start_time, end_time in intervals:
        # Convert time to seconds
        start_seconds = sum(x * int(t) for x, t in zip([3600, 60, 1], start_time.split(":")))
        end_seconds = sum(x * int(t) for x, t in zip([3600, 60, 1], end_time.split(":")))

        # Cut the interval and append it to the list
        edited_clip = video_clip.subclip(start_seconds, end_seconds)
        edited_clips.append(edited_clip)

    # Concatenate the edited clips
    final_clip = concatenate_videoclips(edited_clips, method="compose")

    # Get the complement clip (original video - kept intervals)
    original_clip = concatenate_videoclips([video_clip.subclip(0, edited_clips[0].start)] +
                                           [video_clip.subclip(edited_clips[i].end, edited_clips[i+1].start)
                                            for i in range(len(edited_clips)-1)] +
                                           [video_clip.subclip(edited_clips[-1].end, video_clip.duration)])

    # Write the final edited video to a file with the correct fps
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=fps)

video_path = "/content/drive/MyDrive/Python_1.mp4"  # Update with your file path in Colab
output_path = "/content/drive/MyDrive/Python_1_edited.mp4"

# Specify intervals to be kept [(start_time_1, end_time_1), (start_time_2, end_time_2), ...]
intervals_to_keep =  [ ("00:06:13","00:18:50"),("00:31:33","00:40:00"),("00:41:52","00:57:00"),("00:58:30","01:30:50"),("01:31:46","01:46:47"),("01:47:50","02:11:17"),("02:16:54" ,"02:22:48"),("02:29:47","02:35:50")]
keep_intervals(video_path, intervals_to_keep, output_path)
