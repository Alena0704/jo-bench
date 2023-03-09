SELECT MIN(t.title) AS complete_downey_ironman_movie
FROM complete_cast AS cc,
     comp_cast_type AS cct1,
     comp_cast_type AS cct2,
     char_name AS chn,
     cast_info AS ci,
     keyword AS k,
     kind_type AS kt,
     movie_keyword AS mk,
     name AS n,
     title AS t
WHERE cct1.kind = $1
  AND cct2.kind LIKE $2
  AND chn.name NOT LIKE $3
  AND (chn.name LIKE $4
       OR chn.name LIKE $5)
  AND k.keyword IN ($6,
                   $7,
                   $8,
                   $9,
                   $10,
                   $11,
                   $12,
                   $13)
  AND kt.kind = $14
  AND n.name LIKE $15
  AND t.production_year > $16
  AND kt.id = t.kind_id
  AND t.id = mk.movie_id
  AND t.id = ci.movie_id
  AND t.id = cc.movie_id
  AND mk.movie_id = ci.movie_id
  AND mk.movie_id = cc.movie_id
  AND ci.movie_id = cc.movie_id
  AND chn.id = ci.person_role_id
  AND n.id = ci.person_id
  AND k.id = mk.keyword_id
  AND cct1.id = cc.subject_id
  AND cct2.id = cc.status_id;

