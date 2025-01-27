#include<iostream>

using namespace std;

int main(){
    int x, i, j;
    cin >> x;
    i = 0;
    while(i < x){
        j = 0;
        while(j <= i){
            if(j % 2 == 0){
                cout << "***";
            }
            else if(j % 3 == 0){
                cout << "**";
            }
            else{
                cout << "*";
            }
            j = j + 1;
        }
        cout << endl;
        i = i + 1;
        int a = 32;
        continue;
    }
    while(1 == 1){
        break;
    }
    cout<<"___________________"<<endl;
    int e = 1e5;
    int a, khar3[e];
    float b = 1, c;
    cout << "*+-/%=!;,{}()[]<>";
    a = 1;
    a = b = 1.0;
    a = b = c = 1e8;
    a = 1.0e8;
    a = 1e+8;
    a = 1.0e+8;
    a = 1e-1;
    a = 1.0e-1;
    cout << "________ int ___________" << endl;
    return 0;
}