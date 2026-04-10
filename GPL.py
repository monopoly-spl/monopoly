from vmetamodel import *
from metamodel import Enum, TypeRef
from analysis import *
from z3 import Solver, And, Or, Implies, Not, AtMost

AlgF = Bool("Alg") # mandatory

NumberF = Bool("Number")

ConnectedF = Bool("Connected")

##

StrongCF = Bool("StrongC")

StronglyConnectedF = Bool("StronglyConnected")

TransposeF = Bool("Transpose")

##

CycleF = Bool("Cycle")

MSTPrimF = Bool("MSTPrim")

MSTKruskalF = Bool("MSTKruskal")

#
SrcF = Bool("Src") # mandatory

BfsF = Bool("BFS")

DfsF = Bool("DFS")

#


HiddenWgtF = Bool("HiddenWgt") # mandatory

##
WeightOptionsF = Bool("WeightOptions") # mandatory

WeightedWithEdgesF = Bool("WeightedWithEdges")

WeightedWithNeighboursF = Bool("WeightedWithNeighbours")

WeightedOnlyVerticesF = Bool("WeightedOnlyVertices")

###

WgtF = Bool("Wgt")

WeightedF = Bool("Weighted")

UnWeightedF = Bool("Unweighted")

###

GtpF = Bool("Gtp") # Mandatory

DirectedF = Bool("Directed")

DirectedOnlyVerticesF = Bool("DirectedOnlyVertices")

DirectedWithNeighboursF = Bool("DirectedWithNeighbours")

DirectedWithEdgesF = Bool("DirectedWithEdged")

UndirectedOnlyVerticesF = Bool("UndirectedOnlyVertices")

UndirectedWithNeighboursF = Bool("UndirectedWithNeighbours")

UndirectedWithEdgesF = Bool("UndirectedWithEdged")



UndirectedF = Bool("Undirected")

###


ImplementationF = Bool("Implementation") # mandatory

OnlyVerticesF = Bool("OnlyVertices")

WithNeighboursF = Bool("WithNeighbours")

WithEdgesF = Bool("WithEdges")

##

BaseF = Bool("Base") # Mandatory

gplFeatures = [BaseF, WithEdgesF, WithNeighboursF, OnlyVerticesF, ImplementationF, 
               UndirectedF, UndirectedWithEdgesF, UndirectedWithNeighboursF,
               DirectedF, DirectedWithEdgesF, DirectedWithNeighboursF, DirectedOnlyVerticesF, GtpF, 
               UnWeightedF, WeightedF, WgtF, WeightedOnlyVerticesF, WeightedWithNeighboursF, WeightedWithEdgesF,
               HiddenWgtF, SrcF, BfsF, DfsF, CycleF, MSTKruskalF, MSTPrimF, CycleF,TransposeF, StronglyConnectedF, StrongCF, 
               AlgF, NumberF, ConnectedF]

## Constraints 

# Mandatory Features 

AlgMandatory = AlgF 
SrcMandatory = SrcF 
HiddenWgtMandatory = HiddenWgtF
WgtMandatory = WgtF
GtpMandatory = GtpF
ImplementationMandatory = ImplementationF
BaseMandatory = BaseF

mandatoryFeatures = [AlgMandatory, SrcMandatory, HiddenWgtMandatory, WgtMandatory,
                     GtpMandatory,ImplementationMandatory,BaseMandatory] 

# Parent Constraints

# StrongCChildren = Implies(Or(StronglyConnectedF,TransposeF), StrongCF)
StrongCChildren2 = (StrongCF == And(StronglyConnectedF,TransposeF))
# TranposeImpStronglyConnected = Implies(TransposeF, StronglyConnectedF)
# StronglyConnectedImpTranspose = Implies(StronglyConnectedF, TransposeF)
HiddenWgtImpWeightOptions = Implies(HiddenWgtF, WeightOptionsF)

parentConstraints = [StrongCChildren2,
                     HiddenWgtImpWeightOptions,
                    #   TranposeImpStronglyConnected, StronglyConnectedImpTranspose
                      ]

# alternative constraints

