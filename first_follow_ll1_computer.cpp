#include<bits/stdc++.h>
using namespace std;

int n;

unordered_map<string, int> ind;

vector<string> symbol;

vector<vector<int>> g, back_edges;

vector<set<int>> first, follow;

vector<bool> terminal, in_path, mark;

vector<int> par;

vector<vector<vector<int>>> productions;

void unite(set<int> &set1, set<int> &set2){
    for(auto e: set2)
        set1.insert(e);
    return;
}

void dfs_first(int u, int prv){
    par[u] = prv;
    mark[u] = in_path[u] = true;
    if(terminal[u])
        first[u].insert(u);
    for(auto v: g[u])
        if(in_path[v])
            back_edges[v].push_back(u);
        else{
            if(!mark[v])
                dfs_first(v, u);
            unite(first[u], first[v]);
        }
    in_path[u] = false;
    return;
}

void dfs_back_edge(int u){
    mark[u] = true;
    for(auto e: back_edges[u]){
        int child = e;
        while(child != u){
            unite(first[child], first[u]);
            child = par[child];
        }
    }
    for(auto v: g[u])
        if(!mark[v])
            dfs_back_edge(v);
    return;
}

int main(){
    cout << "enter the directory of the grammer file:" << '\n';
    string dir;
    cin >> dir;
    if(dir.back() == '/' || dir.back() == '\\')
        dir.pop_back();
    ifstream file(dir + "/grammer.txt");
    int cnt = 0;
    while(cnt != 2){
        string s = "~";
        file >> s;
        if(s[0] == '~'){
            ++cnt;
            continue;
        }
        symbol.push_back(s);
        ind[s] = n;
        if(!cnt)
            terminal.push_back(false);
        else
            terminal.push_back(true);
        ++n;
    }
    /// /////////
    productions.assign(n, {});
    g.assign(n, {}), back_edges.assign(n, {});
    first.assign(n, {}), follow.assign(n, {});
    in_path.assign(n, false), mark.assign(n, false);
    back_edges.assign(n, {}), par.assign(n, -1);
    /// /////////
    while(true){
        string sym;
        file >> sym;
        cout << "- " << sym << '\n';
        if(sym == "0")
            break;
        int i = ind[sym];
        while(true){
            string pr, token = "";
            file >> pr;
            cout << " - " << pr << '\n';
            productions[i].push_back({});
            if(pr[0] == '~')
                break;
            int cnt = 0;
            cout << "  => ";
            for(int j = 0; j < pr.size(); ++j){
                cout << pr[j];
                if(pr[j] == '\''){
                    int k = ind[token];
                    if(!cnt)
                        g[i].push_back(k);
                    ++cnt;
                    productions[i].back().push_back(k), token = "";
                }
                else
                    token += pr[j];
            }
            cout << '\n';
        }
    }
    file.close();
    /// ///////
    for(int i = 0; i < n; ++i){
        cout << symbol[i] << ":\n\t";
        for(int e: g[i])
            cout << symbol[e] << " ";
        cout << '\n';
    }
    /// //////
    for(int i = 0; i < n; ++i)
        if(!mark[i])
            dfs_first(i, i);
    for(int i = 0; i < n; ++i)
        mark[i] = false;
    for(int i = 0; i < n; ++i)
        if(!mark[i])
            dfs_back_edge(i);
    /// //////
    ofstream first_follow(dir + "/first_follow.txt");
    cout << "First:\n-----------------\n";
    for(int i = 0; i < n; ++i){
        first_follow << symbol[i] << " ";
        cout << "First(" << symbol[i] << ")=\n\t{";
        for(auto e: first[i]){
            first_follow << e << " ";
            cout << symbol[e] << ", ";
        }
        cout << "\b\b}\n";
    }
    first_follow.close();
    return 0;
}
