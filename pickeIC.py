#!/usr/bin/env python

import os
import sys
import math
import pickle
from argparse import ArgumentParser

from orangecontrib.bio.ontology import OBOOntology


def pickleIC(obo_file, assoc_file, prefix=None):
    if not prefix:
        prefix = os.path.basename(assoc_file)
        prefix = prefix.split(".")[0]

    tree = OBOOntology(obo_file)

    assoc_feature = {}
    for root in tree.root_terms():
        if root.is_obsolete:
            continue
        assoc_feature.setdefault(root.id, {})

    term_to_root = {}
    for term in tree.terms():
        if term.is_obsolete:
            continue
        root_id = term.id
        for ans in tree.super_terms(term.id):
            if ans.id in assoc_feature:
                root_id = ans.id
                break
        assoc_feature[root_id].setdefault(term.id, set())
        term_to_root.setdefault(term.id, root_id)

    for line in open(assoc_file):
        term_id, feature = line.rstrip().split("\t")
        if not term_to_root.has_key(term_id):
            continue
        assoc_feature[term_to_root[term_id]][term_id].add(feature)
        for ans in tree.super_terms(term_id):
            assoc_feature[term_to_root[ans.id]][ans.id].add(feature)

    for root_id in assoc_feature:
        root_freq = float(len(assoc_feature[root_id][root_id]))
        if root_freq == 0:
            raise Exception("root frequency is zero")
        assoc_ic = {}
        for term_id in assoc_feature[root_id]:
            fs = assoc_feature[root_id][term_id]
            term_freq = len(fs)
            if term_freq == 0:
                assoc_ic.setdefault(term_id, float('nan'))
                continue
            ic = -math.log10(term_freq/root_freq)
            assoc_ic.setdefault(term_id, ic)
        name = tree.term(root_id).name.replace(" ","_")
        f = open(".".join([prefix,name,"ic"]), "wb")
        pickle.dump(assoc_ic, f)
        f.close()


if __name__ == "__main__":
    description = "Generate gene-term log10 IC data"
    parser = ArgumentParser(description=description)
    parser.add_argument("--prefix", type=str, help="Output prefix", default=None)
    parser.add_argument("obo", type=str, help="Ontology OBO")
    parser.add_argument("assoc", type=str, help="Term and gene association")
    args = parser.parse_args()
    try:
        pickleIC(args.obo, args.assoc, args.prefix)
    except KeyboardInterrupt: pass
