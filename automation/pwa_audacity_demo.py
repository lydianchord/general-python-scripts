# use py -2.7

import pywinauto


def generate_tone():
    main_window.Wait('exists enabled')
    main_window.MenuSelect('Generate -> Tone...')
    tone_gen = app['Tone Generator']
    tone_gen.Wait('exists enabled')
    tone_gen['Waveform:ComboBox'].Select('Sawtooth')
    tone_gen['Amplitude (0-1):Edit'].TypeKeys('^a{BACKSPACE}0.5')
    tone_gen['OK'].CloseClick()


def shift_semitones(semitones, filename):
    main_window.Wait('exists enabled')
    main_window.MenuSelect('Effect -> Change Pitch...')
    change_pitch = app['Change Pitch']
    change_pitch.Wait('exists enabled')
    change_pitch['Semitones (half-steps):Edit'].TypeKeys('^a{BACKSPACE}' + str(semitones))
    change_pitch['OK'].CloseClick()
    
    main_window.Wait('exists enabled')
    main_window.MenuSelect('File -> Export Audio...')
    export = app['Export Audio']
    export.Wait('exists enabled')
    export['File name:Edit'].TypeKeys(filename)
    export['Save'].CloseClick()
    
    warning = app['Warning']
    # warning.Wait('exists enabled', 0.1)
    if warning.Exists():
        warning['Yes'].CloseClick()
    
    metadata = app['Edit Metadata']
    metadata.Wait('exists enabled')
    metadata['OK'].CloseClick()


def undo():
    main_window.Wait('exists enabled')
    main_window.TypeKeys('^z')


if __name__ == '__main__':
    try:
        app = pywinauto.application.Application()
        app.start_(r'C:\Program Files (x86)\Audacity\audacity.exe')
        main_window = app['Audacity']
        main_window.Wait('exists enabled')
        
        generate_tone()
        
        shift_semitones(0.33, 'saw_up.wav')
        undo()
        shift_semitones(-0.33, 'saw_down.wav')
        undo()

    finally:
        app.kill_()
