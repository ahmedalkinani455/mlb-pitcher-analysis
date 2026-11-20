-- PART 1
select *
from pitchers;

select "last_name, first_name", woba, xwoba
from pitchers;

select "last_name, first_name"
from pitchers
where whiff_percent > 30;

select "last_name, first_name"
from pitchers
order by bb_percent asc
limit 5;

select "last_name, first_name"
from pitchers
where k_percent > 25
order by k_percent desc;



-- PART 2
select round(avg(woba), 2) as avg_woba, round(avg(xwoba), 2) as avg_xwoba
from pitchers;

select max(k_percent) as max_strikeout, min(k_percent) as min_strikeout
from pitchers;

select round(avg(k_percent), 2) as avg_strikeout, round(avg(bb_percent), 2) as avg_walk, round(avg(whiff_percent), 2) as avg_whiff
from pitchers;

select count(*) as total_pitchers
from pitchers;

select round(avg(woba), 2) as avg_woba
from pitchers
where k_percent > 25;


-- PART 3
select "last_name, first_name", whiff_percent, 
	case 
	when whiff_percent >= 30 then 'High'
	when whiff_percent >= 22 then 'Average'
	else 'Low'
	end as whiff_category
from pitchers;

select
	case 
	when whiff_percent >= 30 then 'High'
	when whiff_percent >= 22 then 'Average'
	else 'Low'
	end as whiff_category,
	count(*) as pitcher_count
from pitchers
group by whiff_category;


select
	case 
	when whiff_percent >= 30 then 'High'
	when whiff_percent >= 22 then 'Average'
	else 'Low'
	end as whiff_category,
	round(avg(k_percent), 2) as avg_strikeout
from pitchers
group by whiff_category
having avg_strikeout > 25;

-- PART 4
select "last_name, first_name", k_percent
from pitchers
where k_percent > (select avg(k_percent) from pitchers);

select "last_name, first_name", whiff_percent, (select avg(whiff_percent) from pitchers) as avg_whiff
from pitchers
where whiff_percent > (select avg(whiff_percent) from pitchers);

select "last_name, first_name", woba, (select avg(woba) from pitchers) as avg_woba
from pitchers
where woba < (select avg(woba) from pitchers);

select "last_name, first_name", k_percent, bb_percent
from pitchers
where k_percent > (select avg(k_percent) from pitchers) and bb_percent < (select avg(bb_percent) from pitchers);

select "last_name, first_name", whiff_percent
from pitchers
where whiff_percent = (select max(whiff_percent) from pitchers);

select "last_name, first_name", bb_percent
from pitchers
where bb_percent = (select min(bb_percent) from pitchers);

with strikeout_avg as (select avg(k_percent) as avg_strikeout from pitchers)
select "last_name, first_name", k_percent
from pitchers 
where k_percent > (select avg_strikeout from strikeout_avg);

with average as (select avg(whiff_percent) as avg_whiff from pitchers)
select "last_name, first_name", whiff_percent, avg_whiff
from pitchers, average
where whiff_percent > (select avg_whiff from average);

with strikeout as (select avg(k_percent) as avg_strikeout from pitchers), walk as (select avg(bb_percent) as avg_walk from pitchers)
select "last_name, first_name", k_percent, bb_percent
from pitchers, strikeout, walk
where k_percent > (select avg_strikeout from strikeout) and bb_percent < (select avg_walk from walk);

select "last_name, first_name", k_percent, avg(k_percent) over() as avg_k_percent
from pitchers;

select "last_name, first_name", k_percent, avg(k_percent) over() as avg_strikeout, k_percent - avg(k_percent) over() as difference
from pitchers;

select "last_name, first_name", whiff_percent, avg(whiff_percent) over() as avg_whiff, whiff_percent - avg(whiff_percent) over() as difference
from pitchers
order by difference desc;


-- PART 5
WITH average_strikeout AS (
    SELECT AVG(k_percent) AS avg_strikeout
    FROM pitchers
),
pitcher_groups AS (
    SELECT
        "last_name, first_name",
        k_percent,
        whiff_percent,
        CASE
            WHEN k_percent > avg_strikeout THEN 'High K%'
            ELSE 'Low/Equal K%'
        END AS k_category
    FROM pitchers, average_strikeout
)
SELECT
    "last_name, first_name",
    k_percent,
    k_category,
    AVG(whiff_percent) OVER(
        PARTITION BY k_category
    ) AS avg_group_whiff
FROM pitcher_groups;

-- PART 6
select "last_name, first_name", k_percent, rank() over(order by k_percent desc)
from pitchers;

select "last_name, first_name", whiff_percent, row_number() over(order by whiff_percent desc)
from pitchers;

select "last_name, first_name", whiff_percent, rank() over(order by whiff_percent desc)
from pitchers;

select "last_name, first_name", whiff_percent, dense_rank() over(order by whiff_percent desc)
from pitchers;

-- PART 6
with average as (select avg(k_percent) as avg_strikeout from pitchers),
pitcher_category as (
select "last_name, first_name", k_percent, whiff_percent,
case 
	when k_percent > avg_strikeout then 'High K%'
	else 'Low/Equal K%'
end as strikeout_category
from pitchers, average)
select "last_name, first_name", k_percent, whiff_percent, rank() over(PARTITION by strikeout_category order by whiff_percent desc) as whiff_rank
from pitcher_category;
