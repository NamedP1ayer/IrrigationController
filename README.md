# Irrigation Controller
## What does it do?
This is a slack bot which can communicate to the IrrigationServer program which controlls relays to make an irrigation system water.  

The point of the slack bot integration is to:
* Allow direct control of the irrigation remotely 
* Read information provided by other slack bots to create an automated, aware and scheduled.  The bots currently planned are:
  * Google calander bot to do scheduling (recurring events on a calander app are easy for people to visualise and setup)
  * Forecast a weather bot to make sure we don't water while its raining (it looks bad)

## What should it do that it doesn't?
At the moment it doesnt have any of the AAS features.

## What do I need?
* python3 with pip setup
* Something running IrrigationServer
* A SLACK_BOT_TOKEN and BOT_ID as described [here](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html)
   * I [jam](https://coreos.com/os/docs/latest/using-environment-variables-in-systemd-units.html) these into my [system-d](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/) environment.
* pip3 install SlackClient

## Setup using systemd
sudo systemctl restart IrrigationController.service

## How do I contribute?
Your kidding right?
