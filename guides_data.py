# guides_data.py
# Single source of truth for device repair information.
# To add a device, copy an existing entry and change the values.

DEVICES = {
    "iphone 13": {
        "brand": "Apple",
        "name": "iPhone 13",
        "category": "Phone",
        "repair_score": 5,
        "diy_difficulty": "Hard",
        "issues": [
            {
                "problem": "Battery degradation",
                "symptoms": "Drains quickly, shuts off at 20% or with no warning.",
                "steps": [
                    "Go to Settings > Battery > Battery Health & Charging.",
                    "If Maximum Capacity is below 80%, a battery replacement is likely needed.",
                    "Buy a reputable replacement battery and power off the phone before opening it.",
                    "Remove the two pentalobe screws at the bottom, then use a suction cup and plastic pry tool to lift the screen.",
                    "Disconnect the battery connector before removing the old battery.",
                ],
                "safety": "Lithium batteries can swell or catch fire when damaged. Do not puncture or bend a swollen battery. Take it to a recycling drop-off.",
            },
            {
                "problem": "Cracked screen",
                "symptoms": "Visible cracks, touch not responding in parts of the screen.",
                "steps": [
                    "Confirm the display itself is damaged and not just the glass cover.",
                    "Buy a display assembly that matches the model exactly.",
                    "Heat the edges of the screen gently to soften the adhesive.",
                    "Transfer the front camera and sensor cable from the old screen if your replacement does not include them.",
                ],
                "safety": "Broken glass can cut you. Wear gloves and wrap the screen in tape while working.",
            },
            {
                "problem": "Charging port failure",
                "symptoms": "Phone charges only at certain angles or not at all.",
                "steps": [
                    "Inspect the port with a flashlight for lint or debris.",
                    "Clean it carefully with a wooden or plastic toothpick. Never use metal.",
                    "If cleaning does not help, replace the lightning port flex cable.",
                ],
                "safety": "Unplug the phone before cleaning the port.",
            },
        ],
    },
    "arduino uno": {
        "brand": "Arduino",
        "name": "Arduino Uno R3",
        "category": "Microcontroller",
        "repair_score": 10,
        "diy_difficulty": "Easy",
        "issues": [
            {
                "problem": "Fried ATmega328P chip",
                "symptoms": "Board no longer uploads sketches, power LED is on but the board does not respond.",
                "steps": [
                    "Check the power LED and make sure the board is powered from USB.",
                    "Try loading a simple Blink sketch in the Arduino IDE.",
                    "If it still fails, remove the chip with a chip puller or a small flat screwdriver.",
                    "Carefully insert a new ATmega328P chip, or use a Uno bootloader programmer.",
                ],
                "safety": "Disconnect power before swapping chips. Avoid touching exposed pins with static charge.",
            },
            {
                "problem": "Broken USB port connector",
                "symptoms": "Board is loose in the port or does not connect to the computer.",
                "steps": [
                    "Look for cracked solder joints around the USB connector.",
                    "Reflow the solder joints with a soldering iron.",
                    "If the connector is torn off, replace the USB-B connector.",
                ],
                "safety": "Use a soldering iron in a ventilated area and wash your hands after handling solder.",
            },
        ],
    },
}