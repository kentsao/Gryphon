-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- 1. PROFILES (Public profile linked to auth.users)
create table public.profiles (
  id uuid references auth.users(id) on delete cascade primary key,
  full_name text,
  updated_at timestamp with time zone default timezone('utc'::text, now())
);

-- Secure the table
alter table public.profiles enable row level security;
create policy "Public profiles are viewable by everyone." on public.profiles for select using (true);
create policy "Users can insert their own profile." on public.profiles for insert with check (auth.uid() = id);
create policy "Users can update own profile." on public.profiles for update using (auth.uid() = id);

-- 2. PORTFOLIOS (User containers for stocks)
create table public.portfolios (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references auth.users(id) not null,
  name text not null,
  created_at timestamp with time zone default timezone('utc'::text, now())
);

alter table public.portfolios enable row level security;
create policy "Users can view own portfolios." on public.portfolios for select using (auth.uid() = user_id);
create policy "Users can insert own portfolios." on public.portfolios for insert with check (auth.uid() = user_id);
create policy "Users can update own portfolios." on public.portfolios for update using (auth.uid() = user_id);
create policy "Users can delete own portfolios." on public.portfolios for delete using (auth.uid() = user_id);

-- 3. POSITIONS (Stock holdings)
create table public.positions (
  id uuid default uuid_generate_v4() primary key,
  portfolio_id uuid references public.portfolios(id) on delete cascade not null,
  ticker text not null,
  shares numeric not null,
  avg_price numeric,
  created_at timestamp with time zone default timezone('utc'::text, now())
);

alter table public.positions enable row level security;
create policy "Users can view own portfolio positions." on public.positions for select using (
  exists ( select 1 from public.portfolios where id = positions.portfolio_id and user_id = auth.uid() )
);
create policy "Users can manage own portfolio positions." on public.positions for all using (
  exists ( select 1 from public.portfolios where id = positions.portfolio_id and user_id = auth.uid() )
);

-- 4. REPORTS (Gryphon Analysis Results)
create table public.reports (
  id uuid default uuid_generate_v4() primary key,
  portfolio_id uuid references public.portfolios(id) on delete cascade,
  risk_metrics jsonb, -- {beta: 1.2, volatility: 0.15, ...}
  llm_summary text,
  rebalance_recommendation text,
  created_at timestamp with time zone default timezone('utc'::text, now())
);

alter table public.reports enable row level security;
create policy "Users can view own reports." on public.reports for select using (
  exists ( select 1 from public.portfolios where id = reports.portfolio_id and user_id = auth.uid() )
);
create policy "System/User can insert reports." on public.reports for insert with check (
  exists ( select 1 from public.portfolios where id = reports.portfolio_id and user_id = auth.uid() )
);

-- 5. EVENTS (Monitoring & Analytics)
create table public.events (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references auth.users(id),
  event_type text not null, -- 'ANALYSIS_START', 'ERROR', etc.
  details jsonb,
  created_at timestamp with time zone default timezone('utc'::text, now())
);

alter table public.events enable row level security;
create policy "Admins can view all events" on public.events for select using (
    -- Simple check: assuming a specific admin email or role. 
    -- For MVP, we might allow users to see their own events, or keep it private.
    -- Let's allow insert for authenticated users (logging their actions)
    auth.uid() = user_id
);
create policy "Users can log events" on public.events for insert with check (auth.uid() = user_id);

-- Trigger to create profile on signup
create or replace function public.handle_new_user() 
returns trigger as $$
begin
  insert into public.profiles (id, full_name)
  values (new.id, new.raw_user_meta_data->>'full_name');
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();
