#include <cstdio>
#include <iostream>
#include <string>
// Optional: #include "Item.hpp"
#include "Inventory.hpp"
int main(int argc, char *argv[]) {
    if (argc < 2) {
        std::cout << "Usage:\n\t./main inventory_fname [requested_item] [requested_qty] [lump_sum]\n";
        return 0;
    }
    Inventory i(argv[1]);
    i.Print();
    if (argc >= 3) {
        std::cout << "Handling an export request." << std::endl;
        std::string item(argv[2]);
        int   qty   = std::atoi(argv[3]);
        double funds = std::atof(argv[4]);
        if (i.AttemptExport(item, qty, funds))
          std::cout << i.SummarizeTransaction() << '\n';
    }
    std::printf("Total number of items in inventory: %d, valued at %g\n", i.TotalStock(), i.Value());
}
