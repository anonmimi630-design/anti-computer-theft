
import tkinter as tk
import subprocess
import time
import numpy as np
import sounddevice as sd
import cv2
from PIL import Image, ImageTk
from pathlib import Path
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

PASSWORD = "AirbusA350-1000XWB"

DURATION = 600.0
FLASH_INTERVAL = 1000

FREQUENCY = 1000
VOLUME = 0.25
SAMPLE_RATE = 44100

CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
VIDEO_FPS = 20.0

BLACK = "#000000"
RED = "#db270f"
TEXT_RED = "#FF4500"
WHITE = "#ffffff"

VIDEOS_FOLDER = Path.home() / "Videos"
VIDEOS_FOLDER.mkdir(parents=True, exist_ok=True)

running = True
start_time = time.perf_counter()

audio_stream = None
camera = None
video_writer = None
recording_path = None
phase = 0.0
speech_process = None

# ============================================================
# WINDOW
# ============================================================

root = tk.Tk()
root.title("コンピューター窃盗防止プログラム")
root.attributes("-fullscreen", True)
root.configure(bg=BLACK)

# ============================================================
# AUDIO
# ============================================================

def audio_callback(outdata, frames, time_info, status):
    global phase

    if not running:
        outdata.fill(0)
        return

    positions = np.arange(frames)

    angles = (
        phase
        + 2 * np.pi * FREQUENCY
        * positions / SAMPLE_RATE
    )

    outdata[:, 0] = VOLUME * np.sin(angles)

    phase = (
        phase
        + 2 * np.pi * FREQUENCY
        * frames / SAMPLE_RATE
    ) % (2 * np.pi)


def start_audio():
    global audio_stream

    try:
        audio_stream = sd.OutputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            callback=audio_callback,
            blocksize=1024
        )

        audio_stream.start()

    except Exception as error:
        print("Audio unavailable:", error)
        audio_stream = None

# ============================================================
# REPEATING WINDOWS VOICE ANNOUNCEMENT
# ============================================================

def start_voice_alarm():
    global speech_process

    # The voice runs in a separate process so the interface stays responsive.
    # It will be terminated by close_screen().
    powershell_script = r"""
Add-Type -AssemblyName System.Speech
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speaker.Volume = 100
$speaker.Rate = 0
try {
    while ($true) {
        $speaker.Speak('コンピューターが盗まれました。')
        Start-Sleep -Milliseconds 800
    }
} finally {
    $speaker.Dispose()
}
"""
    try:
        speech_process = subprocess.Popen(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", powershell_script],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except OSError as error:
        print("Speech unavailable:", error)
        speech_process = None


# ============================================================
# EXIT AND PASSWORD
# ============================================================

def close_screen(event=None):
    global running, video_writer

    if not running:
        return

    running = False

    # Stop the repeating spoken announcement.
    if speech_process is not None:
        try:
            speech_process.terminate()
            speech_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            speech_process.kill()
            speech_process.wait()
        except OSError:
            pass

    # Stop sound
    if audio_stream is not None:
        try:
            audio_stream.abort()
            audio_stream.close()
        except Exception:
            pass

    # Finalize MP4 recording
    if video_writer is not None:
        try:
            video_writer.release()
            video_writer = None
        except Exception:
            pass

    # Release camera
    if camera is not None:
        try:
            camera.release()
        except Exception:
            pass

    root.destroy()


def check_password(event=None):
    if password_entry.get() == PASSWORD:
        close_screen()
    else:
        error_label.config(text="無効です。10分以内に正解してください。")
        password_entry.delete(0, tk.END)


root.bind_all("<Escape>", close_screen)
root.protocol("WM_DELETE_WINDOW", close_screen)

# ============================================================
# MAIN INTERFACE
# ============================================================

main_frame = tk.Frame(root, bg=BLACK)
main_frame.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


def create_label(text, size, color, bold=False):
    label = tk.Label(
        main_frame,
        text=text,
        font=(
            "Consolas",
            size,
            "bold" if bold else "normal"
        ),
        fg=color,
        bg=BLACK
    )

    label.pack(pady=12)
    return label


simulation_label = create_label(
    "コンピューター窃盗防止プログラム作動中",
    14,
    WHITE
)

warning_label = create_label(
    "コンピューターが盗まれた可能性があります。",
    40,
    TEXT_RED,
    True
)

bitcoin_label = create_label(
    "10分以内にパスワードを入力してください。",
    28,
    TEXT_RED,
    True
)

timer_label = create_label(
    "10:00.000",
    48,
    WHITE,
    True
)

password_label = create_label(
    "パスワード入力",
    22,
    WHITE
)

password_entry = tk.Entry(
    main_frame,
    font=("Consolas", 20),
    width=22,
    show="*",
    justify="center",
    fg=WHITE,
    bg="#222222",
    insertbackground=WHITE
)

password_entry.pack(
    pady=10,
    ipady=8
)

password_entry.bind("<Return>", check_password)

unlock_button = tk.Button(
    main_frame,
    text="UNLOCK",
    font=("Consolas", 16, "bold"),
    command=check_password,
    fg=WHITE,
    bg="#880000",
    activebackground="#aa0000",
    activeforeground=WHITE,
    padx=30,
    pady=8
)

unlock_button.pack(pady=15)

error_label = create_label(
    "",
    14,
    TEXT_RED
)

# ============================================================
# CAMERA DISPLAY
# ============================================================

camera_frame = tk.Frame(
    root,
    bg=BLACK,
    highlightbackground=TEXT_RED,
    highlightthickness=2
)

camera_frame.place(
    x=20,
    rely=1.0,
    y=-20,
    anchor="sw"
)

recording_label = tk.Label(
    camera_frame,
    text="録画中（この録画は管理者に保存されます。）",
    font=("Consolas", 15, "bold"),
    fg=TEXT_RED,
    bg=BLACK
)

recording_label.pack(pady=5)

camera_label = tk.Label(
    camera_frame,
    bg=BLACK,
    width=CAMERA_WIDTH,
    height=CAMERA_HEIGHT
)

camera_label.pack()

camera_status = tk.Label(
    camera_frame,
    text="カメラ初期化中",
    font=("Consolas", 10),
    fg=WHITE,
    bg=BLACK
)

camera_status.pack(pady=5)

# ============================================================
# CAMERA RECORDING
# ============================================================

def start_camera():
    global camera, video_writer, recording_path

    try:
        camera = cv2.VideoCapture(
            0,
            cv2.CAP_DSHOW
        )

        if not camera.isOpened():
            recording_label.config(text="カメラオフ")
            camera_status.config(text="カメラ使用不可")
            return

        camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            CAMERA_WIDTH
        )

        camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            CAMERA_HEIGHT
        )

        filename = (
            "Camera_"
            + datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S"
            )
            + ".mp4"
        )

        recording_path = VIDEOS_FOLDER / filename

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        video_writer = cv2.VideoWriter(
            str(recording_path),
            fourcc,
            VIDEO_FPS,
            (CAMERA_WIDTH, CAMERA_HEIGHT)
        )

        if not video_writer.isOpened():
            video_writer = None
            recording_label.config(
                text="録画失敗"
            )
            camera_status.config(
                text="録画保存失敗"
            )
            return

        recording_label.config(text="録画中")
        camera_status.config(
            text="管理者フォルダに保存中…"
        )

        update_camera()

    except Exception as error:
        recording_label.config(text="カメラにエラー")
        camera_status.config(text=str(error))


