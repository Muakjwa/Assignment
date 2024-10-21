#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <string.h>
#include <cstring>
#include <cmath>
#include <vector>
#include <map>
#include <tuple>
#include <algorithm>
#include <iomanip>

using namespace std;

long long int fromHexToDeci(string value);
int containTag(vector<pair<long long int, tuple<int, int>>>& vec, int tag);
int lru_victim(vector<pair<long long int, tuple<int, int>>>& vec, int tag);
void lru_update(vector<pair<long long int, tuple<int, int>>>& vec);
void eviction_update(vector<pair<long long int, tuple <int, int>>>& vec, int kill, int& dirty_eviction, int& clean_eviction);
int find_tag(vector<pair<long long int, tuple<int, int>>>& vec, int tag);

class Cache
{
    public:
    map<long long int, vector<pair<long long int, tuple<int, int>>>> cache_list; // index, tag, recent, dirty 순서
    Cache(int index, int tag, int associativity){
        for (int i = 0; i < pow(2, index); i++){
            vector<pair<long long int, tuple<int, int>>> vec;
            cache_list[i] = vec;
        }
    }
};

int main(int argc, char** argv)
{	
    srand(time(NULL));
    string object_file = "";
    int L2_capacity = 4; int L1_capacity = 4;
    int L2_associativity = 1; int L1_associativity = 1;
    int block_size = 16;
    bool LRU = false;
    bool RANDOM = false;

    int read_count = 0; int write_count = 0; int L1_hit = 0; int L2_hit = 0; int L1_read_miss = 0; int L2_read_miss = 0; int L1_write_miss = 0; int L2_write_miss = 0; 
    int L1_clean_eviction = 0; int L2_clean_eviction = 0; int L1_dirty_eviction = 0; int L2_dirty_eviction = 0;

    // Parsing Command
    for (int i = 1; i < argc; i++){
        string instruction = argv[i];
        if (instruction == "-c"){
            L2_capacity = stoi(argv[++i]);
        }
        else if (instruction == "-a"){
            L2_associativity = stoi(argv[++i]);
            L1_associativity = stoi(argv[i]);
        }
        else if (instruction == "-b"){
            block_size = stoi(argv[++i]);
        }
        else if (instruction == "-lru"){
            LRU = true;
        }
        else if (instruction == "-random"){
            RANDOM = true;
        }
        else{
            object_file = argv[i];
        }
    }

	string s;
	ifstream fp(object_file);

    int L2_index = log2(L2_capacity * 1024 / block_size / L2_associativity);
    int L2_tag = 64 - L2_index - log2(block_size);
    int L1_index; int L1_tag;
    int log_block_size = log2(block_size);
    Cache L2(L2_index, L2_tag, L2_associativity);
    L1_capacity = L2_capacity / 4;
    if (L2_associativity >= 4){
        L1_associativity = L2_associativity / 4;
    }
    L1_index = log2(L1_capacity * 1024 / block_size / L1_associativity);
    L1_tag = 64 - L1_index - log2(block_size);
    Cache L1(L1_index, L1_tag, L1_associativity);

	if (!fp.is_open())
	{
		cout << stderr << "can't read file...\n" << endl;
		exit(1);
	}

	while(getline(fp, s))
	{
        stringstream ss(s);
        string instr; string addr; long long int address;

        ss >> instr; ss >> addr;
        address = stoll(addr, nullptr, 16);

        
        long long int L1_index_mask = (1 << L1_index) - 1; long long int L1_tag_mask = (1 << L1_tag) - 1;
        long long int L1_index_val = (address >> log_block_size) & L1_index_mask;
        long long int L1_tag_val = (address >> log_block_size >> L1_index) & L1_tag_mask;
        long long int L2_index_mask = (1 << L2_index) - 1; long long int L2_tag_mask = (1 << L2_tag) - 1;
        long long int L2_index_val = (address >> log_block_size) & L2_index_mask;
        long long int L2_tag_val = (address >> log_block_size >> L2_index) & L2_tag_mask;
        int L1_exist = containTag(L1.cache_list[L1_index_val], L1_tag_val); int L2_exist = containTag(L2.cache_list[L2_index_val], L2_tag_val);


        if (instr == "R"){
            // 벡터에 있으면 hit
            if ((L1_exist) != -1){
                L1_hit++;
                if (LRU){
                    // L1 LRU update
                    lru_update(L1.cache_list[L1_index_val]);
                    get<0>(L1.cache_list[L1_index_val][L1_exist].second) = 1;
                    // // L2 LRU update
                    // lru_update(L2.cache_list[L2_index_val]);
                    // get<0>(L2.cache_list[L2_index_val][L2_exist].second) = 1;
                }
            }
            else if ((L2_exist) != -1){
                L2_hit++; L1_read_miss++; int kill = 0;
                if (LRU){
                    // L2 LRU update
                    lru_update(L2.cache_list[L2_index_val]);
                    get<0>(L2.cache_list[L2_index_val][L2_exist].second) = 1;
                    // L2 Cache Data -> L1 Cache
                    kill = lru_victim(L1.cache_list[L1_index_val], L1_tag_val);
                }
                else{
                    kill = rand() % L1.cache_list[L1_index_val].size();
                }
                // L1 Way 다 안찼으면 채워주기
                if (L1.cache_list[L1_index_val].size() < L1_associativity){
                    lru_update(L1.cache_list[L1_index_val]);
                    L1.cache_list[L1_index_val].push_back(make_pair(L1_tag_val, make_tuple(1,0)));
                }
                // L1 Way 다 차면 Eviction 후 cache update
                else{
                    // dirty eviction OR clean eviction
                    eviction_update(L1.cache_list[L1_index_val], kill, L1_dirty_eviction, L1_clean_eviction);
                    L1.cache_list[L1_index_val].erase(L1.cache_list[L1_index_val].begin() + kill);
                    lru_update(L1.cache_list[L1_index_val]);
                    L1.cache_list[L1_index_val].push_back(make_pair(L1_tag_val, make_tuple(1,0)));
                }
            }
            else{
                L1_read_miss++; L2_read_miss++;
                // L1 Way 다 안찼으면 채워주기
                if (L1.cache_list[L1_index_val].size() < L1_associativity){
                    lru_update(L1.cache_list[L1_index_val]);
                    L1.cache_list[L1_index_val].push_back(make_pair(L1_tag_val, make_tuple(1,0)));
                }
                // L1 Way 다 차면 Eviction 후 cache update
                else{
                    int kill = 0;
                    if (LRU){
                        kill = lru_victim(L1.cache_list[L1_index_val], L1_tag_val);
                    }
                    else{
                        kill = rand() % L1.cache_list[L1_index_val].size();
                    }

                    // 죽이기 전에 L1 dirty이고 L2에도 있으면 L2를 dirty로 변경
                    if (get<1>(L1.cache_list[L1_index_val][kill].second) != 0){
                        long long int L1_kill_index = L1_index_val;
                        long long int L1_kill_tag = L1.cache_list[L1_index_val][kill].first;
                        long long int addr = 0;
                        addr = addr | (L1_kill_index << log_block_size);
                        addr = addr | (L1_kill_tag << log_block_size << L1_index);
                        long long int L2_update_index = (addr >> log_block_size) & L2_index_mask;
                        long long int L2_update_tag = (addr >> log_block_size >> L2_index) & L2_tag_mask;
                        int L1X_L2_exist = containTag(L2.cache_list[L2_update_index], L2_update_tag);
                        if (L1X_L2_exist != -1){
                            get<1>(L2.cache_list[L2_update_index][L1X_L2_exist].second) = 1;
                            lru_update(L2.cache_list[L2_update_index]);
                            get<0>(L2.cache_list[L2_update_index][L1X_L2_exist].second) = 1;
                        }
                    }

                    eviction_update(L1.cache_list[L1_index_val], kill, L1_dirty_eviction, L1_clean_eviction);
                    L1.cache_list[L1_index_val].erase(L1.cache_list[L1_index_val].begin() + kill);
                    lru_update(L1.cache_list[L1_index_val]);
                    L1.cache_list[L1_index_val].push_back(make_pair(L1_tag_val, make_tuple(1,0)));
                }
                // L2 Way 다 안찼으면 채워주기
                if (L2.cache_list[L2_index_val].size() < L2_associativity){
                    lru_update(L2.cache_list[L2_index_val]);
                    L2.cache_list[L2_index_val].push_back(make_pair(L2_tag_val, make_tuple(1,0)));
                }
                // L2 Way 다 차면 Eviction 후 cache update
                else{
                    int kill = 0;
                    if (LRU){
                        kill = lru_victim(L2.cache_list[L2_index_val], L2_tag_val);
                    }
                    else{
                        kill = rand() % L2.cache_list[L2_index_val].size();
                    }

                    // 삭제할 L2 값의 주소
                    long long int delete_addr = (L2_index_val << log_block_size) + (L2.cache_list[L2_index_val][kill].first << log_block_size << L2_index);
                    eviction_update(L2.cache_list[L2_index_val], kill, L2_dirty_eviction, L2_clean_eviction);
                    L2.cache_list[L2_index_val].erase(L2.cache_list[L2_index_val].begin() + kill);
                    lru_update(L2.cache_list[L2_index_val]);
                    L2.cache_list[L2_index_val].push_back(make_pair(L2_tag_val, make_tuple(1,0)));
                    // 삭제할 L2 값이 L1에 있는지 확인
                    L1_index_val = (delete_addr >> log_block_size) & L1_index_mask;
                    L1_tag_val = (delete_addr >> log_block_size >> L1_index) & L1_tag_mask;
                    L1_exist = containTag(L1.cache_list[L1_index_val], L1_tag_val);
                    if (L1_exist != -1){
                        int delete_index = find_tag(L1.cache_list[L1_index_val], L1_tag_val);
                        eviction_update(L1.cache_list[L1_index_val], delete_index, L1_dirty_eviction, L1_clean_eviction);
                        L1.cache_list[L1_index_val].erase(L1.cache_list[L1_index_val].begin() + delete_index);
                    }
                }
            }
            read_count++;
        }
        else if (instr == "W"){
            // 벡터에 있으면 hit
            if ((L1_exist) != -1){
                L1_hit++;
                if (LRU){
                    // L1 LRU update
                    lru_update(L1.cache_list[L1_index_val]);
                    get<0>(L1.cache_list[L1_index_val][L1_exist].second) = 1;
                    get<1>(L1.cache_list[L1_index_val][L1_exist].second) = 1;
                    // L2 LRU update
                    // lru_update(L2.cache_list[L2_index_val]);
                    // get<0>(L2.cache_list[L2_index_val][L2_exist].second) = 1;
                    // get<1>(L2.cache_list[L2_index_val][L2_exist].second) = 1;
                }
            }
            else if ((L2_exist) != -1){
                L2_hit++; L1_write_miss++; int kill = 0;
                if (LRU){
                    // L2 LRU update
                    lru_update(L2.cache_list[L2_index_val]);
                    get<0>(L2.cache_list[L2_index_val][L2_exist].second) = 1;
                    get<1>(L2.cache_list[L2_index_val][L2_exist].second) = 1;
                    // L2 Cache Data -> L1 Cache
                    kill = lru_victim(L1.cache_list[L1_index_val], L1_tag_val);
                }
                else{
                    kill = rand() % L1.cache_list[L1_index_val].size();
                }
                // L1 Way 다 안찼으면 채워주기
                if (L1.cache_list[L1_index_val].size() < L1_associativity){
                    lru_update(L1.cache_list[L1_index_val]);
                    L1.cache_list[L1_index_val].push_back(make_pair(L1_tag_val, make_tuple(1,1)));
                }
                // L1 Way 다 차면 Eviction 후 cache update
                else{
                    // dirty eviction OR clean eviction
                    eviction_update(L1.cache_list[L1_index_val], kill, L1_dirty_eviction, L1_clean_eviction);
                    // L1 cache eviction
                    L1.cache_list[L1_index_val].erase(L1.cache_list[L1_index_val].begin() + kill);
                    lru_update(L1.cache_list[L1_index_val]);
                    L1.cache_list[L1_index_val].push_back(make_pair(L1_tag_val, make_tuple(1,1)));
                }
            }
            else{
                L1_write_miss++; L2_write_miss++;
                // L1 Way 다 안찼으면 채워주기
                if (L1.cache_list[L1_index_val].size() < L1_associativity){
                    lru_update(L1.cache_list[L1_index_val]);
                    L1.cache_list[L1_index_val].push_back(make_pair(L1_tag_val, make_tuple(1,1)));
                }
                // L1 Way 다 차면 Eviction 후 cache update
                else{
                    int kill = 0;
                    if (LRU){
                        kill = lru_victim(L1.cache_list[L1_index_val], L1_tag_val);
                    }
                    else{
                        kill = rand() % L1.cache_list[L1_index_val].size();
                    }

                    // 죽이기 전에 L1 dirty이고 L2에도 있으면 L2를 dirty로 변경
                    if (get<1>(L1.cache_list[L1_index_val][kill].second) != 0){
                        long long int L1_kill_index = L1_index_val;
                        long long int L1_kill_tag = L1.cache_list[L1_index_val][kill].first;
                        long long int addr = 0;
                        addr = addr | (L1_kill_index << log_block_size);
                        addr = addr | (L1_kill_tag << log_block_size << L1_index);
                        long long int L2_update_index = (addr >> log_block_size) & L2_index_mask;
                        long long int L2_update_tag = (addr >> log_block_size >> L2_index) & L2_tag_mask;
                        int L1X_L2_exist = containTag(L2.cache_list[L2_update_index], L2_update_tag);
                        if (L1X_L2_exist != -1){
                            get<1>(L2.cache_list[L2_update_index][L1X_L2_exist].second) = 1;
                            lru_update(L2.cache_list[L2_update_index]);
                            get<0>(L2.cache_list[L2_update_index][L1X_L2_exist].second) = 1;
                        }
                    }

                    eviction_update(L1.cache_list[L1_index_val], kill, L1_dirty_eviction, L1_clean_eviction);
                    L1.cache_list[L1_index_val].erase(L1.cache_list[L1_index_val].begin() + kill);
                    lru_update(L1.cache_list[L1_index_val]);
                    L1.cache_list[L1_index_val].push_back(make_pair(L1_tag_val, make_tuple(1,1)));
                }
                // L2 Way 다 안찼으면 채워주기
                if (L2.cache_list[L2_index_val].size() < L2_associativity){
                    lru_update(L2.cache_list[L2_index_val]);
                    L2.cache_list[L2_index_val].push_back(make_pair(L2_tag_val, make_tuple(1,1)));
                }
                // L2 Way 다 차면 Eviction 후 cache update
                else{
                    int kill = 0;
                    if (LRU){
                        kill = lru_victim(L2.cache_list[L2_index_val], L2_tag_val);
                    }
                    else{
                        kill = rand() % L2.cache_list[L2_index_val].size();
                    }
                    // 삭제할 L2 값의 주소
                    long long int delete_addr = (L2_index_val << log_block_size) + (L2.cache_list[L2_index_val][kill].first << log_block_size << L2_index);
                    eviction_update(L2.cache_list[L2_index_val], kill, L2_dirty_eviction, L2_clean_eviction);
                    L2.cache_list[L2_index_val].erase(L2.cache_list[L2_index_val].begin() + kill);
                    lru_update(L2.cache_list[L2_index_val]);
                    L2.cache_list[L2_index_val].push_back(make_pair(L2_tag_val, make_tuple(1,1)));
                    // 삭제할 L2 값이 L1에 있는지 확인
                    L1_index_val = (delete_addr >> log_block_size) & L1_index_mask;
                    L1_tag_val = (delete_addr >> log_block_size >> L1_index) & L1_tag_mask;
                    L1_exist = containTag(L1.cache_list[L1_index_val], L1_tag_val);
                    if (L1_exist != -1){
                        int delete_index = find_tag(L1.cache_list[L1_index_val], L1_tag_val);
                        eviction_update(L1.cache_list[L1_index_val], delete_index, L1_dirty_eviction, L1_clean_eviction);
                        L1.cache_list[L1_index_val].erase(L1.cache_list[L1_index_val].begin() + delete_index);
                    }
                }
            }
            write_count++;
        }
	}
    // cout << read_count << " " << write_count << " " << L1_read_miss << " " << L2_read_miss << " " << L1_write_miss << " " << L2_write_miss << " " << dirty_eviction << " " << clean_eviction << endl;
	fp.close();


    // cout << "-- General Stats --" << endl;
    // cout << "L1 Capacity: " << L1_capacity << endl;
    // cout << "L1 way: " << L1_associativity << endl;
    // cout << "L2 Capacity: " << L2_capacity << endl;
    // cout << "L2 way: " << L2_associativity << endl;
    // cout << "Block Size: " << block_size << endl;
    // cout << "Total accesses: " << read_count + write_count << endl;
    // cout << "Read accesses: " << read_count << endl;
    // cout << "Write accesses: " << write_count << endl;
    // cout << "L1 Read misses:" << L1_read_miss << endl;
    // cout << "L2 Read misses:" << L2_read_miss << endl;
    // cout << "L1 Write misses:" << L1_write_miss << endl;
    // cout << "L2 Write misses:" << L2_write_miss << endl;
    // cout << "L1 Read miss rate: " << float(L1_read_miss) / float(read_count) * 100. << "%" << endl;
    // cout << "L2 Read miss rate: " << double(L2_read_miss) / double(L1_read_miss) * 100. << "%" << endl;
    // cout << "L1 Write miss rate: " << float(L1_write_miss) / float(write_count) * 100. << "%" << endl;
    // cout << "L2 write miss rate: " << double(L2_write_miss) / double(L1_write_miss) * 100. << "%" << endl;
    // cout << "L1 Clean eviction: " << L1_clean_eviction << endl;
    // cout << "L2 clean eviction: " << L2_clean_eviction << endl;
    // cout << "L1 dirty eviction: " << L1_dirty_eviction << endl;
    // cout << "L2 dirty eviction: " << L2_dirty_eviction << endl;
    // cout << "read miss rate : " << double(L2_read_miss)/double(read_count) *100. <<"%"<<endl;
    // cout << "write miss rate : " << double(L2_write_miss)/double(write_count) * 100. <<"%"<<endl;

    int pos = object_file.find('.');
    string filename = object_file.substr(0, pos) + "_" + to_string(L2_capacity) + "_" + to_string(L2_associativity) + "_" + to_string(block_size) + ".out";
    ofstream outfile(filename);

    if (outfile.is_open()) {
        outfile << "-- General Stats --" << endl;
        outfile << "L1 Capacity: " << L1_capacity << endl;
        outfile << "L1 way: " << L1_associativity << endl;
        outfile << "L2 Capacity: " << L2_capacity << endl;
        outfile << "L2 way: " << L2_associativity << endl;
        outfile << "Block Size: " << block_size << endl;
        outfile << "Total accesses: " << read_count + write_count << endl;
        outfile << "Read accesses: " << read_count << endl;
        outfile << "Write accesses: " << write_count << endl;
        outfile << "L1 Read misses:" << L1_read_miss << endl;
        outfile << "L2 Read misses:" << L2_read_miss << endl;
        outfile << "L1 Write misses:" << L1_write_miss << endl;
        outfile << "L2 Write misses:" << L2_write_miss << endl;
        outfile << "L1 Read miss rate: " << float(L1_read_miss) / float(read_count) * 100. << "%" << endl;
        outfile << "L2 Read miss rate: " << double(L2_read_miss) / double(L1_read_miss) * 100. << "%" << endl;
        outfile << "L1 Write miss rate: " << float(L1_write_miss) / float(write_count) * 100. << "%" << endl;
        outfile << "L2 write miss rate: " << double(L2_write_miss) / double(L1_write_miss) * 100. << "%" << endl;
        outfile << "L1 Clean eviction: " << L1_clean_eviction << endl;
        outfile << "L2 clean eviction: " << L2_clean_eviction << endl;
        outfile << "L1 dirty eviction: " << L1_dirty_eviction << endl;
        outfile << "L2 dirty eviction: " << L2_dirty_eviction;
        
        outfile.close();
    }

	return 0;
}