# AlgAlternatives = AtMost(NumberF, ConnectedF, StrongCF, CycleF, MSTPrimF, MSTKruskalF, 1)
SrcAlternatives = AtMost(BfsF,DfsF,1)
WgtAlternatives = AtMost(WeightedF,UnWeightedF,1)
GtpAlternatives = AtMost(DirectedF,UndirectedF,1)
ImplementationAlternatives = AtMost(OnlyVerticesF,WithNeighboursF,WithEdgesF,1)

alternativesConstraints = [SrcAlternatives, WgtAlternatives, GtpAlternatives, ImplementationAlternatives]

# Choice Constraints

AlgChoice = Implies(AlgF, Or(StrongCF, MSTKruskalF, CycleF, NumberF, MSTPrimF, ConnectedF))
SrcChoice = Implies(SrcF, Or(BfsF, DfsF))
WgtChoice = Implies(WgtF, Or(WeightedF, UnWeightedF))
GtpChoice = Implies(GtpF, Or(DirectedF, UndirectedF))
ImplementationChoice = Implies(ImplementationF,Or(WithEdgesF,OnlyVerticesF,WithNeighboursF))

choiceConstraints = [AlgChoice, SrcChoice, WgtChoice, GtpChoice, ImplementationChoice]

## Cross-tree constraints

crossTreeConstraints = []

NumberImpGtpSrc = Implies(NumberF, And(GtpF, SrcF)) 
ConnectedImpUndirectedSrc = Implies(ConnectedF, And(UndirectedF, SrcF))
StrongImpDirectedDFS = Implies(StrongCF, And(DirectedF, DfsF))
CycleImpGtpDFS = Implies(CycleF, And(GtpF, DfsF))
MSTImp = Implies(Or(MSTKruskalF, MSTPrimF), And(UndirectedF, WeightedF))
MSTExclusion = Implies(Or(MSTKruskalF, MSTPrimF), Not(And(MSTPrimF, MSTKruskalF)))
MSTKruskalImp = Implies(MSTKruskalF, WithEdgesF)


crossTreeConstraints.extend([NumberImpGtpSrc,ConnectedImpUndirectedSrc, StrongImpDirectedDFS,
                             CycleImpGtpDFS,MSTImp, MSTExclusion,MSTKruskalImp])


# EdgesWeightedImp = Implies(And(WithEdgesF,WeightedF), WeightedWithEdgesF)
# NeighboursWeightedImp = Implies(And(WithNeighboursF, WeightedF), WeightedWithNeighboursF)
# OnlyVerticesWeightedImp = Implies(And(OnlyVerticesF, WeightedF), WeightedOnlyVerticesF)

EdgesWeightedImp = (And(WithEdgesF,WeightedF) == WeightedWithEdgesF)
NeighboursWeightedImp = (And(WithNeighboursF, WeightedF) == WeightedWithNeighboursF)
OnlyVerticesWeightedImp = (And(OnlyVerticesF, WeightedF) == WeightedOnlyVerticesF)

# OnlyVerticesDirectedImp = Implies(And(OnlyVerticesF, DirectedF), DirectedOnlyVerticesF)
# WithNeighboursDirectedImp = Implies(And(WithNeighboursF,DirectedF), DirectedWithNeighboursF)
# WithEdgesDirectedImp = Implies(And(WithEdgesF,DirectedF), DirectedWithEdgesF)

OnlyVerticesDirectedImp = (And(OnlyVerticesF, DirectedF) == DirectedOnlyVerticesF)
WithNeighboursDirectedImp = (And(WithNeighboursF,DirectedF) == DirectedWithNeighboursF)
WithEdgesDirectedImp = (And(WithEdgesF,DirectedF) == DirectedWithEdgesF)

# OnlyVerticesUndirectedImp = Implies(And(OnlyVerticesF, UndirectedF), UndirectedOnlyVerticesF)
# WithNeighboursUndirectedImp = Implies(And(WithNeighboursF,UndirectedF), UndirectedWithNeighboursF)
# WithEdgesUndirectedImp = Implies(And(WithEdgesF,UndirectedF), UndirectedWithEdgesF)

OnlyVerticesUndirectedImp = (And(OnlyVerticesF, UndirectedF) == UndirectedOnlyVerticesF)
WithNeighboursUndirectedImp = (And(WithNeighboursF,UndirectedF) == UndirectedWithNeighboursF)
WithEdgesUndirectedImp = (And(WithEdgesF,UndirectedF) == UndirectedWithEdgesF)


