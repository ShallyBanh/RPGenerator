import rule_enactor


enactor = rule_enactor.RuleEnactor

rule = "if x then y \n 1+1 \n 1 + 1 \n 5 * 5 \n 5 < 6 \n 5 less than 6 \n 5d6"

print(enactor.perform_action(enactor, rule))