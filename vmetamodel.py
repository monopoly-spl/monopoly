from z3 import Bool, And, Or, Not, BoolRef, BoolVal, simplify
from dataclasses import dataclass, field
from typing import List, Optional, Union, Tuple
from variational import Variational

from metamodel import *

@dataclass
class vAttribute:
    name: str
    type: TypeRef
    multiplicity: Multiplicity = field(default_factory=lambda: Multiplicity(1,1))
    presence_condition: Optional[BoolRef] = None  

@dataclass
class vReference:
    name: str
    type: TypeRef
    multiplicity: Multiplicity = field(default_factory=lambda: Multiplicity(1,1))
    containment: bool = False
    presence_condition: Optional[BoolRef] = None

Feature = Union[vAttribute, vReference]

@dataclass
class vOperation:
    name: str
    return_type: TypeRef
    multiplicity: Multiplicity = field(default_factory=lambda: Multiplicity(1,1))
    body: Optional[str] = None
    presence_condition: Optional[BoolRef] = None


@dataclass
class vModifier:
    condition: BoolRef                  # presence condition for the modifier
    extend: List[str] = field(default_factory=list)   # interfaces or classes to extend
    reduce: List[str] = field(default_factory=list)   # optional reductions (like in Edge)

@dataclass
class vInvariant:
    name: str
    expression: str
    presence_condition: Optional[BoolRef] = None

@dataclass
class vMetaClass:
    name: str
    attributes: List[vAttribute] = field(default_factory=list)
    references: List[vReference] = field(default_factory=list)
    operations: List[vOperation] = field(default_factory=list)
    invariants: List[vInvariant] = field(default_factory=list)
    presence_condition: Optional[BoolRef] = None

    def get_reference_pc(self, name : str):
        for r in self.references:
            if r.name == name: 
                return r.presence_condition 
        return None 
    
    def get_all_refs(self):
        refs = []
        for r in self.references: 
            refs += [(r.name, r.presence_condition)]
        return refs 

    def get_attribute_pc(self, name : str):
        for a in self.attributes:
            if a.name == name: 
                return a.presence_condition
        return None 

    def get_all_attrs(self):
        attrs = []
        for a in self.attributes:
            attrs += [(a.name, a.presence_condition)]
        return attrs 
    
    def get_operation_pc(self, name : str):
        for o in self.operations:
            if o.name == name: 
                return o.presence_condition
        return None 
    
    def get_all_ops(self):
        ops = []
        for o in self.operations:
            ops += [(o.name, o.presence_condition)]
        return ops 
    
    def get_invariant_pc(self, name : str):
        for inv in self.invariants:
            if inv.name == name: 
                return inv.presence_condition
        return None 

    def get_all_invs(self):
        invs = []
        for inv in self.invariants:
            invs += [(inv.name, inv.presence_condition)]
        return invs 


@dataclass
class vEnum:
    name: str
    literals: List[EnumLiteral] = field(default_factory=list)
    presence_condition: Optional[BoolRef] = None


@dataclass
class vMetamodel:
    name: str
    ns_uri: Optional[str] = None
    classes: List[vMetaClass] = field(default_factory=list)
    enums: List[vEnum] = field(default_factory=list)
    inheritance : List[Tuple[Tuple[str,str],BoolRef]] = field(default_factory=list)


