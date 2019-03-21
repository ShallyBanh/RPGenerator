import rule_enactor


enactor = rule_enactor.RuleEnactor()

rule = "target guy\n"
rule += "x = 0\n"
rule += "x\n"
rule += "increase x by 5\n"
rule += "x\n"
rule += "multiply x by 2 \n"
rule += "x\n"
rule += "divide x by 10\n"
rule += "x\n"
rule += "reduce x by 1\n"
rule += "x\n"
rule += "set x to 11\n"
rule += "x\n"
rule += "y = 1 + 1\n"
rule += "y\n"
rule += "z = 5-1\n"
rule += "z\n"
rule += "5==5\n"
rule += "y equals 2\n"
rule += "y equals 5\n"
rule += "1<3\n"
rule += "3<1\n"
rule += "1>3\n"
rule += "3>1\n"
rule += "3 less than 1\n"
rule += "1 less than 3\n"
rule += "3 greater than 1\n"
rule += "1 greater than 3\n"
rule += "a = 5*5\n"
rule += "a\n"
rule += "b = 5/5\n"
rule += "b\n"
rule += "a += 5\n"
rule += "a\n"
rule += "a -= 5\n"
rule += "a\n"
rule += "b *= 10\n"
rule += "b\n"
rule += "b /= 2\n"
rule += "b\n"

rule += "test1 = 5\n"
rule += "test2 = 5\n"
rule += "test3 = 0\n"
rule += "if test1 equals test2 and test1 > 2 then test3 = 900\n"
rule += "test3\n"

rule += "test1 = 1\n"
rule += "test2 = 5\n"
rule += "test3 = 0\n"
rule += "if test1 equals test2 or test1 equals 1 then test3 = 900\n"
rule += "test3\n"

rule += "self.HP\n"
rule += "target.HP\n"

rule += "if all self within(3,3) of entity then reduce entity.HP by 3\n"

rule += "self.HP\n"
rule += "target.HP\n"

hp_time = rule_enactor.Attribute('HP', 10)
actor = rule_enactor.Entity("actor", "entity")
actor.add_attribute(hp_time)

hp_boys = rule_enactor.Attribute('HP', 20)
within_guy = rule_enactor.Entity("guy", "entity")
within_guy.add_attribute(hp_boys)
within_guy.x = 2
within_guy.y = 2

enactor.add_new_entity(actor)
enactor.add_new_entity(within_guy)

enactor.perform_action(rule, actor)