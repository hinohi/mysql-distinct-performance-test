import argparse
import uuid


def main():
    p = argparse.ArgumentParser()
    p.add_argument('n_col', type=int)
    p.add_argument('n_row', type=int)
    args = p.parse_args()

    buf = [
        'drop database if exists distinct_test;',
        'create database distinct_test;',
        f'create table distinct_test.t{args.n_col} (',
        'id int primary key',
    ]
    for i in range(args.n_col):
        buf.append(f', col{i} varchar(36) not null')
    buf.append(') ROW_FORMAT=DYNAMIC;')
    print('\n'.join(buf))

    for i in range(args.n_row):
        s = '(%i, %s)' % (i + 1, ', '.join(repr(str(uuid.uuid4())) for _ in range(args.n_col)))
        if i % 100 == 0:
            print(f';insert into distinct_test.t{args.n_col} values', s)
        else:
            print(',', s)
    print(';')

    print(f"""
create table distinct_test.s{args.n_col} (
    id int primary key auto_increment,
    col varchar(36) not null,
    key i_s_col (col)
) ROW_FORMAT=DYNAMIC;
insert into distinct_test.s{args.n_col} (col) select col0 from distinct_test.t{args.n_col};
insert into distinct_test.s{args.n_col} (col) select col0 from distinct_test.t{args.n_col};
insert into distinct_test.s{args.n_col} (col) select col0 from distinct_test.t{args.n_col};
insert into distinct_test.s{args.n_col} (col) select col0 from distinct_test.t{args.n_col};
insert into distinct_test.s{args.n_col} (col) select col0 from distinct_test.t{args.n_col};
""")


if __name__ == '__main__':
    main()
