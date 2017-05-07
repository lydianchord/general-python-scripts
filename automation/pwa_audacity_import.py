# use py -2.7

import itertools
import os
import pywinauto


def name_files(base, extension, start_num, stop_num, *var_lists):
    var_combos = [''.join(x) for x in itertools.product(*var_lists)]
    file_range = range(start_num, stop_num + 1)
    filenames = [base + str(num) + var + extension
                 for num in file_range for var in var_combos]
    return filenames


def audactiy_import(path):
    main_window.Wait('exists enabled')
    main_window.TypeKeys('^+i')
    importer = app['Select one or more audio files...']
    importer.Wait('exists enabled')
    importer['File name: Edit'].TypeKeys(path, with_spaces=True)
    importer['Open'].Click()
    
    warning = app['Warning']
    warning.Wait('exists enabled')
    warning['OK'].Click()


def shift_semitones(semitones):
    main_window.Wait('exists enabled')
    main_window.MenuSelect('Effect -> Change Pitch...')
    change_pitch = app['Change Pitch']
    change_pitch.Wait('exists enabled')
    change_pitch['Semitones (half-steps): Edit'].TypeKeys('^a{BACKSPACE}' + str(semitones))
    change_pitch['OK'].Click()


def audacity_export(path):
    main_window.Wait('exists enabled')
    main_window.MenuSelect('File -> Export Audio...')
    export = app['Export Audio']
    export.Wait('exists enabled')
    export['File name: Edit'].TypeKeys(path, with_spaces=True)
    export['Save'].CloseClick()
    
    warning = app['Warning']
    if warning.Exists():
        warning['Yes'].Click()
    
    metadata = app['Edit Metadata']
    metadata.Wait('exists enabled')
    metadata['OK'].Click()


def undo():
    main_window.Wait('exists enabled')
    main_window.TypeKeys('^z')


if __name__ == '__main__':
    base = ''
    ext = '.wav'
    start = 1
    stop = 3
    var_list1 = ('_1', '_2')
    var_list2 = ('_0', '_33', '_-33')
    
    # filenames = name_files(base, ext, start, stop)
    filenames = name_files(base, ext, start, stop, var_list2)
    # filenames = name_files(base, ext, start, stop, var_list1, var_list2)
    
    basedir = r'\test folder'       # alter
    os.chdir(basedir)
    old_dir = 'tones'               #
    new_dir = 'tonesnew'            #
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    num_to_skip = 0                 #
    working_files = os.listdir(os.path.join(basedir, old_dir))[num_to_skip:]
    
    try:
        app = pywinauto.application.Application()
        app.start_(r'\Program Files (x86)\Audacity\audacity.exe')               #
        main_window = app['Audacity']
        main_window.Wait('exists enabled ready')
        idx = 0
        for f in working_files:
            audactiy_import(os.path.join(basedir, old_dir, f))
            main_window = app[f[:-3]]
            
            shift_semitones(0.165)
            shift_semitones(-0.165)
            audacity_export(os.path.join(basedir, new_dir, filenames[idx]))
            idx += 1
            undo()
            undo()
            shift_semitones(0.33)
            audacity_export(os.path.join(basedir, new_dir, filenames[idx]))
            idx += 1
            undo()
            shift_semitones(-0.33)
            audacity_export(os.path.join(basedir, new_dir, filenames[idx]))
            idx += 1
            undo()
            
            undo()
    
    except:
        raise

    finally:
        app.kill_()
