# Bloxflip Smart Bet
A program that uses real statistics to choose the best times to bet on BloxFlip's crash gamemode. https://bloxflip.com/crash. <br>
THIS DOES NOT PREDICT WHEN ITS GOING TO CRASH. Instead it just compares many games to see what the chances are of reaching a certain multiplier and if the chances are high enough it places the bet. <br>

# Configuration and set up
To edit the configuration simply go into the config.json file. 
- The multiplier is the point at which the program will auto bet at 
- The bet amount is the amount of robux to bet each time
- Games averaged is the amount of games the program will check
- Your authorization is the token used on bloxflip to place bets. To get your own auth go onto bloxflip press inspect element and go into the console. Then paste the following code
```
localStorage.getItem('_DO_NOT_SHARE_BLOXFLIP_TOKEN')
```
 This will print your auth token to the console. Copy it without the quotes then put it into the config.json file
# Martingale vs Streakbased
- The Martingale strategy is based on the fact that every time you lose the chance of you winning increases the next game. So when you lose if you just increase your bet amount by 2 or more the chances of you making profit the next game is higher and the more games you lose the higher chance you'll eventually end up with more than what you started up with. <br> <br>

- The StreakBased strategy is similiar to the Martingale strategy in the sense that the games come in streaks of winning and losing because if a bunch of games end up crashing at low numbers then theirs a high chance the next group of games will chrash at higher numbers. So to get a good prediction of wether the next game is going to win or not you can look at the previous few games and see wether they've been winning or not. <br> <br>

Based on my testing I can conclude that Martingale is more stable and **more profitable** then StreakBased
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
