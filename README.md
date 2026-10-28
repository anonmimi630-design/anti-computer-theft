## Never want to get stolen? -> Then add this program!!
Computer Theft Prevention System is a Windows-based security alert and theft-deterrence application developed using Python. The program is designed to provide a highly visible and audible warning when activated, combining a fullscreen security interface, password-based deactivation, continuous alarm generation, automated voice announcements, live webcam monitoring, and local video recording.

The primary objective of the application is to discourage unauthorized possession or use of a computer by displaying a prominent theft warning and generating an audible security alert. Simultaneously, the application can capture video footage from the computer's built-in or connected webcam, providing a local record of the environment during the alarm session.

Unlike conventional security applications that primarily operate in the background, Computer Theft Prevention System uses an immediately noticeable visual interface. Its design emphasizes visibility, sound, and continuous monitoring rather than remaining hidden from the person operating the computer.

The application is intended to function as a supplementary security measure, particularly for laptops used in educational institutions, offices, libraries, shared workspaces, and other environments where unauthorized physical access may be a concern.

It is important to distinguish this application from a complete endpoint security solution. It does not provide hardware-level theft protection, operating-system authentication, file encryption, remote device tracking, or guaranteed protection against computer shutdown.

1. Fullscreen Security Warning Interface

Upon activation, the application opens a fullscreen graphical interface developed using Python's Tkinter framework.

The interface is designed to occupy the entire display, presenting a prominent warning that the computer may have been stolen or accessed without authorization.

The application uses a high-contrast color scheme consisting primarily of black, red, orange-red, and white. These colors emphasize the warning message and create a visually distinctive security alert.

The interface contains several important elements:

Security status indicator: Identifies the application as an active computer theft-prevention system.

Theft warning message: Displays a Japanese-language warning indicating that the computer may have been stolen.

Countdown display: Presents the remaining time in minutes, seconds, and milliseconds.

Password authentication field: Allows an authorized user to deactivate the alarm.

Live camera monitoring window: Displays footage from the computer's webcam.

Recording status indicator: Informs users that video recording is active.

The interface is primarily written in Japanese, making it suitable for Japanese-language Windows environments.

Although the interface occupies the full screen, it is not a secure Windows lock screen. Standard operating-system controls remain available.

2. Red-and-Black Visual Alert System

One of the application's central features is its alternating background-color effect.

The display transitions between black and red at a configurable interval, producing a recognizable security-warning appearance.

The current configuration uses approximately one second per color.

Visual sequence:

BLACK → RED → BLACK → RED → BLACK → RED

The program schedules these transitions using Tkinter's event-handling system. The colors alternate automatically while the application remains active.

This visual effect is intended to draw attention to the computer and communicate that a security alert is in progress.

The flashing system can be customized by modifying the background colors or the interval between transitions.

Because flashing displays can cause discomfort or photosensitive reactions, the application should be used with restrained brightness and transition frequency.

3. Continuous 1,000 Hz Audio Alarm

The application incorporates an electronically generated audio alarm operating at a frequency of 1,000 hertz.

Rather than requiring a prerecorded audio file, the system generates a sine-wave signal mathematically using NumPy.

The sound is delivered through the computer's audio output using the sounddevice library.

The signal generation system uses a sample rate of 44,100 samples per second, allowing the program to produce a consistent waveform.

Audio specifications:

Signal type: Sine wave

Frequency: 1,000 Hz

Sample rate: 44.1 kHz

Default digital amplitude: 0.03

Playback duration: Continuous while the alarm is active

Output device: Windows-selected audio output

The audio system is intended to operate alongside the visual warning and other security features.

Audio playback depends on the computer's active audio device, Windows volume settings, and mute status. The application does not guarantee that sound will be audible when the computer is muted or its speakers are disconnected.

4. Automated Text-to-Speech Security Announcements

In addition to the electronically generated alarm, the application supports automated spoken security announcements.

This functionality uses Windows' built-in speech synthesis capabilities through PowerShell and the System.Speech framework.

When enabled, the voice announcement can repeatedly state:

"Computer stolen."

The repeated message is intended to communicate the nature of the security alert to people nearby.

The speech system can also support Japanese-language announcements when a compatible Japanese speech synthesis voice is installed.

The announcement runs independently of the graphical interface so that speech playback does not prevent the countdown, camera preview, or other interface components from updating.

The voice process is terminated during normal application shutdown.

Speech volume is controlled separately from the generated 1,000 Hz signal, although both depend on Windows' master audio settings.
5. Live Front-Facing Camera Monitoring

Computer Theft Prevention System integrates a live webcam monitoring feature using OpenCV.

When the application starts, it attempts to initialize the computer's default camera.

