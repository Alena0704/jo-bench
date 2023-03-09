SELECT MIN(n.name) AS cast_member_name,
       MIN(pi.info) AS cast_member_info
FROM aka_name AS an,
     cast_info AS ci,
     info_type AS it,
     link_type AS lt,
     movie_link AS ml,
     name AS n,
     person_info AS pi,
     title AS t
WHERE an.name IS NOT NULL
  AND (an.name LIKE $1
       OR an.name LIKE $2)
  AND it.info = $3
  AND lt.link IN ($4,
                 $5,
                 $6,
                 $7)
  AND n.name_pcode_cf BETWEEN $8 AND $9
  AND (n.gender= $10
       OR (n.gender = $11
           AND n.name LIKE $12))
  AND pi.note IS NOT NULL
  AND t.production_year BETWEEN $13 AND $14
  AND n.id = an.person_id
  AND n.id = pi.person_id
  AND ci.person_id = n.id
  AND t.id = ci.movie_id
  AND ml.linked_movie_id = t.id
  AND lt.id = ml.link_type_id
  AND it.id = pi.info_type_id
  AND pi.person_id = an.person_id
  AND pi.person_id = ci.person_id
  AND an.person_id = ci.person_id
  AND ci.movie_id = ml.linked_movie_id;