crossTreeConstraints.extend([EdgesWeightedImp, NeighboursWeightedImp, OnlyVerticesWeightedImp,
                             OnlyVerticesDirectedImp,WithNeighboursDirectedImp,WithNeighboursUndirectedImp,
                             OnlyVerticesUndirectedImp, WithNeighboursUndirectedImp, WithEdgesUndirectedImp])

GPLFeatModelConstraints = mandatoryFeatures + parentConstraints + alternativesConstraints + choiceConstraints + crossTreeConstraints


EdgeIfcPC = Or(BaseF,WeightedOnlyVerticesF,WeightedWithEdgesF, WeightedWithNeighboursF)
EdgeIfcClass = vMetaClass(
    name="EdgeIfc",
    presence_condition= EdgeIfcPC,
    attributes=[],
    references=[],
    operations=[],
    invariants=[]
)

EdgeIterPC = BaseF
EdgeIterClass = vMetaClass(
    name="EdgeIter",
    presence_condition=EdgeIterPC,
    attributes=[],
    references=[],
    operations=[],
    invariants=[]
)

NeighbourIfcPC = BaseF 
NeighbourIfcClass =  vMetaClass(
    name="NeighborIfc",
    presence_condition= NeighbourIfcPC,
    attributes=[],
    references=[],
    operations=[],
    invariants=[]
)

VertexIterClassPC = BaseF
VertexIterClass = vMetaClass(
    name="VertexIter",
    presence_condition=VertexIterClassPC,
    attributes=[],
    references=[],
    operations=[],
    invariants=[]
)


VertexClassPC = Or(BfsF, ConnectedF, CycleF, DfsF, DirectedWithEdgesF, DirectedWithNeighboursF, MSTKruskalF, MSTPrimF, NumberF, StronglyConnectedF, UndirectedOnlyVerticesF, UndirectedWithEdgesF, UndirectedWithNeighboursF, WeightedOnlyVerticesF, WeightedWithNeighboursF)
VertexClass = vMetaClass(
    name="Vertex",
    presence_condition= VertexClassPC,
    attributes=[
        vAttribute(
            name="visited",
            type=TypeRef("Boolean"),
            multiplicity=Multiplicity(1,1),
            presence_condition=And(VertexClassPC,Or(BfsF, DfsF))
        ),
        vAttribute(
            name="componentNumber",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=And(VertexClassPC,ConnectedF)
        ),
        vAttribute(
            name="VertexCycle",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=And(VertexClassPC,CycleF)
        ),
        vAttribute(
            name="VertexColor",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=And(VertexClassPC,CycleF)
        ),
        vAttribute(
            name="name",
            type=TypeRef("String"),
            multiplicity=Multiplicity(0,1),
            presence_condition= And(VertexClassPC, Or(DirectedOnlyVerticesF, DirectedWithEdgesF, DirectedWithNeighboursF, UndirectedOnlyVerticesF, UndirectedWithEdgesF, UndirectedWithNeighboursF))
        ),
        vAttribute(
            name="pred",
            type=TypeRef("String"),
            multiplicity=Multiplicity(0,1),
            presence_condition=And(VertexClassPC,MSTPrimF)
        ),
        vAttribute(
            name="akey",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=And(VertexClassPC,MSTPrimF)
        ),
        vAttribute(
            name="VertexNumber",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=And(VertexClassPC,NumberF)
        ),
        vAttribute(
            name="finishTime",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=And(VertexClassPC,StronglyConnectedF)
        ),
        vAttribute(
            name="strongComponentNumber",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=And(VertexClassPC,StronglyConnectedF)
        ),
        vAttribute(
            name="weightsList",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(0,None),
            presence_condition=And(VertexClassPC,WeightedOnlyVerticesF)
        )
    ],
    references=[
        vReference(
            name="adjacentVertices",
            type=TypeRef("Vertex"),
            multiplicity=Multiplicity(0,None),
            presence_condition= And(VertexClassPC,Or(DirectedOnlyVerticesF, UndirectedOnlyVerticesF))
        ),
        vReference(
            name="neighbors",
            type=TypeRef("Neighbor"),
            multiplicity=Multiplicity(0,None),
            presence_condition= And(VertexClassPC,Or(DirectedWithEdgesF, UndirectedWithEdgesF))
        ),
        vReference(
            name="adjacentNeighbors",
            type=TypeRef("Neighbor"),
            multiplicity=Multiplicity(0,None),
            presence_condition= And(VertexClassPC,Or(DirectedWithNeighboursF, UndirectedWithNeighboursF))
        ),
        vReference(
            name="representative",
            type=TypeRef("Vertex"),
            multiplicity=Multiplicity(0,1),
            presence_condition=And(VertexClassPC,MSTKruskalF)
        ),
        vReference(
            name="members",
            type=TypeRef("Vertex"),
            multiplicity=Multiplicity(0,None),
            presence_condition=And(MSTKruskalF,VertexClassPC)
        )
    ],
    operations=[],
    invariants=[
        vInvariant(
            name="validColor",
            expression="self.VertexColor = 0 or self.VertexColor = 1 or self.VertexColor = 2",
            presence_condition=And(VertexClassPC,CycleF)
        )
    ]
)

