create database cache;
create database stats;

create table `source_statistics` (
  `id` int(11) not null auto_increment,
  `source_id` varchar(255) default 'all',
  `segment_id` varchar(255) default 'all',
  `avg_values_per_day` double ,
  `avg_records_per_day` double,
  `median_values_per_day` double,
  `median_records_per_day` double,
  `avg_stddev` double,
  `median_stddev` double,
  `values_last_7_days` double,
  `values_last_14_days` double,
  `values_last_21_days` double,
  `values_last_28_days` double,
  `values_last_60_days` double,
  `values_last_90_days` double,
  `records_last_7_days` double,
  `records_last_14_days` double,
  `records_last_21_days` double,
  `records_last_28_days` double,
  `records_last_60_days` double,
  `records_last_90_days` double,
  `additional_values` longtext,
  `updated` timestamp default current_timestamp,
  primary key (`id`),
  key `cache_table_updated` (`updated`),
  key `logical_key` (`source_id`, `segment_id` )
) engine=innodb default charset=utf8;

insert into source_statistics
(source_id,segment_id,  values_last_14_days, records_last_21_days,
values_last_60_days, median_records_per_day,
records_last_90_days, avg_records_per_day, avg_values_per_day,
avg_stddev, records_last_60_days, values_last_28_days, median_values_per_day,
 median_stddev, records_last_14_days, values_last_90_days, values_last_7_days,
 values_last_21_days, records_last_7_days, records_last_28_days )
 VALUES
 ('device_grid_widget', 'all', 5,6,4,3,4,5,6,7,8,6,5,4,3,3,4,5,6,7)
 ;