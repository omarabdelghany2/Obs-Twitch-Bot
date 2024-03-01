import keyboard

def on_key_event(event):
    if event.event_type == keyboard.KEY_DOWN:
        if(event.name.lower() =='s'):
                print("S")
        elif(event.name.lower() =='r'):
                print("r")
        elif(event.name.lower() =='p'):
                print("p")               

keyboard.hook(on_key_event)
