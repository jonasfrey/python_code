import PySimpleGUI as sg

# layout = [      
#     [sg.Canvas(size=(100, 100), key= 'canvas',)],      
#     [sg.T('Change circle color to:'), sg.Button('Red'), sg.Button('Blue')]      
#     ]  

# window = sg.Window('Sample window', layout,
#                keep_on_top=True,
#                auto_size_buttons=False,
#                grab_anywhere=False,
#                no_titlebar=True,
#                return_keyboard_events=False,
#                alpha_channel=0.8,
#                use_default_focus=False,
#                transparent_color='red',
#                finalize=True)  

# window.read()
a_layout = [
    [sg.Text('Some text on Row 1', key="s_id_string")]
    ]
s_window_name = "asdf"
o_window = sg.Window(
    keep_on_top=True, 
    title=s_window_name,
    layout=a_layout,
    margins=(100, 50),
    finalize=True
    )
o_window["s_id_string"].update('My new text value')
o_window.read(timeout=1)

# window = sg.Window(keep_on_top=True,  title=s_window_name, layout=a_layout, margins=(100, 50)).read()
ni = 0
while True:             # Event Loop
    ni = ni+1
    # event, values = window.read()
    window["s_id_string"].update(str(ni))
    window.read(timeout=1)
    # if event == sg.WIN_CLOSED:
        # break
    # window['-TEXT-'].update('My new text value')