class VariationalMetamodel(Variational):
    def __init__(self, features, model, featModel):
        super().__init__(features, model, featModel)

    def get_class(self, name : str):
        for c in self.model.classes:
            if c.name == name: 
                return c 
        return None
    
    def derive(self, config):
        # Derive attributes
        def derive_attributes(attrs: list[vAttribute]) -> list[Attribute]:
            result = []
            for a in attrs:
                # print(a)
                if self.present(a.presence_condition,config):
                    result.append(Attribute(
                        name=a.name,
                        type=a.type,
                        multiplicity=a.multiplicity
                    ))
            return result

        # Derive references
        def derive_references(refs: list[vReference]) -> list[Reference]:
            result = []
            for r in refs:
                if self.present(r.presence_condition,config):
                    result.append(Reference(
                        name=r.name,
                        type=r.type,
                        multiplicity=r.multiplicity,
                        containment=r.containment
                    ))
            return result

        # Derive operations
        def derive_operations(ops: list[vOperation]) -> list[Operation]:
            result = []
            for op in ops:
                if self.present(op.presence_condition,config):
                    result.append(Operation(
                        name=op.name,
                        return_type=op.return_type,
                        multiplicity=op.multiplicity,
                        body=op.body
                    ))
            return result

        # Derive invariants
        def derive_invariants(invs: list[vInvariant]) -> list[Invariant]:
            result = []
            for inv in invs:
                if self.present(inv.presence_condition,config):
                    result.append(Invariant(
                        name=inv.name,
                        expression=inv.expression
                    ))
            return result

        # Derive classes
        derived_classes = []
        for c in self.model.classes:
            # print(c.name)
            if self.present(c.presence_condition,config):
                derived_classes.append(MetaClass(
                    name=c.name,
                    attributes=derive_attributes(c.attributes),
                    references=derive_references(c.references),
                    operations=derive_operations(c.operations),
                    invariants=derive_invariants(c.invariants),
                ))

        # Derive enums
        derived_enums = []
        for e in self.model.enums:
            if self.present(e.presence_condition,config):
                # Optionally prune literals based on presence conditions if they were variational
                derived_enums.append(Enum(
                    name=e.name,
                    literals=e.literals
                ))
        
        derived_inheritance = []
        for inh in self.model.inheritance:
            rel = inh[0]
            pc = inh[1]
            if self.present(pc, config):
                derived_inheritance.append(rel)

        return Metamodel(
            name=self.model.name + "_derived_product",
            ns_uri=None,
            classes=derived_classes,
            enums=derived_enums,
            inheritance = derived_inheritance
        )
    
    def upward(self, p):

        def classUpward(c_prod:MetaClass, c_annotated: vMetaClass):    
            ## all references in c_prod must be present
            ref_pcs = []
            for r in c_prod.references: 
                check = c_annotated.get_reference_pc(r.name)
                if check is not None:
                    ref_pcs += [check]

            # all attributes in c_prod must be present 
            attr_pcs = []
            for a in c_prod.attributes: 
                check = c_annotated.get_attribute_pc(a.name)
                if check is not None:
                    attr_pcs += [check]

            # all operations in c_prod must be present 
            op_pcs = []
            for o in c_prod.operations: 
                check = c_annotated.get_operation_pc(o.name)
                if check is not None:
                    op_pcs += [check]

            # all invariants in c_prod must be present 
            inv_pcs = []
            for inv in c_prod.invariants: 
                check = c_annotated.get_invariant_pc(inv.name)
                if check is not None:
                    inv_pcs += [check]
            return ref_pcs + attr_pcs + op_pcs + inv_pcs

        constraints = []
        classes = p.classes 
        for c in classes: 
            ann_c = self.get_class(c.name)
            if ann_c is not None:
                constraints += [ann_c.presence_condition]
                constraints += classUpward(c, ann_c)
        
        for inh in p.inheritance:
            for x in self.model.inheritance:
                if x[0] == inh[0]:
                    constraints += [x[1]]
        
        return simplify(And(constraints))
         
    
    def downward(self, p):
        constraints = []

        def class_downward(c_prod: MetaClass, c_ann : vMetaClass):
            constraints = []
            # no references which are not in c_prod 
            prod_refs = c_prod.references
            for ref in c_ann.references:
                if all([r.name != ref.name for r in prod_refs]):
                    constraints += [Not(ref.presence_condition)]

            # no attributes which are not in c_prod 
            prod_attrs = c_prod.attributes
            for attr in c_ann.attributes:
                if all([a.name != attr.name for a in prod_attrs]):
                    constraints += [Not(attr.presence_condition)]

            # no operations which are not in c_prod 
            prod_ops = c_prod.operations
            for op in c_ann.operations:
                if all([o.name != op.name for o in prod_ops]):
                    constraints += [Not(op.presence_condition)]

            # no invariants which are not in c_prod
            prod_invs = c_prod.invariants
            for inv in c_ann.invariants:
                if all([i.name != inv.name for i in prod_invs]):
                    constraints += [Not(inv.presence_condition)]

            return constraints
        
        for cls in self.model.classes:
            if all([c.name !=  cls.name for c in p.classes]):
                constraints += [Not(cls.presence_condition)]

        for c in p.classes:
            ann_c = self.get_class(c.name)
            if ann_c is not None:
                constraints += class_downward(c, ann_c)
       
        all_inheritances = self.model.inheritance 
        inheritances = p.inheritance 
        for inh in all_inheritances:
            # print(all([x[0][0] != inh[0][0] and x[0][1] != inh[0][1] for x in inheritances]))
            if all([x != inh[0] for x in inheritances]):
                constraints += [Not(inh[1])]

        return simplify(And(constraints))
    


