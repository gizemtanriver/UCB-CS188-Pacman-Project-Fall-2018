# UCB-CS188-Pacman-Project-Fall-2018

Project 1 - Search Algorithms
https://inst.eecs.berkeley.edu/~cs188/fa18/project1.html

Project 2 - Multiagent Search
https://inst.eecs.berkeley.edu/~cs188/fa18/project2.html

Project 4 - Ghostbusters
https://inst.eecs.berkeley.edu/~cs188/fa18/project4.html


Running Search Algorithms:

Depth-First Search:
python pacman.py -l tinyMaze -p SearchAgent
python pacman.py -l mediumMaze -p SearchAgent
python pacman.py -l bigMaze -z .5 -p SearchAgent
python pacman.py -l openMaze -z .5 -p SearchAgent

Breadth-First Search :
python pacman.py -l tinyMaze -p SearchAgent -a fn=bfs
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l bigMaze -p SearchAgent -a fn=bfs
python pacman.py -l openMaze -p SearchAgent -a fn=bfs

Iterative Deepening Search:
python pacman.py -l tinyMaze -p SearchAgent -a fn=ids
python pacman.py -l mediumMaze -p SearchAgent -a fn=ids -z .5
python pacman.py -l bigMaze -p SearchAgent -a fn=ids -z .5
python pacman.py -l openMaze -p SearchAgent -a fn=ids -z .5

A* Search:
python pacman.py -l tinyMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
python pacman.py -l mediumMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
python pacman.py -l openMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

Heuristic Function:
python pacman.py -l tinyCorners -p AStarCornersAgent -z 0.5
python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5

Eating all the dots problem with A* with a null heuristic function:
python pacman.py -l testSearch -p AStarFoodSearchAgent
python pacman.py -l trickySearch -p AStarFoodSearchAgent
