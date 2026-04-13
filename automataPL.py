from vmetamodel import *
from metamodel import Enum, TypeRef
from analysis import *
from z3 import Solver, AtMost

TransitionF = Bool("Transition")
TransitionConstraint = TransitionF

# Transition Subfeatures
InputF = Bool("Input")
OutputF = Bool("Output")
ProbabilityF = Bool("Probability")
DeterministicF = Bool("Deterministic")

DeterminismConstraint = Or(Not(DeterministicF),OutputF)

MemoryF = Bool("Memory")
MemoryConstraint = MemoryF

# Memory Subfeatures

StackF = Bool("Stack")

StatesF = Bool("States")
StatesConstraint = StatesF

# States Subfeatures 

InitialF = Bool("Initial")

# Initial Subfeatures 

NoIncomingTransF = Bool("NoIncomingTrans")

# well-formedness 
NoIncomingTransParentConstraint = Or(Not(NoIncomingTransF),InitialF)

FinalF = Bool("Final")

# Final Subfeatures 

NoOutgoingTransF = Bool("NoOutgoingTrans1")

# well-formedness 
NonOutgoingTransParentConstraint = Or(Not(NoOutgoingTransF), FinalF)


# Hierarchical
HierarchicalF = Bool("Hierarchical")

AcceptanceConditionF = Bool("AcceptanceCondition")
AcceptanceConditionConstraint = AcceptanceConditionF

## Acceptance Condition Subfeatures
FininteF = Bool("Finite")

InfiniteF = Bool("Infinite")

ProbabilisticF = Bool("Probabilistic")

# constraints 

InfiniteConstraint = Or(Not(InfiniteF), Not(FinalF))

AcceptanceChoiceConstraint = Or(FininteF, InfiniteF, ProbabilisticF)

ShapeF = Bool("Shape")
ShapeConstraint = ShapeF 

ConnectedF = Bool("Connected")

acceptanceConditionAlt = AtMost(FininteF,InfiniteF,ProbabilisticF,1)

features = [TransitionF, 
            InputF, 
            OutputF, 
            ProbabilityF, 
            DeterministicF,
            MemoryF, 
            StackF, 
            StatesF, 
            InitialF, 
            NoIncomingTransF, 
            FinalF, 
            NoOutgoingTransF, 
            HierarchicalF, 
            AcceptanceConditionF, 
            FininteF, 
            InfiniteF,
            ProbabilisticF, 
            ShapeF, 
            ConnectedF]

# <?xml version="1.0" encoding="UTF-8" standalone="no"?>
# 	<featureModel>
# 		<properties/>
# 		<struct>
# 			<and abstract="true" mandatory="true" name="Automata">
# 				<and mandatory="true" name="Transitions">
# 					<feature name="Input"/>
# 					<feature name="Output"/>
# 					<feature name="Probability"/>
# 					<feature name="Deterministic"/>
# 				</and>
# 				<and mandatory="true" name="Memory">
# 					<feature name="Stack"/>
# 					<and mandatory="true" name="States">
# 						<and name="Initial">
# 							<feature name="NoIncomingTrans"/>
# 						</and>
# 						<and name="Final">
# 							<feature name="NoOutgoingTrans"/>
# 						</and>
# 						<feature name="Hierarchical"/>
# 					</and>
# 				</and>
# 				<alt mandatory="true" name="AcceptanceCondition">
# 					<feature name="Finite"/>
# 					<feature name="Infinite"/>
# 					<feature name="Probabilistic"/>
# 				</alt>
# 				<and mandatory="true" name="Shape">
# 					<feature name="Connected"/>
# 				</and>
# 			</and>
# 		</struct>
# 		<constraints>
# 			<rule>
# 				<imp>
# 					<var>Infinite</var>
# 					<not>
# 						<var>Final</var>
# 					</not>
# 				</imp>
# 			</rule>
# 			<rule>
# 				<imp>
# 					<var>Deterministic</var>
# 					<var>Output</var>
# 				</imp>
# 			</rule>
# 		</constraints>
# 		<calculations Auto="true" Constraints="true" Features="true" Redundant="true" Tautology="true"/>
# 		<comments/>
# 		<featureOrder userDefined="false"/>
# 	</featureModel>


featModelConstraints = And(
    TransitionConstraint, 
    DeterminismConstraint, 
    MemoryConstraint, 
    StatesConstraint, 
    NoIncomingTransParentConstraint,
    NonOutgoingTransParentConstraint, 
    AcceptanceConditionConstraint, 
    InfiniteConstraint, 
    AcceptanceChoiceConstraint, 
    ShapeConstraint,
    acceptanceConditionAlt
)

autopl = vMetamodel(
    name = "AutomataPL"
)

acceptance_kind = vEnum(
    name="AcceptanceKind",
    literals=[
        EnumLiteral("Finite"),
        EnumLiteral("Infinite"),
        EnumLiteral("Probabilistic")
    ],
    presence_condition=BoolVal(True)
)

autopl.enums.append(acceptance_kind)

