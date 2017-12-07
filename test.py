import ParentChildren

events = [
    # parent has one child, but all characteristics are owned by parent
    { 'parent': 'parentof_A'  , 'child': 'A'       , 'name': 'Parent of A'         },

    # parent has one child, child's name on separate event
    { 'parent': 'parentof_B'  , 'child': 'B'       , 'name': 'Parent of B'         },
    {                           'child': 'B'       , 'name': 'Child of parentof_B' },

    # parent has two children, each via separate event
    { 'parent': 'parentof_C_D', 'child': 'C'       , 'name': 'Parent of C D'       },
    { 'parent': 'parentof_C_D', 'child': 'D'       , 'name': 'Parent of C D'       },

    # orphan
    {                           'child': 'E'       , 'name': 'Child of NUL'        },

    # parent has two children defined on same event
    { 'parent': 'parentof_F_G', 'child': ['F', 'G'], 'name': 'Parent of F G'       },

    # parent has one child defined later.  relationship and characteristics in separate events
    { 'parent': 'parentof_H'  ,                      'name': 'Parent of H'         },
    {                           'child': 'H'       , 'name': 'Child of H'          },
    { 'parent': 'parentof_H'  , 'child': 'H'       ,                               },

    # parent has one child, but later child characteristics event has multiple child values
    { 'parent': 'parentof_I'  , 'child': 'I'       , 'name': 'Parent of I not J'  },
    {                           'child': ['I', 'J'], 'name': 'Child I and J'      },

    # no parent or child
    {                                                'name': 'Unrelated'           },
]

expected_parents = {
    'parentof_A': {
        'parent': set(['parentof_A']),
        'child' : set(['A']),
        'name'  : set(['Parent of A']),
    },
    'parentof_B': {
        'parent': set(['parentof_B']),
        'child' : set(['B']),
        'name'  : set(['Parent of B', 'Child of parentof_B']),
    },
    'parentof_C_D': {
        'parent': set(['parentof_C_D']),
        'child' : set(['C', 'D']),
        'name'  : set(['Parent of C D']),
    },
    'parentof_F_G': {
        'parent': set(['parentof_F_G']),
        'child' : set(['F', 'G']),
        'name'  : set(['Parent of F G']),
    },
    'parentof_H': {
        'parent': set(['parentof_H']),
        'child' : set(['H']),
        'name'  : set(['Parent of H', 'Child of H']),
    },
    'parentof_I': {
        'parent': set(['parentof_I']),
        'child' : set(['I', 'J']),
        'name'  : set(['Parent of I not J', 'Child I and J']),
    },
}

expected_orphans = {
    'E': {
        'child': set(['E']),
        'name':  set(['Child of NUL']),
    },
    'J': {
        'child': set(['I', 'J']),
        'name':  set(['Child I and J']),
    },
}

families = ParentChildren.Families()

for event in events:
    families.process(event)

assert( len(list(families.family_units())) == len(expected_parents) )
for family_unit in families.family_units():
    assert( len(family_unit.characteristics['parent']) == 1 )
    parent_name = family_unit.characteristics['parent'].copy().pop()
    assert( parent_name in expected_parents )
    expected_parent = expected_parents[parent_name]
    assert( expected_parent == family_unit.characteristics )

assert( len(list(families.orphans())) == len(expected_orphans) )
for orphan_result in families.orphans():
    orphan_name = orphan_result['name']
    orphan      = orphan_result['individual']

    assert( orphan_name in expected_orphans )
    expected_orphan = expected_orphans[orphan_name]
    assert( expected_orphan == orphan.characteristics )
