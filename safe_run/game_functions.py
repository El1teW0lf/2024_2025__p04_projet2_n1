from child import send_message
import data

def get_door_status():
    if data.state["closed"] == False:
        return "0"
    else:
        return "1"
def door_close():
    status = get_door_status()
    if status == "1":
        send_message("/door/close", "Door is already closed")
    else:
        send_message("/door/close", "Close the door")
def door_open():
    status = get_door_status()
    if status == "0":
        send_message("/door/open", "Door is already open")
    else:
        send_message("/door/open", "Open the door")

def get_blinds_status(blind):

    if data.state["blinds"][f"{blind}_closed"] == False:
        return "0"
    else:
        return "1"
    
    

def blinds_close(blind):
    status = get_blinds_status(blind)
    if status == "1":
        send_message(f"/blinds/close/{blind}", f"{blind} is already closed")
    else:
        send_message(f"/blinds/close/{blind}", f"Close {blind}")

def blinds_open(blind):
    status = get_blinds_status(blind)
    if status == "0":
        send_message(f"/blinds/open/{blind}", f"{blind} is already open")
    else:
        send_message(f"/blinds/open/{blind}", f"Open {blind}")