GraphClassPC = Or(BfsF,ConnectedF,CycleF,DfsF,DirectedOnlyVerticesF, DirectedWithEdgesF, DirectedWithNeighboursF,
           MSTKruskalF, MSTPrimF, NumberF, StronglyConnectedF, TransposeF, UndirectedOnlyVerticesF,
           UndirectedWithEdgesF, UndirectedWithNeighboursF, WeightedOnlyVerticesF, WeightedWithNeighboursF) 
GraphClass = vMetaClass(
    name="Graph",
    presence_condition=GraphClassPC,
    attributes=[
        vAttribute(
            name="isDirected",
            type=TypeRef("Boolean"),
            multiplicity=Multiplicity(0,1),
            presence_condition=
            And(GraphClassPC,
                Or(DirectedOnlyVerticesF,DirectedWithEdgesF, DirectedWithNeighboursF, UndirectedOnlyVerticesF, UndirectedWithEdgesF, UndirectedWithNeighboursF))
        )
    ],
    references=[
        vReference(
            name="vertices",
            type=TypeRef("Vertex"),
            multiplicity=Multiplicity(0,None),
            presence_condition=
            And(GraphClassPC,
                Or(DirectedOnlyVerticesF,DirectedWithEdgesF, DirectedWithNeighboursF,
                   UndirectedOnlyVerticesF, UndirectedWithEdgesF, UndirectedWithNeighboursF))
        ),
        vReference(
            name="edges",
            type=TypeRef("Edge"),
            multiplicity=Multiplicity(0,None),
            presence_condition=And(GraphClassPC,Or(DirectedWithEdgesF,UndirectedWithEdgesF))
        )
    ],
    operations=[],
    invariants=[]
)

GlobalVarsWrapperClass = vMetaClass(
    name="GlobalVarsWrapper",
    presence_condition=BfsF,
    attributes=[],
    references=[],
    operations=[],
    invariants=[]
)

WorkspaceClassPC = Or(BfsF, DfsF)
WorkspaceClass = vMetaClass(
    name="WorkSpace",
    presence_condition= WorkspaceClassPC,
    attributes=[],
    references=[],
    operations=[],
    invariants=[]
)


RegionWorkspacePC = ConnectedF
RegionWorkspaceClass = vMetaClass(
    name="RegionWorkSpace",
    presence_condition=RegionWorkspacePC,
    attributes=[
        vAttribute(
            name="counter",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=And(RegionWorkspacePC,ConnectedF)
        )
    ],
    references=[],
    operations=[],
    invariants=[
        vInvariant(
            name="counterValue",
            expression="self.counter >= 0",
            presence_condition=And(RegionWorkspacePC,ConnectedF)
        )
    ]
)

