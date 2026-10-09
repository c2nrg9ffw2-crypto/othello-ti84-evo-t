# Othello for the TI-84 Evo-T

**Othello** (also called **Reversi**) for the **TI-84 Evo-T** graphing calculator, written in Python.

> **Made with AI:** this game and this README were created with the help of AI (Claude by Anthropic).
> Everything was tested on a real TI-84 Evo-T.

## Features

- **1 player** against the calculator, with 3 levels: **Easy**, **Medium** and **Hard**
- **2 players** on one calculator
- **Small dots** show every square where you may play
- Disc counts for black and white on the right side
- Wins and draws stay saved after you quit

## Rules

- **Black** starts. Players take turns putting a disc on the board.
- Your disc must **trap** at least one of the other colour's discs in a straight line
  (across, up and down, or diagonal) between your new disc and another disc of yours.
- All trapped discs **flip** to your colour.
- If you can't make a move, you **pass**.
- When nobody can move, the player with **more discs** wins.

**Tip:** the **corners** are the best squares, because a disc there can never be flipped.

## What you need

- A **TI-84 Evo-T** calculator
- A USB cable to connect it to your computer
- **Google Chrome** or **Microsoft Edge** (Safari and Firefox do not work with the TI tool)
- The file [`othello.py`](othello.py) from this repo

## Setup

1. Download [`othello.py`](othello.py) to your computer.
2. Connect the calculator to your computer with the USB cable.
   Leave the calculator on the **home screen**.
3. Open **https://connectevo.ti.com** in **Chrome** or **Edge**.
4. Connect to your calculator in the page and allow access when the browser asks.
5. Drag `othello.py` onto the page to send it to the calculator.
6. **Choose RAM** to play right away.
   The Python app on the Evo-T only shows files that are in RAM.
   (Want to keep the game safe? See [Don't lose the game](#dont-lose-the-game).)

> **Already sent it to Archive?** On the **home screen** (not in the Python app) press **2nd → mem → Mem Management**,
> find **OTHELLO** and press **enter**. The `*` in front of the name disappears, which means
> it is now in RAM.

## Start the game

1. Open the **Python** app on the calculator.
2. Choose **OTHELLO** and run it.
3. Choose **1 player** or **2 players** with ▲ ▼ and press **enter**.
4. For 1 player, choose **Easy**, **Medium** or **Hard** (or **clear** to go back).

## Keys

| Key | What it does |
|---|---|
| ◀ ▶ ▲ ▼ | Move the yellow frame |
| enter | Put your disc there (only where a dot is) |
| clear | Quit |

## Levels

In 1 player mode you are **black** and the calculator is **white**.

| Level | How the calculator plays |
|---|---|
| Easy | Looks only at its own move, and sometimes plays a random move |
| Medium | Looks 2 moves ahead |
| Hard | Looks 4 moves ahead (thinks up to about half a second) |

The calculator knows that corners are good and that the squares next to corners are risky.

## Don't lose the game

The Evo-T **deletes RAM** when it stays turned off for a while.
A normal turn-off is fine, but after some time the game is gone.

**Best way:**

1. Keep the game in **Archive**. Archive is never deleted.
2. Go to the **home screen**. If you are in the Python app, leave it with **2nd → quit**
   (quit is above the **mode** key). In the Python app, **2nd → mem** does nothing.
3. Press **2nd → mem** (mem is above the **+** key) and choose **2: Mem Management**.
4. Choose the list with Python programs (or **All**).
5. Find **OTHELLO** and press **enter**. The `*` disappears, which means the game is now in RAM.
6. Open the **Python** app and play.

Programs can't move files between Archive and RAM by themselves, so this step can't be automatic.
The wins list **OTHEL** is in RAM too, so it can be deleted the same way.

## Wins

Wins for black and white, and draws, are saved in a calculator list called **OTHEL**,
so they stay after you quit. The start screen shows them.

- To reset them, delete the list **OTHEL** in **2nd → mem → Mem Management** (on the home screen).
- A calculator reset (RAM clear) also resets them.

## Good to know

- Keep `othello.py` on your computer too, so you can always send it again.
- Made for the TI-84 Evo-T. Other TI-84 models are not tested.
