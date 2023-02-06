with fan_grouping as
(
select distinct fan_id, merchant as fan_grouping from SILAB.FAN_JOURNEY.F_TRANSACTION where merchant IN ('washington_nationals', 'washington_mystics', 'washington_capitals', 'washington_wizards', 'washington_spirit', 'dc_united', 'washington_commanders')
)
, subcategory_list as (
SELECT DISTINCT f.category, f.subcategory, f.partner_transaction_id, g.fan_grouping
    FROM SILAB.FAN_JOURNEY.F_TRANSACTION f
    JOIN fan_grouping g
        ON f.fan_id = g.fan_id    
)
, raw_measures AS (
   SELECT
      s.CATEGORY, 
      s.SUBCATEGORY,
      ft.FAN_ID,
      s.fan_grouping,
      MEDIAN(ft.SPEND) AS MEDIAN_SPEND,
      SUM(ft.SPEND) AS SPEND,
      SUM(ft.PURCHASES) AS PURCHASES
   FROM SILAB.FAN_JOURNEY.F_TRANSACTION_BASE ft
   JOIN subcategory_list s
      ON s.partner_transaction_id = ft.partner_transaction_id
   -- WHERE ft.CATEGORY = 'Telecommunication'
   GROUP BY s.CATEGORY, s.SUBCATEGORY, ft.FAN_ID, s.fan_grouping
)
SELECT
   FAN_GROUPING,
   CATEGORY, 
   SUBCATEGORY,
   SUM(SPEND) AS TOTAL_SPEND,
   SUM(PURCHASES) AS TOTAL_PURCHASES,
   COUNT(DISTINCT FAN_ID) AS FAN_COUNT,
   TOTAL_PURCHASES / FAN_COUNT AS PURCHASES_PER_FAN,
   TOTAL_SPEND / FAN_COUNT AS SPEND_PER_FAN,
   TOTAL_SPEND / TOTAL_PURCHASES AS SPEND_PER_PURCHASE,
   AVG(MEDIAN_SPEND) AS AVERAGE_MEDIAN_SPEND_PER_TRANSACTION,
   MEDIAN(SPEND) AS MEDIAN_SPEND_PER_FAN,
   MEDIAN(PURCHASES) AS MEDIAN_PURCHASES_PER_FAN
FROM raw_measures
GROUP BY CATEGORY, SUBCATEGORY, FAN_GROUPING