CycleWorkSpacePC = CycleF
CycleClass = vMetaClass(
    name="CycleWorkSpace",
    presence_condition=CycleWorkSpacePC,
    attributes=[
        vAttribute(
            name="AnyCycles",
            type=TypeRef("Boolean"),
            multiplicity=Multiplicity(1,1),
            presence_condition=CycleF
        ),
        vAttribute(
            name="count",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=CycleF
        ),
        vAttribute(
            name="isDirected",
            type=TypeRef("Boolean"),
            multiplicity=Multiplicity(1,1),
            presence_condition=CycleF
        ),
        vAttribute(
            name="WHITE",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=CycleF
        ),
        vAttribute(
            name="GRAY",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=CycleF
        ),
        vAttribute(
            name="BLACK",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=CycleF
        )
    ],
    references=[
        vReference(
            name="vertices",
            type=TypeRef("Vertex"),
            multiplicity=Multiplicity(0,None),
            presence_condition=CycleF
        )
    ],
    operations=[],
    invariants=[
        vInvariant(
            name="colorValues",
            expression="self.WHITE = 0 and self.GRAY = 1 and self.BLACK = 2",
            presence_condition=CycleF
        )
    ]
)

NeighbourClassPC = Or(DirectedWithEdgesF, DirectedWithNeighboursF, UndirectedWithEdgesF, UndirectedWithNeighboursF, WeightedWithNeighboursF)
NeighbourClass = vMetaClass(
    name="Neighbor",
    presence_condition= NeighbourClassPC,
    attributes=[
        vAttribute(
            name="weight",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=And(NeighbourClassPC,WeightedWithNeighboursF)
        )
    ],
    references=[
        vReference(
            name="end",
            type=TypeRef("Vertex"),
            multiplicity=Multiplicity(0,1),
            presence_condition=And(NeighbourClassPC,Or(DirectedWithEdgesF, UndirectedWithEdgesF))
        ),
        vReference(
            name="edge",
            type=TypeRef("Edge"),
            multiplicity=Multiplicity(0,1),
            presence_condition=And(NeighbourClassPC,Or(DirectedWithEdgesF,UndirectedWithEdgesF))
        ),
        vReference(
            name="neighbor",
            type=TypeRef("Vertex"),
            multiplicity=Multiplicity(0,1),
            presence_condition=And(NeighbourClassPC,Or(DirectedWithNeighboursF,UndirectedWithNeighboursF))
        )
    ],
    operations=[],
    invariants=[]
)

EdgeClassPC = Or(DirectedWithEdgesF, UndirectedWithEdgesF, WeightedWithEdgesF)
EdgeClass = vMetaClass(
    name="Edge",
    presence_condition= EdgeClassPC,
    attributes=[
        vAttribute(
            name="weight",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=And(EdgeClassPC,WeightedWithEdgesF)
        )
    ],
    references=[
        vReference(
            name="start",
            type=TypeRef("Vertex"),
            multiplicity=Multiplicity(0,1),
            presence_condition= And(EdgeClassPC,Or(DirectedWithEdgesF, UndirectedWithEdgesF))
        )
    ],
    operations=[],
    invariants=[]
)

NumberWorkspaceClass = vMetaClass(
    name="NumberWorkSpace",
    presence_condition=NumberF,
    attributes=[
        vAttribute(
            name="vertexCounter",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=NumberF
        )
    ],
    references=[],
    operations=[],
    invariants=[
        vInvariant(
            name="counterValue",
            expression="self.vertexCounter >= 0",
            presence_condition=NumberF
        )
    ]
)

FinishTimeWorkspaceClass = vMetaClass(
    name="FinishTimeWorkSpace",
    presence_condition=StronglyConnectedF,
    attributes=[
        vAttribute(
            name="FinishCounter",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=StronglyConnectedF
        )
    ],
    references=[],
    operations=[],
    invariants=[
        vInvariant(
            name="counterValue",
            expression="self.FinishCounter > 0",
            presence_condition=StronglyConnectedF
        )
    ]
)

WorkspaceTransposeClass = vMetaClass(
    name="WorkSpaceTranspose",
    presence_condition=StronglyConnectedF,
    attributes=[
        vAttribute(
            name="SCCCounter",
            type=TypeRef("EInt"),
            multiplicity=Multiplicity(1,1),
            presence_condition=StronglyConnectedF
        )
    ],
    references=[],
    operations=[],
    invariants=[
        vInvariant(
            name="counterValue",
            expression="self.SCCCounter >= 0",
            presence_condition=StronglyConnectedF
        )
    ]
)




