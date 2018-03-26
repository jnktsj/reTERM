# reTERM

How to run the script:

```shell
#!/bin/sh

reTERM="/data/tsujij/mouse_epigenome/functional_terms/reTERM/reTERM.py"

GO_OBO="/data/tsujij/mouse_epigenome/functional_terms/term_db/go/go-basic.obo"
GO_BP="/data/tsujij/mouse_epigenome/functional_terms/term_db/go/goa_mouse.biological_process.ic"
GO_CC="/data/tsujij/mouse_epigenome/functional_terms/term_db/go/goa_mouse.cellular_component.ic"
GO_MF="/data/tsujij/mouse_epigenome/functional_terms/term_db/go/goa_mouse.molecular_function.ic"

MGI_OBO="/data/tsujij/mouse_epigenome/functional_terms/term_db/mgi/mpheno.obo"
MGI_IC="/data/tsujij/mouse_epigenome/functional_terms/term_db/mgi/mpheno_assoc.mammalian_phenotype.ic"

HPO_OBO="/data/tsujij/mouse_epigenome/functional_terms/term_db/hpo/hpo.obo"
HPO_IC="/data/tsujij/mouse_epigenome/functional_terms/term_db/hpo/hpo_assoc.All.ic"

PARENT="/data/tsujij/mouse_epigenome/functional_terms/enhancer/filtered_terms/"
INPUT="/data/tsujij/mouse_epigenome/functional_terms/enhancer/input/"


python ${reTERM} --sim-cutoff 0.4 ${GO_OBO} ${GO_BP} ${INPUT}/go_terms/BP/${1} > ${PARENT}/semsim_40/go_terms/BP/${1}
python ${reTERM} --sim-cutoff 0.4 ${GO_OBO} ${GO_MF} ${INPUT}/go_terms/MF/${1} > ${PARENT}/semsim_40/go_terms/MF/${1}
python ${reTERM} --sim-cutoff 0.4 ${GO_OBO} ${GO_CC} ${INPUT}/go_terms/CC/${1} > ${PARENT}/semsim_40/go_terms/CC/${1}
python ${reTERM} --sim-cutoff 0.4 ${MGI_OBO} ${MGI_IC} ${INPUT}/phenotype/mouse/${1} > ${PARENT}/semsim_40/phenotype/mouse/${1}
python ${reTERM} --sim-cutoff 0.4 ${HPO_OBO} ${HPO_IC} ${INPUT}/phenotype/human/${1} > ${PARENT}/semsim_40/phenotype/human/${1}
```

> Maybe it can be compared to revigo or similar tools?
