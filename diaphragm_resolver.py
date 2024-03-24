
#%%

# 梁断面のスペック
# ダイアフラム解決に必要な値だけを抜き出したオブジェクト
class BeamSectionSpec:
    def __init__(self, no, depth, selectable_depth_list):
        self.section_no = no
        self.depth = depth
        self.selectable_depth_list = selectable_depth_list

    # 当該断面がもたらす制約を生成する
    def build_constraints(self):
        return [ 
            DiaphragmConstraint(self.depth, self.depth), \
            DiaphragmConstraint(0, self.depth - 200), \
            DiaphragmConstraint(self.depth + 200, LIMIT_DEPTH) 
        ]

# ある階の梁断面リスト
class BeamSectionList:
    def __init__(self, section_list):
        self.list = section_list

    def find(self, no):
        for section in self.list:
            if section.section_no == no :
                return section
        return None

# 平面的な軸位置
# たとえば、x2-y3 : x_position = 2, y_position = 3 とする。  
class PlanAxisPosition:
    def __init__(self, x_position, y_position):
        self.x_position = x_position
        self.y_position = y_position
    
    def key(self):
        return "x%d@y%d" % (self.x_position, self.y_position) 

    def same_position(self, target):
        return self.x_position == target.x_position and \
               self.y_position == target.y_position



# 梁配置
class BeamCoordination:
    def __init__(self, no, start_position, end_position, section_no):
        self.no = no
        self.start_position = start_position
        self.end_position = end_position
        self.section_no = section_no

    def key(self):
        return "%s-%s" % \
            (self.start_position.key(), self.end_position.key()) 
            


    def same_position(self, target):
        return self.start_position.same_position(target.start_position) and \
               self.end_position.same_position(target.end_position)

