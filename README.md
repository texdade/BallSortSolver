# Ball Sort Puzzle Solver
A simple solver for the Ball Sort Puzzle game application. Ball Sort Puzzle is a game where you have n vials filled with balls (usually 4) of n-2 different colors. 2 vials are empty. The goal of each puzzle is to move the balls so that each vials only contains balls of the same color. There are only two rules: a vial cannot contains more than 4 balls (can be 5, depending on puzzle) and a ball can only be moved to an empty vial or a vial whose uppermost ball is of the same color.

## Why?
I like the game and I have been looking for a simple project like this for a while now. When the idea came to me, I jumped right in.

## How?
The solver works as a recursive backtracking problem. For each "board" state, the possible legal moves are detected. For each move we then change the board accordingly and check whether the same board has already been encountered before (by hashing it and checking the hash against a set). If the board is in the set, we stop, because we were already in this situation before and it brought to a blocking board (a board with no possible moves). If the board isn't in the set, we add it and we continue down that path.
