#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <omp.h>

using namespace std;

// This function extracts the IP address from one log line.
// Example line: [INFO] 192.168.0.0 Disk Full
// The IP is the second value, so we take the text between first and second space.
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

int main() {
    string file_path = "logs_1000000.txt";
    int top_n = 3;

    vector<string> lines;
    string line;

    // Read the full log file into a vector.
    // Then OpenMP threads can process different parts of this vector.
    ifstream file(file_path);

    if (!file.is_open()) {
        cout << "Could not open file: " << file_path << endl;
        return 1;
    }

    while (getline(file, line)) {
        lines.push_back(line);
    }

    file.close();

    cout << "OpenMP Static Thread Scaling Results:" << endl;

    // Run the program with different numbers of threads.
    // This helps us observe how performance changes as threads increase.
    for (int num_threads : {1, 2, 4, 8}) {
        omp_set_num_threads(num_threads);

        double start = omp_get_wtime();

        // Each thread has its own local map.
        // This avoids race conditions while counting IPs.
        vector<unordered_map<string, int>> local_counts(num_threads);

        #pragma omp parallel
        {
            int tid = omp_get_thread_num();
            int total_threads = omp_get_num_threads();

            int n = lines.size();
            int chunk_size = n / total_threads;

            // Static splitting: each thread gets a fixed range of lines.
            int start_index = tid * chunk_size;
            int end_index = (tid == total_threads - 1)
                                ? n
                                : start_index + chunk_size;

            // Each thread processes only its assigned range.
            for (int i = start_index; i < end_index; i++) {
                if (lines[i].empty()) {
                    continue;
                }

                string ip = parse_line(lines[i]);

                if (ip.empty()) {
                    continue;
                }

                // Store count in the local map of this thread.
                local_counts[tid][ip]++;
            }
        }

        // Merge all thread-local counts into one final map.
        unordered_map<string, int> total_counts;

        for (int i = 0; i < num_threads; i++) {
            for (auto& pair : local_counts[i]) {
                total_counts[pair.first] += pair.second;
            }
        }

        // Convert map to vector so we can sort by count.
        vector<pair<string, int>> ip_vector;

        for (auto& pair : total_counts) {
            ip_vector.push_back(pair);
        }

        // Sort IPs in descending order of frequency.
        sort(ip_vector.begin(), ip_vector.end(),
             [](const auto& a, const auto& b) {
                 return a.second > b.second;
             });

        double end = omp_get_wtime();

        cout << "\nThreads: " << num_threads << endl;
        cout << "Time: " << (end - start) << " seconds" << endl;

        // Print the top N most frequent IP addresses.
        cout << "Top IPs:" << endl;
        for (int i = 0; i < top_n && i < ip_vector.size(); i++) {
            cout << ip_vector[i].first << " -> " << ip_vector[i].second << endl;
        }
    }

    return 0;
}