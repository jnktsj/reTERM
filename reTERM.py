#!/usr/bin/env python

import os
import sys
import math
import pickle
from operator import itemgetter
from argparse import ArgumentParser

from orangecontrib.bio.ontology import OBOOntology


def reTERM(obo_file, term_ic_file, term_list_file, sim_cutoff, freq_cutoff):
    tree = OBOOntology(obo_file)
    ic = pickle.load(open(term_ic_file,"rb"))

    term_p = {}
    super_terms = set()
    for line in open(term_list_file):
        line = line.rstrip().split("\t")
        term_id = line[0]
        if not ic.has_key(term_id):
            continue
        p_value = float(line[1])
        term_p.setdefault(term_id, p_value)
        sp = [t.id for t in tree.super_terms(term_id)
              if not t.is_obsolete]
        super_terms = super_terms.union(sp)

    # compute semantic similarity
    sem_sim = []
    terms = sorted(term_p.keys())
    for i in xrange(len(terms)-1):
        for j in xrange(i+1, len(terms)):
            ans_i = set([t.id for t in tree.super_terms(terms[i])
                         if not t.is_obsolete])
            ans_j = set([t.id for t in tree.super_terms(terms[j])
                         if not t.is_obsolete])
            common_ans = ans_i.intersection(ans_j)
            if len(common_ans) == 0:
                continue
            ica_cand = [ic[t] for t in common_ans if not math.isnan(ic[t])]
            if len(ica_cand) == 0:
                continue
            ica = max(ica_cand)
            weight = 1 - 10**-ica
            simrel_val = (2*ica)/(ic[terms[i]]+ic[terms[j]]) * weight
            if math.isnan(simrel_val):
                continue
            sem_sim.append([(terms[i],terms[j]), simrel_val])
    sem_sim = sorted(sem_sim, key=itemgetter(1), reverse=True)

    # decide terms to be removed
    winner = {}
    grave = set()
    for i in xrange(len(sem_sim)):
        if sem_sim[i][1] < sim_cutoff:
            break
        term_i = sem_sim[i][0][0]
        term_j = sem_sim[i][0][1]
        freq_i = 10**-ic[term_i]
        freq_j = 10**-ic[term_j]
        survival, dead = "", ""
        if freq_i >= freq_cutoff or freq_j >= freq_cutoff:
            if freq_i > freq_j:
                survival, dead = term_j, term_i
            else:
                survival, dead = term_i, term_j
        elif term_p[term_i] == term_p[term_j]:
            if freq_i > freq_j:
                survival, dead = term_j, term_i
            else:
                survival, dead = term_i, term_j
        else:
            if term_p[term_i] > term_p[term_j]:
                survival, dead = term_j, term_i
            else:
                survival, dead = term_i, term_j
        grave.add(dead)
        winner.setdefault(survival, set()).add(dead)        

    for term_id in terms:
        if term_id in grave:
            continue
        heads = str(len(winner.get(term_id, set())))
        print "\t".join([term_id, heads, str(term_p[term_id])])


if __name__ == "__main__":
    description = "Compute semantic similarity and reduce terms"
    parser = ArgumentParser(description=description)
    parser.add_argument("obo", type=str, help="Ontology OBO")
    parser.add_argument("term_ic", type=str, help="Term IC data")
    parser.add_argument("term_list", type=str, help="Term list")
    parser.add_argument("--sim-cutoff", type=float, default=0.4,
                        help="Semantic similarity cutoff (default=%(default)s)")
    parser.add_argument("--freq-cutoff", type=float, default=0.05,
                        help="Term frequency cutoff for broad terms (default=%(default)s)")
    args = parser.parse_args()
    try:
        reTERM(args.obo, args.term_ic, args.term_list,
               args.sim_cutoff, args.freq_cutoff)
    except KeyboardInterrupt: pass

