#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🚀 SafeAI Project Completion Setup');
console.log('=====================================\n');

// Check if .env.local exists
const envPath = path.join(__dirname, '.env.local');
const envExamplePath = path.join(__dirname, 'env.example');

if (fs.existsSync(envPath)) {
    console.log('✅ .env.local file already exists');
} else {
    console.log('📝 Creating .env.local file...');
    
    if (fs.existsSync(envExamplePath)) {
        const envContent = fs.readFileSync(envExamplePath, 'utf8');
        fs.writeFileSync(envPath, envContent);
        console.log('✅ .env.local file created from template');
    } else {
        const defaultEnv = `# Supabase Configuration
# Replace these with your actual Supabase project credentials
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

# Optional: Email Service (for emergency alerts)
EMAILJS_SERVICE_ID=your_emailjs_service_id
EMAILJS_TEMPLATE_ID=your_emailjs_template_id
EMAILJS_PUBLIC_KEY=your_emailjs_public_key`;
        
        fs.writeFileSync(envPath, defaultEnv);
        console.log('✅ .env.local file created with default template');
    }
}

console.log('\n📋 Next Steps:');
console.log('1. Go to https://supabase.com and create a new project');
console.log('2. Get your Project URL and anon key from Settings → API');
console.log('3. Update the .env.local file with your Supabase credentials');
console.log('4. Run the database schema in Supabase SQL Editor');
console.log('5. Start the development server with: npm run dev');
console.log('\n🎯 Your SafeAI project will be complete!');

console.log('\n📚 Database Setup:');
console.log('1. Copy the contents of database/schema.sql');
console.log('2. Paste it in your Supabase SQL Editor');
console.log('3. Run the SQL to create all tables and policies');

console.log('\n🔧 Authentication Setup:');
console.log('1. Go to Authentication → Settings in Supabase');
console.log('2. Enable Email provider');
console.log('3. Set Site URL to http://localhost:3000');

console.log('\n✨ Features Available:');
console.log('- 🏠 Home: Beautiful login/signup page');
console.log('- 📊 Dashboard: Main features overview');
console.log('- 🗺️ Map: Interactive safety map with location tracking');
console.log('- 💬 Chat: AI safety agent');
console.log('- 👤 Profile: User settings and emergency contacts');
console.log('- 🚨 Emergency: SOS button and alerts');

console.log('\n🛡️ ASTRA - Intelligent Safety Beyond Boundaries');
console.log('By Team MINDSHARK');
