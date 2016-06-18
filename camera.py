#!/usr/bin/env python3

import subprocess


def record_camera():
    subprocess.call(
        [
            "v4l2-ctl",
            "-d",
            "/dev/video0",
            "-c",
            "focus_auto=0"
        ]
    )

    subprocess.call(
        [
            "v4l2-ctl",
            "-d",
            "/dev/video0",
            "--set-parm=30"
        ]
    )

    subprocess.call(
        [
            "v4l2-ctl",
            "-d",
            "/dev/video0",
            "--set-fmt-video=width=1280,height=720,pixelformat=0"
        ]
    )

    subprocess.call(
        [
            "nice",
            "-n", "0",
            "ffmpeg",
            "-y",
            "-f", "video4linux2",
            "-thread_queue_size", "512",
            "-framerate", "30",
            "-input_format", "mjpeg",
            "-i", "/dev/video0",
            "-f", "alsa",
            "-thread_queue_size", "512",
            "-i", "pulse",
            "-filter_complex", "aresample=async=1",
            "-ac", "1",
            "-b:a", "160k",
            "-acodec", "mp2",
            "-c:v", "copy",
            "-copyinkf",
            "-threads", "0"
            "-f", "matroska",
            "test.mkv"
        ]
    )

    subprocess.call(
        [
            "ffmpeg",
            "-i",
            "test.mkv",
            "-c:v",
            "libx265",
            "-filter:v",
            "fps=30",
            "-preset",
            "superfast",
            "-crf",
            "20",
            "-c:a",
            "mp2",
            "-af",
            "volume=2.0",
            "-ac",
            "1",
            "-y",
            "test2.mkv"
        ]
    )

    subprocess.call(
        [
            "mv",
            "test2.mkv",
            "test.mkv"
        ]
    )

if __name__ == '__main__':
    record_camera()

