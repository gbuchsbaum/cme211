#ifndef CASHREGISTER_HPP
#define CASHREGISTER_HPP

class CashRegister {
  double revenue_, funds_;

public:
  void Sale(double revenue, double funds);
  void Print(void);
  double getRevenue(void);
  double getFunds(void);
};

#endif /* CASHREGISTER_HPP */
