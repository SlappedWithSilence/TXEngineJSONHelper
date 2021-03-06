import PySimpleGUI as sg

import WindowHelper
import requests

###### Globals #######
itemHelper = WindowHelper.ItemWindowHelper()  # The class that stores the data and functions necessary to operate the Item Window
text_box_size = (30, 2)
CONFIG_URL = "https://raw.githubusercontent.com/SlappedWithSilence/TXEngineJSONHelper/master/config.json"

remote_config_values = requests.get(CONFIG_URL).json()


def make_main_window():
    print("Making main window")
    layout = [[sg.Button('Items'), sg.Button('Rooms')],
              [sg.Button('Conversations'), sg.Button('Combats')]]
    return sg.Window('TXEngine JSON Editor', layout, finalize=True, resizable=True)  # Create the Window


def make_item_window(mode: int = 0, path: str = ''):
    print("Making item window")

    if mode == 1:
        itemHelper.load_manifest(path)

    sub_effect_col_left = sg.Column([[sg.Listbox(tooltip='Effects', values=itemHelper.get_effects_as_strings(0),
                                                 size=(30, 6), enable_events=True, key='-EFFECT_LIST-')]])
    sub_effect_col_right = sg.Column([[sg.Button("Edit", key='-EDIT_EFFECT-')],
                                      [sg.Button("Remove", key='-REMOVE_EFFECT-')]])

    left_col = sg.Column([[sg.Text('Current Item', justification='center')],
                          [sg.Text("Name"), sg.InputText(tooltip='Name', key='-ITEM_NAME-', size=text_box_size)],
                          [sg.Text("ID"), sg.InputText(tooltip='ID', key='-ITEM_ID-', size=text_box_size)],
                          [sg.Text("Description"),
                           sg.InputText(tooltip='Description', key='-ITEM_DESC-', size=text_box_size)],
                          [sg.Text("Max Stack"),
                           sg.InputText(tooltip='Max Stacks', key='-ITEM_MAX_STACK-', size=text_box_size)],
                          [sg.Text("Value"), sg.InputText(tooltip="Value", key='-ITEM_VALUE-', size=text_box_size)],
                          [sg.Text("Item Class"), sg.Combo(tooltip='Class Name', key='-CLASS_NAME_SELECTOR-',
                                                           values=remote_config_values['item_classes'])],
                          [sg.Text("Effects")],
                          [sub_effect_col_left, sub_effect_col_right],
                          [sg.Button("New Effect", key='-NEW_EFFECT-'), sg.Button("New Combat Effect", key='-NEW_COMBAT_EFFECT-')],
                          [sg.Button("Save")]])

    right_col = sg.Column([[sg.Text("All Items")],
                           [sg.Listbox(values=itemHelper.get_items_as_strings(), key="-ALL_ITEM_LIST-",
                                       select_mode='extended', size=(30, 30), enable_events=True)]])
    layout = [[left_col, right_col]]

    return sg.Window(title="Item Helper", layout=layout, finalize=True, resizable=True)


def make_effect_window(mode: str = 'effect_classes', effect: dict = None):
    layout = None

    if effect is None:
        layout = [[sg.Text('New Effect')],
                  [sg.InputCombo(tooltip='Class Name', values=remote_config_values[mode])],
                  [sg.Text('Properties')],
                  [sg.InputText(tooltip='Properties'), sg.Button('Save', key='-SAVE_EFFECT-')]]
    else:
        layout = [[sg.Text('View Effect')],
                  [sg.InputCombo(tooltip='Class Name', values=remote_config_values[mode], default_value=effect['className'])],
                  [sg.Text('Properties')],
                  [sg.InputText(tooltip='Properties', default_text=",".join("{0}".format(n) for n in effect['properties'])), sg.Button('Save', key='-SAVE_EFFECT-')]]

    return sg.Window(title="New Effect", layout=layout, finalize=True, resizable=True,)


print("Making windows")
main_window = make_main_window()
item_window, room_window, convo_window, combat_window = None, None, None, None
effect_window, action_window = None, None

print("Entering loop")
# Event Loop to process "events" and get the "values" of the inputs
while True:
    window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED:  # if user closes a window
        if window == item_window:  # if the user closes the item window
            item_window.close()
            item_window = None

            if effect_window is not None: effect_window.close(); effect_window = None  # Close the effect window if its open

        elif window == room_window:  # if the user closes the room window
            room_window = None
        elif window == convo_window:  # if the user closes the conversation window
            convo_window = None
        elif window == combat_window:  # if the user closes the combat window
            combat_window = None
        elif window == effect_window:
            effect_window.close()
            effect_window = None

        elif window == main_window:  # if the user closes the main window
            break  # terminate the program

    if event == 'Items':
        if item_window is None:
            item_window = make_item_window(1, 'items.json')
            # item_window = make_item_window()

    if event == 'Save':
        print("Saving item...")

        name = item_window.find_element('-ITEM_NAME-').get()
        item_id = int(item_window.find_element('-ITEM_ID-').get())
        desc = item_window.find_element('-ITEM_DESC-').get()
        max_stacks = int(item_window.find_element('-ITEM_MAX_STACK-').get())
        value = int(item_window.find_element('-ITEM_VALUE-').get())
        class_name = item_window.find_element('-CLASS_NAME_SELECTOR-').get()

        itemHelper.item_map[item_id] = WindowHelper.make_item(name, item_id, desc, class_name, [], value, max_stacks)
        item_window['-ALL_ITEM_LIST-'].update(itemHelper.get_items_as_strings())

    # Any time the user selects an item off the "All Items" list, update the left column's fields to have its properties
    if event == '-ALL_ITEM_LIST-':
        index = int(values['-ALL_ITEM_LIST-'][0][0])
        item_window.find_element('-ITEM_NAME-').update(value=itemHelper.item_map[index]['name'])
        item_window.find_element('-ITEM_ID-').update(itemHelper.item_map[index]['id'])
        item_window.find_element('-ITEM_DESC-').update(itemHelper.item_map[index]['description'])
        item_window.find_element('-ITEM_MAX_STACK-').update(itemHelper.item_map[index]['maxStacks'])
        item_window.find_element('-ITEM_VALUE-').update(itemHelper.item_map[index]['value'])
        item_window.find_element('-CLASS_NAME_SELECTOR-').update(itemHelper.item_map[index]['type'])
        item_window.find_element('-EFFECT_LIST-').update(values=itemHelper.get_effects_as_strings(index))

    # Whenever the user clicks the "New Effect" button, launch a window
    if event == '-NEW_EFFECT-':
        effect_window = make_effect_window()
    if event == '-EDIT_EFFECT-':
        try:
            item_index = int(values['-ALL_ITEM_LIST-'][0][0])
            effect_index = item_window['-EFFECT_LIST-'].get_indexes()[0]
            effect = itemHelper.item_map[item_index]['effects'][effect_index]
            effect_window = make_effect_window(effect=effect)
        except IndexError:
            pass

    # Whenever the user clicks the "Remove Effect" button, remove the corresponding effect in the "All Effects" list
    # and commits the change to the JSON manifest
    if event == '-REMOVE_EFFECT-':
        try:
            item_index = int(values['-ALL_ITEM_LIST-'][0][0])
            effect_index = item_window['-EFFECT_LIST-'].get_indexes()[0]
            itemHelper.item_map[item_index]['effects'].pop(effect_index)
            item_window.find_element('-EFFECT_LIST-').update(values=itemHelper.get_effects_as_strings(index))
        except IndexError:
            pass
window.close()
