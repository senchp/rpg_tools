#!/usr/bin/env python
"""Evaluate rolls from dice expressions."""

import random

def eval_roll(exp):
    """Evaluate a roll from a dice expression.

    Accepts dice expression including terms of the form:
        ndN (roll and add n dN dice), 
        nd% (roll n d100 dice and add),
        n (add n)
    Returns the random result and a list containing strings
        representing the results of each term.

    Example:
        3d6+8+d%
        rolls 3 d6 dice and 1 d100 dice, and adds the results
        together with 8.
    """
    random.seed(a=None) #initializes with system time

    results = 0
    results_verbose = []
    #split the expression into its parts and evaluate:
    exp = exp.strip()
    while len(exp)>0:
        a_pos, s_pos = exp.rfind('+'), exp.rfind('-')
        if a_pos > s_pos:
            roll, exp = exp[a_pos+1:], exp[:a_pos]
            mult = 1
        elif a_pos < s_pos:
            roll, exp = exp[s_pos+1:], exp[:s_pos]
            mult = -1
        else:
            assert (a_pos == -1) and (s_pos == -1), "Parsing error!"
            roll, exp = exp, ''
            mult = 1
        
        res = 0
        res_verbose = '-(' if mult==-1 else '+('
        if 'd' in roll:
            num, _, die = roll.partition('d')
            if num == '':
                num = 1
            else:
                num = int(num)

            if die == '%':
                die = 100
            else:
                die = int(die)

            for i in range(num):
                val = random.randint(1, die)
                res += val
                res_verbose += '+%s'%val
        else:
            res = int(roll)
            res_verbose += '%s'%res
        res *= mult
        results_verbose.append(res_verbose + ')')
        results += res
    return results, results_verbose[::-1]

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Roll a set of dice')
    parser.add_argument('expression', metavar='exp', type=str, 
            help='dice expression to roll')
    parser.add_argument('--verbose', help="increase output verbosity",
            action="store_true")

    args = parser.parse_args()

    exp = args.expression
    print('Evaluating {0}:'.format(exp))

    results, results_verbose = eval_roll(exp)

    if args.verbose:
        print(''.join(results_verbose))
    print(results)
