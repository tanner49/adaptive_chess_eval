# Adaptive Chess Engine
This chess engine and simple app evaluate a chess position, adaptive to the practical skill of the players.

## How to use it:
 - Make sure you have installed all packages in the requirments.txt file
 - Swamp the path to stockfish in line 3 of the main.py file out with the path to your local stockfish binary
 - Change the centi_detect (see below) to your desired setting.
 - Run main.py

## How does it work?
The calculation is quite simple. The core engine is stockfish. However, we also take an additional input, the "Centipawn perception" level. This is the **minimum difference in position** that a player could detect, on average, based on their skill. So at a Centipawn perception level of 100, the player cannot detect the difference in any move that less than blunders a pawn in one move. 

Based on this centipawn perception parameter, we then look at all moves that stockfish evaluates as within that level of the top move, and assume that they player is essentially choosing at random between them. We can then calculate the NEW evaluation for that position as the average evaluation (by stockfish) of all the moves that the player cannot detect difference betwen.

## What does this mean in practice?
- **Your eval can go UP after you move.** Essentially, the engine thinks you suck until you prove otherwise. If you manage to play the best move in a tense position, your evaluation will actually go up after you move (because the engine basically didn't think you would fine that move). This can be particullary jarring in the opening, when most players have at least of few moves of theory memorized.
- **It still doesn't think you're going to blunder.** In real games, amature players will randomly just hang a queen. Some advanced chess engines attempt to build this in, but it always feels weird and incorrect. I decided to just leave that out of the evaluation.
- **Engines still are better at end games.** This is still build on top of stockfish. And in endgames, stockfish knows that some random pawn move is a draw and another seemingly random pawn move (to us mortals) is +10. Because of this, the engine still evaluates some endgames like a computer when there are really tense queening situations.