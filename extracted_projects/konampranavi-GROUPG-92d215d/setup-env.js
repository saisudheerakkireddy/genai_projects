#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🔧 SafeAI Environment Setup');
console.log('==========================\n');

const envPath = path.join(process.cwd(), '.env.local');

if (fs.existsSync(envPath)) {
  console.log('✅ .env.local already exists');
  console.log('📝 Please update it with your Supabase credentials:\n');
  
  const content = fs.readFileSync(envPath, 'utf8');
  console.log(content);
} else {
  console.log('📝 Creating .env.local file...\n');
  
  const envContent = `# Supabase Configuration
# Get these values from your Supabase project settings
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url_here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key_here

# Optional: Email Service (for emergency alerts)
# EMAILJS_SERVICE_ID=your_emailjs_service_id
# EMAILJS_TEMPLATE_ID=your_emailjs_template_id
# EMAILJS_PUBLIC_KEY=your_emailjs_public_key`;

  fs.writeFileSync(envPath, envContent);
  console.log('✅ .env.local created successfully!\n');
}

console.log('📋 Next Steps:');
console.log('1. Go to https://supabase.com');
console.log('2. Create a new project');
console.log('3. Go to Settings → API');
console.log('4. Copy your Project URL and anon key');
console.log('5. Update .env.local with these values');
console.log('6. Go to SQL Editor and run database/schema.sql');
console.log('7. Go to Authentication → Settings and enable Email provider');
console.log('8. Set Site URL to http://localhost:3000');
console.log('9. Refresh your browser and test the app!\n');

console.log('🎉 Your SafeAI app will be fully functional!');
console.log('ASTRA - Intelligent Safety Beyond Boundaries');
console.log('By Team MINDSHARK');
