-- Таблица для синхронизации тетрадей. Выполнить один раз в Supabase → SQL Editor.
create table if not exists public.notes (
  user_id uuid not null default auth.uid() references auth.users on delete cascade,
  id text not null,
  data jsonb,
  updated bigint not null,
  deleted boolean not null default false,
  primary key (user_id, id)
);

alter table public.notes enable row level security;

-- каждый видит и меняет только свои тетради
create policy "own notes" on public.notes
  for all to authenticated
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

-- Картинки и страницы PDF (хранятся отдельно, чтобы заметки оставались лёгкими).
create table if not exists public.assets (
  user_id uuid not null default auth.uid() references auth.users on delete cascade,
  id text not null,
  data text,
  primary key (user_id, id)
);
alter table public.assets enable row level security;
create policy "own assets" on public.assets
  for all to authenticated
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
