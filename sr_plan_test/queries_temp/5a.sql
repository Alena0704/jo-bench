SELECT MIN(t.title) AS typical_european_movie
FROM company_type AS ct,
     info_type AS it,
     movie_companies AS mc,
     movie_info AS mi,
     title AS t
WHERE ct.kind = $1
  AND mc.note LIKE $2
  AND mc.note LIKE $3
  AND mi.info IN ($4,
                 $5,
                 $6,
                 $7,
                 $8,
                 $9,
                 $10,
                 $11)
  AND t.production_year > $12
  AND t.id = mi.movie_id
  AND t.id = mc.movie_id
  AND mc.movie_id = mi.movie_id
  AND ct.id = mc.company_type_id
  AND it.id = mi.info_type_id;

