#include<iostream>

using namespace std;

int main(){
    int x, i, j;
    cin >> x;
    i = 0;
    while(i < x){
        j = 0;
        while(j <= i){
            cout << "*";
            j = j + 1;
        }
        cout << "\n";
        i = i + 1;
    }
    while(true){
        break;
    }
    cout << "___________________\n";
    return 0;
}