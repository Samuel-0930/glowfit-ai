create table public.products (
    product_id text primary key,
    name text not null,
    category text not null,
    brand text not null,
    price_usd numeric(10, 2) not null check (price_usd >= 0),
    average_rating numeric(2, 1) not null check (average_rating between 0 and 5),
    review_count integer not null check (review_count >= 0),
    created_at timestamptz not null default now()
);

create table public.product_tags (
    product_id text not null references public.products(product_id) on delete cascade,
    tag text not null,
    primary key (product_id, tag)
);

create table public.reviews (
    review_id text primary key,
    user_id text not null,
    product_id text not null references public.products(product_id) on delete cascade,
    rating smallint not null check (rating between 1 and 5),
    text text not null,
    reviewed_on date not null,
    created_at timestamptz not null default now()
);

create index product_tags_product_id_idx on public.product_tags(product_id);
create index reviews_product_id_reviewed_on_idx on public.reviews(product_id, reviewed_on desc);

alter table public.products enable row level security;
alter table public.product_tags enable row level security;
alter table public.reviews enable row level security;

grant usage on schema public to service_role;
grant select on public.products, public.product_tags, public.reviews to service_role;
