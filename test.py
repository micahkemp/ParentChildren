import ParentChildren

parentfield = 'parent'
childfield = 'child'

events = [
    { 'parent': 'parentof_A'  , 'child': 'A',   'name': 'Parent of A'   },
    { 'parent': 'parentof_B'  , 'child': 'B',   'name': 'Parent of B'   },
    { 'parent': 'parentof_C_D', 'child': 'C',   'name': 'Parent of C D' },
    { 'parent': 'parentof_C_D', 'child': 'D',   'name': 'Parent of C D' },
]

families = ParentChildren.Families()

for event in events:
    if parentfield in event:
        parent = families.parent(event[parentfield])
        parent.has_characteristics(event)
        if childfield in event:
            parent.has_children([event[childfield]])
    else:
        if childfield in event:
            child = families.individual(event[childfield])
            child.has_characteristics(event)

for parent in families.families():
    print parent.characteristics
