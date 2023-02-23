# 概要

MySQL で select distinct の対象として多すぎるカラムを指定するとカラム数に比例して遅くなる。
そういった場合、一旦 pk を含む少数のカラムで distinct してから pk で引き直す方が早い。

対象カラムに pk が含まれていても同じ。

## 検証結果

時間単位は秒、3回やった中央値。

| MySQL                       | カラム数 | そのまま select distinct | pk 引き直し |
| :-------------------------- | -------: | -----------------------: | ----------: |
| docker mysql:8.0.32(oracle) |      150 |                     0.89 |        0.17 |
|                             |      100 |                     0.57 |        0.16 |
|                             |       50 |                     0.25 |        0.05 |
| docker mysql:8.0.32-debian  |      150 |                     1.05 |        0.16 |
|                             |      100 |                     0.61 |        0.06 |
|                             |       50 |                     0.33 |        0.06 |
| docker mysql:5.7.41-debian  |      150 |                     0.55 |        0.03 |
|                             |      100 |                     0.31 |        0.03 |
|                             |       50 |                     0.17 |        0.03 |
| Aurora MySQL v2 r6g.large   |      150 |                     1.09 |        0.08 |
|                             |      100 |                     0.63 |        0.08 |
|                             |       50 |                     0.26 |        0.08 |

## テーブルセットアップ

カラム数=3 の例。

```sql
drop database if exists distinct_test;
create database distinct_test;

create table distinct_test.t3 (
id int primary key
, col0 varchar(36) not null
, col1 varchar(36) not null
, col2 varchar(36) not null
) ROW_FORMAT=DYNAMIC;

insert into distinct_test.t3 values
(1, '2c43777b-4d8d-4aac-aa46-8559606ead38', 'f5230b65-261c-4939-a481-ec335bdbc642', 'e360893e-dd6c-4695-8cfb-a9b3a75a207c')
-- 続く
;

create table distinct_test.s3 (
    id int primary key auto_increment,
    col varchar(36) not null,
    key i_s_col (col)
) ROW_FORMAT=DYNAMIC;
insert into distinct_test.s3 (col) select col0 from distinct_test.t3;
insert into distinct_test.s3 (col) select col0 from distinct_test.t3;
insert into distinct_test.s3 (col) select col0 from distinct_test.t3;
insert into distinct_test.s3 (col) select col0 from distinct_test.t3;
insert into distinct_test.s3 (col) select col0 from distinct_test.t3;
```

## 再現手順

1. SQL 生成

    ```sh
    mkdir -p sql
    python gen_data_sql.py 150 10000 > sql/150.sql
    ```
1. mysql 起動

    ```sh
    docker compose up -d
    ```
1. MySQL に入って table 作成 & データ投入

    ```sh
    docker compose exec mysql8 mysql
    ```

    ```
    mysql> source /sql/150.sql
    ```
1. pk + nカラムを select distinct

    ```sql
    -- 150
    select distinct
        t.id, col0, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15, col16, col17, col18, col19, col20, col21, col22, col23, col24, col25, col26, col27, col28, col29, col30, col31, col32, col33, col34, col35, col36, col37, col38, col39, col40, col41, col42, col43, col44, col45, col46, col47, col48, col49, col50, col51, col52, col53, col54, col55, col56, col57, col58, col59, col60, col61, col62, col63, col64, col65, col66, col67, col68, col69, col70, col71, col72, col73, col74, col75, col76, col77, col78, col79, col80, col81, col82, col83, col84, col85, col86, col87, col88, col89, col90, col91, col92, col93, col94, col95, col96, col97, col98, col99, col100, col101, col102, col103, col104, col105, col106, col107, col108, col109, col110, col111, col112, col113, col114, col115, col116, col117, col118, col119, col120, col121, col122, col123, col124, col125, col126, col127, col128, col129, col130, col131, col132, col133, col134, col135, col136, col137, col138, col139, col140, col141, col142, col143, col144, col145, col146, col147, col148, col149
    from distinct_test.t150 as t join distinct_test.s150 as s on t.col0 = s.col
    order by t.col0
    limit 50;
    
    -- 100
    select distinct
        t.id, col0, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15, col16, col17, col18, col19, col20, col21, col22, col23, col24, col25, col26, col27, col28, col29, col30, col31, col32, col33, col34, col35, col36, col37, col38, col39, col40, col41, col42, col43, col44, col45, col46, col47, col48, col49, col50, col51, col52, col53, col54, col55, col56, col57, col58, col59, col60, col61, col62, col63, col64, col65, col66, col67, col68, col69, col70, col71, col72, col73, col74, col75, col76, col77, col78, col79, col80, col81, col82, col83, col84, col85, col86, col87, col88, col89, col90, col91, col92, col93, col94, col95, col96, col97, col98, col99
    from distinct_test.t150 as t join distinct_test.s150 as s on t.col0 = s.col
    order by t.col0
    limit 50;

    -- 50
    select distinct
        t.id, col0, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15, col16, col17, col18, col19, col20, col21, col22, col23, col24, col25, col26, col27, col28, col29, col30, col31, col32, col33, col34, col35, col36, col37, col38, col39, col40, col41, col42, col43, col44, col45, col46, col47, col48, col49
    from distinct_test.t150 as t join distinct_test.s150 as s on t.col0 = s.col
    order by t.col0
    limit 50;
    ```

