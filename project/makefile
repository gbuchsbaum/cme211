CXX := g++
CXXFLAGS := -std=c++11 -O3 -Wall -Wextra -Wconversion -Wpedantic

TARGET := main
OBJS := main.o CGSolver.o COO2CSR.o matvecops.o heat.o sparse.o
INCS1 := main.cpp CGSolver.cpp COO2CSR.cpp matvecops.cpp heat.cpp sparse.cpp
INCS2 := CGSolver.hpp COO2CSR.hpp matvecops.hpp heat.hpp sparse.hpp

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS)

%.o: %.cpp $(INCS1) $(INCS2)
	$(CXX) -c -o $@ $< $(CXXFLAGS)

.PHONY: clean
clean:
	rm -f *.o *~ main
