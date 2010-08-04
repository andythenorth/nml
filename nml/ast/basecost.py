from nml import expression, generic, nmlop
from nml.ast import assignment
from nml.actions import action0

class BaseCost:
    """
    AST Node for a base costs table.

    @ivar costs: List of base cost values to set.
    @type costs: C{list} of L{Assignment}

    @ivar pos: Position information of the basecost block.
    @type pos: L{Position}
    """
    def __init__(self, costs, pos):
        self.costs = costs
        self.pos = pos

    def pre_process(self):
        new_costs = []

        for cost in self.costs:
            cost.value = cost.value.reduce()
            if isinstance(cost.value, expression.ConstantNumeric):
                generic.check_range(cost.value.value, -8, 16, 'Base cost value', cost.value.pos)
                cost.value.value += 8 #8 is the 'neutral value' for base costs
            else:
                cost.value = expression.BinOp(nmlop.ADD, cost.value, expression.ConstantNumeric(8), cost.value.pos)

            if isinstance(cost.name, expression.Identifier):
                if cost.name.value in base_cost_table:
                    cost.name = expression.ConstantNumeric(base_cost_table[cost.name.value][0])
                    new_costs.append(cost)
                elif cost.name.value in generic_base_costs:
                    #create temporary list, so it can be sorted for efficiency
                    tmp_list = []
                    for num, type in base_cost_table.values():
                        if type == cost.name.value:
                            tmp_list.append(assignment.Assignment(expression.ConstantNumeric(num), cost.value, cost.name.pos))
                    tmp_list.sort(lambda x, y: cmp(x.name.value, y.name.value))
                    new_costs.extend(tmp_list)
                else:
                    raise generic.ScriptError("Unrecognized base cost identifier '%s' encountered" % cost.name.value)
            else:
                cost.name = cost.name.reduce()
                if isinstance(cost.name, expression.ConstantNumeric):
                    generic.check_range(cost.name.value, 0, len(base_cost_table), 'Base cost number', cost.name.pos)
                new_costs.append(cost)
        self.costs = new_costs

    def debug_print(self, indentation):
        print indentation*' ' + 'Base costs'
        for cost in self.costs:
            cost.debug_print(indentation + 2)

    def get_action_list(self):
        return action0.get_basecost_action(self)

