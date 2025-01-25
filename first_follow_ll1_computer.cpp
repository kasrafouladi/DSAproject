#include<bits/stdc++.h>
using namespace std;

int n, nt, te;

map<string, int> ind;

map<vector<int>, vector<int>> p_table;

vector<string> symbol;

vector<vector<int>> g, g_last, back_edges;

vector<set<int>> first, last, follow;

vector<bool> terminal, in_path, mark;

vector<int> par;

vector<vector<vector<int>>> productions;

ifstream file;
ofstream first_follow, ll_1_pars, symbols, prd;

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

void dfs_last(int u, int prv){
    par[u] = prv;
    mark[u] = in_path[u] = true;
    if(u != ind["e"])
        last[u].insert(u);
    for(auto v: g_last[u])
        if(in_path[v])
            back_edges[v].push_back(u);
        else{
            if(!mark[v])
                dfs_last(v, u);
            unite(last[u], last[v]);
        }
    in_path[u] = false;
    return;
}

void dfs_back_edge_last(int u){
    mark[u] = true;
    for(auto e: back_edges[u]){
        int child = e;
        while(child != u){
            unite(last[child], last[u]);
            child = par[child];
        }
    }
    for(auto v: g_last[u])
        if(!mark[v])
            dfs_back_edge_last(v);
    return;
}

void enumerate_symbols(){
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
    nt = te = 0;
    for(int i = 0; i < n; ++i)
        if(terminal[i])
            ++te;
        else
            ++nt;
    return;
}

void initialize_vectors(){
    productions.assign(n, {}), last.assign(n, {});
    g.assign(n, {}), g_last.assign(n, {});
    first.assign(n, {}), follow.assign(n, {});
    in_path.assign(n, false), mark.assign(n, false);
    back_edges.assign(n, {}), par.assign(n, -1);
    return;
}

void build_prod_list(){
    while(true){
        string sym;
        file >> sym;
        if(sym[0] == '~')
            break;
        int i = ind[sym];
        cout << "-----------\n";
        cout << "- " << sym << "(" << i << ")" << '\n';
        while(true){
            string pr, token = "";
            file >> pr;
            if(pr[0] == '~')
                break;
            cout << " - " << pr << "\n    ";
            productions[i].push_back({});
            int cnt = 0;
            for(int j = 0; j < pr.size(); ++j){
                if(pr[j] == '\''){
                    int k = ind[token];
                    if(!cnt)
                        g[i].push_back(k);
                    if(j + 1 == pr.size())
                        g_last[i].push_back(k);
                    ++cnt;
                    cout << token << "(" << ind[token] << ") ";
                    productions[i].back().push_back(k), token = "";
                }
                else
                    token += pr[j];
            }
            cout << '\n';
        }
    }
    return;
}

void print_g(){
    cout << "____________________________\n";
    cout << "G adjancey list:";
    for(int i = 0; i < n; ++i){
        cout << symbol[i] << ":\n\t";
        for(int e: g[i])
            cout << symbol[e] << " ";
        cout << '\n';
    }
    cout << "____________________________\n";
    return;
}

void print_g_last(){
    cout << "____________________________\n";
    cout << "G_last adjancey list:";
    for(int i = 0; i < n; ++i){
        cout << symbol[i] << ":\n\t";
        for(int e: g_last[i])
            cout << symbol[e] << " ";
        cout << '\n';
    }
    cout << "____________________________\n";
    return;
}

void compute_first(){
    back_edges.assign(n, {});
    for(int i = 0; i < n; ++i)
        mark[i] = false, par[i] = -1;
    for(int i = 0; i < n; ++i)
        if(!mark[i])
            dfs_first(i, i);
    for(int i = 0; i < n; ++i)
        mark[i] = false;
    for(int i = 0; i < n; ++i)
        if(!mark[i])
            dfs_back_edge(i);
    return;
}

void compute_last(){
    back_edges.assign(n, {});
    for(int i = 0; i < n; ++i)
        mark[i] = false, par[i] = -1;
    for(int i = 0; i < n; ++i)
        if(!mark[i])
            dfs_last(i, i);
    for(int i = 0; i < n; ++i)
        mark[i] = false;
    for(int i = 0; i < n; ++i)
        if(!mark[i])
            dfs_back_edge_last(i);
    return;
}

void compute_follow(){
    for(int i = 0; i < n; ++i)
        for(const auto &token: productions[i])
            for(int j = 0; j + 1 < token.size(); ++j)
                for(auto &k: last[token[j]])
                    unite(follow[k], first[token[j + 1]]), follow[k].erase(ind["e"]);
    for(int i = 0; i < n; ++i)
        if(follow[i].empty())
            follow[i].insert(ind["$"]);
    for(int i = 0; i < n; ++i)
        for(auto e: last[i]){
            if(binary_search(follow[e].begin(), follow[e].end(), ind["$"]))
                follow[i].insert(ind["$"]);
                break;
        }
    return;
}