def update_camera():
    if not running:
        return

    if camera is not None and camera.isOpened():

        success, frame_image = camera.read()

        if success:
            # Mirror front-camera image
            frame_image = cv2.flip(frame_image, 1)

            frame_image = cv2.resize(
                frame_image,
                (CAMERA_WIDTH, CAMERA_HEIGHT)
            )

            # Record frame to MP4
            if video_writer is not None:
                video_writer.write(frame_image)

            # Convert frame for Tkinter
            rgb_image = cv2.cvtColor(
                frame_image,
                cv2.COLOR_BGR2RGB
            )

            image = Image.fromarray(rgb_image)
            photo = ImageTk.PhotoImage(image)

            camera_label.configure(image=photo)
            camera_label.image = photo

    if running:
        root.after(
            int(1000 / VIDEO_FPS),
            update_camera
        )

# ============================================================
# FLASHING EFFECT
# ============================================================

flash_state = False


def flash_screen():
    global flash_state

    if not running:
        return

    flash_state = not flash_state

    background = (
        RED if flash_state else BLACK
    )

    root.configure(bg=background)
    main_frame.configure(bg=background)
    camera_frame.configure(bg=background)

    for widget in (
        simulation_label,
        warning_label,
        bitcoin_label,
        timer_label,
        password_label,
        error_label,
        recording_label,
        camera_status
    ):
        widget.configure(bg=background)

    root.after(
        FLASH_INTERVAL,
        flash_screen
    )

# ============================================================
# COUNTDOWN TIMER
# ============================================================

def update_timer():
    if not running:
        return

    elapsed = time.perf_counter() - start_time

    remaining = max(
        0.0,
        DURATION - elapsed
    )

    total_ms = int(remaining * 1000)

    minutes = total_ms // 60000
    seconds = (total_ms // 1000) % 60
    milliseconds = total_ms % 1000

    timer_label.configure(
        text=(
            f"{minutes:02d}:"
            f"{seconds:02d}."
            f"{milliseconds:03d}"
        )
    )

    if remaining > 0:
        root.after(10, update_timer)

# ============================================================
# START PROGRAM
# ============================================================

start_audio()
start_camera()
start_voice_alarm()

password_entry.focus_set()

flash_screen()
update_timer()

root.mainloop()
