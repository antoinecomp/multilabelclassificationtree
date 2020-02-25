# multilabelclassificationtree

Here is a project to adapt a [binary decision tree algorithm created by Joel Grus](https://github.com/joelgrus/data-science-from-scratch/blob/master/scratch/decision_trees.py), the man who wrote Data Science from Scratch, to one that can decide on multiple tags. 

For instance if we have a party with several potential labels:

```
data = [({'Age': 1, 'Quartier': 'A', 'Income': 10}, 'PartyB'),
 ({'Age': 2, 'Quartier': 'B', 'Income': 20}, "PartyA"),
 ({'Age': 3, 'Quartier': 'C', 'Income': 30}, 'ABS'),
 ({'Age': 4, 'Quartier': 'D', 'Income': 40}, 'ABS')]
```


I want to be able to predict the etiquette of the following: `{'Age': 1, 'Quartier': 'A', 'Income': 15}`.