void print_grammer(){
    cout << "\n-----------------\nGrammer:\n-----------------\n";
    for(int i = 0; i < n; ++i){
        prd << productions[i].size() << '\n';
        for(const auto &token: productions[i]){
            cout << symbol[i] << " -> ";
            prd << token.size() << '\n';
            for(int j = 0; j < token.size(); ++j){
                cout << symbol[token[j]] << "(" << token[j] << ") ";
                prd << token[j] << " ";
            }
            prd << '\n';
            cout << '\n';
        }
    }
    return;
}

int main(){
    cout << "enter the directory of the grammer file:" << '\n';
    string dir = "./grammers/cppiler";
    //cin >> dir;
    if(dir.back() == '/' || dir.back() == '\\')
        dir.pop_back();
    /// ////////
    file.open(dir + "/grammer.txt");
    enumerate_symbols();
    initialize_vectors();
    build_prod_list();
    file.close();
    /// ///////
    print_g();
    print_g_last();
    /// //////
    compute_first();
    /// //////
    first_follow.open(dir + "/first_follow.txt");
    /// //////
    compute_last();
    /// //////
    compute_follow();
    /// //////
    prd.open(dir + "/productions.txt");
    print_grammer();
    prd.close();
    /// /////
    symbols.open(dir + "/symbols.txt");
    for(int i = 0; i < n; ++i)
        symbols << symbol[i] << " ";
    symbols << '\n';
    symbols.close();
    /// //////
    cout << "\n-----------------\nFirst:\n-----------------\n";
    for(int i = 0; i < n; ++i){
        cout << "First(" << symbol[i] << "):\n\t{";
        first_follow << first[i].size() << '\n';
        for(auto e: first[i]){
            first_follow << e << " ";
            cout << symbol[e] << ", ";
        }
        first_follow << '\n';
        cout << "\b\b}\n";
    }
    cout << "\n-----------------\nLast:\n-----------------\n";
    for(int i = 0; i < n; ++i){
        cout << "Last(" << symbol[i] << "):\n\t{";
        for(auto e: last[i])
            cout << symbol[e] << ", ";
        cout << "\b\b}\n";
    }
    cout << "\n-----------------\nFollow:\n-----------------\n";
    for(int i = 0; i < n; ++i){
        cout << "Follow(" << symbol[i] << "):\n\t{";
        first_follow << follow[i].size() << '\n';
        for(auto e: follow[i]){
            first_follow << e << " ";
            cout << symbol[e] << ", ";
        }
        first_follow << '\n';
        if(!follow[i].empty())
            cout << "\b\b";
        cout << "}\n";
    }
    first_follow.close();
    cout << "\n-----------------\nLL1-Pars-table:\n-----------------\n";
    ll_1_pars.open(dir + "/ll_1_pars.txt");
    for(int i = 0; i < nt; ++i)
        for(int j = nt; j < n; ++j){
                int k = 0;
                p_table[{i, j}] = {};
                for(const auto &token: productions[i]){
                    if(binary_search(first[token[0]].begin(), first[token[0]].end(), j))
                        p_table[{i, j}].push_back(k);
                    ++k;
                }
                if(j != nt && p_table[{i, j}].size()){
                    cout << "~ [" << i << ":" << symbol[i] << ", " << j << ":" << symbol[j] << "] = " << p_table[{i, j}].size() << '\n';
                    cout << symbol[i] << "("<< i << "):\n";
                    ll_1_pars << i << " " << j << '\n' << p_table[{i, j}].size() << '\n';
                    for(auto &e: p_table[{i, j}]){
                        ll_1_pars << e << '\n';
                        for(auto &e1: productions[i][e])
                            cout << symbol[e1] << "(" << e1 << ")";
                        cout << '\n';
                    }
                }
                if(j == nt && p_table[{i, j}].size()){
                    for(auto &e: follow[i]){
                        p_table[{i, e}] = p_table[{i, j}];
                        cout << "~ [" << i << ":" << symbol[i] << ", " << e << ":" << symbol[e] << "] = " << p_table[{i, e}].size() << '\n';
                        cout << symbol[i] << "("<< i << "):\n";
                        ll_1_pars << i << " " << e << '\n' << p_table[{i, e}].size() << '\n';
                        for(auto &e1: p_table[{i, e}]){
                            ll_1_pars << e1 << '\n';
                            for(auto &e2: productions[i][e1])
                                cout << symbol[e2] << "(" << e2 << ")";
                            cout << '\n';
                        }
                    }
                    p_table[{i, j}] = {};
                }
        }
    ll_1_pars.close();
    cout << "---\n";
    return 0;
}
