# Bloxflip Smart Bet 🧠
**Join the discord and create a ticket if you wan't help with a bug**: https://discord.gg/3xh6ku7HxX <br>
**You can message me at**: Ice Bear#3333

A program that uses strategies and probability maths to choose the best times to bet on BloxFlip's crash gamemode <br>
**THIS IS NOT A PREDICTOR**: <br>
It's only a betting strategy, remember casinos **always have the house edge**<br>

# Configuration and set up ⚙
To edit the configuration simply go into the config.json file. 
- The multiplier is the point at which the program will auto bet at 
- The bet amount is the amount of robux to bet each time
- Games averaged is the amount of games the program will check (Streakbased only)
- Auto stop is the amount of Robux at which the program will stop betting.
- Auto restart means the program won't ask you to restart betting with your origanal amount when the new increased bet amount is more than your account's balance (Streakbased only)
- Your authorization is the token used on bloxflip to place bets. To get your own auth go onto bloxflip press inspect element and go into the console. Then paste the following code
```
localStorage.getItem('_DO_NOT_SHARE_BLOXFLIP_TOKEN')
```
 This will print your auth token to the console. Copy it without the quotes then put it into the config.json file


# Usage ⚠
To run the program make sure you have python installed and also pip. If you don't install python here https://www.python.org/downloads/. <br>
Pip should be preinstalled but if it isn't go to  https://pip.pypa.io/en/stable/installation/ <br>
Once you have done these two things either run installer.bat or open cmd CD to the directory and type the following command
```
pip install -r requirements.txt
```
# Errors ❌
If the program randomly closes with no message check for errors.txt inside the same folder as the python file. <br>
Then create a issue on this github by going to (https://github.com/TheonlyIcebear/Bloxflip-Smart-Bet/issues/new) <br>
Simply title the issue and put the text inside errors.txt
You can also join the discord and create a ticket for real time support. https://discord.gg/3xh6ku7HxX
