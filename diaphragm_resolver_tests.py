
import unittest

from diaphragm_resolver import *


class DiaphragmResolverTests(unittest.TestCase):

    def default_beam_coordinations(self):
        return \
            [ BeamCoordination( PlanAxisPosition(1, 1), PlanAxisPosition(2, 1), 2 ) \
            , BeamCoordination( PlanAxisPosition(2, 1), PlanAxisPosition(3, 1), 1 ) \
            , BeamCoordination( PlanAxisPosition(3, 1), PlanAxisPosition(4, 1), 2 ) \
            , BeamCoordination( PlanAxisPosition(1, 2), PlanAxisPosition(2, 2), 3 ) \
            , BeamCoordination( PlanAxisPosition(2, 2), PlanAxisPosition(3, 2), 1 ) \
            , BeamCoordination( PlanAxisPosition(3, 2), PlanAxisPosition(4, 2), 3 ) \
            , BeamCoordination( PlanAxisPosition(4, 2), PlanAxisPosition(5, 2), 4 ) \
            , BeamCoordination( PlanAxisPosition(1, 3), PlanAxisPosition(2, 3), 3 ) \
            , BeamCoordination( PlanAxisPosition(2, 3), PlanAxisPosition(3, 3), 1 ) \
            , BeamCoordination( PlanAxisPosition(3, 3), PlanAxisPosition(4, 3), 3 ) \
            , BeamCoordination( PlanAxisPosition(4, 3), PlanAxisPosition(5, 3), 4 ) \
            , BeamCoordination( PlanAxisPosition(1, 4), PlanAxisPosition(2, 4), 2 ) \
            , BeamCoordination( PlanAxisPosition(2, 4), PlanAxisPosition(3, 4), 1 ) \
            , BeamCoordination( PlanAxisPosition(3, 4), PlanAxisPosition(4, 4), 2 ) \
            , BeamCoordination( PlanAxisPosition(1, 1), PlanAxisPosition(1, 2), 12 ) \
            , BeamCoordination( PlanAxisPosition(1, 2), PlanAxisPosition(1, 3), 11 ) \
            , BeamCoordination( PlanAxisPosition(1, 3), PlanAxisPosition(1, 4), 12 ) \
            , BeamCoordination( PlanAxisPosition(2, 1), PlanAxisPosition(2, 2), 13 ) \
            , BeamCoordination( PlanAxisPosition(2, 2), PlanAxisPosition(2, 3), 11 ) \
            , BeamCoordination( PlanAxisPosition(2, 3), PlanAxisPosition(2, 4), 13 ) \
            , BeamCoordination( PlanAxisPosition(3, 1), PlanAxisPosition(3, 2), 13 ) \
            , BeamCoordination( PlanAxisPosition(3, 2), PlanAxisPosition(3, 3), 11 ) \
            , BeamCoordination( PlanAxisPosition(3, 3), PlanAxisPosition(3, 4), 13 ) \
            , BeamCoordination( PlanAxisPosition(4, 1), PlanAxisPosition(4, 2), 12 ) \
            , BeamCoordination( PlanAxisPosition(4, 2), PlanAxisPosition(4, 3), 11 ) \
            , BeamCoordination( PlanAxisPosition(4, 3), PlanAxisPosition(4, 4), 12 ) \
            , BeamCoordination( PlanAxisPosition(5, 2), PlanAxisPosition(5, 3), 14 ) \
            ]

    def default_section_list(self):
        selectable_section_list = list(range(200, 1500, 50))
        return \
            [ BeamSectionSpec( 1,  500, selectable_section_list )
            , BeamSectionSpec( 2,  700, selectable_section_list )
            , BeamSectionSpec( 3,  600, selectable_section_list )
            , BeamSectionSpec( 4,  400, selectable_section_list )
            , BeamSectionSpec(11,  800, selectable_section_list )
            , BeamSectionSpec(12, 1000, selectable_section_list )
            , BeamSectionSpec(13,  900, selectable_section_list )
            , BeamSectionSpec(14,  400, selectable_section_list )
            ]
    
    def default_plan(self):
        return \
            Plan(self.default_beam_coordinations(), BeamSectionList(self.default_section_list()))

    def test_plan_axis_position_key(self):
        position = PlanAxisPosition(1, 2)
        self.assertEqual("x1@y2", position.key())

    def test_plan_axis_position_same(self):
        position1 = PlanAxisPosition(1, 2)
        position2 = PlanAxisPosition(1, 2)
        position3 = PlanAxisPosition(2, 2)
        self.assertTrue(position1.same_position(position2))
        self.assertTrue(position2.same_position(position1))
        self.assertFalse(position2.same_position(position3))

    def test_beam_position_same(self):
        position1 = PlanAxisPosition(1, 1)
        position2 = PlanAxisPosition(2, 1)
        position3 = PlanAxisPosition(1, 2)
        beam1 = BeamCoordination(position1, position2, 1)
        beam2 = BeamCoordination(position1, position2, 2)
        beam3 = BeamCoordination(position2, position3, 1)
        self.assertTrue(beam1.same_position(beam2))
        self.assertTrue(beam2.same_position(beam1))
        self.assertFalse(beam2.same_position(beam3))

    def test_constraint(self):
        const1 = DiaphragmConstraint(200, 1000, False)
        const2 = DiaphragmConstraint(500, 1200, False)
        impossible_const = DiaphragmConstraint(0, 0, True)

        self.assertTrue( not const1.merge(const2).impossible )
        self.assertTrue( const1.merge(const2).range_lower == 500 )
        self.assertTrue( const1.merge(const2).range_upper == 1000 )
        self.assertTrue( const2.merge(const1).range_lower == 500 )
        self.assertTrue( const2.merge(const1).range_upper == 1000 )
        self.assertTrue( impossible_const.merge(const1).impossible )
        self.assertTrue( const1.merge(impossible_const).impossible )

        self.assertTrue( const1.satisfied(400) )
        self.assertFalse( const1.satisfied(1200) )
        self.assertFalse( const1.satisfied(100) )
        self.assertFalse( impossible_const.satisfied(500) )

    def test_plan_beam_relations(self):
        plan = self.default_plan()
        beam = plan.beam_coordinations[0]
        relations = plan.connected_beam_relations(beam)
        self.assertTrue(12 in relations)
        self.assertTrue(13 in relations)
        self.assertTrue( 1 in relations)
        
        beam = plan.beam_coordinations[1]
        relations = plan.connected_beam_relations(beam)
        self.assertTrue( 2 in relations)
        self.assertTrue(13 in relations)
        self.assertFalse( 1 in relations)

    def test_plan_section_relations(self):
        plan = self.default_plan()
        sec_no = 1
        section = plan.section_list.find(sec_no)
        relations = plan.connected_section_relations(section)
        for target_sec_no in [ 2, 3, 11, 13 ]:
            self.assertTrue( target_sec_no in relations)

    def test_connected_section_constraints(self):
        plan = self.default_plan()
        sec_no = 1
        section = plan.section_list.find(sec_no)
        constraints = plan.connected_section_constraints(section)
        satisfiedConstraints = \
            [ c for c in constraints if c.satisfied(section.depth) ] 

        self.assertTrue(0 < len(constraints))
        self.assertTrue(0 == len(satisfiedConstraints))

        for constraint in constraints:
            #print(constraint.range_lower)
            #print(constraint.range_upper)
            self.assertTrue(
                constraint.range_upper == 400 or \
                constraint.range_lower == 1100
            )



    def test_require_update_section_nos(self):
        plan = self.default_plan()
        require_update_section_nos = plan.require_update_section_nos()
        self.assertTrue( 0 < len(require_update_section_nos))
        for target_sec_no in [ 1, 3 ]:
            self.assertTrue( target_sec_no in require_update_section_nos)

    def test_plan_mark_changable(self):
        plan = self.default_plan()
        beams = plan.mark_changable_beams()
        self.assertEqual(4, len(beams))

if __name__ == '__main__':
    unittest.main()