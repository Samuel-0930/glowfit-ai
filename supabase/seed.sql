insert into public.products (
    product_id, name, category, brand, price_usd, average_rating, review_count
) values
    ('p_glow_gel', 'Glow Barrier Gel Cream', 'moisturizer', 'Aster Lab', 24.00, 4.6, 1180),
    ('p_calm_ampoule', 'Calm Cica Ampoule', 'serum', 'Seoul Leaf', 19.00, 4.4, 860),
    ('p_velvet_sunscreen', 'Velvet Air Sunscreen', 'sunscreen', 'Namu Studio', 17.00, 4.1, 640)
on conflict (product_id) do update set
    name = excluded.name,
    category = excluded.category,
    brand = excluded.brand,
    price_usd = excluded.price_usd,
    average_rating = excluded.average_rating,
    review_count = excluded.review_count;

insert into public.product_tags (product_id, tag) values
    ('p_glow_gel', 'light texture'),
    ('p_glow_gel', 'fragrance free'),
    ('p_glow_gel', 'dry skin'),
    ('p_glow_gel', 'barrier care'),
    ('p_calm_ampoule', 'sensitive skin'),
    ('p_calm_ampoule', 'redness'),
    ('p_calm_ampoule', 'watery texture'),
    ('p_calm_ampoule', 'low irritation'),
    ('p_velvet_sunscreen', 'matte finish'),
    ('p_velvet_sunscreen', 'oily skin'),
    ('p_velvet_sunscreen', 'scented'),
    ('p_velvet_sunscreen', 'no white cast')
on conflict (product_id, tag) do nothing;

insert into public.reviews (review_id, user_id, product_id, rating, text, reviewed_on) values
    ('r_001', 'u_1', 'p_glow_gel', 5, 'Light gel texture but still moisturizing. My dry skin felt calm and the fragrance free formula did not sting.', '2025-01-02'),
    ('r_002', 'u_2', 'p_glow_gel', 4, 'Great barrier cream for winter. It can feel a little sticky under makeup.', '2025-01-03'),
    ('r_003', 'u_3', 'p_calm_ampoule', 5, 'The watery texture absorbs fast and helped with redness. Very gentle for sensitive skin.', '2025-01-04'),
    ('r_004', 'u_4', 'p_calm_ampoule', 3, 'Gentle but not hydrating enough for dry patches. I needed another moisturizer.', '2025-01-05'),
    ('r_005', 'u_5', 'p_velvet_sunscreen', 4, 'Matte finish is excellent for oily skin and there is no white cast, but the scent is noticeable.', '2025-01-06')
on conflict (review_id) do update set
    user_id = excluded.user_id,
    product_id = excluded.product_id,
    rating = excluded.rating,
    text = excluded.text,
    reviewed_on = excluded.reviewed_on;
