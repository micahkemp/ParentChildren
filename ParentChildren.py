class Individual:
    def __init__(self):
        self.characteristics = {}

    def has_characteristics(self, characteristics):
        for key in characteristics:
            self.characteristics.setdefault(key, set())
            if isinstance(characteristics[key], list) or isinstance(characteristics[key], set):
                for value in characteristics[key]:
                    self.characteristics[key].add(value)
            else:
                self.characteristics[key].add(characteristics[key])
        
class Parent(Individual):
    def __init__(self):
        Individual.__init__(self)
        self.children = set()

    def has_children(self, children):
        for child in children:
            self.children.add(child)

class Families:
    def __init__(self):
        self._parents = {}
        self.individuals = {}

    def individual(self, individual_name):
        if not individual_name in self.individuals:
            self.individuals[individual_name] = Individual()
        return self.individuals[individual_name]

    def parent(self, parent_name):
        if not parent_name in self._parents:
            self._parents[parent_name] = Parent()
        return self._parents[parent_name]

    def parent_children(self, parent_name):
        for child in self._parents[parent_name].children:
            if child in self.individuals:
                yield self.individuals[child]

    def parents(self):
        for parent in self._parents:
            yield self._parents[parent]

    def families(self):
        for parent_name in self._parents:
            parent = self._parents[parent_name]
            family = Individual()
            family.has_characteristics(parent.characteristics)
            for child_name in parent.children:
                child = self.individual(child_name)
                family.has_characteristics(child.characteristics)
            yield family
