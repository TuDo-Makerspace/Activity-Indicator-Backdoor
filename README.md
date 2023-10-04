# Activity Indicator Backdoor

The following repository contains the code for the Activity Indicator backdoor bot.
The backdoor bot allows trusted members of the Makerspace to manually set the activity
status of the Activity Indicator via the backdoor chatbot.

The backdoor bot is intended to be used in cases where the makerspace (or more specifically, 
the university) is suffering from internet outages, or other types of failurs. Trusted members
have access to a group chat in which the backdoor bot is accessible.

The use of the backdoor should be limited to technical difficulities and the occasional mishaps
where the activity indicator has been forgotten to be manually switched. It shall NOT replace
the activity indicator itself!

## Setting up the backdoor

For obvious reasons, the backdoor must be hosted on an external server rather than the indicator
itself (ex. a VPS). To configure it, ensure all required fields in the [`acitvity-indicator-backdoor.ini`](acitvity-indicator-backdoor.ini) configuration file are filled out. To then set-up the server,
simply execute the [`setup.sh`](setup.sh) script with the `install` argument.

```
# ./setup.sh install
```

## Usage

To manually set the activity status of the indicator, use send the `/open` or `/close` commands
in the appropriate group chat for the backdoor bot.