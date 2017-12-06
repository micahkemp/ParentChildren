class Individual:
    def __init__(self):
        self.characteristics = {}

    def has_characteristics(self, characteristics):
        for key in characteristics:
            #print "found %s characteristic %s" % (key, characteristics[key])
            self.characteristics.setdefault(key, set())
            if isinstance(characteristics[key], list) or isinstance(characteristics[key], set):
                for value in characteristics[key]:
                    self.characteristics[key].add(value)
            else:
                self.characteristics[key].add(characteristics[key])

        #print "after has_characteristics %s" % self.characteristics
        
#class Parent(Individual):
class Parent:
    def __init__(self):
#        Individual.__init__(self)
        self.children = set()

    def has_children(self, children):
        for child in children:
            self.children.add(child)

class Families:
    def __init__(self, parentfield='parent', childfield='child'):
        self._parents     = {}
        self._children    = set()
        self._individuals = {}
        self._parentfield = parentfield
        self._childfield  = childfield

    def process(self, event):
        individual_name = None

        if self._parentfield in event:
            individual_name = event[self._parentfield]
            parent = self.parent_with_name(individual_name)
            if self._childfield in event:
                children = event[self._childfield]
                if not isinstance(children, list) or isinstance(children, set):
                    children = [children]
                for child in children:
                    self._children.add(child)
                    parent.has_children([child])
        elif self._childfield in event:
            individual_name = event[self._childfield]

        if individual_name:
            self.individual_with_name(individual_name).has_characteristics(event)

    def individual_with_name(self, individual_name):
        if not individual_name in self._individuals:
            self._individuals[individual_name] = Individual()
        return self._individuals[individual_name]

    def parent_with_name(self, parent_name):
        if not parent_name in self._parents:
            self._parents[parent_name] = Parent()
        return self._parents[parent_name]

    def parent_names(self):
        for parent_name in self._parents:
            yield parent_name

    def family_units(self):
        for parent_name in self.parent_names():
            parent_individual = self.individual_with_name(parent_name)
            family_unit = Individual()
            parent = self._parents[parent_name]
            family_unit.has_characteristics(parent_individual.characteristics)
            for child_name in parent.children:
                child = self.individual_with_name(child_name)
                family_unit.has_characteristics(child.characteristics)
            #print "family unit characteristics %s" % family_unit.characteristics
            yield family_unit

    def orphans(self):
        for individual_name in self._individuals:
            if individual_name not in self._children and individual_name not in self._parents:
                orphan = self._individuals[individual_name]
                yield orphan
