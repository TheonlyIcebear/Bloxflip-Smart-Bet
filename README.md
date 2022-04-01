# Bloxflip Smart Bet
A program that uses real statistics to choose the best times to bet on BloxFlip's crash gamemode. https://bloxflip.com/crash. <br>
THIS DOES NOT PREDICT WHEN ITS GOING TO CRASH. Instead it just compares many games to see what the chances are of reaching a certain multiplier and if the chances are high enough it places the bet. <br>

# IMPORTANT
Sadly bloxflip has made the decision to block people from connecting to their websockets unless their on the website. I am not sure how I can work around this and if you know feel free to dm me on discord: Ice Bear#0167. <br>

But for now sadly this program does not work
# Probability vs Streak based
Probability based means that it checks it compares the probability of it being a certain multipler but streak based means it ignores the probabilities and just sees if a certain amount of the recent games have gone over a certain amount and if they have it places the bet. <br>
Based on some tests I've done Streak Based is better in the long term but Probability based is better in the short term because of it's ability to recognize and take each game's crash point into account unlike the streak based on that just looks at all the recent games together

# Configuration and set up
To edit the configuration simply go into the config.json file. 
- The multiplier is the point at which the program will auto bet at 
- The chance is the chance of winning the program will aim for when betting your multiplier (Probability based only)
- The bet amount is the amount of robux to bet each time
- Your authorization is the token used on bloxflip to place bets. To get your own auth go onto bloxflip press inspect element and go into the console. Then paste the following code
```
localStorage.getItem('_DO_NOT_SHARE_BLOXFLIP_TOKEN')
```
 This will print your auth token to the console. Copy it without the quotes then put it into the config.json file
# Usage
To run the program make sure you have python installed and also pip. If you don't install python here https://www.python.org/downloads/. <br>
Pip should be preinstalled but if it isn't go to  https://pip.pypa.io/en/stable/installation/ <br>
Once you have done these two things either run installer.bat or open cmd CD to the directory and type the following command
```
pip install -r requirements.txt
```
Or you could always just upload the files to replit (https://replit.com/) and run it there. If you run into any problems for every package inside requirements.txt do:
```
pip install "NameOfPackage"
```
# Supporting me
Consider donating please as I make all my tools free https://www.roblox.com/game-pass/20395764/Donate#!/sales <br>
