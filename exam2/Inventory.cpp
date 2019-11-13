#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include "Item.hpp"
#include "Inventory.hpp"
#include "CashRegister.hpp"

Inventory::Inventory(std::string fileName) {
  std::ifstream f;
  f.open(fileName);
  if (f.is_open()) {
    std::string line;
    while (getline(f, line)) {
      std::string tmp;
      std::stringstream s(line);
      std::getline(s, tmp, ',');
      std::string name = tmp;
      std::getline(s, tmp, ',');
      double price = std::stof(tmp);
      std::getline(s, tmp, ',');
      int nStock = std::stoi(tmp);
      items_.emplace_back(name, price, nStock);
    }
    f.close();
  }
  else {
    std::cerr << "Unable to open " << fileName << std::endl;
  }
}

int Inventory::AttemptExport(std::string item, int qty, double funds) {
  if (qty < 0) {
    std::cout << "Number requested cannot be negative" << std::endl;
    return 0;
  }
  if (funds < 0) {
    std::cout << "Cannot have negative funds" << std::endl;
    return 0;
  }
  for (unsigned int i = 0; i < items_.size(); i++) {
    if (item.compare(items_[i].getName()) == 0) {
      double price= items_[i].getPrice();
      int nAfforded = (int)(funds / price);
      int nSold = std::min(qty, std::min(nAfforded, items_[i].getStock()));
      items_[i].Sell(nSold);
      double revenue = ((double)nSold) * price;
      register_.Sale(revenue, funds);
      return nSold;
    }
  }
  return 0;
}

double Inventory::SummarizeTransaction(void) {
  register_.Print();
  return register_.getRevenue();
}

void Inventory::Print(void) {
  for (unsigned int i = 0; i < items_.size(); i++) {
    std::cout << items_[i].getName() << std::endl;
    std::cout << "  " << items_[i].getPrice() << ", ";
    std::cout << items_[i].getStock() << std::endl;
  }
}

unsigned int Inventory::TotalStock(void) {
  unsigned int total = 0;
  for (unsigned int i = 0; i < items_.size(); i++) {
    total += (unsigned int)items_[i].getStock();
  }
  return total;
}

double Inventory::Value(void) {
   double total = 0;
  for (unsigned int i = 0; i < items_.size(); i++) {
    double price = items_[i].getPrice();
    double  nStock = (double)items_[i].getStock();
    total += price * nStock;
  }
  return total;
}
