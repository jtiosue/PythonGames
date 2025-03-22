#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>


const int WIN[8][3][2] = {
    {{0, 0}, {0, 1}, {0, 2}}, 
    {{1, 0}, {1, 1}, {1, 2}},
    {{2, 0}, {2, 1}, {2, 2}}, 
    {{0, 0}, {1, 0}, {2, 0}},
    {{0, 1}, {1, 1}, {2, 1}}, 
    {{0, 2}, {1, 2}, {2, 2}},
    {{0, 0}, {1, 1}, {2, 2}}, 
    {{2, 0}, {1, 1}, {0, 2}}
};


typedef int Board[3][3];
typedef int ValidMoves[9][2];


void initialize_board(Board board) {
    for(int r=0; r<3; r++) {
        for (int c=0; c<3; c++) {
            board[r][c] = 0;
        }
    }
}

void Board_print(Board board) {
    char a[3];
    for (int r=0; r<=2; r++) {
        for(int i=0; i<3; i++) {
            switch(board[r][i]) {
            case 0:
                a[i] = ' ';
                break;
            case 1:
                a[i] = 'X';
                break;
            case 2:
                a[i] = 'O';
                break;
            }
        }

        printf("%c | %c | %c \n", a[0], a[1], a[2]);
        if(r < 2)
            printf("-----------\n");
    }
}

inline bool Board_is_valid(Board board, int row, int col) {
    if(row < 0 || row > 2 || col < 0 || col > 2) 
        return false;
    return board[row][col] == 0;
}

void Board_all_moves(Board board, ValidMoves valid_moves) {
    int index = 0;
    for(int r=0; r<=2; r++) {
        for (int c=0; c<=2; c++) {
            if(Board_is_valid(board, r, c)) {
                valid_moves[index][0] = r;
                valid_moves[index][1] = c;
                index++;
            }
        }
    }
    if(index < 9) {
        valid_moves[index][0] = -1;
    }
}

bool all(Board board, int win, int player) {
    // return true if all positions in WIN[win]
    // are occupied by the player
    for(int j=0; j<3; j++) {
        if(board[WIN[win][j][0]][WIN[win][j][1]] != player)
            return false;
    }
    return true;
}


int Board_state(Board board) {
    for(int win=0; win<8; win++) {
        if(all(board, win, 1)) {
            return 1;
        } else if(all(board, win, 2)) {
            return 2;
        }
    }
    for(int r=0; r<3; r++) {
        for(int c=0; c<3; c++) {
            if(Board_is_valid(board, r, c))
                return 0;
        }
    }

    return 3;
}


typedef struct Status {
    int row, col, score, count;
} Status;

Status pick_next(Board board, int player, int count) {
    Status s = {0};
    s.count = count;
    int other = (player == 2) ? 1 : 2;
    int state = Board_state(board);
    if(state == player) {
        s.score = 10;
        return s;
    } else if (state == other) {
        s.score = -10;
        return s;
    }
    count++;

    int row, col;

    Status best = {-1};
    ValidMoves valid_moves; 
    Board_all_moves(board, valid_moves);
    for(int move=0; move<9; move++) {
        if(valid_moves[move][0] == -1) {
            break;
        }
        row = valid_moves[move][0]; col = valid_moves[move][1];
        board[row][col] = player;
        s = pick_next(board, other, count);
        board[row][col] = 0;
        s.score *= -1;
        if(best.row == -1 || s.score > best.score || (s.score == best.score && ((s.score >= 0 && s.count < best.count) || (s.score < 0 && s.count > best.count)))) {
            best.row = row; best.col = col; best.score = s.score; best.count = s.count;
        }
    }

    if(best.row == -1) {
        best.row = -1; best.col = -1; best.score = 0; best.count = count;
    }
    return best;
}


void play(bool first) {
    Board board;
    initialize_board(board);
    int i = 0;
    if(!first) {
        // board[0][0] = 1;
        i--;
    }

    int r, c;

    int first_player = first ? 1 : 2;
    int other_player = first_player == 2 ? 1 : 2;

    while(Board_state(board) == 0) {
        i++;
        Board_print(board);
        if(i % 2) {
            printf("Row, col:\n");
            scanf("%d,%d", &r, &c);
            if(Board_is_valid(board, r, c)) {
                board[r][c] = first_player;
            } else {
                printf("Invalid move\n");
                i--;
            }
        } else {
            Status status = pick_next(board, other_player, 0);
            board[status.row][status.col] = other_player;
        }
    }

    Board_print(board);
    switch(Board_state(board)) {
    case 1:
        printf("Player X wins\n");
        break;
    case 2:
        printf("Player O wins\n");
        break;
    case 3:
        printf("It's a tie\n");
        break;
    }
}


int main() {
    int first;
    printf("Play first?\n");
    scanf("%d", &first);
    play(first);
    return 0;
}