import os
import bibtexparser

from dash import html

with open(os.path.join('assets', 'references.bib')) as bibtex_file:
    references = bibtexparser.load(bibtex_file).entries


references_dict = {}
for item in references:
    references_dict[item['ID']] = item


months = {
    '1': 'January', '01': 'January', 'Jan': 'January', 'January': 'January',
    '2': 'February', '02': 'February', 'Feb': 'February', 'February': 'February',
    '3': 'March', '03': 'March', 'Mar': 'March', 'March': 'March',
    '4': 'April', '04': 'April', 'Apr': 'April', 'April': 'April',
    '5': 'May', '05': 'May', 'May': 'May', 'May': 'May',
    '6': 'June', '06': 'June', 'Jun': 'June', 'June': 'June',
    '7': 'July', '07': 'July', 'Jul': 'July', 'July': 'July',
    '8': 'August', '08': 'August', 'Aug': 'August', 'August': 'August',
    '9': 'September', '09': 'September', 'Sep': 'September', 'September': 'September',
    '10': 'October', 'Oct': 'October', 'October': 'October',
    '11': 'November', 'Nov': 'November', 'November': 'November',
    '12': 'December', 'Dec': 'December', 'December': 'December',
}


def cite(key, full=False, markdown=False):
    if key not in references_dict:
        return

    ref = references_dict[key]
    authors = []
    for i, a in enumerate(ref['author'].split(' and ')):
        assert ', ' in a
        familyname, givenname = a.split(', ')
        a = givenname + ' ' + familyname
        authors.append(a)
        if i == 0:
            first_author_familyname = familyname
    authors_str = ', '.join(authors[:-1]) + ' and ' + authors[-1]

    if not full:
        if 'url' in ref:
            if markdown:
                return f"[({first_author_familyname}, et al. {ref['year']})]({ref['url']})"
            else:
                return html.A(f"({first_author_familyname}, et al. {ref['year']})", href=ref['url'], target='blank')
        else:
                return f"({first_author_familyname}, et al. {ref['year']})"


    if 'doi' in ref:
        doi_url = 'https://doi.org/' + ref['doi']
        if markdown:
            doi_url = f"[{doi_url}]({doi_url})"
        else:
            doi_url = html.A(doi_url, href=doi_url, target='blank')
    else:
        doi_url = None

    if ref.get('journal'):
        published_str = "Published:"
        jour = ref['journal']
    else:
        published_str = "Submitted:"
        jour = ''
        if ref.get('publisher'):
            jour = ref['publisher']
    if 'month' in ref:
        published_str += ' ' + months[ref['month']] 
    published_str += ' ' + ref['year']

    if markdown:
        return f'''
“{ref['title'].strip('{}')}.”  
{authors_str}.  
*{jour}*{', Volume ' + ref['volume'] if 'volume' in ref else ''}{', Issue ' + ref['number'] if 'number' in ref else ''}  
{doi_url}  
{published_str}
'''

    return html.Div([
        html.Span('“' + ref['title'].strip('{}') + '”. '), html.Br(),
        html.Span(authors_str + '. '), html.Br(),
        html.I(jour),
        ', Volume ' + ref['volume'] if 'volume' in ref else None,
        ', Issue ' + ref['number'] if 'number' in ref else None,
        html.Br() if doi_url else None,
        doi_url,
        html.Br() if published_str else None,
        published_str,
    ])
