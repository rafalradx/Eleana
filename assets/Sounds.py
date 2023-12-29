import platform
import subprocess

class Sound:
    def beep(self):
        if platform.system() == 'Windows':
            import winsound
            winsound.Beep(500, 100)
        else:
            # Odtwórz dźwięk w systemie Unix/Linux/macOS
            command = 'paplay /usr/share/sounds/freedesktop/stereo/bell.oga'
            subprocess.run(command, shell=True)
