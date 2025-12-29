# Guide

## First start

- Create virtual environment `python3 -m venv venv` (venv is the name of your choice)
- Activate virtual environment `source venv/bin/activate`
- Install requirements `pip install -r requirements.txt`

## How to use

### Send - Receive model with menu

- Run `python3 receiver.py`
- Run `python3 sender.py`
- Use menu in sender log to choose messages.

### Can bus simulator

- Run `python3 car_node.py CAR_A`
- Run `python3 car_node.py CAR_B`
- ...
- All cars will communicate with each other in the same network. 
