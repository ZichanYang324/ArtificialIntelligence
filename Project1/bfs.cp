#include <iostream>
#include <cstring>
#include <stack>
#include <queue>

#define MAXSTATE 9999999
#define HASHSIZE 9999999

using namespace std;

typedef int State[9];

static State st[MAXSTATE], goal;
static int dist[MAXSTATE], p[MAXSTATE];
static queue<int> states;

static const int dx[] = {-1, 1, 0, 0};
static const int dy[] = {0, 0, -1, 1};

static int head[HASHSIZE], next_pos[MAXSTATE];

static void init_lookup_table() {
    memset(head, 0, sizeof(head));//initial head to all zeros
}

static int hash_state(State& s) { //avoid repeating
    int v = 0;

    for (int i = 0; i < 9; ++i) {
        v = v * 10 + s[i];
    }

    return v % HASHSIZE;
}

static int try_to_insert(int s) {
    int h = hash_state(st[s]);
    int u = head[h];
    while (u) {
        if (memcmp(st[u], st[s], sizeof(st[s])) == 0) {
            return 0;
        }
        u = next_pos[u];
    }
    next_pos[s] = head[h];
    head[h] = s;

    return 1;
}

static int bfs() {
    init_lookup_table();//initial head to all zeros

    int cnt = 1;//step counting
    states.push(cnt);
    while (!states.empty()) {
        int index = states.front();//output the first one of queue
        states.pop();
        State &s = st[index];//record the current state

        if (memcmp(s, goal, sizeof(s)) == 0) {//if  s and goal are equal,return the count
            return index;
        }

        int z;
        for (z = 0; z < 9; ++z) {//find the location of 0 in list
            if (s[z] == 0) {
                break;
            }
        }

        int x = z / 3, y = z % 3;//x is the row of 0, y is column of 0
        for (int d = 0; d < 4; ++d) {//traversal every location around the 0
            int newX = x + dx[d];
            int newY = y + dy[d];
            if (newX >= 0 && newX < 3 && newY >= 0 && newY < 3) {
                int newZ = newX * 3 + newY;   //convert 2 dimensional  array into 1 dimensional  array 

                State &t = st[cnt + 1];   //define next step state
                memcpy(&t, &s, sizeof(s));  //t=s
                //moving the blocks
                t[newZ] = s[z];
                t[z] = s[newZ];

                if (try_to_insert(cnt + 1) == 1) { //put current state into hashmap
                    ++cnt;  
                    states.push(cnt);
                    p[cnt] = index;
                    dist[cnt] = dist[index] + 1;
                }
            }
        }
    }

    return 0;
}

static void print_board(State &s) {
    for (int i = 0; i < 9; ++i) {
        if (i % 3 == 0 && i > 0) {
            cout << endl;
        }
        cout << s[i] << " ";
    }
    cout << endl;
}

static void print_paths(int start, int end) {
    int count = 1;
    stack<int> stack;

    while (start != end) {
        stack.push(end);
        end = p[end];
    }
    while (!stack.empty()) {
        int i = stack.top();
        stack.pop();
        cout << "Step " << count++ << " : " << endl;
        print_board(st[i]);
    }
}

int main() {
    int lenOfslide;
    cout<<"This is bfs algorithm"<<endl;
    cout<<"Input length of slideblocking here:(the maximum number is 3)"<<endl;
    cin>>lenOfslide;
    while(lenOfslide!=3){
        cout<<"Length of slideblocking fix at 3,please input 3 here:"<<endl;
        cin>>lenOfslide;
    }
    cout<<"Input the start state here:"<<endl;
    for (int i = 0; i < 9; ++i) {
        scanf("%d", &st[1][i]);
    }
    for(int i=0;i<9;i++){
        goal[i] = i;
    }
//    goal[8] = 0;
//    for (int i = 0; i < 9; ++i) {
//        scanf("%d", &goal[i]);
//    }
    cout << "\nStart: " << endl;
    print_board(st[1]);
    cout << "\nGoal:" << endl;
    print_board(goal);
    cout << endl;

    int ans = bfs();
    if (ans > 0) {
        printf("Total paths: %d\n\n", dist[ans]);
        print_paths(1, ans);
    } else {
        cout << "No Solution!" << endl;
    }

    return 0;
}
