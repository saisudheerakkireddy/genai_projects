#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🚀 SafeAI Setup Script');
console.log('====================\n');

// Check if .env.local exists
const envPath = path.join(process.cwd(), '.env.local');
const envExamplePath = path.join(process.cwd(), 'env.local.example');

if (!fs.existsSync(envPath)) {
  if (fs.existsSync(envExamplePath)) {
    console.log('📝 Creating .env.local from template...');
    fs.copyFileSync(envExamplePath, envPath);
    console.log('✅ .env.local created! Please update it with your Supabase credentials.\n');
  } else {
    console.log('❌ env.local.example not found. Please create .env.local manually.\n');
  }
} else {
  console.log('✅ .env.local already exists.\n');
}

console.log('📋 Next Steps:');
console.log('1. Set up your Supabase project:');
console.log('   - Go to https://supabase.com');
console.log('   - Create a new project');
console.log('   - Go to Settings → API');
console.log('   - Copy your Project URL and anon key');
console.log('   - Update .env.local with these values\n');

console.log('2. Set up your database:');
console.log('   - Go to your Supabase project dashboard');
console.log('   - Click on SQL Editor');
console.log('   - Copy and paste the contents of database/schema.sql');
console.log('   - Click "Run" to execute the schema\n');

console.log('3. Enable Authentication:');
console.log('   - Go to Authentication → Settings in Supabase');
console.log('   - Enable "Email" provider');
console.log('   - Set your site URL to http://localhost:3000 (for development)\n');

console.log('4. Start the development server:');
console.log('   npm run dev\n');

console.log('5. Open http://localhost:3000 in your browser\n');

console.log('🎉 Your SafeAI project is ready!');
console.log('ASTRA - Intelligent Safety Beyond Boundaries');
console.log('By Team MINDSHARK');
