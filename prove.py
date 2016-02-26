#!/usr/bin/env python

import agate

def filter_func(r):
    return \
        r['risk_name'] == 'Air pollution' and \
        r['sex_name'] == 'Both' and \
        r['age_name'] == 'All Ages' and \
        r['year_name'] == 2013

def main():
    # text = agate.Text()
    number = agate.Number()
    #
    # columns = OrderedDict([
    #     ('naics', text),
    #     ('emp', number),
    #     ('est', number)
    # ])

    print('Loading')
    table = agate.Table.from_csv('IHME-Data-Air pollution-Deaths.csv')

    print('Filtering')
    table = table.where(filter_func)

    print('Calculating MOE')
    table = table.compute([
        ('nm_moe', agate.Formula(number, lambda r: r['nm_mean'] / (r['nm_mean'] - r['nm_lower']))),
        ('rt_moe', agate.Formula(number, lambda r: r['rt_mean'] / (r['rt_mean'] - r['rt_lower'])))
    ])

    print('Selecting')
    table = table.select([
        'location_name',
        'nm_mean',
        'nm_moe',
        'rt_mean',
        'rt_moe'
    ])

    print('Saving to filtered.csv')
    table.to_csv('filtered.csv')

if __name__ == '__main__':
    main()