long long int fromHexToDeci(string value)
{
    stringstream ss(value);
    long long int decimal_val;
    ss >> hex >> decimal_val;
    return decimal_val;
}

int containTag(vector<pair<long long int, tuple<int, int>>>& vec, int tag) {
    for (size_t i = 0; i < vec.size(); ++i) {
        if (vec[i].first == tag){
            return i;
        }
    }
    return -1;
}

int lru_victim(vector<pair<long long int, tuple<int, int>>>& vec, int tag) {
    int recent = 0; int target = 0;
    for (int i = 0; i < vec.size(); ++i) {
        if (get<0>(vec[i].second) > recent){
            recent = get<0>(vec[i].second);
            target = i;
        }
    }
    return target;
}

void lru_update(vector<pair<long long int, tuple<int, int>>>& vec) {
    for (size_t i = 0; i < vec.size(); ++i) {
        get<0>(vec[i].second) = get<0>(vec[i].second) + 1;
    }
}

void eviction_update(vector<pair<long long int, tuple <int, int>>>& vec, int kill, int& dirty_eviction, int& clean_eviction){
    // dirty eviction OR clean eviction
    if (get<1>(vec[kill].second) == 1){
        dirty_eviction += 1;
    }
    else{
        clean_eviction += 1;
    }
}

int find_tag(vector<pair<long long int, tuple<int, int>>>& vec, int tag) {
    int target = 0;
    for (int i = 0; i < vec.size(); ++i) {
        if ((vec[i].first) == tag){
            target = i;
        }
    }
    return target;
}