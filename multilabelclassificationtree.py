from functools import partial
from statistics import mode
import math
import collections


def entropy(class_probabilities):
    """given a list of class probabilities, compute the entropy"""
    return sum(-p * math.log(p, 2)
               for p in class_probabilities
               if p)


def class_probabilities(labels):
    total_count = len(labels)
    return [count / total_count
            for count in collections.Counter(labels).values()]


def data_entropy(labeled_data):
    labels = [label for _, label in labeled_data]
    probabilities = class_probabilities(labels)
    return entropy(probabilities)


def partition_entropy(subsets):
    """find entropy from this partition of data into subsets
    subsets is a list of lists of labeled data"""
    total_count = sum(len(subset) for subset in subsets)
    return sum(data_entropy(subset) * len(subset) / total_count
               for subset in subsets)


def partition_by(inputs, attribute):
    """each input is a pair (attriute_dict,label).
    returns a dict : attribute_value -> inputs"""
    groups = collections.defaultdict(list)
    for input in inputs:
        key = input[0][attribute]  # get the value of the specified attribute
        groups[key].append(input)  # then add this input to the correct list
    return groups


def partition_entropy_by(inputs, attribute):
    """computes the entropy corresponding to the given partition"""
    partitions = partition_by(inputs, attribute)
    return partition_entropy(partitions.values())


def build_tree_id3(inputs, split_candidates=None):
    # if this is our first pass
    # all keys of the first input are split candidates

    if split_candidates is None:
        split_candidates = inputs[0][0].keys()

    # count different classes
    num_inputs = len(inputs)
    num_different_classes = len(set([label for item, label in inputs if label]))

    if num_different_classes == 1: return (
        [label for item, label in inputs if label])  # only one class? Return this one
    if num_different_classes == num_inputs: return False  # all classes are different?

    if not split_candidates:
        return max(set(inputs), key=inputs.count)

    # otherwise, split on the best attribute
    best_attribute = min(split_candidates, key=partial(partition_entropy_by, inputs))

    partitions = partition_by(inputs, best_attribute)
    new_candidates = [a for a in split_candidates
                      if a != best_attribute]

    # recursively build the subtrees
    subtrees = {attribute_value: build_tree_id3(subset, new_candidates)
                for attribute_value,
                    subset in partitions.items()}

    #   subtrees[None] = max(inputs, key=collections.Counter(inputs).get) # if tree is empty we give the most frequent one
    subtrees[None] = None

    # print("best_attribute: ", best_attribute)
    # print("subtrees: ", subtrees)

    return (best_attribute, subtrees)


def classify(tree, segments, data):
    """classify the input using the given decision tree"""
    if len(tree) == 1 and tree[0] in segments:
        return tree

    # otherwise this tree consists of an attribute to split on
    # and a dictionary whose keys are values of that attribute
    # and whose values of are subtrees to consider next
    attribute, subtree_dict = tree

    subtree_key = data.get(attribute)  # None if input is missing in attribute

    if subtree_key not in subtree_dict:  # if no subtree for key
        subtree_key = None

    subtree = subtree_dict[subtree_key]
    return classify(subtree, segments, data)


def main():
    data = [({'Age': 20, 'Quartier': 'A', 'Income': 600}, 'PartyB'),
            ({'Age': 30, 'Quartier': 'B', 'Income': 675}, "PartyA"),
            ({'Age': 40, 'Quartier': 'C', 'Income': 3000}, 'ABS'),
            ({'Age': 50, 'Quartier': 'D', 'Income': 4000}, 'ABS')]
    tree = build_tree_id3(data)
    segments = ['PartyA', 'PartyB', 'ABS']
    result = classify(tree, segments, {'Age': 20, 'Quartier': 'A', 'Income': 4000})
    print({'Age': 20, 'Quartier': 'A', 'Income': 4000})
    print(result)


if __name__ == "__main__":
    main()
