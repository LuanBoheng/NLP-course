#include <iostream>


using namespace std;

int f(int x) {
    if (x % 1000 == 0)
        cout << x << endl;
    return f(x + 1);
}

int main() {
    f(0);
    return 0;
}
