#include "Item.hpp"
#include <string>

Item::Item(std::string name, double price, int nStock) {
  this->name_ = name;
  this->price_ = price;
  this->nStock_ = nStock;
}

std::string Item::getName(void) {
  return name_;
}

double Item::getPrice(void) {
  return price_;
}

int Item::getStock(void) {
  return nStock_;
}

void Item::Sell(int nSold) {
  nStock_ -= nSold;
}