If the camera is available, a live video feed appears in the bottom-left corner of the security interface.

The video preview provides a real-time view of the environment in front of the computer.

The camera system includes:

Automatic webcam initialization

Live image capture

Horizontally mirrored preview

Video frame resizing

Integration with the Tkinter interface

Visible recording-status information

Camera resource cleanup during shutdown

The configured preview resolution is 320 × 240 pixels, with a target recording frame rate of 20 frames per second.

The actual frame rate depends on the webcam, available processing resources, and the responsiveness of the application's event loop.

The camera preview is displayed directly within the application and does not require an external video player.

6. Automatic Local Video Recording

The application supports recording webcam footage during an active alarm session.

Captured video frames are encoded into an MP4 file using OpenCV's VideoWriter functionality.

The recording is saved locally to the Windows user's Videos directory.

Example output location:

C:\Users\Username\Videos\

Example filename:

Camera_2026-10-28_20-30-00.mp4

The filename incorporates the date and time of the recording session, allowing recordings from different activations to be distinguished.

When the application is closed normally, it releases the video writer and webcam resources, allowing the MP4 file to be finalized.

This provides a record of what the camera observed during the alarm session.

The video recording feature does not automatically transmit footage to an external server, cloud storage provider, or administrator.

Recording is performed locally, and access to the files depends on the Windows account and filesystem permissions.

The recording feature captures webcam video only. It does not currently include microphone audio, the synthesized voice announcement, or the electronic alarm tone.

A visible recording indicator is provided so that people near the computer can recognize that camera recording is active.

7. Ten-Minute Security Countdown

The program includes a digital countdown timer initialized to ten minutes.

The countdown is displayed using the following format:

MM.mmm

For example:

10:00.000

09:59.999

05:30.425

00:00.000

The final three digits represent milliseconds.

The timer uses Python's high-resolution performance counter to calculate elapsed time rather than simply subtracting a fixed value after every graphical update.

This approach helps reduce accumulated timing errors caused by delays in the graphical interface.

The countdown is intended to communicate urgency and provide a clear visual indication of elapsed time during the security alert.

In the current implementation, reaching zero does not automatically shut down Windows, delete files, or perform any destructive operation.

8. Password-Based Alarm Deactivation

The security interface includes a password entry field that allows an authorized user to terminate the alarm session.

The password is checked against a configured value stored in the program.

When a correct password is entered, the program initiates its shutdown procedure.

This procedure stops audio playback, ends the speech announcement, releases the camera, finalizes the video recording, and closes the graphical interface.

If an incorrect password is entered, the application displays an error message and clears the input field.

The program also supports immediate termination through the Escape key.

This ensures that the simulation can be stopped without waiting for the countdown to finish.

The password system is an application-level control rather than a replacement for Windows account authentication. Because the password is stored in the Python source code, it should not be treated as strong protection against a technically knowledgeable attacker.

9. Coordinated Shutdown and Resource Management

The application includes a centralized shutdown procedure intended to stop its active components when the program closes normally.

The shutdown process performs several operations:

Changes the application's running state to inactive.

Stops the generated audio signal.

Terminates the speech announcement process.

Finalizes the active MP4 recording.

Releases the webcam.

Closes the fullscreen graphical interface.

Proper resource management is particularly important when working with cameras and audio devices.

Without appropriate cleanup, a webcam could remain temporarily unavailable to other applications, or an audio process could continue running after its graphical interface has closed.

The coordinated shutdown system reduces these risks during normal operation.

Unexpected operating-system termination, power loss, or a forced process shutdown may prevent all cleanup operations from completing.

10. Laptop Lid and Power Management Compatibility

The application can continue operating when a laptop lid is closed, provided that Windows remains running and the computer does not enter sleep or hibernation.

Windows includes separate lid-close behavior settings for battery operation and external power.

When the lid-close action is configured as "Do nothing," Windows may allow the program to continue executing while the display is closed.

Under these conditions, audio playback, countdown calculations, and other background operations can continue.

However, webcam operation may be interrupted if the laptop lid physically blocks the camera or if the device firmware disables the camera.

The application cannot continue executing after a complete computer shutdown or loss of electrical power.

It is also important to consider battery consumption and thermal management when allowing a laptop to remain active with its lid closed.
## Requirements
On windows
Win + R and type `cmd` and Ctrl+Shift+Enter
Type `py -m pip install numpy sounddevice opencv-python pillow`
&
Close that, then Win + R and type `control.exe /name Microsoft.PowerOptions`
Then click the `When I close the lid` menu and the most left.
Then go to `When I close the lid (The 3rd one)` and make both on battery and plugged in to None(top on the dropdown).
FINISH
