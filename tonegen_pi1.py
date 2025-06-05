import tkinter as tk
import numpy as np
import pyaudio
import threading

class ToneGenerator:
    def __init__(self):
        self.running = False
        self.sample_rate = 22050
        self.p = pyaudio.PyAudio()

    def start(self, wave_l, freq_l, amp_l, wave_r, freq_r, amp_r):
        self.running = True
        threading.Thread(target=self._play, args=(wave_l, freq_l, amp_l, wave_r, freq_r, amp_r)).start()

    def stop(self):
        self.running = False

    def _waveform(self, kind, freq, amp, t):
        if kind == "Sine":
            return amp * np.sin(2 * np.pi * freq * t)
        elif kind == "Square":
            return amp * np.sign(np.sin(2 * np.pi * freq * t))
        elif kind == "Saw":
            return amp * 2 * (t * freq % 1) - amp
        elif kind == "Triangle":
            return amp * 2 * np.abs(2 * (t * freq % 1) - 1) - amp
        else:
            return np.zeros_like(t)

    def _play(self, wave_l, freq_l, amp_l, wave_r, freq_r, amp_r):
        stream = self.p.open(format=pyaudio.paFloat32, channels=2, rate=self.sample_rate, output=True)
        t = 0
        dt = 1 / self.sample_rate
        while self.running:
            length = 512
            time_array = np.linspace(t, t + dt * length, length, False)
            t += dt * length
            left = self._waveform(wave_l, freq_l, amp_l, time_array)
            right = self._waveform(wave_r, freq_r, amp_r, time_array)
            stereo = np.array([left, right]).T.flatten().astype(np.float32)
            stream.write(stereo.tobytes())
        stream.stop_stream()
        stream.close()

    def close(self):
        self.p.terminate()

def start_tone():
    gen.start(
        wave_l.get(), float(freq_l.get()), float(amp_l.get()),
        wave_r.get(), float(freq_r.get()), float(amp_r.get())
    )

def stop_tone():
    gen.stop()

root = tk.Tk()
root.title("Pi1 ToneGen")
gen = ToneGenerator()

tk.Label(root, text="Left Wave").grid(row=0, column=0)
wave_l = tk.StringVar(value="Sine")
tk.OptionMenu(root, wave_l, "Sine", "Square", "Saw", "Triangle").grid(row=0, column=1)

tk.Label(root, text="Freq L").grid(row=1, column=0)
freq_l = tk.StringVar(value="440")
tk.Entry(root, textvariable=freq_l).grid(row=1, column=1)

tk.Label(root, text="Amp L").grid(row=2, column=0)
amp_l = tk.StringVar(value="0.5")
tk.Entry(root, textvariable=amp_l).grid(row=2, column=1)

tk.Label(root, text="Right Wave").grid(row=0, column=2)
wave_r = tk.StringVar(value="Sine")
tk.OptionMenu(root, wave_r, "Sine", "Square", "Saw", "Triangle").grid(row=0, column=3)

tk.Label(root, text="Freq R").grid(row=1, column=2)
freq_r = tk.StringVar(value="440")
tk.Entry(root, textvariable=freq_r).grid(row=1, column=3)

tk.Label(root, text="Amp R").grid(row=2, column=2)
amp_r = tk.StringVar(value="0.5")
tk.Entry(root, textvariable=amp_r).grid(row=2, column=3)

tk.Button(root, text="Start", command=start_tone).grid(row=3, column=0, columnspan=2)
tk.Button(root, text="Stop", command=stop_tone).grid(row=3, column=2, columnspan=2)

root.protocol("WM_DELETE_WINDOW", lambda: [gen.stop(), gen.close(), root.destroy()])
root.mainloop()
