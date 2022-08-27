from moviepy.editor import *


def speeden(video_path: str, speeds: list) -> VideoClip:
    """Changes the playback speed of the video file at the specified intervals.

    speeds: [
        {"start": 0.00, "end": 30.00, "speed": 1.3},
        {"start": 30.00, "end": 95.23, "speed": 2},
        ...,
    ]
    """

    # Assert 'speeds' forms a consecutive, disjoint sequence
    assert speeds[0]["start"] == 0.00
    for i in range(1, len(speeds)):
        assert speeds[i - 1]["end"] == speeds[i]["start"]

    video = VideoFileClip(video_path)

    output = None
    for sp in speeds:
        sub_video: VideoClip = video.subclip(sp["start"], sp["end"])
        sub_video = sub_video.fx(vfx.speedx, sp["speed"])

        if output == None:
            output = sub_video
        else:
            output = concatenate_videoclips([output, sub_video])

    return output
