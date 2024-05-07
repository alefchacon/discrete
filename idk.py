from typing import List
from ucimlrepo import fetch_ucirepo 
import numpy as np

'''
- `values` y `class_values` deben estar alineados.
'''
def get_CAIM(
    intervals: List,
    values: List[float]):
  
  caim = 0
  '''
  {(min, max) : [valor1, valor2, valorn]}
  (4.3  , 4.45): [4.4, 4.4, 4.4]
  (4.45 , 7.9 ): [4.6, 4.6, 4.6, 4.6, 4.7, 4.7, 4.8, 4.8, 4.8, 4.8, 4.8, 4.9, 4.9, 4.9, 4.9, 4.9, 4.9, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.1, 5.1, 5.1, 5.1, 5.1, 5.1, 5.1, 5.1, 5.1, 5.2, 5.2, 5.2, 5.2, 5.3, 5.4, 5.4, 5.4, 5.4, 5.4, 5.4, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.6, 5.6, 5.6, 5.6, 5.6, ...]
  '''
  columns = {}

  max_value = max(values)

  for interval in intervals:
    columns[interval] = []
    for value in values:

      '''
      Formar columnas de la matriz:
      '''
      if interval[0] <= value < interval[1]:
        if interval in columns:
          columns[interval].append(value)


      elif (value == max_value) and value <= interval[1]:
        if interval in columns:
          columns[interval].append(value)


    '''
    maxr is the maximum value among all qir values (maximum value within
    the rth column of the quanta matrix), i=1,2,...,S
    '''
    if interval in columns:
      if (len(columns[interval]) > 0):
        max_interval_value = max(columns[interval])
    else:
      max_interval_value = 0

    '''
    M+r is the total number of continuous values of attribute F that 
    are within the interval (dr-1, dr].
    '''
    M_interval_values = len(columns[interval])

    if M_interval_values > 0:
      caim += (max_interval_value ** 2) / M_interval_values

  return caim / len(intervals)


def get_intervals(boundaries: List[float]):
  intervals = [(boundaries[i], boundaries[i + 1]) 
          for i in range(len(boundaries) - 1)] 
  return intervals


iris = fetch_ucirepo(id=53) 
  
X = iris.data.features 
y = iris.data.targets 
DATA    = X["sepal length"].to_list()
S_CLASSES  = len(set(y["class"].to_list()) )
DATA.sort()

'''
1.1.  find maximum (dn) and minimum (d0) values of Fi
'''
MIN_MAX = [min(DATA), max(DATA)] 

'''
1.2   form a set of all distinct values of Fi in ascending order, and initialize all possible 
      interval boundaries B with minimum, maximum and all the midpoints of all the 
      adjacent pairs in the set
'''
B_boundaries = []
unique_sorted_values = sorted(set(DATA), reverse=False) 
B_boundaries = [(unique_sorted_values[i] + unique_sorted_values[i+1]) / 2 
            for i in range(len(unique_sorted_values) - 1)]

'''
1.3   set the initial discretization scheme as D :{[d ,d ]} 0 n , set GlobalCAIM=0 
2.1 initialize k=1; 
'''
accepted_boundaries = sorted(MIN_MAX) # puntos medios
global_caim = 0
k = 1


def make_schema():
  global global_caim
  global k
  '''
  Obtener los CAIMs de todos los boundaries, dado el esquema actual.
  '''
  caims = []
  for boundary in B_boundaries:

    '''
    2.2.  tentatively add an inner boundary, which is not already in D, from B, and calculate 
          corresponding CAIM value 
    '''
    if (boundary not in accepted_boundaries):
      possible_boundaries = accepted_boundaries + [boundary]
      possible_boundaries.sort()
      possible_intervals = get_intervals(boundaries=possible_boundaries)
      caim = get_CAIM(intervals=possible_intervals, values=DATA)
      caims.append(caim)

  best_caim = max(caims)
  best_caim_index = caims.index(best_caim)
  
  '''
  2.3.  after all the tentative additions have been tried accept the one with the highest value 
        of CAIM 
  2.4.  if (CAIM > GlobalCAIM or k<S) then update D with the accepted in step 2.3 
        boundary and set GlobalCAIM=CAIM, else terminate
  2.5.  set k=k+1 and go to 2.2 
  '''
  if (best_caim > global_caim or k < S_CLASSES):
    next_boundary = B_boundaries[best_caim_index]
    accepted_boundaries.append(next_boundary)
    global_caim = best_caim
    k += 1

def get_schema():
  for k in range(S_CLASSES):
    make_schema()
  return get_intervals(accepted_boundaries)

print(get_schema())

print(B_boundaries)


accepted_boundaries.sort()
print(DATA)
print(X)



'''
Grafica
'''
import matplotlib.pyplot as plt

intervals = get_intervals(accepted_boundaries)
columns = {}
max_value = max(DATA)
data = []
labels = set()
for interval in intervals:
    for value in DATA:
      label = str(interval)
      labels.add(label)
      if interval[0] <= value < interval[1]:
        data.append((value, label))
          
      elif (value == max_value) and value <= interval[1]:
        data.append((value, label))

fig, ax = plt.subplots()

colorDict ={}
colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'brown', 'black', 'pink', 'cyan']
for index, label in enumerate(labels):
  colorDict[label] = colors[index]

label_added = {}
for point, label in data:
    if label not in label_added:
        ax.scatter(point, 0, color=colorDict[label], label=label)
        label_added[label] = True
    else:
        ax.scatter(point, 0, color=colorDict[label])

for interval in accepted_boundaries:
    plt.axvline(x=interval, color='gray', linestyle='--')


ax.set_xlabel('Intervalos')
ax.set_ylabel('')
ax.set_title('Resultados')
ax.legend()


plt.show()