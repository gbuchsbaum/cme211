# Design considerations

I used an Item object to back up Inventory because it allowed me to easily keep track of every item in a vector. It also ensured that I couldn't accidentally change one of the values, and that I could access each value properly.

# Main changes
I replaced float with double to avoid compiler warnings.

# compiler
g++ -std=c++11 -Wall -Wextra -Wconversion -Wpedantic main.cpp Item.cpp Inventory.cpp CashRegister.cpp -o main