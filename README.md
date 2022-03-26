# Bloxflip Smart Bet
A program that uses real statistics to choose the best times to bet on BloxFlip's crash gamemode. https://bloxflip.com/crash
# Configuration and set up
To edit the configuration simply go into the config.json file. 
- The multiplier is the point at which the program will auto bet at 
- The chance is the chance of winning the program will aim for when betting your multiplier
- The bet amount is the amount of robux to bet each time
- Your authorization is the token used on bloxflip to place bets. To get your own auth go onto bloxflip press inspect element and go into the console. Then paste the following code
```
localStorage.getItem('_DO_NOT_SHARE_BLOXFLIP_TOKEN')
```
 This will print your auth token to the console. Copy it without the quotes then put it into the config.json file
# Usage
To run the program make sure you have python installed and also pip. If you don't install python here https://www.python.org/downloads/. Pip should be preinstalled but if it isn't go to  https://pip.pypa.io/en/stable/installation/ 
Once you have done these two things either run installer.bat or open cmd CD to the directory and type the following command
```
pip install -r requirements.txt
```
