from ctypes import sizeof
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import f_oneway
import datetime as dt
import csv

def read_numbers_from_txt(file_path):
    numbers = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                number = float(line.strip())  # Assuming numbers are floats; use int() if they're integers
                if number == -999:
                    numbers.append(0)
                else: 
                    numbers.append(number)
        return numbers
    except FileNotFoundError:
        print("File not found!")
        return None
    except ValueError:
        print("Error: Unable to convert data to number.")
        return None
    
def check_homogeneity(arrays):
    homogeneity_results = []
    for idx, array in enumerate(arrays):
        try:
            statistic, p_value = f_oneway(*arrays)
            homogeneity_results.append((idx, statistic, p_value))
        except ValueError as e:
            print(f"Error with array {idx}: {e}")
            homogeneity_results.append((idx, None, None))
    return homogeneity_results

def create_index_arrays(data_arrays):
    index_arrays = []
    for array in data_arrays:
        index_arrays.append(list(range(len(array))))
    return index_arrays

def find_percentile(data_arrays, index_arrays, percentileVal):
    percentile_values = []
    percentile_indexes = []
    for data, indexes in zip(data_arrays, index_arrays):
        data = np.array(data)
        indexes = np.array(indexes)
        percentile = np.percentile(data, percentileVal)
        values = data[data >= percentile]
        indexes = indexes[data >= percentile]
        percentile_values.append(values)
        percentile_indexes.append(indexes)
    return percentile_values, percentile_indexes

def calculateDatesByOffsetArray(offset_days):
    importantDates = []
    for i in range(0, len(offset_days)):    
        newDate = startDate + dt.timedelta(days=int(offset_days[i]))
        importantDates.append(newDate)
    
    return np.array(importantDates)

def calcDateTimeForArrayReturnString(arrayOfArrayOfOffsets):
    dtDates = None
    arrayOfStringDates = []
    for array in arrayOfArrayOfOffsets:
        dtDates = calculateDatesByOffsetArray(array)
        stringDate = []
        for each in dtDates:
            stringDate.append(each.strftime("%Y-%m-%d"))
        dtDates = None
        arrayOfStringDates.append(stringDate)
    return arrayOfStringDates

def writeStringsToCSV(strings, filename):
    """
    Write an array of strings to a CSV file.

    Parameters:
    - strings: List of strings to be written to the CSV file.
    - filename: Name of the CSV file to write.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\n')
        writer.writerow(strings)
        
def exportArraySeparateCSV(arrayOfImpDates):
    i = 0
    for each in arrayOfImpDates:
        writeStringsToCSV(each, 'output95_'+ str(i) + '.csv')
        i += 1
    print("done exporting")

# Example usage:
file_path = r"D:\DOCs, PDFs\012 PCA Projekat\dataFile\NoviSadPrecOBS.txt"  
numbers_arrayNS = read_numbers_from_txt(file_path)
file_path = r"D:\DOCs, PDFs\012 PCA Projekat\dataFile\PalicPrecOBS.txt"  
numbers_arrayPA = read_numbers_from_txt(file_path)
file_path = r"D:\DOCs, PDFs\012 PCA Projekat\dataFile\VrsacPrecOBS.txt"  
numbers_arrayVR = read_numbers_from_txt(file_path)
file_path = r"D:\DOCs, PDFs\012 PCA Projekat\dataFile\ZrenjaninPrecOBS.txt"  
numbers_arrayZR = read_numbers_from_txt(file_path)
file_path = r"D:\DOCs, PDFs\012 PCA Projekat\dataFile\SremskaMitrovicaPrecOBS.txt"  
numbers_arraySM = read_numbers_from_txt(file_path)
file_path = r"D:\DOCs, PDFs\012 PCA Projekat\dataFile\SomborPrecOBS.txt"  
numbers_arraySO = read_numbers_from_txt(file_path)

"""
if numbers_array is not None:
    print("Numbers array:", numbers_array)