1. pk + order by 用のカラムを select distinct してから pk で引き直し

    ```sql
    -- 150
    select
        id, t.col0, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15, col16, col17, col18, col19, col20, col21, col22, col23, col24, col25, col26, col27, col28, col29, col30, col31, col32, col33, col34, col35, col36, col37, col38, col39, col40, col41, col42, col43, col44, col45, col46, col47, col48, col49, col50, col51, col52, col53, col54, col55, col56, col57, col58, col59, col60, col61, col62, col63, col64, col65, col66, col67, col68, col69, col70, col71, col72, col73, col74, col75, col76, col77, col78, col79, col80, col81, col82, col83, col84, col85, col86, col87, col88, col89, col90, col91, col92, col93, col94, col95, col96, col97, col98, col99, col100, col101, col102, col103, col104, col105, col106, col107, col108, col109, col110, col111, col112, col113, col114, col115, col116, col117, col118, col119, col120, col121, col122, col123, col124, col125, col126, col127, col128, col129, col130, col131, col132, col133, col134, col135, col136, col137, col138, col139, col140, col141, col142, col143, col144, col145, col146, col147, col148, col149
    from 
        (
            select distinct t.id, col0
            from distinct_test.t150 as t join distinct_test.s150 as s on t.col0 = s.col
            order by t.col0 limit 50
        ) as o
        join distinct_test.t150 as t using(id)
    order by col0;

    -- 100
    select
        id, t.col0, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15, col16, col17, col18, col19, col20, col21, col22, col23, col24, col25, col26, col27, col28, col29, col30, col31, col32, col33, col34, col35, col36, col37, col38, col39, col40, col41, col42, col43, col44, col45, col46, col47, col48, col49, col50, col51, col52, col53, col54, col55, col56, col57, col58, col59, col60, col61, col62, col63, col64, col65, col66, col67, col68, col69, col70, col71, col72, col73, col74, col75, col76, col77, col78, col79, col80, col81, col82, col83, col84, col85, col86, col87, col88, col89, col90, col91, col92, col93, col94, col95, col96, col97, col98, col99
    from 
        (
            select distinct t.id, col0
            from distinct_test.t150 as t join distinct_test.s150 as s on t.col0 = s.col
            order by t.col0 limit 50
        ) as o
        join distinct_test.t150 as t using(id)
    order by col0;

    -- 50
    select
        id, t.col0, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15, col16, col17, col18, col19, col20, col21, col22, col23, col24, col25, col26, col27, col28, col29, col30, col31, col32, col33, col34, col35, col36, col37, col38, col39, col40, col41, col42, col43, col44, col45, col46, col47, col48, col49, col50, col51, col52, col53, col54, col55, col56, col57, col58, col59, col60, col61, col62, col63, col64, col65, col66, col67, col68, col69, col70, col71, col72, col73, col74, col75, col76, col77, col78, col79, col80, col81, col82, col83, col84, col85, col86, col87, col88, col89, col90, col91, col92, col93, col94, col95, col96, col97, col98, col99
    from 
        (
            select distinct t.id, col0
            from distinct_test.t150 as t join distinct_test.s150 as s on t.col0 = s.col
            order by t.col0 limit 50
        ) as o
        join distinct_test.t150 as t using(id)
    order by col0;
    ```
1. 片付け

    ```sh
    docker compose down -v
    ```
