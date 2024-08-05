import customtkinter as ctk
import paho.mqtt.client as mqtt
import time
import threading

# MQTT configuration
USERNAME = "hextech-andrea"
PASSWORD = "andrea"
commands = "hextech/hextech-andrea/commands"
unacked_publish = set()

OPEN_STEPS = -400
CLOSE_STEPS = 400

def setup_mqtt():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Assign callbacks
    mqttc.on_publish = on_publish
    mqttc.on_connect = on_connect

    # Set user data (this stores unacknowledged message ids)
    mqttc.user_data_set(unacked_publish)

    # Set username and password for MQTT connection
    mqttc.username_pw_set(username=USERNAME, password=PASSWORD)

    # Connect to the MQTT server
    mqttc.connect("mqtt.hextronics.cloud", 1883)

    # Start the MQTT network loop
    mqttc.loop_start()

    return mqttc

def on_publish(client, userdata, mid, reason_code, properties=None):
    # Removes the message ID from the set of unacknowledged messages
    userdata.remove(mid)
    print(f"Published message ID: {mid}")

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with result code {reason_code}")

def move_steps(mqttc, steps):
    # Create the payload for the MQTT message to move the motor
    steps_payload = f"stepper.00_speed_400|stepper.00_move_{steps}_1"
    # Publish the payload and wait for it to be acknowledged
    publish_and_wait(mqttc, steps_payload)

def publish_and_wait(mqttc, payload):
    msg_info = mqttc.publish(commands, payload, 0, False)
    unacked_publish.add(msg_info.mid)

    # Wait for the message to be acknowledged
    while len(unacked_publish):
        time.sleep(0.1)

    # Ensure the message is published
    msg_info.wait_for_publish()

def feed_cat():
    print("The dispensing disc is opened. Feeding in progress.")
    move_steps(mqttc, OPEN_STEPS)
    time.sleep(4)
    move_steps(mqttc, CLOSE_STEPS)

def set_feeding_schedule(times_per_day):
    print(f"Setting feeding schedule to {times_per_day} times per day.")
    interval = 86400 / times_per_day  # seconds in a day divided by times per day

    def schedule_feeding():
        while True:
            feed_cat()
            time.sleep(interval)

    threading.Thread(target=schedule_feeding, daemon=True).start()

def show_main_menu():
    for widget in window.winfo_children():
        widget.destroy()

    font = ctk.CTkFont(family="Microsoft Sans Serif", size=30)

    # Feed Cat Now button
    feed_button = ctk.CTkButton(window, text="Feed Cat Now", font=font, command=feed_cat)
    feed_button.pack(pady=20)

    # Set Feeding Schedule button
    schedule_button = ctk.CTkButton(window, text="Set Feeding Schedule", font=font, command=show_schedule_page)
    schedule_button.pack(pady=20)

def show_schedule_page():
    for widget in window.winfo_children():
        widget.destroy()

    font = ctk.CTkFont(family="Microsoft Sans Serif", size=30)

    label = ctk.CTkLabel(window, text="How many times per day do you want to feed your cat?", font=font)
    label.pack(pady=20)

    # Buttons for feeding schedule options
    for i in range(1, 5):
        button = ctk.CTkButton(window, text=str(i), font=font, command=lambda i=i: select_schedule(i))
        button.pack(pady=10)

    # Back button to return to the main menu
    back_button = ctk.CTkButton(window, text="Back", font=font, command=show_main_menu)
    back_button.pack(pady=20)

def select_schedule(times_per_day):
    set_feeding_schedule(times_per_day)
    show_main_menu()

def main():
    global window, mqttc

    # Set up MQTT connection
    mqttc = setup_mqtt()

    ctk.set_appearance_mode("system")  # Modes: "system" (default), "light", "dark"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

    window = ctk.CTk()
    window.title("Automatic Cat Feeder")
    window.geometry("800x600")

    show_main_menu()

    window.mainloop()

    # Disconnect MQTT when GUI is closed
    mqttc.disconnect()
    mqttc.loop_stop()

if __name__ == "__main__":
    main()