"""
numbers_arrayNS = np.array(numbers_arrayNS)
numbers_arraySO = np.array(numbers_arraySO)
numbers_arrayVR = np.array(numbers_arrayVR)
numbers_arrayZR = np.array(numbers_arrayZR)
numbers_arrayPA = np.array(numbers_arrayPA)
numbers_arraySM = np.array(numbers_arraySM)

dataSetsListValues = []
dataSetsListValues.append(numbers_arrayNS[4749:])
dataSetsListValues.append(numbers_arrayZR[4749:])
dataSetsListValues.append(numbers_arrayVR[4749:])                            
dataSetsListValues.append(numbers_arrayPA[4749:])
dataSetsListValues.append(numbers_arraySO[4749:])
dataSetsListValues.append(numbers_arraySM[4749:])

homogeneity_results = check_homogeneity(dataSetsListValues)
for idx, result in enumerate(homogeneity_results):
    print(f"Array {idx}: Statistic = {result[1]}, p-value = {result[2]}")

dataSetsListValuesIndexes = create_index_arrays(dataSetsListValues)

data_arrays = dataSetsListValues
index_arrays = dataSetsListValuesIndexes

# Find values and indexes in the 95th percentile
values_95, indexes_95 = find_percentile(data_arrays, index_arrays, 95)

# Find values and indexes in the 99th percentile
values_99, indexes_99 = find_percentile(data_arrays, index_arrays, 99)

# Plotting line for values in the 95th percentile
plt.plot(dataSetsListValuesIndexes[0], dataSetsListValues[0], label = "Precipitation data 1948-2016")
plt.scatter(indexes_95[0], values_95[0], color='red', label='95th Percentile Values')
plt.scatter(indexes_99[0], values_99[0], color='blue', label='99th Percentile Values')
#SHOW WINDOW
#plt.xlim(17500, 17865)

# Adding labels and legend
plt.xlabel('Day Index') 
plt.ylabel('Precipitation')
plt.title('Precipitation Data')
plt.legend()

# Show plot
plt.grid(True)
#plt.show()


"""from scipy.stats import levene

def check_homogeneity(arrays):
    homogeneity_results = []
    for idx, array in enumerate(arrays):
        try:
            # Preprocessing: Remove NaN values and check for constant arrays
            array = np.array(array)
            array = array[~np.isnan(array)]
            if len(np.unique(array)) <= 1:
                print(f"Array {idx + 1} is constant or contains NaN values.")
                homogeneity_results.append((idx + 1, None, None))
                continue
            
            # Perform Levene variance test
            stat, p = levene(*array, center='median')  # Using 'median' centering to make the test more robust
            homogeneity_results.append((idx + 1, stat, p))
        except ValueError as e:
            print(f"Error in array {idx + 1}: {e}")
            homogeneity_results.append((idx + 1, None, None))
        except ZeroDivisionError:
            print(f"Zero division error in array {idx + 1}. Adding a small constant to denominator.")
            constant = np.finfo(np.float64).eps  # Smallest positive floating-point number
            try:
                stat, p = levene(*array, center='median')
                homogeneity_results.append((idx + 1, stat, p))
            except ValueError as e:
                print(f"Error in array {idx + 1}: {e}")
                homogeneity_results.append((idx + 1, None, None))
        except FloatingPointError:
            print(f"Floating point error in array {idx + 1}. Replacing infinite values.")
            array = np.nan_to_num(array, nan=np.nan, posinf=np.nan, neginf=np.nan)
            try:
                stat, p = levene(*array, center='median')
                homogeneity_results.append((idx + 1, stat, p))
            except ValueError as e:
                print(f"Error in array {idx + 1}: {e}")
                homogeneity_results.append((idx + 1, None, None))
    return homogeneity_results

# Example usage:
results = check_homogeneity(dataSetsListValues)

for idx, result in enumerate(results):
    array_num, stat, p = result
    if stat is not None and p is not None:
        print(f"Array {array_num}: Levene statistic = {stat}, p-value = {p}")
        if p > 0.05:
            print("  Homogeneity is supported (p > 0.05)")
        else:
            print("  Homogeneity is not supported (p <= 0.05)")
    else:
        print(f"Array {array_num}: Error in homogeneity test.")

"""
"""plt.plot(dataSetsListValuesIndexes[3], dataSetsListValues[3])
plt.plot((percentile_values95[0]), (percentile_values95[1]))
plt.show()"""

# Starting date
startDate = dt.date(1961, 1, 1)
print("Starting date:", startDate)

# Offset in days for 

importantDatesArray = calcDateTimeForArrayReturnString(indexes_99)
exportArraySeparateCSV(importantDatesArray)

importantDatesArray = calcDateTimeForArrayReturnString(indexes_95)
exportArraySeparateCSV(importantDatesArray)


    
            
            
        

    
    
    
    



        
