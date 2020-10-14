from template_fragmenter import *

BACKBONE_NAMES_DICT = {"_N__": 1,
                       "_H__": 2, 
                       "_CA_": 3, 
                       "_C__": 4, 
                       "_O__": 5}

BACKBONE_PARENTS_DICT = {"_N__": 0,
                         "_H__": 1, 
                         "_CA_": 1, 
                         "_C__": 3, 
                         "_O__": 4}

class CovalentOPLS2005(TemplateOPLS2005):
    def __init__(self, template_file):
       super().__init__(template_file)
       self.template_file = template_file
       self.backbone_atoms = {}
       self.non_backbone_atoms = {}
       self.detect_backbone_atoms()

    def detect_backbone_atoms(self):
        for idx, atom in self.list_of_atoms.items():
            if atom.pdb_atom_name in BACKBONE_NAMES_DICT.keys():
                self.backbone_atoms[idx] = atom
            else:
                self.non_backbone_atoms[idx] = atom
        if len(self.backbone_atoms) != len(BACKBONE_NAMES_DICT):
            raise ValueError("The template does not contain all BACKBONE atoms." 
                             "Check which is missing. Content: {} Expected {}".format([x.pdb_atom_name for x in self.backbone_atoms.values()],
                                                                                      BACKBONE_NAMES_DICT.keys()))

    def find_correct_atom_order(self):
        indexes_corrections = []
        for idx, atom in self.backbone_atoms.items():
            indexes_corrections.append((BACKBONE_NAMES_DICT[atom.pdb_atom_name], idx))
        for atom_in_dict, new_idx in zip(self.non_backbone_atoms.items(), \
                                     range(len(self.backbone_atoms), \
                                     len(self.backbone_atoms)+len(self.non_backbone_atoms))):
            indexes_corrections.append((new_idx+1, atom_in_dict[0]))
        return indexes_corrections

    def correct_atom_order(self):
        indexes_relation = self.find_correct_atom_order()
        templ_copy = CovalentOPLS2005(self.template_file)
        self.correct_atom_objects(templ_copy, indexes_relation)
        self.correct_backbone_atoms_parents(indexes_relation)
        # Now we should correct the conectivity tree to define all parents from the new core

    def correct_atom_objects(self, templ_copy, indexes_relation):
        for pair in sorted(indexes_relation):
            new_idx, old_idx = pair
            self.list_of_atoms[new_idx] = templ_copy.list_of_atoms[old_idx]

    def correct_backbone_atoms_parents(self):
        for idx, atom in self.backbone_atoms.items():
            self.list_of_atoms[BACKBONE_NAMES_DICT[atom.pdb_atom_name]].parent_id = BACKBONE_PARENTS_DICT[atom.pdb_atom_name]
