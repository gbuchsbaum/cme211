#ifndef INVENTORY_HPP
#define INVENTORY_HPP

#include <string>
#include <vector>
#include "Item.hpp"
#include "CashRegister.hpp"

class Inventory {
  std::vector<Item> items_;
  CashRegister register_;

public:
  Inventory(std::string fileName);
  int AttemptExport(std::string item, int qty, double funds);
  double SummarizeTransaction(void);
  void Print(void);
  unsigned int TotalStock(void);
  double Value(void);
};

#endif /* INVENTORY_HPP */
