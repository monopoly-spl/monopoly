from dataclasses import dataclass, field
from typing import List, Optional, Union,Tuple

# ---------------------------
# BASIC TYPES
# ---------------------------

@dataclass
class TypeRef:
    name: str

@dataclass
class Multiplicity:
    lower: int = 0
    upper: Optional[int] = None  # None = *

@dataclass
class Attribute:
    name: str
    type: TypeRef
    multiplicity: Multiplicity = field(default_factory=lambda: Multiplicity(1,1))

@dataclass
class Reference:
    name: str
    type: TypeRef
    multiplicity: Multiplicity = field(default_factory=lambda: Multiplicity(1,1))
    containment: bool = False

Feature = Union[Attribute, Reference]


@dataclass
class Operation:
    name: str
    return_type: TypeRef
    multiplicity: Multiplicity = field(default_factory=lambda: Multiplicity(1,1))
    body: Optional[str] = None

@dataclass
class Invariant:
    name: str
    expression: str


@dataclass
class MetaClass:
    name: str
    attributes: List[Attribute] = field(default_factory=list)
    references: List[Reference] = field(default_factory=list)
    operations: List[Operation] = field(default_factory=list)
    invariants: List[Invariant] = field(default_factory=list)
    superclasses: List[Tuple[str,str]] = field(default_factory=list)


@dataclass
class EnumLiteral:
    name: str

@dataclass
class Enum:
    name: str
    literals: List[EnumLiteral] = field(default_factory=list)


@dataclass
class Metamodel:
    name: str
    ns_uri: Optional[str] = None
    classes: List[MetaClass] = field(default_factory=list)
    enums: List[Enum] = field(default_factory=list)
    inheritance : List[Tuple[MetaClass,MetaClass]] = field(default_factory=list)

def pretty_print_package(pkg):
    print(f"Package: {pkg.name} (ns_uri={pkg.ns_uri})\n")
    
    for cls in pkg.classes:
        # Header: class name + inheritance
        supers = f" : {', '.join(cls.superclasses)}" if cls.superclasses else ""
        print(f"Class {cls.name}{supers}")
        
        # Attributes
        if cls.attributes:
            print("  Attributes:")
            for attr in cls.attributes:
                upper = '*' if attr.multiplicity.upper is None else attr.multiplicity.upper
                print(f"    - {attr.name} : {attr.type.name}[{attr.multiplicity.lower}..{upper}]")
        
        # References
        if cls.references:
            print("  References:")
            for ref in cls.references:
                upper = '*' if ref.multiplicity.upper is None else ref.multiplicity.upper
                cont = " (composes)" if ref.containment else ""
                print(f"    - {ref.name} : {ref.type.name}[{ref.multiplicity.lower}..{upper}]{cont}")
        
        # Operations
        if cls.operations:
            print("  Operations:")
            for op in cls.operations:
                upper = '*' if op.multiplicity.upper is None else op.multiplicity.upper
                print(f"    - {op.name}() : {op.return_type.name}[{op.multiplicity.lower}..{upper}]")
        
        # Invariants
        if cls.invariants:
            print("  Invariants:")
            for inv in cls.invariants:
                print(f"    - {inv.name} : {inv.expression}")
        
        print()  # blank line between classes
    
    # Enums
    if pkg.enums:
        print("Enums:")
        for e in pkg.enums:
            literals = ', '.join(l.name for l in e.literals)
            print(f"  {e.name} = {{ {literals} }}")
    if pkg.inheritance: 
        print("Inheritances:")
        for inh in pkg.inheritance:
            print(inh)

def atLeast2ClassesWithAtLeast4Fields(mm : Metamodel):
    count = 0
    for c in mm.classes: 
        if len(c.references) + len(c.attributes) + len(c.operations) >= 4:
            count += 1 
    return count >= 2