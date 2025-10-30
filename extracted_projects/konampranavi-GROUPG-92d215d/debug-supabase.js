#!/usr/bin/env node

const { createClient } = require('@supabase/supabase-js');

console.log('🔍 Detailed Supabase Debug...');
console.log('=====================================');

// Test different possible issues
const supabaseUrl = 'https://xvzacfnsitcgxhpyflfu.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh2emFjZm5zaXRjZ3hocHlsZmx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEzNzUzMzUsImV4cCI6MjA3Njk1MTMzNX0.gMcv_FM7P4O70be9p3l05dt5tpYHNINldaw8y1_mqxo';

console.log('1. Testing basic fetch...');
fetch(supabaseUrl + '/rest/v1/', {
  headers: {
    'apikey': supabaseKey,
    'Authorization': 'Bearer ' + supabaseKey
  }
})
.then(response => {
  console.log('✅ Basic fetch works - Status:', response.status);
  return response.text();
})
.then(data => {
  console.log('✅ Supabase API is responding');
  console.log('');
  console.log('🎯 The issue might be:');
  console.log('1. Project might be paused/inactive');
  console.log('2. Authentication provider not properly configured');
  console.log('3. Site URL mismatch');
  console.log('');
  console.log('🔧 Try this:');
  console.log('1. Go to https://supabase.com/dashboard/project/xvzacfnsitcgxhpyflfu');
  console.log('2. Check if project status is "Active"');
  console.log('3. Go to Authentication → Settings');
  console.log('4. Make sure Email is enabled');
  console.log('5. Set Site URL to: http://localhost:3000');
  console.log('6. Save and wait 30 seconds');
  console.log('7. Try your app again');
})
.catch(error => {
  console.log('❌ Basic fetch failed:', error.message);
  console.log('');
  console.log('🚨 Possible issues:');
  console.log('1. Project is paused or deleted');
  console.log('2. Wrong project URL');
  console.log('3. Network connectivity issue');
  console.log('');
  console.log('🔧 Solutions:');
  console.log('1. Check if project exists and is active');
  console.log('2. Verify the project URL is correct');
  console.log('3. Try creating a new Supabase project');
});

