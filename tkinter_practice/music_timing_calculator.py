import re

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    try:
        import Tkinter as tk
        import ttk
    except ImportError:  # Tkinter unnecessary if importing into Ren'py
        pass


class MusicTimingCalculator(object):
    
    def __init__(self, tempo=0, beats_per_measure=0, num_measures=0):
        input_dict = {k: v for (k, v) in locals().items() if k != 'self'}
        self.configurable = set(input_dict)
        self.config(**input_dict)
        self.calculate()
    
    def config(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.configurable:
                setattr(self, k, v)
    
    def calculate(self):
        if self.tempo > 0:
            self.one_beat = 60.0 / self.tempo
            self.one_measure = self.one_beat * self.beats_per_measure
            self.song_length = self.one_measure * self.num_measures
            num_min, num_sec = divmod(self.song_length, 60)
            self.song_length_min = (int(num_min), num_sec)
        else:
            self.one_beat = 0
            self.one_measure = 0
            self.song_length = 0
            self.song_length_min = (0, 0)


class MusicTimingCalculatorApp(object):
    
    def __init__(self, master):
        self.master = master
        self.frame = frame = ttk.Frame(master)
        self.calc = MusicTimingCalculator()
        
        master.title('Music Timing Calculator')
        
        self.one_beat_text = tk.StringVar()
        self.one_measure_text = tk.StringVar()
        self.song_length_text = tk.StringVar()
        self.song_length_min_text = tk.StringVar()
        
        self.set_results_text()
        
        tempo_vcmd = (frame.register(self.validate_tempo), '%P')
        beats_vcmd = (frame.register(self.validate_beats), '%P')
        measures_vcmd = (frame.register(self.validate_measures), '%P')
        
        self.tempo_entry = ttk.Entry(frame, validate='key', validatecommand=tempo_vcmd, justify='right')
        self.beats_entry = ttk.Entry(frame, validate='key', validatecommand=beats_vcmd, justify='right')
        self.measures_entry = ttk.Entry(frame, validate='key', validatecommand=measures_vcmd, justify='right')
        
        self.calculate_button = ttk.Button(frame, text='Calculate', command=self.calculate)
        
        self.one_beat_display = ttk.Entry(frame, state='readonly', textvariable=self.one_beat_text, justify='right')
        self.one_measure_display = ttk.Entry(frame, state='readonly', textvariable=self.one_measure_text, justify='right')
        self.song_length_display = ttk.Entry(frame, state='readonly', textvariable=self.song_length_text, justify='right')
        self.song_length_min_display = ttk.Entry(frame, state='readonly', textvariable=self.song_length_min_text, justify='right')
        
        master.bind('<Return>', self.calculate)
        
        # --Layout--
        
        default_pad = 5
        
        master.minsize(width=300, height=150)
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        
        frame.grid(padx=10, pady=10, sticky='nsew')
        
        ttk.Label(frame, text='Tempo (beats per min):').grid(row=0, column=0, sticky='nw')
        ttk.Label(frame, text='Beats per measure:').grid(row=0, column=1, sticky='nw', padx=default_pad)
        ttk.Label(frame, text='Number of measures:').grid(row=0, column=2, sticky='nw')
        
        self.tempo_entry.grid(row=1, column=0, sticky='ew')
        self.beats_entry.grid(row=1, column=1, sticky='ew', padx=default_pad)
        self.measures_entry.grid(row=1, column=2, sticky='ew')
        
        self.calculate_button.grid(row=2, column=0, columnspan=3)
        
        ttk.Separator(frame, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky='ew')
        
        ttk.Label(frame, text='One beat:').grid(row=4, column=0, sticky='e')
        self.one_beat_display.grid(row=4, column=1, sticky='ew', padx=default_pad)
        
        ttk.Label(frame, text='One measure:').grid(row=5, column=0, sticky='e')
        self.one_measure_display.grid(row=5, column=1, sticky='ew', padx=default_pad)
        
        ttk.Label(frame, text='Song length:').grid(row=6, column=0, sticky='e')
        self.song_length_display.grid(row=6, column=1, sticky='ew', padx=default_pad)
        self.song_length_min_display.grid(row=6, column=2, sticky='ew')
        
        num_cols, num_rows = frame.grid_size()
        for i in range(num_cols):
            frame.grid_columnconfigure(i, weight=1, pad=default_pad)
        for i in range(3, num_rows):
            frame.grid_rowconfigure(i, weight=1, pad=default_pad)
        for i in range(3):
            frame.grid_rowconfigure(i, weight=0, pad=default_pad)
    
    def set_results_text(self):
        template1 = '{0:.3f} sec'
        template2 = '{0} min  {1:.3f} sec'
        self.one_beat_text.set(template1.format(self.calc.one_beat))
        self.one_measure_text.set(template1.format(self.calc.one_measure))
        self.song_length_text.set(template1.format(self.calc.song_length))
        self.song_length_min_text.set(template2.format(*self.calc.song_length_min))
    
    def validate(self, new_val, input_var):
        if not new_val:
            self.calc.config(**{input_var: 0})
        else:
            if re.match(r'^\d*\.?\d*$', new_val) is None:
                return False
            try:
                self.calc.config(**{input_var: float(new_val)})
            except ValueError:
                return False
        return True
    
    def validate_tempo(self, new_val):
        return self.validate(new_val, 'tempo')
    
    def validate_beats(self, new_val):
        return self.validate(new_val, 'beats_per_measure')
    
    def validate_measures(self, new_val):
        return self.validate(new_val, 'num_measures')
    
    def calculate(self, event=None):
        self.calc.calculate()
        self.set_results_text()


if __name__ == '__main__':
    root = tk.Tk()
    app = MusicTimingCalculatorApp(root)
    root.mainloop()
