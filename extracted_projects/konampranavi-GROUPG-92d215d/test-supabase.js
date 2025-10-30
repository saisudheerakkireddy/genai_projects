#!/usr/bin/env node

const { createClient } = require('@supabase/supabase-js');

// Test Supabase connection
const supabaseUrl = 'https://xvzacfnsitcgxhpyflfu.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh2emFjZm5zaXRjZ3hocHlsZmx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEzNzUzMzUsImV4cCI6MjA3Njk1MTMzNX0.gMcv_FM7P4O70be9p3l05dt5tpYHNINldaw8y1_mqxo';

const supabase = createClient(supabaseUrl, supabaseKey);

console.log('🔍 Testing Supabase Connection...');
console.log('=====================================');
console.log('URL:', supabaseUrl);
console.log('Key:', supabaseKey.substring(0, 20) + '...');
console.log('');

async function testConnection() {
  try {
    // Test basic connection
    const { data, error } = await supabase.from('safe_places').select('count').limit(1);
    
    if (error) {
      console.log('❌ Database Connection Error:', error.message);
      return false;
    }
    
    console.log('✅ Database Connection: SUCCESS');
    
    // Test auth service
    const { data: authData, error: authError } = await supabase.auth.getSession();
    
    if (authError) {
      console.log('❌ Auth Service Error:', authError.message);
      return false;
    }
    
    console.log('✅ Auth Service: SUCCESS');
    console.log('');
    console.log('🎉 Supabase is working correctly!');
    console.log('');
    console.log('Next Steps:');
    console.log('1. Go to https://supabase.com/dashboard/project/xvzacfnsitcgxhpyflfu');
    console.log('2. Click "Authentication" → "Settings"');
    console.log('3. Enable "Email" provider');
    console.log('4. Set Site URL to: http://localhost:3000');
    console.log('5. Save changes');
    console.log('');
    console.log('Then test your app at http://localhost:3000');
    
    return true;
  } catch (error) {
    console.log('❌ Connection Error:', error.message);
    return false;
  }
}

testConnection();

