# multilabelclassificationtree

Here is a project to adapt a binary decision tree algorithm to one that can decide on multiple tags. 

For instance if we have a party with several potential labels:

```
data = [({'Age': 1, 'Quartier': 'A', 'Income': 10}, 'PartyB'),
 ({'Age': 2, 'Quartier': 'B', 'Income': 20}, "PartyA"),
 ({'Age': 3, 'Quartier': 'C', 'Income': 30}, 'ABS'),
 ({'Age': 4, 'Quartier': 'D', 'Income': 40}, 'ABS')]
```


I want to be able to predict the etiquette of the following: `{'Age': 1, 'Quartier': 'A', 'Income': 15}` 