# Locations
BIN := ./bin
SRC := ./src
LIB := ./lib

# C++ compiler flags.
CXX   := g++ -g -Wall 
FLAGS := -std=c++17 $(shell root-config --cflags) -I/cvmfs/cms.cern.ch/el9_amd64_gcc12/external/boost/1.80.0-4e27c6908892e3529bfbcf4445a96fe6/include

LIBS  := $(shell root-config --libs) -L/cvmfs/cms.cern.ch/el9_amd64_gcc12/external/boost/1.80.0-4e27c6908892e3529bfbcf4445a96fe6/lib

# Analyzer sources and header
ANALYZER_SRC := $(SRC)/LeptonEfficiencyCorrector.cc \
				$(SRC)/MainEvent.cc \
				$(SRC)/RoccoR.cc \
				$(SRC)/WeightCalculatorFromHistogram.cc \
				$(SRC)/HmmAnalyzer.cc

ANALYZER_HEADERS := $(LIB)/BTagCalibrationStandalone.h \
				$(LIB)/LeptonEfficiencyCorrector.h \
				$(LIB)/MainEvent.h \
				$(LIB)/RoccoR.h \
				$(LIB)/WeightCalculatorFromHistogram.h \
				$(LIB)/HmmAnalyzer.h


# Histogram sources and header
HISTOGRAM_SRC := $(SRC)/CreateHistograms.cc
HISTOGRAM_HEADERS := $(LIB)/Run3Constants.h $(LIB)/Constants.h $(LIB)/CreateHistograms.h

# Histogram sources and header
SKIM_SRC := $(SRC)/SkimTuple.cc
SKIM_HEADERS := $(LIB)/Run3Constants.h $(LIB)/Constants.h $(LIB)/SkimTuples.h

SOURCES := $(ANALYZER_SRC) $(HISTOGRAM_SRC) $(SKIM_SRC)


# Object files
ANALYZER_OBJECTS := LeptonEfficiencyCorrector.o \
				MainEvent.o \
				RoccoR.o \
				WeightCalculatorFromHistogram.o \
				HmmAnalyzer.o
 
HISTOGRAM_OBJECTS := CreateHistograms.o

SKIM_OBJECTS := SkimTuples.o

OBJECTS := $(ANALYZER_OBJECTS) $(HISTOGRAM_OBJECTS) $(SKIM_OBJECTS)

# Executables
ANALYZER_EXECUTABLE := $(BIN)/HmmAnalyzer
HISTOGRAM_EXECUTABLE := $(BIN)/CreateHistograms
SKIM_EXECUTABLE := $(BIN)/SkimTuples

# Default target: build both executables
.PHONY: all
all: $(ANALYZER_EXECUTABLE) $(HISTOGRAM_EXECUTABLE) $(SKIM_EXECUTABLE)

# Compile only the Analyzer
.PHONY: analyzer
analyzer: $(ANALYZER_EXECUTABLE)

# Compile only the Histograms
.PHONY: histogram
histogram: $(HISTOGRAM_EXECUTABLE)

# Compile only the Skim 
.PHONY: skim
skim: $(SKIM_EXECUTABLE)

# Compile all the objects
$(OBJECTS): %.o: $(SRC)/%.cc $(LIB)/%.h
#$(OBJECTS): %.o: $(SOURCES) $(LIB)/%.h
	@echo "Compiling $<..."
	$(CXX) $(FLAGS) -c $< -o $@

# Linking for HmmAnalyzer
$(ANALYZER_EXECUTABLE): $(ANALYZER_OBJECTS)
	@echo "Linking $(ANALYZER_EXECUTABLE)..."
	$(CXX) $(FLAGS) -o $@ $^ $(LIBS)
	@echo "done"

# Linking for CrekteHistograms
$(HISTOGRAM_EXECUTABLE): $(HISTOGRAM_OBJECTS)
	@echo "Linking $(HISTOGRAM_EXECUTABLE)..."
	$(CXX) $(FLAGS) -o $@ $^ $(LIBS)
	@echo "done"

# Linking for CrekteHistograms
$(SKIM_EXECUTABLE): $(SKIM_OBJECTS)
	@echo "Linking $(SKIM_EXECUTABLE)..."
	$(CXX) $(FLAGS) -o $@ $^ $(LIBS)
	@echo "done"
	
# Specifying the object files as intermediates deletes them automatically after the build process.
.INTERMEDIATE: $(ANALYZER_OBJECTS) $(HISTOGRAM_OBJECTS) $(SKIM_OBJECTS)

# Clean target
.PHONY: clean
clean:
	rm -f $(ANALYZER_OBJECTS) $(HISTOGRAM_OBJECTS) $(SKIM_OBJECTS) $(ANALYZER_EXECUTABLE) $(HISTOGRAM_EXECUTABLE) $(SKIM_EXECUTABLE)
