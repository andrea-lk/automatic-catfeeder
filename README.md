# Automatic Cat Feeder

This project is an automatic cat feeder that uses MQTT for communication and a graphical user interface (GUI) built with `customtkinter`. The feeder allows you to feed your cat manually or set a feeding schedule.

## Table of Contents
- [Features](#features)
- [Possible Challenges](#possible-challenges)
- [Installation](#installation)
- [Usage](#usage)
- [Code Overview](#code-overview)
- [Organization](#organization)
- [License](#license)

## Features
- **Manual Feeding**: Feed your cat instantly with a click of a button.
- **Scheduled Feeding**: Set a schedule to feed your cat multiple times a day.
- **MQTT Integration**: Utilizes MQTT protocol for reliable communication with the feeder hardware.


## Possible Challenges 
Animal Behavior: Other animals such as racoons might try to tamper with the feeder.

Calibration: Calibrating the dispenser to ensure accurate portions. 

## Installation
To set up this project locally, follow these steps:

1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-username/automatic-cat-feeder.git
   cd automatic-cat-feeder
   
   
2. **Install dependencies**:
   ```sh
   pip install customtkinter paho-mqtt
3. **Running the GUI**:
   To run the graphical user interface, execute the following command:
   ```sh
   python GUI.py

## Code Overview

### GUI.py

This file contains the code for the graphical user interface using `customtkinter`.

* **MQTT Setup**: Connects to the MQTT server and sets up callbacks.
* **Feeding Functionality**: Defines functions for feeding the cat and setting a feeding schedule.
* **GUI Components**: Creates buttons and labels for user interaction.




## Organization
The src contians all code created for the project. 

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
