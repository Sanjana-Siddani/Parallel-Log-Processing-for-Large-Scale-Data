#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <thread>
#include <chrono>

using namespace std;

// This function extracts the IP address from one log line.
// Example line: [INFO] 192.168.0.0 Disk Full
// Here the IP is the second value, so we take the text between first and second space.
string parse_line(const string& line) {
    size_t first_space = line.find(' ');

    if (first_space == string::npos) {
        return "";
    }

    size_t second_space = line.find(' ', first_space + 1);

    if (second_space == string::npos) {
        return "";
    }

    return line.substr(first_space + 1, second_space - first_space - 1);
}

// This function is executed by each thread.
// Each thread processes only its assigned range of lines and stores counts locally.
void process_range(
    const vector<string>& lines,
    int start_index,
    int end_index,
    unordered_map<string, int>& local_count
) {
    for (int i = start_index; i < end_index; i++) {
        if (lines[i].empty()) {
            continue;
        }

        string ip = parse_line(lines[i]);

        if (ip.empty()) {
            continue;
        }
        
        // Count IPs in this thread's local map.
        // This avoids multiple threads writing to the same map.
        local_count[ip]++;
    }
}

int main() {
    string file_path = "logs_1000000.txt";
    int top_n = 3;

    vector<string> lines;
    string line;

    // Read the full log file into memory first.
    // After this, threads can process different parts of this vector.
    ifstream file(file_path);

    if (!file.is_open()) {
        cout << "Could not open file: " << file_path << endl;
        return 1;
    }

    while (getline(file, line)) {
        lines.push_back(line);
    }

    file.close();

    cout << "std::thread Static Thread Scaling Results:" << endl;

    // Run the same program with different thread counts
    // so we can observe how performance changes.
    for (int num_threads : {1, 2, 4, 8}) {
        vector<thread> threads;

        // Each thread gets its own local unordered_map.
        // This prevents race conditions while counting.
        vector<unordered_map<string, int>> local_counts(num_threads);

        int n = lines.size();
        int chunk_size = n / num_threads;

        auto start_time = chrono::high_resolution_clock::now();

        // Create threads and assign each thread a fixed chunk of lines.
        for (int t = 0; t < num_threads; t++) {
            int start_index = t * chunk_size;
            int end_index;

            // Last thread takes remaining lines also.
            if (t == num_threads - 1) {
                end_index = n;
            } else {
                end_index = start_index + chunk_size;
            }

            threads.emplace_back(
                process_range,
                cref(lines),
                start_index,
                end_index,
                ref(local_counts[t])
            );
        }

        // Wait for all threads to complete before merging results.
        for (auto& th : threads) {
            th.join();
        }

        // Merge all local thread results into one final map.
        unordered_map<string, int> total_counts;

        for (int i = 0; i < num_threads; i++) {
            for (auto& pair : local_counts[i]) {
                total_counts[pair.first] += pair.second;
            }
        }

        // Convert map to vector so that we can sort by count.
        vector<pair<string, int>> ip_vector;

        for (auto& pair : total_counts) {
            ip_vector.push_back(pair);
        }

        // Sort IPs in descending order of frequency.
        sort(ip_vector.begin(), ip_vector.end(),
             [](const auto& a, const auto& b) {
                 return a.second > b.second;
             });

        auto end_time = chrono::high_resolution_clock::now();
        chrono::duration<double> elapsed = end_time - start_time;

        cout << "\nThreads: " << num_threads << endl;
        cout << "Time: " << elapsed.count() << " seconds" << endl;

        // Print top N most frequent IP addresses.
        cout << "Top IPs:" << endl;
        for (int i = 0; i < top_n && i < ip_vector.size(); i++) {
            cout << ip_vector[i].first << " -> " << ip_vector[i].second << endl;
        }
    }

    return 0;
}