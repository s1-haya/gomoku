#include <chrono>
#include <iostream>

// --- Benchmark Constants ---
constexpr long long ITERATIONS = 1000'000'000LL;
constexpr int BOARD_SIZE = 19;

inline int dummy_check_line(int r, int c, int dr, int dc, int player) {
    return (r * BOARD_SIZE + c) ^ (dr * 31 + dc * 17 + player);
}

int main() {
    volatile long long sink = 0;
    int n=19;

    const auto start = std::chrono::steady_clock::now();
    for (long long idx = 0; idx < ITERATIONS; ++idx) {
        int r = static_cast<int>((idx / BOARD_SIZE) % BOARD_SIZE);
        int c = static_cast<int>(idx % BOARD_SIZE);
        sink += dummy_check_line(r, c, 0, 1, 1);
    }
    const auto end = std::chrono::steady_clock::now();

    const std::chrono::duration<double> elapsed = end - start;
    const double avg_ns = (elapsed.count() / static_cast<double>(ITERATIONS)) * 1e9;

    std::cout << "Iterations : " << ITERATIONS << "\n";
    std::cout << "Total time : " << elapsed.count() << " s\n";
    std::cout << "Avg / call : " << avg_ns << " ns\n";
    std::cout << "Sink       : " << sink << "\n";
    return 0;
}