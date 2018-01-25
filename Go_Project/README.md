# yueqin_urop

Useful links:

Alphago zero Nature paper: https://www.nature.com/articles/nature24270

Alphago zero cheat sheet: https://medium.com/applied-data-science/alphago-zero-explained-in-one-diagram-365f5abf67e0

*New*:   Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm: https://arxiv.org/abs/1712.01815


Tutorials on convolutional neural networks:

https://www.youtube.com/watch?v=FmpDIaiMIeA

https://www.youtube.com/watch?v=HMcx-zY8JSg


Reinforcement learning lectures:

Lecture 1:      https://www.youtube.com/watch?v=2pWv7GOvuf0

Lecture 10 (with visible slides):     https://www.youtube.com/watch?v=N1LKLc6ufGY

Lecture 2:      https://www.youtube.com/watch?v=lfHX2hHRMVQ

Lecture 3:      https://www.youtube.com/watch?v=Nd1-UUMVfz4

Lecture 4:      https://www.youtube.com/watch?v=PnHCvfgC_ZA

Lecture 5:      https://www.youtube.com/watch?v=0g4j2k_Ggc4

Lecture 6:      https://www.youtube.com/watch?v=UoPei5o4fps&list=PLwQyV9I_3POuVsyB3hCyl3Iieb1oWVfPP&index=6

Lecture 7:      https://www.youtube.com/watch?v=KHZVXao4qXs&list=PLwQyV9I_3POuVsyB3hCyl3Iieb1oWVfPP&index=7

Lecture 8:      https://www.youtube.com/watch?v=ItMutbeOHtc&index=8&list=PLwQyV9I_3POuVsyB3hCyl3Iieb1oWVfPP

Lecture 9:      https://www.youtube.com/watch?v=sGuiWX07sKw&index=9&list=PLwQyV9I_3POuVsyB3hCyl3Iieb1oWVfPP


Data format:

Use numpy arrays to represent board position and probability vector:

    Format for arrays:
    N = board size

    (a) Board position: 
        Size N * N, row majorized, i.e. Index = row * N + column, where rows start from the top (row 0) and columns start from the left (column 0).
        This means that the (1, 1) point (top left corner) is index 0, (1, N) point (top right corner) is index N - 1, 
        and the (N, N) point (bottom right corner) is the last index

        1: Black
        -1: White
        0: Empty intersection

    (b) Probability vector for move selection:
        Array must have non-negative entries and sum to 1.
        Size N*N + 1, first N * N indices represent same positions as the board position vector in (a), last index to represent pass move

Using tensorboard:

Before each training session, move away existing files in the log folder. After training, type the following:

    tensorboard --logdir=path

where path is the location of your log folder without quotes.

Type localhost:6006 in your web-browser to see the output.


TODO:

Yueqin:

(i)    Add mean-squared error loss (scaled by 0.01) of value-head of the network to the current (cross-entropy) loss. 

(ii)    Learn tensorboard (https://www.tensorflow.org/get_started/summaries_and_tensorboard) and use it to plot the graphs for total loss, cross-entropy loss (policy-head) and MSE loss (value-head) over time.
        Also plot the accuracy of the policy output and value output (implement code for this) using tensorboard.

(iii)   Record the typical mistakes the neural network makes in different stages of the game (for both policy and value evaluations).

Jiankun:

(i)    Upload javascript code in a separate folder.

(ii)    Watch CNN tutorials and reinforcement learning lectures 1 and 10; learn tensorboard.