# 平面プラン
class Plan:
    def __init__(self, beam_coordinations, section_list):
        self.beam_coordinations = beam_coordinations
        self.section_list = section_list

    # ある梁に接続する断面一覧を取得する
    def connected_beam_relations(self, target_beam):
        target_positions = []
        target_positions.append(target_beam.start_position)
        target_positions.append(target_beam.end_position)
        
        connected_section_nos = []
        for position in target_positions:
            for beam in self.beam_coordinations:
                    
                if not (target_beam.same_position(beam)) and  \
                   (position.same_position(beam.start_position) or \
                    position.same_position(beam.end_position)):
                    connected_section_nos.append( beam.section_no )
        
        connected_section_nos = list(set(connected_section_nos))
        return connected_section_nos

    # ある断面に接続する断面一覧を取得する
    def connected_section_relations(self, target_section):
        target_section_members = \
            filter(lambda beam: beam.section_no == target_section.section_no , self.beam_coordinations)
        
        connected_section_nos = []
        for member in target_section_members:
            connected_section_nos += self.connected_beam_relations(member)


        # 重複排除
        connected_section_nos = list(set(connected_section_nos))

        return connected_section_nos

    # ある断面によってもたらされる制約をマージする
    def merge_constraints(self, sections):
        # All Range
        constraints = [ DiaphragmConstraint(0, LIMIT_DEPTH, False) ]
        
        for section in sections:
            updated_constraints = []
            for current_constraint in constraints:
                for target_constraint in section.build_constraints():
                    merged = current_constraint.merge(target_constraint)
                    if not merged.impossible:
                        updated_constraints.append(merged)
            constraints = updated_constraints
        return constraints

    # ある断面に対する制約を取得
    def connected_section_constraints(self, target_section):

        connected_section_nos = self.connected_section_relations(target_section)

        sections = \
            list(map(lambda no: self.section_list.find(no), connected_section_nos))

        return self.merge_constraints(sections)

    # 更新が必要な断面Noを取得
    def require_update_section_nos(self):
        require_update = []
        for section in self.section_list.list:
            constraints = self.connected_section_constraints(section)
            satisfied_constraints = \
                [ c for c in constraints if c.satisfied(section.depth) ] 

            if len(satisfied_constraints) == 0:
                require_update.append(section.section_no)
        return require_update

    # 制約を満たせない位置がある符号のうち、
    # 制約を満たせている位置の梁を抽出する
    def mark_changable_beams(self):
        target_beams = []
        
        require_update_section_nos = self.require_update_section_nos()
        for section_no in require_update_section_nos:
            section = self.section_list.find(section_no)
            for beam in filter(lambda beam : beam.section_no == section_no, self.beam_coordinations):
                connected_section_nos = self.connected_beam_relations(beam)
                connected_sections = list(map(lambda section_no: self.section_list.find(section_no), connected_section_nos))
                constraints = self.merge_constraints(connected_sections)
                for constraint in constraints:
                    if constraint.satisfied(section.depth):
                        # 制約を満たせているなら追加
                        target_beams.append(beam)
                        break

        return target_beams

    # 合理化のため断面を追加
    def add_new_section(self, copy_from_section_no):
        copy_from = self.section_list.find(copy_from_section_no)
        max_no = max(list(map(lambda section: section.section_no, self.section_list.list)))
        next_no = max(100, max_no + 1)

        index = [ i for i, x in enumerate(self.section_list.list) if x.section_no == next_no ]
        if len( index ) == 0:
            new_section = BeamSectionSpec(next_no, copy_from.depth, copy_from.selectable_depth_list)
            self.section_list.list.append(new_section)
            return new_section 
        else:
            return self.section_list.list[index[0]]

    
    # 断面符号を変更する
    # ダイアフラム制約を満たすために、
    # すでに満たしている断面符号を別符号として退避することで
    # 合理化をするための処理
    def change_section_no(self, target_coordination):
        for coordination in self.beam_coordinations:
            if coordination.same_position(target_coordination):
                coordination.section_no = target_coordination.section_no

    # 制約を満たす梁せいを選定する
    def resolve_section(self, section_no):
        target_section = self.section_list.find(section_no)

        constraints = self.connected_section_constraints(target_section)

        # 一旦、「近いほう」に合わせる
        depth = target_section.depth

        lower_target_depth = depth
        upper_target_depth = depth
        for constraint in constraints:
            if constraint.range_upper <= depth:
                lower_target_depth = constraint.range_upper
            if depth <= constraint.range_lower:
                upper_target_depth = constraint.range_lower

        if abs(depth - lower_target_depth) <= abs(upper_target_depth - depth):
            target_section.depth = \
                list(filter(lambda depth: depth <= lower_target_depth, target_section.selectable_depth_list))[-1]
        else:
            target_section.depth = \
                list(filter(lambda depth: upper_target_depth <= depth, target_section.selectable_depth_list))[0]

    def resolve(self):
        target_section_nos = self.require_update_section_nos()
        for section_no in target_section_nos:
            self.resolve_section(section_no)





# 全層の平面プラン
class AllFloorPlans:
    def __init__(self, plans, enabled_change_mark, iteration_limit = 10):
        self.plans = plans
        self.enabled_change_mark = enabled_change_mark
        self.iteration_limit = iteration_limit


    # 符号変更可能な位置の梁を抽出する
    # 各フロアで共通の符号とするため、全層通して
    # 制約を満たしていることを確認する必要がある。
    def change_mark_changable_beam(self):
        beam_position_map = {}

        new_section_map = {}
        for plan in self.plans:
            beams = plan.mark_changable_beams()
            for beam in beams:
                key = beam.key()
                if not (key in beam_position_map):
                    beam_position_map[key] = 0
                beam_position_map[key] += 1
        
        
        floor_count = len(self.plans)

        changable_beam_positions = []
        for key in beam_position_map.keys():
            if beam_position_map[key] == floor_count:
                if not (key in changable_beam_positions):
                    changable_beam_positions.append(key)
        
        new_section_map = {}
        for key in changable_beam_positions:
            for plan in self.plans:
                for beam in filter(lambda beam: beam.key() == key, plan.beam_coordinations):
                    new_section = plan.add_new_section(beam.section_no)
                    if not (beam.section_no in new_section_map):
                        new_section_map[beam.section_no] = new_section

        for plan in self.plans:
            for key in changable_beam_positions:
                for beam in filter(lambda beam: beam.key() == key, plan.beam_coordinations):
                    new_section = new_section_map[beam.section_no]
                    new_beam_coordination = BeamCoordination(beam.start_position, beam.end_position, new_section.section_no)
                    plan.change_section_no( new_beam_coordination )

    def resolve(self):
        for try_count in range(1, self.iteration_limit):
            print("loop %d" % try_count)
            sum_required_update_sections = sum([ len(plan.require_update_section_nos()) for plan in self.plans ])

            if sum_required_update_sections == 0:
                print("終了")
                break

            if self.enabled_change_mark:
                self.change_mark_changable_beam()

            for plan in self.plans:
                plan.resolve()
            


