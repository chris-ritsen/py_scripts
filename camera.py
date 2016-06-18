#!/usr/bin/env python3

import subprocess
import time


def process_video():
    subprocess.check_output(
        [
            "ffmpeg",
            "-y",
            "-loglevel", "quiet",
            "-i", "/home/chris/test.mkv",
            "-c:v", "libx265",
            "-filter:v", "fps=30",
            "-preset", "superfast",
            "-crf", "20",
            "-b:a", "160k",
            "-c:a", "mp2",
            "-af", "volume=2.0",
            "-ac", "1",
            "-ss", "00:00:00.033",
            "/home/chris/test2.mkv"
        ],
        stderr=subprocess.PIPE
    )

    rename_video()


def setup_camera():

    subprocess.call(
        [
            "v4l2-ctl",
            "-d", "/dev/video0",
            "-c", "focus_auto=0"
        ]
    )

    subprocess.check_output(
        [
            "v4l2-ctl",
            "-d", "/dev/video0",
            "--set-parm=30"
        ]
    )

    subprocess.call(
        [
            "v4l2-ctl",
            "-d", "/dev/video0",
            "--set-fmt-video=width=1280,height=720,pixelformat=0"
        ]
    )

    time.sleep(1)


def rename_video():
    subprocess.call(
        [
            "mv",
            "/home/chris/test2.mkv",
            "/home/chris/test.mkv"
        ]
    )


def fix_audio_delay():

    # Corrects audio starting late (10 frames of video)
    # It remains to be seen whether the audio and video stream duration
    # difference is the problem or not.

    subprocess.call(
        [
            "test.mkv",
            "-itsoffset", "-00:00:00.333",
            "-i", "test.mkv",
            "-c:v", "copy",
            "-c:a", "copy",
            "-map", "0:0",
            "-map", "1:1",
            "test2.mkv"
        ]
    )

    rename_video()


def record_camera():

    subprocess.call(
        [
            "nice",
            "-n", "0",
            "ffmpeg",
            "-y",
            "-loglevel", "quiet",
            "-f", "video4linux2",
            "-thread_queue_size", "512",
            "-framerate", "30",
            "-input_format", "mjpeg",
            "-i", "/dev/video0",
            "-f", "alsa",
            "-thread_queue_size", "512",
            "-i", "pulse",
            "-filter_complex", "aresample=async=1000",
            "-ac", "1",
            "-b:a", "160k",
            "-c:a", "mp2",
            "-c:v", "copy",
            "-copyinkf",
            "-threads", "0",
            "-f", "matroska",
            "/home/chris/test.mkv"
        ]
    )

if __name__ == '__main__':
    setup_camera()
    record_camera()
    process_video()
    # fix_audio_delay()

