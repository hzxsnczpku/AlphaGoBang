# AlphaGoBang - Implement AlphaZero in Gobang Game

MCTS and RL!



## CURRENT STAGE

(2017.11.2) It seems that AI understands open three. Red for BLACK and green for WHITE, numbers for pi (in percentage) and `--` for pi less than 1%.
![avatar](./docs/selfplay.png)
(2017.10.23) 1s /step (1 process) (200 simulations with depth 45), without network evaluation. Clear MCTS Tree every 100 round for memory reasons. 

(2017.10.21) Finish MCTS (hope so), with randomly choosen (p, v).

(2017.10.21) Speed test, single process: 13s / step (800 simulations with depth 40)


![avatar](./docs/implementation0/Slide4.jpg)

![avatar](./docs/implementation0/Slide6.jpg)
![avatar](./docs/implementation0/Slide7.jpg)
![avatar](./docs/implementation0/Slide8.jpg)


## Working

* Training and self-playing.