symbol = vMetaClass(
    name="Symbol",
    attributes=[
        vAttribute("name", TypeRef("String"), presence_condition=BoolVal(True))
    ],
    presence_condition=BoolVal(True)
)

alphabet = vMetaClass(
    name="Alphabet",
    references=[
        vReference("symbols", TypeRef("Symbol"), 
                   multiplicity=Multiplicity(0, None), 
                   containment=True,
                   presence_condition=BoolVal(True))
    ],
    invariants=[
        vInvariant(
            "different",
            "self.symbols->forAll(s1 | self.symbols->forAll(s2 | s1<>s2 implies s1.name<>s2.name))",
            presence_condition=BoolVal(True)
        )
    ],
    presence_condition=BoolVal(True)
)


state = vMetaClass(
    name="State",
    attributes=[
        vAttribute("name", TypeRef("String"), presence_condition=BoolVal(True)),
        vAttribute("isInitial", TypeRef("Boolean"), presence_condition=InitialF),
        vAttribute("isFinal", TypeRef("Boolean"), presence_condition=FinalF)
    ],
    operations=[
        vOperation(
            "adjacent",
            TypeRef("State"),
            multiplicity=Multiplicity(0, None),
            body="self.inTrans().from->union(self.outTrans().to)->asSet()",
            presence_condition=BoolVal(True)
        ),
        vOperation(
            "inTrans",
            TypeRef("Transition"),
            multiplicity=Multiplicity(0, None),
            body="Transition.allInstances()->select(t | t.to = self)",
            presence_condition=BoolVal(True)
        ),
        vOperation(
            "outTrans",
            TypeRef("Transition"),
            multiplicity=Multiplicity(0, None),
            body="Transition.allInstances()->select(t | t.from = self)",
            presence_condition=BoolVal(True)
        ),
    ],
    invariants=[
        vInvariant(
            "isDeterministic",
            "self.outTrans()->isUnique(t | t.output)",
            presence_condition=DeterministicF
        ),
        vInvariant(
            "noIncoming",
            "self.isInitial implies self.inTrans()->isEmpty()",
            presence_condition=And(InitialF,NoIncomingTransF)
        ),
        vInvariant(
            "noOutgoing",
            "self.isFinal implies self.outTrans()->isEmpty()",
            presence_condition=And(FinalF, NoOutgoingTransF)
        )
    ],
    presence_condition=BoolVal(True)
)


transition = vMetaClass(
    name="Transition",
    attributes=[
        vAttribute("probability", TypeRef("Real"), multiplicity=Multiplicity(0,1), presence_condition=ProbabilityF)
    ],
    references=[
        vReference("input", TypeRef("Symbol"), presence_condition=InputF),
        vReference("output", TypeRef("Symbol"), presence_condition=OutputF),
        vReference("stackCheck", TypeRef("Symbol"), presence_condition=StackF),
        vReference("stackPush", TypeRef("Symbol"), multiplicity=Multiplicity(2,2), presence_condition=StackF),
        vReference("from_state", TypeRef("State"),presence_condition=BoolVal(True)),
        vReference("to_state", TypeRef("State"),presence_condition=BoolVal(True))
    ],
    presence_condition=BoolVal(True)
)

hierarchical_state = vMetaClass(
    name="HierarchicalState",
    references=[
        vReference("states", TypeRef("State"), multiplicity=Multiplicity(0, None), containment=True, presence_condition=HierarchicalF),
        vReference("transitions", TypeRef("Transition"), multiplicity=Multiplicity(0, None), containment=True, presence_condition=HierarchicalF)
    ],
    presence_condition=HierarchicalF
)

automaton = vMetaClass(
    name="Automaton",
    references=[
        vReference("inputAlphabet", TypeRef("Alphabet"), multiplicity=Multiplicity(1,1), containment=True, presence_condition=InputF),
        vReference("outputAlphabet", TypeRef("Alphabet"), multiplicity=Multiplicity(1,1), containment=True, presence_condition=OutputF),
        vReference("stackAlphabet", TypeRef("Alphabet"), multiplicity=Multiplicity(1,1), containment=True, presence_condition=StackF),
        vReference("initialStackSymbol", TypeRef("Symbol"), multiplicity=Multiplicity(1,1), presence_condition=StackF),
        vReference("states", TypeRef("State"), multiplicity=Multiplicity(0, None), presence_condition=BoolVal(True)),
        vReference("transitions", TypeRef("Transition"), multiplicity=Multiplicity(0, None), presence_condition=BoolVal(True))
    ],
    operations=[
        vOperation("acceptanceCondition", TypeRef("AcceptanceKind"), multiplicity=Multiplicity(1,1),presence_condition=BoolVal(True))
    ],
    invariants=[
        vInvariant(
            "connected",
            "self.states->forAll(s | Set{s}->closure(adjacent())->includesAll(self.states))",
            presence_condition=ConnectedF
        )
    ],
    presence_condition=BoolVal(True)
)

autopl.classes.extend([
    automaton,
    state,
    hierarchical_state,
    transition,
    alphabet,
    symbol
])

autopl.inheritance.extend([(("hierarchical_state", "state"), HierarchicalF)])

