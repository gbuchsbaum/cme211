#ifndef ITEM_HPP
#define ITEM_HPP

#include <string>

class Item {
  std::string name_;
  double price_;
  int nStock_;

public:
  Item(std::string name, double price, int nStock);
  std::string getName(void);
  double getPrice(void);
  int getStock(void);
  void Sell(int nSold);
};

#endif /* ITEM_HPP */
