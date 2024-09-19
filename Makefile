# C++ compiler flags.
CXX   := g++ -g -Wall 
#CXX   := g++
FLAGS := -std=c++17 $(shell root-config --cflags) -I/cvmfs/cms.cern.ch/el9_amd64_gcc12/external/boost/1.80.0-4e27c6908892e3529bfbcf4445a96fe6/include

LIBS  := $(shell root-config --libs) -L/cvmfs/cms.cern.ch/el9_amd64_gcc12/external/boost/1.80.0-4e27c6908892e3529bfbcf4445a96fe6/lib

#SOURCES := WeightCalculatorFromHistogram.cc LeptonEfficiencyCorrector.cc RoccoR.cc MainEvent.cc HmmAnalyzer.cc
#HEADERS := WeightCalculatorFromHistogram.h LeptonEfficiencyCorrector.h RoccoR.h MainEvent.h HmmAnalyzer.h

# Locations.
BIN := ./bin
SRC := ./src
LIB := ./lib

OBJECTS := WeightCalculatorFromHistogram.o \
				LeptonEfficiencyCorrector.o \
				RoccoR.o \
				MainEvent.o \
				HmmAnalyzer.o 

EXECUTABLE := $(BIN)/HmmAnalyzer

#all: $(SOURCES) $(EXECUTABLE)
all: $(EXECUTABLE)

#%.o: %.cc $(HEADERS)
$(OBJECTS): %.o: $(SRC)/%.cc $(LIB)/%.h
	@echo Compiling $<...
	$(CXX) $(FLAGS) -c $< -o $@ 

#$(EXECUTABLE): $(OBJECTS)
	#@echo "Linking $(EXECUTABLE) ..."
	#@echo "@$(CXX) $(LIBS) $(OBJECTS) -o $@"
	#@$(CXX) -o $@ $^ $(LIBS) 
	#@echo "done"
#$(EXECUTABLE): $(BIN)/%: $(SRC)/%.cc $(OBJECTS)
	#$(CXX) $(FLAGS) $(OBJECTS) $< -o $@ $(LIBS)
$(EXECUTABLE): $(OBJECTS)
	@echo "Linking $(EXECUTABLE) ..."
	@$(CXX) $(FLAGS) -o $@ $^ $(LIBS)
	@echo "done"

# Specifying the object files as intermediates deletes them automatically after the build process.
.INTERMEDIATE:  $(OBJECTS)

# The default target, which gives instructions, can be called regardless of whether or not files need to be updated.
.PHONY : clean
clean:
	rm -f $(OBJECTS) $(EXECUTABLE)

###
MainEvent.o:  $(LIB)/MainEvent.h
AnalyzeHmm.o: $(LIB)/MainEvent.h $(LIB)/HmmAnalyzer.h
