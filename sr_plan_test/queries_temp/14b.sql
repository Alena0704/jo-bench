SELECT MIN(mi_idx.info) AS rating,
       MIN(t.title) AS western_dark_production
FROM info_type AS it1,
     info_type AS it2,
     keyword AS k,
     kind_type AS kt,
     movie_info AS mi,
     movie_info_idx AS mi_idx,
     movie_keyword AS mk,
     title AS t
WHERE it1.info = $1
  AND it2.info = $2
  AND k.keyword IN ($3,
                   $4)
  AND kt.kind = $5
  AND mi.info IN ($8,
                 $9,
                 $10,
                 $11,
                 $12,
                 $13,
                 $14,
                 $15,
                 $16,
                 $17,
                 $18)
  AND mi_idx.info > $19
  AND t.production_year > $20
  AND (t.title LIKE $21
       OR t.title LIKE $22
       OR t.title LIKE $23)
  AND kt.id = t.kind_id
  AND t.id = mi.movie_id
  AND t.id = mk.movie_id
  AND t.id = mi_idx.movie_id
  AND mk.movie_id = mi.movie_id
  AND mk.movie_id = mi_idx.movie_id
  AND mi.movie_id = mi_idx.movie_id
  AND k.id = mk.keyword_id
  AND it1.id = mi.info_type_id
  AND it2.id = mi_idx.info_type_id;

