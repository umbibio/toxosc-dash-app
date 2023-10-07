from dash import dcc
from dash import html

import dash_bootstrap_components as dbc

from references import cite


description = f'''
# Toxo Single Cell Atlas

This web portal offers convenient access to some of the datasets and analysis tools used in the corresponding publication {cite('lou2023singlecell_preprint', markdown=True)}.
The datasets here presented are scRNAseq and scATACseq on rapidly dividing Toxoplasma gondii tachyzoites. We also offer a visualization of the protein terciary
structure of several transciption factors of the AP2 family.

## Data and Code availablility

Part of the data is available for download in the [Data](/toxosc/data) section of this portal.

The analysis R code is available on GitHub: 
[https://github.com/umbibio/scToxoplasmaCDC](https://github.com/umbibio/scToxoplasmaCDC) (DOI: [10.5281/zenodo.8219739](10.5281/zenodo.8219739)).
scRNA-seq and CUT&RUN data (fastq) have been deposited to the Sequence Read Archive (SRA) under the accession number SUB13707798.

## Contact

For questions or comments please contact:
[ArriojasMaldonado001@umb.edu](mailto:ArriojasMaldonado001@umb.edu?Subject=About%20your%20ToxoSC%20web%20app)

## Citation
{cite('lou2023singlecell_preprint', full=True, markdown=True)}
'''

menu = None

body = [
    dbc.Row(dbc.Col(
        dbc.Card([
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(dcc.Markdown(description),
                    width={'size': '12', 'offset': '0'}),
                ])
            ),
        ], color="light", outline=True),
    ), class_name="mb-4 mt-4"),
]

