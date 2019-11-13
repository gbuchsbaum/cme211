#include <iostream>
#include <vector>
#include "CashRegister.hpp"

void CashRegister::Sale(double revenue, double funds) {
  this->revenue_ = revenue;
  this->funds_ = funds;
}

void CashRegister::Print(void) {
  std::vector<double> bills = {20, 10, 5, 1, 0.25, 0.10, 0.05, 0.01};
  std::cout.setf(std::ios_base::fixed,std::ios_base::floatfield);
  std::cout.precision(2);
  for (unsigned int i = 0; i < bills.size(); i++) {
    int number = 0;
    while (bills[i] <= funds_) {
      number++;
      funds_ -= bills[i];
    }
    if (bills[i] < 1) {
      std::cout << bills[i] << " : " << number << std::endl;
    }
    else if (bills[i] < 10) {
      std::cout << (int)bills[i] << "  : " << number << std::endl;
    }
    else {
      std::cout << (int)bills[i] << " : " << number << std::endl;
    }
  }
}

double CashRegister::getRevenue(void) {
  return revenue_;
}

double CashRegister::getFunds(void) {
  return funds_;
}