base_cost_table = {
    'PR_STATION_VALUE'              : (0,  ''),
    'PR_BUILD_RAIL'                 : (1,  'PR_CONSTRUCTION'),
    'PR_BUILD_ROAD'                 : (2,  'PR_CONSTRUCTION'),
    'PR_BUILD_SIGNALS'              : (3,  'PR_CONSTRUCTION'),
    'PR_BUILD_BRIDGE'               : (4,  'PR_CONSTRUCTION'),
    'PR_BUILD_DEPOT_TRAIN'          : (5,  'PR_CONSTRUCTION'),
    'PR_BUILD_DEPOT_ROAD'           : (6,  'PR_CONSTRUCTION'),
    'PR_BUILD_DEPOT_SHIP'           : (7,  'PR_CONSTRUCTION'),
    'PR_BUILD_TUNNEL'               : (8,  'PR_CONSTRUCTION'),
    'PR_BUILD_STATION_RAIL'         : (9,  'PR_CONSTRUCTION'),
    'PR_BUILD_STATION_RAIL_LENGTH'  : (10, 'PR_CONSTRUCTION'),
    'PR_BUILD_STATION_AIRPORT'      : (11, 'PR_CONSTRUCTION'),
    'PR_BUILD_STATION_BUS'          : (12, 'PR_CONSTRUCTION'),
    'PR_BUILD_STATION_TRUCK'        : (13, 'PR_CONSTRUCTION'),
    'PR_BUILD_STATION_DOCK'         : (14, 'PR_CONSTRUCTION'),
    'PR_BUILD_VEHICLE_TRAIN'        : (15, 'PR_BUILD_VEHICLE'),
    'PR_BUILD_VEHICLE_WAGON'        : (16, 'PR_BUILD_VEHICLE'),
    'PR_BUILD_VEHICLE_AIRCRAFT'     : (17, 'PR_BUILD_VEHICLE'),
    'PR_BUILD_VEHICLE_ROAD'         : (18, 'PR_BUILD_VEHICLE'),
    'PR_BUILD_VEHICLE_SHIP'         : (19, 'PR_BUILD_VEHICLE'),
    'PR_BUILD_TREES'                : (20, 'PR_CONSTRUCTION'),
    'PR_TERRAFORM'                  : (21, 'PR_CONSTRUCTION'),
    'PR_CLEAR_GRASS'                : (22, 'PR_CONSTRUCTION'),
    'PR_CLEAR_ROUGH'                : (23, 'PR_CONSTRUCTION'),
    'PR_CLEAR_ROCKS'                : (24, 'PR_CONSTRUCTION'),
    'PR_CLEAR_FIELDS'               : (25, 'PR_CONSTRUCTION'),
    'PR_CLEAR_TREES'                : (26, 'PR_CONSTRUCTION'),
    'PR_CLEAR_RAIL'                 : (27, 'PR_CONSTRUCTION'),
    'PR_CLEAR_SIGNALS'              : (28, 'PR_CONSTRUCTION'),
    'PR_CLEAR_BRIDGE'               : (29, 'PR_CONSTRUCTION'),
    'PR_CLEAR_DEPOT_TRAIN'          : (30, 'PR_CONSTRUCTION'),
    'PR_CLEAR_DEPOT_ROAD'           : (31, 'PR_CONSTRUCTION'),
    'PR_CLEAR_DEPOT_SHIP'           : (32, 'PR_CONSTRUCTION'),
    'PR_CLEAR_TUNNEL'               : (33, 'PR_CONSTRUCTION'),
    'PR_CLEAR_WATER'                : (34, 'PR_CONSTRUCTION'),
    'PR_CLEAR_STATION_RAIL'         : (35, 'PR_CONSTRUCTION'),
    'PR_CLEAR_STATION_AIRPORT'      : (36, 'PR_CONSTRUCTION'),
    'PR_CLEAR_STATION_BUS'          : (37, 'PR_CONSTRUCTION'),
    'PR_CLEAR_STATION_TRUCK'        : (38, 'PR_CONSTRUCTION'),
    'PR_CLEAR_STATION_DOCK'         : (39, 'PR_CONSTRUCTION'),
    'PR_CLEAR_HOUSE'                : (40, 'PR_CONSTRUCTION'),
    'PR_CLEAR_ROAD'                 : (41, 'PR_CONSTRUCTION'),
    'PR_RUNNING_TRAIN_STEAM'        : (42, 'PR_RUNNING'),
    'PR_RUNNING_TRAIN_DIESEL'       : (43, 'PR_RUNNING'),
    'PR_RUNNING_TRAIN_ELECTRIC'     : (44, 'PR_RUNNING'),
    'PR_RUNNING_AIRCRAFT'           : (45, 'PR_RUNNING'),
    'PR_RUNNING_ROADVEH'            : (46, 'PR_RUNNING'),
    'PR_RUNNING_SHIP'               : (47, 'PR_RUNNING'),
    'PR_BUILD_INDUSTRY'             : (48, 'PR_CONSTRUCTION'),
    'PR_CLEAR_INDUSTRY'             : (49, 'PR_CONSTRUCTION'),
    'PR_BUILD_UNMOVABLE'            : (50, 'PR_CONSTRUCTION'),
    'PR_CLEAR_UNMOVABLE'            : (51, 'PR_CONSTRUCTION'),
    'PR_BUILD_WAYPOINT_RAIL'        : (52, 'PR_CONSTRUCTION'),
    'PR_CLEAR_WAYPOINT_RAIL'        : (53, 'PR_CONSTRUCTION'),
    'PR_BUILD_WAYPOINT_BUOY'        : (54, 'PR_CONSTRUCTION'),
    'PR_CLEAR_WAYPOINT_BUOY'        : (55, 'PR_CONSTRUCTION'),
    'PR_TOWN_ACTION'                : (56, 'PR_CONSTRUCTION'),
    'PR_BUILD_FOUNDATION'           : (57, 'PR_CONSTRUCTION'),
    'PR_BUILD_INDUSTRY_RAW'         : (58, 'PR_CONSTRUCTION'),
    'PR_BUILD_TOWN'                 : (59, 'PR_CONSTRUCTION'),
    'PR_BUILD_CANAL'                : (60, 'PR_CONSTRUCTION'),
    'PR_CLEAR_CANAL'                : (61, 'PR_CONSTRUCTION'),
    'PR_BUILD_AQUEDUCT'             : (62, 'PR_CONSTRUCTION'),
    'PR_CLEAR_AQUEDUCT'             : (63, 'PR_CONSTRUCTION'),
    'PR_BUILD_LOCK'                 : (64, 'PR_CONSTRUCTION'),
    'PR_CLEAR_LOCK'                 : (65, 'PR_CONSTRUCTION'),
}

generic_base_costs = ['PR_CONSTRUCTION', 'PR_RUNNING', 'PR_BUILD_VEHICLE']