# RegionWorkspaceClass ===   ConnectedF ===> Workspace
RegionInheritance = ((RegionWorkspaceClass, WorkspaceClass), And(RegionWorkspacePC,ConnectedF,WorkspaceClassPC))

# vertexClass === DirectedOnlyVerticesF \/ UndirectedOnlyVerticesF ===> {EdgeIfc, NeighbourIfc}
VertexInheritance1 = ((VertexClass, EdgeIfcClass), And(VertexClassPC,Or(DirectedOnlyVerticesF, UndirectedOnlyVerticesF),EdgeIfcPC))
VertexInheritance2 = ((VertexClass, NeighbourIfcClass), And(VertexClassPC,Or(DirectedOnlyVerticesF, UndirectedOnlyVerticesF),NeighbourIfcPC))

## Neighbour === DirectedWith NeighboursF \/ UndirectedWithNeighboursF ===> {EdgeIfc, NeighbourIfc}
NeighbourInheritance1 = ((NeighbourClass, EdgeIfcClass), And(NeighbourClassPC,Or(DirectedWithNeighboursF, UndirectedWithNeighboursF),EdgeIfcPC))
NeighbourInheritance2 = ((NeighbourClass, NeighbourIfcClass), And(NeighbourClassPC,Or(DirectedWithNeighboursF, UndirectedWithNeighboursF),NeighbourIfcPC))

## Neighbour === UndirectedWithEdgesF ==> NeighbourIfc
NeighbourInheritance3 = ((NeighbourClass, NeighbourIfcClass), And(NeighbourClassPC,UndirectedWithEdgesF,NeighbourIfcPC))

## Edge == ~(WeightedWithEdgesF)  => Neighbour, EdgeIfc
EdgeInheritance1 = ((EdgeClass,NeighbourClass), And(EdgeClassPC, Not(WeightedWithEdgesF), NeighbourClassPC))
EdgeInheritance2 = ((EdgeClass,EdgeIfcClass), And(EdgeClassPC, Not(WeightedWithEdgesF), EdgeIfcPC))

## NumberWorkSpace == NumberF ===> Workspace
NWorkspaceInheritance = ((NumberWorkspaceClass, WorkspaceClass), And(NumberF, WorkspaceClassPC))


## FinishTimeWorkspace === StronglyConnectedF ===> Workspace
FWorkspaceInheritance = ((FinishTimeWorkspaceClass, WorkspaceClass), And(StronglyConnectedF,WorkspaceClassPC))

## WorkspaceTranspose === StronglyConnectedF ==> Workspace
TransposeWorkspaceInheritance = ((WorkspaceTransposeClass, WorkspaceClass), And(StronglyConnectedF,WorkspaceClassPC))

all_classes = [EdgeIfcClass, EdgeIterClass, NeighbourIfcClass, VertexIterClass, VertexClass, 
               GraphClass, GlobalVarsWrapperClass, WorkspaceClass, RegionWorkspaceClass, CycleClass,
               NeighbourClass, EdgeClass, NumberWorkspaceClass, FinishTimeWorkspaceClass, WorkspaceTransposeClass]

all_inheritances = [RegionInheritance, VertexInheritance1, VertexInheritance2, NeighbourInheritance1, NeighbourInheritance2, NeighbourInheritance3, EdgeInheritance1, EdgeInheritance2, NWorkspaceInheritance,FWorkspaceInheritance,TransposeWorkspaceInheritance]

gpl_ = vMetamodel("GPL", classes = all_classes, enums=[],inheritance=all_inheritances)

GPL = VariationalMetamodel(features=gplFeatures,model=gpl_,featModel=GPLFeatModelConstraints)

s = Solver()

# print(count_models(s, gplFeatures, GPLFeatModelConstraints))
def atLeast2ClassesWithAtLeast4Fields(mm : Metamodel):
    count = 0
    for c in mm.classes: 
        if len(c.references) + len(c.attributes) + len(c.operations) >= 4:
            count += 1 
    return count >= 2

myExampleAnalysis = AnalysisInstance(GPL, atLeast2ClassesWithAtLeast4Fields)

myExampleAnalysis.analyze()