SELECT MIN(cn.name) AS company_name,
       MIN(lt.link) AS link_type,
       MIN(t.title) AS western_follow_up
FROM company_name AS cn,
     company_type AS ct,
     keyword AS k,
     link_type AS lt,
     movie_companies AS mc,
     movie_info AS mi,
     movie_keyword AS mk,
     movie_link AS ml,
     title AS t
WHERE cn.country_code != $1
  AND (cn.name LIKE $2
       OR cn.name LIKE $3)
  AND ct.kind = $4
  AND k.keyword = $5
  AND lt.link LIKE $6
  AND mc.note IS NULL
  AND mi.info IN ($7,
                   $8,
                   $9,
                   $10,
                   $11,
                   $12,
                   $13,
                   $14)
  AND t.production_year BETWEEN $15 AND $16
  AND lt.id = ml.link_type_id
  AND ml.movie_id = t.id
  AND t.id = mk.movie_id
  AND mk.keyword_id = k.id
  AND t.id = mc.movie_id
  AND mc.company_type_id = ct.id
  AND mc.company_id = cn.id
  AND mi.movie_id = t.id
  AND ml.movie_id = mk.movie_id
  AND ml.movie_id = mc.movie_id
  AND mk.movie_id = mc.movie_id
  AND ml.movie_id = mi.movie_id
  AND mk.movie_id = mi.movie_id
  AND mc.movie_id = mi.movie_id;

