#include<bits/stdc++.h>
using namespace std;

int n;

map<string, int> ind;

set<string> Str;

vector<vector<int>> g, back_edges;

vector<set<int>> first, follow;

vector<bool> terminal, in_path, mark;

vector<int> par;

vector< pair<string, vector<string> > > G;

void unite(int u, int v){
    for(auto e: first[v])
        first[u].insert(e);
    return;
}

void dfs_first(int u, int prv){
    par[u] = prv;
    mark[u] = in_path[u] = true;
    if(terminal[u])
        first[u].insert(u);
    for(auto v: g[u])
        if(in_path[v])
            back_edge[v].push_back(u);
        else{
            if(!mark[v])
                dfs(v, u);
            unite(u, v);
        }
    in_path[u] = false;
    return;
}

void dfs_back_edge(int u){
    mark[u] = true;
    for(auto e: back_edges[u]){
        int child = e;
        while(child != u){
            unite(child, u);
            child = par[child];
        }
    }
    for(auto v: g[u])
        if(!mark[v])
            dfs_back_edge(v);
    return;
}

int main(){
    cout << "enter the directory of the grammer file" << '\n';
    string dir, line;
    cin >> dir;
    vector<string> file;
    while(true){
        getline(dir, line);
        if(line[0] == '~')
            break;
        file.push_back(line);
    }
    for(int i = 0; i < file.size(); ++i){
        str = ;
    }

    int src = ind["Start"];
    dfs_first(src, src);
    for(int i = 0; i < n; ++i)
        mark[i] = false;
    dfs_back_edge(src);

    return 0;
}