LIMIT_DEPTH = 10000

# ダイアフラムによる制約を表現するクラス
class DiaphragmConstraint:
    def __init__(self, lower, upper = LIMIT_DEPTH, impossible = False):
        self.impossible = impossible
        self.range_lower = lower 
        self.range_upper = upper

    # 制約を満たすか
    def satisfied(self, depth):
        if self.impossible: 
            return False
        else:
            return self.range_lower <= depth and \
                   depth <= self.range_upper  


    # 制約を重ね合わせる
    def merge(self, target):
        impossible_result = DiaphragmConstraint(0, 0, True)
        if self.impossible or target.impossible: 
            return impossible_result 
        else:
            lower1 = self.range_lower
            upper1 = self.range_upper
            lower2 = target.range_lower
            upper2 = target.range_upper

            max_lower = max( lower1,  lower2 )
            min_upper = min( upper1,  upper2 )
            if 0 < lower2 - upper1 or 0 < lower1 - upper2 :
                # 重なりがない場合
                return impossible_result
            else :
                return DiaphragmConstraint(max_lower, min_upper)


class DiaphragmResolverConfig:
    def __init__(self):
        self.enabled_change_mark = True

class DiaphragmResolver:
    def __init__(self, all_floor_plans, config):
        self.all_floor_plans = AllFloorPlans(all_floor_plans, config.enabled_change_mark)

    def resolve(self):
        self.all_floor_plans.resolve()

    def dump_beams(self, floor_index):
        plan = self.all_floor_plans.plans[floor_index]
        for beam in plan.beam_coordinations:
            section = plan.section_list.find(beam.section_no)
            print("%s : No.%d(d=%d)" % (beam.key(), beam.section_no, section.depth))


    def dump_section_list(self, floor_index):
        plan = self.all_floor_plans.plans[floor_index]
        for section in plan.section_list.list:
            print("No.%d(d=%d)" % (section.section_no, section.depth))


if __name__ == "__main__":
    beam_coordinations1 = \
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
    beam_coordinations2 = \
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
    selectable_section_list = list(range(200, 1500, 50))
    section_list1 = \
        [ BeamSectionSpec( 1,  500, selectable_section_list )
        , BeamSectionSpec( 2,  700, selectable_section_list )
        , BeamSectionSpec( 3,  600, selectable_section_list )
        , BeamSectionSpec( 4,  400, selectable_section_list )
        , BeamSectionSpec(11,  800, selectable_section_list )
        , BeamSectionSpec(12, 1000, selectable_section_list )
        , BeamSectionSpec(13,  900, selectable_section_list )
        , BeamSectionSpec(14,  400, selectable_section_list )
        ]
    section_list2 = \
        [ BeamSectionSpec( 1,  500, selectable_section_list )
        , BeamSectionSpec( 2,  700, selectable_section_list )
        , BeamSectionSpec( 3,  600, selectable_section_list )
        , BeamSectionSpec( 4,  400, selectable_section_list )
        , BeamSectionSpec(11,  800, selectable_section_list )
        , BeamSectionSpec(12, 1000, selectable_section_list )
        , BeamSectionSpec(13,  900, selectable_section_list )
        , BeamSectionSpec(14,  400, selectable_section_list )
        ]
    all_floor_plans = \
        [ Plan(beam_coordinations1, BeamSectionList(section_list1) )
        , Plan(beam_coordinations2, BeamSectionList(section_list2) )
        ]
    
    resolver = DiaphragmResolver(all_floor_plans, DiaphragmResolverConfig())
    resolver.resolve()

    resolver.dump_beams(0)
    #resolver.dump_section_list(0)



# %%
