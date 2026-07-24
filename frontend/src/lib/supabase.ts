import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || 'https://nfhiqwyvluoqzluzuxup.supabase.co';
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5maGlxd3l2bHVvcXpsdXp1eHVwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI1ODUwODgsImV4cCI6MjA5ODE2MTA4OH0.LgS7OFLUyT4wAHk5VoE-DeKxhv2-jq9QHvdysq2mVJk';

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
