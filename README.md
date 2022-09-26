# Bloxflip Smart Bet 🧠
**Join the discord and create a ticket if you wan't help with a bug**: https://discord.gg/f6mqzCCa <br>
**You can message me at**: Ice Bear#0167

A program that uses strategies and probability maths to choose the best times to bet on BloxFlip's crash gamemode https://bloxflip.com/a/IceBear. <br>
**THIS DOES NOT PREDICT 100% WHEN ITS GOING TO CRASH**: <br>
Instead either it uses a betting strategy or compares the previous crash games to see if it'd be a good idea to bet or to find a good multiplier  <br>

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

Setup tutorial by SteelyXs#1316: <br>
[![Video](http://img.youtube.com/vi/9o7_NDLlyfE/0.jpg)](http://www.youtube.com/watch?v=9o7_NDLlyfE "| TUTORIAL | How to install Martingale (Bloxflip Smart Bet)")
# Martingale vs StreakBased
- The Martingale strategy is based on the fact that every time you lose the chance of you winning increases the next game. So when you lose if you just increase your bet amount by 2 or more the chances of you making profit the next game is higher and the more games you lose the higher chance you'll eventually end up with more than what you started up with. <br> <br>

- The StreakBased strategy is similiar to the Martingale strategy in the sense that the games come in streaks of winning and losing because if a bunch of games end up crashing at low numbers then theirs a high chance the next group of games will chrash at higher numbers. So to get a good prediction of wether the next game is going to win or not you can look at the previous few games and see wether they've been winning or not. <br> <br>

Based on my testing I can conclude that Martingale is more stable and **more profitable** then StreakBased
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
You can also join the discord and create a ticket for real time support. https://discord.gg/b3g5UszgAs
# Supporting me 🤲
Consider donating please as I make all my tools free 
Roblox Gamepass: https://www.roblox.com/game-pass/20395764/Donate#!/sales <br>
Btc Address: bc1qq8k7h002dlkwxxy35xpw8z2amjpk9nquajvtqw <br>
Monero Adress: 452ogMtEPc9T2sLQHVy3NcARkmTADVbLiY1hyoBp6xhfASdR2R7MPuRjZD4XSe8kHiKjZ1ozVGQqPEVqjjFt2mLcDmGfwXu <br>
